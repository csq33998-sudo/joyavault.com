"""Deterministic SEO head shared by every page renderer; no network dependencies."""
from functools import lru_cache
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://joyavault.com'
IMAGE = ORIGIN + '/assets/social/joyagoo-spreadsheet-og.jpg'
MANAGED = {'WebSite', 'Organization', 'BreadcrumbList', 'Article', 'FAQPage'}


class Element:
    def __init__(self, tag='', attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def all(self, tag):
        return [n for child in self.children if isinstance(child, Element)
                for n in ([child] if child.tag == tag else []) + child.all(tag)]

    def text(self):
        return ' '.join(''.join(c.text() if isinstance(c, Element) else c for c in self.children).split())


class Document(HTMLParser):
    VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.root = Element()
        self.stack = [self.root]
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        node = Element(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                self.stack = self.stack[:i]
                break

    def handle_data(self, text):
        self.stack[-1].children.append(text)


def visible_faqs(root):
    """Only question disclosures within main, excluding hidden content and UI menus."""
    result = []
    def visit(node, hidden=False):
        hidden = hidden or 'hidden' in node.attrs or node.attrs.get('aria-hidden') == 'true' or bool(re.search(r'display\s*:\s*none|visibility\s*:\s*hidden', node.attrs.get('style','')))
        if hidden:
            return
        if node.tag == 'details':
            summaries = node.all('summary')
            if len(summaries) == 1:
                question = summaries[0].text()
                answer = ' '.join(c.text() if isinstance(c, Element) else c.strip() for c in node.children if c is not summaries[0]).strip()
                answer = ' '.join(answer.split())
                if question and answer:
                    result.append({'@type':'Question','name':question,'acceptedAnswer':{'@type':'Answer','text':answer}})
            return
        for child in node.children:
            if isinstance(child, Element):
                visit(child, hidden)
    for main in root.all('main'):
        visit(main)
    return result


@lru_cache
def overrides():
    return json.loads((ROOT / 'src/seo/pages.json').read_text(encoding='utf-8'))


@lru_cache
def records():
    return json.loads((ROOT / 'src/data/finds.json').read_text(encoding='utf-8'))


def render_seo(path, text):
    route = '/' + Path(path).relative_to(ROOT).as_posix().removesuffix('index.html')
    url, lang = ORIGIN + route, route.split('/')[1]
    doc = Document(text).root
    headings = doc.all('h1')
    if len(headings) != 1:
        raise ValueError(f'{route}: expected exactly one H1')
    headline = headings[0].text()
    title = doc.all('title')[0].text()
    description = next((m.attrs.get('content','') for m in doc.all('meta') if m.attrs.get('name') == 'description'), '')
    custom = overrides().get(route, {})
    title, description = custom.get('title',title), custom.get('description',description)
    image = custom.get('image', IMAGE)
    record = next((r for r in records() if r['detailUrl'] == route), None)
    if record:
        duplicate = sum(r['title'] == record['title'] for r in records()) > 1
        label = record['title'] + (f" — Saved record {record['id'].removeprefix('find-')}" if duplicate else '')
        title = label + ' | JoyaVault'
        description = (f"Explore {label} as an illustrative research record. Review category, QC, and shipping questions; no verified seller offer is supplied." if record['isPlaceholder'] else f"Review {label}, saved source details, and QC and shipping questions before opening the external listing. Confirm current options at the source.")
        image = record['image'] if not record['image'].endswith('.svg') else IMAGE
    if not title or not description:
        raise ValueError(f'{route}: missing authored SEO metadata')
    if image.startswith('/'):
        image = ORIGIN + image
    for img in doc.all('img'):
        if 'alt' not in img.attrs:
            raise ValueError(f'{route}: image needs authored alt: {img.attrs.get("src")}')

    from indexability import exclusion_reason
    excluded = exclusion_reason(route, records())
    if excluded:
        text = re.sub(r'<meta\b[^>]*name=[\"\'](?:robots|googlebot)[\"\'][^>]*>\s*', '', text, flags=re.I)
        text = text.replace('</head>', '<meta name="robots" content="noindex, follow" />\n</head>')

    # Replace existing owned nodes, retaining other intentional schemas such as HowTo.
    retained = []
    def strip_schema(match):
        payload = json.loads(match.group(1))
        nodes = payload if isinstance(payload,list) else payload.get('@graph',[payload])
        for node in nodes:
            kinds = node.get('@type',[])
            kinds = [kinds] if isinstance(kinds,str) else kinds
            if not MANAGED.intersection(kinds):
                retained.append(node)
        return ''
    text = re.sub(r'<script\b[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>(.*?)</script>\s*', strip_schema, text, flags=re.S|re.I)
    text = re.sub(r'<!-- seo:head -->\s*|<!-- /seo:head -->\s*', '', text)
    text = re.sub(r'<title>.*?</title>\s*', '', text, flags=re.S|re.I)
    def strip_meta(match):
        node = Document(match.group()).root.all('meta')[0]
        key = node.attrs.get('name', node.attrs.get('property','')).lower()
        return '' if key == 'description' or key.startswith(('og:','twitter:')) else match.group()
    text = re.sub(r'<meta\b[^>]*>\s*', strip_meta, text, flags=re.I)
    text = re.sub(r'<link\b[^>]*rel=[\"\']canonical[\"\'][^>]*>\s*', '', text, flags=re.I)

    article = ('/articles/' in route and route != f'/{lang}/articles/') or ('/blog/' in route and route not in (f'/{lang}/blog/',f'/{lang}/blog/routes/'))
    from localization import load_locale
    home_label = 'Home' if lang == 'en' else load_locale(lang)['ui']['home']
    crumbs = [{'@type':'ListItem','position':1,'name':home_label,'item':ORIGIN+f'/{lang}/'}]
    if route != f'/{lang}/':
        crumbs.append({'@type':'ListItem','position':2,'name':headline,'item':url})
    graph = [
        {'@type':'Organization','@id':ORIGIN+'/#organization','name':'JoyaVault','url':ORIGIN+'/en/','logo':{'@type':'ImageObject','url':ORIGIN+'/assets/icons/joyagoo-spreadsheet-transparent.png','caption':'Joyagoo spreadsheet'}},
        {'@type':'WebSite','@id':ORIGIN+'/#website','url':ORIGIN+'/en/','name':'JoyaVault','publisher':{'@id':ORIGIN+'/#organization'},'inLanguage':['en','zh','de','fr','pt','pl','it','ar'],'potentialAction':{'@type':'SearchAction','target':{'@type':'EntryPoint','urlTemplate':ORIGIN+'/en/best-joyagoo-finds/?q={search_term_string}'},'query-input':'required name=search_term_string'}},
        {'@type':'BreadcrumbList','@id':url+'#breadcrumb','itemListElement':crumbs},
    ]
    if article:
        graph.append({'@type':'Article','@id':url+'#article','headline':headline,'description':description,'image':[image],'url':url,'inLanguage':lang,'mainEntityOfPage':{'@type':'WebPage','@id':url},'publisher':{'@id':ORIGIN+'/#organization'}})
    faqs = visible_faqs(doc)
    if faqs:
        graph.append({'@type':'FAQPage','@id':url+'#faq','inLanguage':lang,'mainEntity':faqs})
    graph.extend(retained)
    tags = [f'<title>{escape(title)}</title>',f'<meta name="description" content="{escape(description)}" />',f'<link rel="canonical" href="{url}" />']
    for key,value in {'og:title':title,'og:description':description,'og:image':image,'og:url':url,'og:type':'article' if article else 'website','og:site_name':'JoyaVault'}.items():
        tags.append(f'<meta property="{key}" content="{escape(value)}" />')
    for key,value in {'twitter:card':'summary_large_image','twitter:title':title,'twitter:description':description,'twitter:image':image}.items():
        tags.append(f'<meta name="{key}" content="{escape(value)}" />')
    payload = json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    tags.append(f'<script type="application/ld+json">{payload}</script>')
    text = text.replace('</head>', '<!-- seo:head -->\n'+'\n'.join(tags)+'\n<!-- /seo:head -->\n</head>')

    commercial = {'maisonlooks.com','streetstyle.maisonlooks.com','mgt.joyagoo.com','joyagoo.com','www.joyagoo.com','taobao.com','weidian.com','1688.com'}
    def rel_link(match):
        raw = match.group()
        attrs = Document(raw+'</a>').root.all('a')[0].attrs
        host = urlsplit(attrs.get('href','')).hostname or ''
        if not host or host == 'joyavault.com':
            return raw
        rel = set(attrs.get('rel','').split()) | {'noopener', 'noreferrer'}
        if any(host == d or host.endswith('.'+d) for d in commercial):
            rel |= {'sponsored', 'nofollow'}
        raw = re.sub(r'\srel\s*=\s*([\"\']).*?\1','',raw,flags=re.I)
        raw = re.sub(r'\starget\s*=\s*([\"\']).*?\1','',raw,flags=re.I)
        ordered = [token for token in ('sponsored', 'nofollow', 'noopener', 'noreferrer') if token in rel]
        ordered += sorted(rel - set(ordered))
        return raw[:-1] + ' target="_blank" rel="'+' '.join(ordered)+'">'
    return re.sub(r'<a\b[^>]*>',rel_link,text,flags=re.I)
