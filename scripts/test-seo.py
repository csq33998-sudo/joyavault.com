"""Full-site rendered SEO contract and regression checks for hidden FAQ content."""
from collections import Counter
import json
import unittest
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
from seo import Document, visible_faqs, render_seo, ORIGIN, ROOT
from site_routes import CANONICAL_ROUTES, page_path


class SeoTests(unittest.TestCase):
    def test_pages(self):
        titles, descriptions, indexable = [], [], set()
        for route in CANONICAL_ROUTES:
            with self.subTest(route=route):
                path = page_path(route)
                text = path.read_text(encoding='utf-8')
                doc = Document(text).root
                self.assertEqual(len(doc.all('head')),1)
                self.assertEqual(len(doc.all('h1')),1)
                self.assertEqual(len(doc.all('title')),1)
                title = doc.all('title')[0].text()
                metadata = {}
                for m in doc.all('meta'):
                    key = m.attrs.get('name',m.attrs.get('property',''))
                    if key in metadata:
                        self.fail(f'Duplicate meta: {key}')
                    metadata[key] = m.attrs.get('content','')
                desc = metadata['description']
                self.assertTrue(title and desc)
                titles.append(title); descriptions.append(desc)
                self.assertEqual(metadata['og:title'],title)
                self.assertEqual(metadata['og:description'],desc)
                self.assertEqual(metadata['twitter:card'],'summary_large_image')
                self.assertEqual(metadata['twitter:title'],title)
                self.assertEqual(metadata['twitter:description'],desc)
                self.assertEqual(metadata['twitter:image'],metadata['og:image'])
                self.assertTrue(metadata['og:image'].startswith('https://'))
                if metadata['og:image'].startswith(ORIGIN):
                    self.assertTrue((ROOT/urlsplit(metadata['og:image']).path.lstrip('/')).is_file())
                canonical = [n.attrs['href'] for n in doc.all('link') if n.attrs.get('rel')=='canonical']
                self.assertEqual(canonical,[ORIGIN+route])
                self.assertEqual(metadata['og:url'],ORIGIN+route)
                self.assertTrue(all('alt' in n.attrs for n in doc.all('img')))
                graph = []
                for s in doc.all('script'):
                    if s.attrs.get('type')=='application/ld+json':
                        graph.extend(json.loads(s.text())['@graph'])
                counts = Counter(n['@type'] for n in graph)
                for kind in ('WebSite','Organization','BreadcrumbList'):
                    self.assertEqual(counts[kind],1)
                website = next(n for n in graph if n['@type']=='WebSite')
                self.assertEqual(website['potentialAction']['target']['urlTemplate'],ORIGIN+'/en/best-joyagoo-finds/?q={search_term_string}')
                crumbs = next(n for n in graph if n['@type']=='BreadcrumbList')['itemListElement']
                self.assertEqual(crumbs[-1]['item'],ORIGIN+route)
                self.assertEqual([c['position'] for c in crumbs],list(range(1,len(crumbs)+1)))
                faqs = [n for n in graph if n['@type']=='FAQPage']
                visible = visible_faqs(doc)
                self.assertEqual(len(faqs),int(bool(visible)))
                if visible:
                    self.assertEqual(faqs[0]['mainEntity'],visible)
                parts = route.strip('/').split('/')
                article = len(parts)==3 and parts[1] in ('articles','blog') and parts[2]!='routes'
                self.assertEqual(counts['Article'],int(article))
                for a in doc.all('a'):
                    host=urlsplit(a.attrs.get('href','')).hostname
                    commercial = {'streetstyle.maisonlooks.com', 'joyagoo.com', 'taobao.com', 'weidian.com', '1688.com'}
                    if host and any(host == domain or host.endswith('.' + domain) for domain in commercial):
                        self.assertTrue({'sponsored','nofollow'} <= set(a.attrs.get('rel','').split()))
                if 'noindex' not in metadata.get('robots','') and 'noindex' not in metadata.get('googlebot',''):
                    indexable.add(ORIGIN+route)
                self.assertEqual(render_seo(path,text),text,'SEO rendering must be idempotent')
        self.assertEqual(len(titles),len(set(titles)),'Duplicate titles')
        self.assertEqual(len(descriptions),len(set(descriptions)),'Duplicate descriptions')
        sitemap=ET.parse(ROOT/'sitemap.xml').getroot()
        urls=[n.text for n in sitemap.findall('{*}url/{*}loc')]
        self.assertEqual(set(urls),indexable)
        self.assertEqual(len(urls),len(set(urls)))
        self.assertTrue(all(not urlsplit(u).query and not urlsplit(u).fragment for u in urls))

    def test_hidden_faq_and_navigation_excluded(self):
        html='<header><details><summary>Language</summary>English</details></header><main><section hidden><details><summary>Hidden?</summary><p>No</p></details></section><details><summary>Visible?</summary><p>Yes</p></details></main>'
        result=visible_faqs(Document(html).root)
        self.assertEqual([(q['name'],q['acceptedAnswer']['text']) for q in result],[('Visible?','Yes')])

    def test_search_and_robots(self):
        text=(ROOT/'js/finds-search.js').read_text(encoding='utf-8')
        self.assertIn("params.get('q')",text)
        self.assertIn('render(readUrl())',text)
        self.assertEqual((ROOT/'robots.txt').read_text(encoding='utf-8'),'User-agent: *\nAllow: /\n\nSitemap: https://joyavault.com/sitemap.xml\n')


if __name__=='__main__': unittest.main()
