"""Static, cached whole-site translation. English HTML remains the source of truth.

Only the explicit translate command uses the network. Extraction, builds and
availability checks never send text or credentials to a service.
"""
from functools import lru_cache
from hashlib import sha256
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'src/translations'
TARGETS = ('de', 'fr', 'pt', 'pl', 'it', 'ar')
ORIGIN = 'https://joyavault.com'
MARKER = '<!-- generated-site-translation -->'
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
TEXT_ATTRS = {'alt', 'title', 'placeholder', 'aria-label', 'data-label', 'data-empty'}
META_TEXT = {'description','og:title','og:description','twitter:title','twitter:description'}
SCHEMA_TEXT = {'name','headline','description','text','articleBody','caption','alternativeHeadline'}
DYNAMIC = (
    'Day', 'Night', 'Toggle navigation', 'No finds match these filters.',
    'Image unavailable: {name}',
    'Enter a valid price range: use non-negative amounts with Min no greater than Max.',
    'Showing {start}–{end} of {count} matching finds.',
    'Showing {start}–{end} of {count} total finds.',
    'Showing {count} of {total} matching finds.',
    'Showing {count} featured finds from {total} records.',
    'Page {page} of {total}', '{count} of {total} finds',
    '{count} of {total} example finds', '{count} example pick',
    '{count} example picks', '{count} example pick matching your search',
    '{count} example picks matching your search',
)


def read_json(path, default):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else default


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def normalized(value):
    return ' '.join(value.split())


def key(value):
    return sha256(normalized(value).encode()).hexdigest()


@lru_cache
def protected_terms():
    terms = {'JoyaVault','Joyagoo','Taobao','Weidian','1688'}
    for filename in ('finds.json', 'shoes-page.json', 'accessories-page.json'):
        value = read_json(ROOT / 'src/data' / filename, [])
        rows = value if isinstance(value, list) else value.get('items', [])
        for row in rows:
            for field in ('title','name','brand','sourceName'):
                if row.get(field):
                    terms.add(row[field])
    return terms


def translatable(value):
    text = normalized(value)
    return bool(re.search(r'[A-Za-z]', text)) and text not in protected_terms() and not re.fullmatch(r'(?:https?://|mailto:|/|\{\{).*', text)


def source_html(text):
    # Menu availability and metadata change during a build; they are not content.
    text = re.sub(r'<details class="locale-switcher">.*?</details>', '{{language_switcher}}', text, flags=re.S)
    text = re.sub(r'<link\b[^>]*hreflang=[^>]*>\s*', '', text)
    text = re.sub(r'<script\b[^>]*(?:src="/js/i18n.js"|id="site-translation-data")[^>]*>.*?</script>\s*', '', text, flags=re.S)
    text = re.sub(r'<link rel="stylesheet" href="/locale.css" />\s*', '', text)
    # A historical footer applied translate=no to its full legal disclaimer.
    text = text.replace('class="footer-brand" translate="no"', 'class="footer-brand"')
    return text


def fingerprint(text):
    return sha256(source_html(text).encode()).hexdigest()


@lru_cache
def published_routes():
    manifest = read_json(DATA / 'published.json', {})
    result = set()
    for route, record in manifest.items():
        source = ROOT / 'en' / route.split('/', 2)[2] / 'index.html'
        target = ROOT / route.strip('/') / 'index.html'
        if (source.exists() and target.exists()
                and record['sourceHash'] == fingerprint(source.read_text(encoding='utf-8'))):
            result.add(route)
    return result


def local_url(url, lang, available):
    parts = urlsplit(url)
    if parts.netloc and parts.netloc != 'joyavault.com':
        return url
    if not parts.path.startswith('/en/'):
        return url
    candidate = f'/{lang}/' + parts.path[4:]
    route = candidate.removesuffix('index.html')
    if route not in available:
        return url
    return urlunsplit((parts.scheme, parts.netloc, candidate, parts.query, parts.fragment))


class Page(HTMLParser):
    """Preserve HTML/CSS/JS bytes; modify only text, selected attrs and JSON-LD.

    Positions are recorded against the original document so inline scripts, form
    values, product IDs and URLs never go through a translation model.
    """
    def __init__(self, text, translations=None, lang='en', available=()):
        super().__init__(convert_charrefs=True)
        self.source = text
        self.catalog = translations
        self.lang = lang
        self.available = set(available)
        self.strings = set()
        self.edits = []
        self.stack = []
        self.lines = [0]
        for match in re.finditer('\n', text): self.lines.append(match.end())
        self.feed(text)

    def position(self):
        line, column = self.getpos()
        return self.lines[line-1] + column

    def translate(self, value):
        text = normalized(value)
        if not translatable(text): return value
        self.strings.add(text)
        if self.catalog is None: return value
        record = self.catalog.get(key(text))
        if not record or record.get('source') != text or not record.get('translation', '').strip():
            raise ValueError(f'Missing {self.lang} translation: {text[:100]}')
        translated = record['translation']
        if sorted(re.findall(r'\{\w+\}', translated)) != sorted(re.findall(r'\{\w+\}', text)):
            raise ValueError(f'Changed placeholders: {text[:100]}')
        return re.match(r'^\s*', value)[0] + translated + re.search(r'\s*$', value)[0]

    def schema(self, value, field='', parent_type=''):
        if isinstance(value, dict):
            kind = value.get('@type', '')
            return {k:self.schema(v,k,kind) for k,v in value.items()}
        if isinstance(value, list): return [self.schema(v,field,parent_type) for v in value]
        if not isinstance(value,str): return value
        if field == 'inLanguage': return self.lang if self.catalog is not None else value
        if field in SCHEMA_TEXT and not (field == 'name' and parent_type in ('Organization','Brand','Product')):
            return self.translate(value)
        if field in ('url','@id','item','mainEntityOfPage','urlTemplate'):
            return local_url(value,self.lang,self.available) if self.catalog is not None else value
        return value

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get('class', '').split()
        skip = (bool(self.stack and self.stack[-1][1]) or attrs.get('translate') == 'no'
                or tag in ('style','code','pre','svg') or 'notranslate' in classes)
        raw = self.get_starttag_text()
        replacements = {}
        if not skip:
            for name, value in attrs.items():
                if name in TEXT_ATTRS and value:
                    replacements[name] = self.translate(value)
            if tag == 'meta' and (attrs.get('name') or attrs.get('property')) in META_TEXT:
                replacements['content'] = self.translate(attrs.get('content', ''))
        if self.catalog is not None:
            if tag == 'html': replacements.update(lang=self.lang, dir='rtl' if self.lang == 'ar' else 'ltr')
            if attrs.get('lang') == 'en' and not skip: replacements['lang'] = self.lang
            if tag in ('a','form','link'):
                for name in ('href','action'):
                    if name in attrs: replacements[name] = local_url(attrs[name],self.lang,self.available)
            if tag == 'meta' and attrs.get('property') == 'og:url':
                replacements['content'] = local_url(attrs['content'],self.lang,self.available)
            for name,value in replacements.items():
                if name in attrs:
                    pattern = r'(?<![\w:-])'+re.escape(name)+r'\s*=\s*(?:"[^"]*"|\x27[^\x27]*\x27|[^\s>]+)'
                    raw = re.sub(pattern, lambda _: name+'="'+escape(value,quote=True)+'"', raw, count=1)
                else:
                    raw = raw[:-1] + ' '+name+'="'+escape(value,quote=True)+'">'
            self.edits.append((self.position(),self.position()+len(self.get_starttag_text()),raw))
        if tag not in VOID:
            self.stack.append((tag,skip,attrs))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag,attrs)
        if tag not in VOID: self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack)-1,-1,-1):
            if self.stack[index][0] == tag:
                self.stack = self.stack[:index]
                break

    def handle_data(self, data):
        if not self.stack: return
        tag,skip,attrs = self.stack[-1]
        start = self.position()
        if tag == 'script':
            if attrs.get('type') == 'application/ld+json':
                value = self.schema(json.loads(data))
                if self.catalog is not None:
                    self.edits.append((start,start+len(data),json.dumps(value,ensure_ascii=False).replace('<','\\u003c')))
            return
        if skip: return
        # HTMLParser has decoded entities. Find the raw span for lossless edits.
        end = self.source.find('<',start)
        if end < 0: end = len(self.source)
        raw = self.source[start:end]
        translated = self.translate(data)
        if self.catalog is not None and translated != data:
            self.edits.append((start,start+len(raw),escape(translated,quote=False)))

    def render(self):
        result = self.source
        for start,end,replacement in sorted(self.edits,reverse=True):
            result = result[:start]+replacement+result[end:]
        return result


def inventory():
    pages = {}
    strings = set(DYNAMIC)
    for path in sorted((ROOT / 'en').rglob('index.html')):
        text = source_html(path.read_text(encoding='utf-8'))
        route = '/' + path.relative_to(ROOT).as_posix().removesuffix('index.html')
        page = Page(text)
        pages[route] = {'sourceHash':fingerprint(text),'strings':sorted(key(s) for s in page.strings)}
        strings.update(page.strings)
    return pages, {key(s):s for s in sorted(strings)}


@lru_cache
def protection_pattern():
    terms = sorted(protected_terms(),key=len,reverse=True)
    return re.compile(r'https?://[^\s<>]+|\{\w+\}|\b(?:'+'|'.join(re.escape(t) for t in terms)+r')\b')


@lru_cache
def protect(value):
    """Keep source names, brands, URLs and format placeholders unchanged."""
    saved = []
    def replace(match):
        saved.append(match[0])
        return f'JVKEEP{len(saved)-1:04d}X'
    return protection_pattern().sub(replace,value), saved


def restore(value, saved):
    for index,original in enumerate(saved):
        token = f'JVKEEP{index:04d}X'
        if value.count(token) != 1:
            raise ValueError('Translation changed a protected token; batch was not saved')
        value = value.replace(token,original)
    return value
