"""Validate the requested editorial and SEO contract in rendered HTML."""
from collections import Counter
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import json
import re

from site_routes import ROOT, ARTICLE_MOVES, CANONICAL_ROUTES, all_redirects


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def plain(text):
    return unescape(re.sub(r'<[^>]+>', ' ', text)).strip()


expected = {
    'joyagoo-spreadsheet-qc-checklist', 'joyagoo-spreadsheet-shipping-planning',
    'joyagoo-spreadsheet-coupon-fee-checklist', 'taobao-weidian-1688-finds-guide',
    'joyagoo-spreadsheet-vs-raw-spreadsheet', 'dead-product-link-fix',
    'warehouse-consolidation-checklist',
}
sources = list((ROOT / 'src/content/articles').glob('*.md'))
assert {p.stem for p in sources} == expected
titles, descriptions = [], []
for source in sorted(sources):
    route = f'/en/articles/{source.stem}/'
    text = (ROOT / route.strip('/') / 'index.html').read_text(encoding='utf-8')
    tags = Tags(text).tags
    article = re.search(r'<article\b[^>]*>(.*?)</article>', text, re.S).group(1)
    body = re.sub(r'<nav\b[^>]*>.*?</nav>', '', article, flags=re.S)
    words = len(re.findall(r"\b\w+(?:['’-]\w+)*\b", plain(body)))
    assert 800 <= words <= 1200, (route, words)
    h1 = re.findall(r'<h1>(.*?)</h1>', text)
    assert len(h1) == 1, route
    h2s = re.findall(r'<h2>(.*?)</h2>', text)
    assert 4 <= len(h2s) <= 7, route
    assert '<ul class="article-checklist">' in article, route
    assert '<table class="comparison-table">' in article, route
    assert '<th scope="col">' in article and '<th scope="row">' in article
    links = [attrs['href'] for tag, attrs in Tags(article).tags if tag == 'a']
    for required in ['/en/joyagoo-spreadsheet/', '/en/best-joyagoo-finds/', '/en/joyagoo-buying-guide/']:
        assert required in links, (route, required)
    assert any(link.startswith('/en/best-joyagoo-finds/') and link != '/en/best-joyagoo-finds/' for link in links)
    title = plain(re.search(r'<title>(.*?)</title>', text).group(1))
    description = next(a['content'] for t, a in tags if t == 'meta' and a.get('name') == 'description')
    titles.append(title)
    descriptions.append(description)
    for attr, key, expected_value in [('property', 'og:title', title), ('property', 'og:description', description), ('name', 'twitter:title', title), ('name', 'twitter:description', description)]:
        assert next(a['content'] for t, a in tags if t == 'meta' and a.get(attr) == key) == expected_value
    graph = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', text, re.S).group(1))['@graph']
    data = next(item for item in graph if item['@type'] == 'Article')
    assert data['headline'] == plain(h1[0]) and data['description'] == description
    assert data['url'] == data['mainEntityOfPage']['@id'] == 'https://joyavault.com' + route
    faqs = next(item for item in graph if item['@type'] == 'FAQPage')['mainEntity']
    visible = re.findall(r'<details open><summary>(.*?)</summary><p>(.*?)</p></details>', article, re.S)
    assert len(visible) == len(faqs) >= 4
    for (q, answer), faq in zip(visible, faqs):
        assert plain(q) == faq['name'] and plain(answer) == faq['acceptedAnswer']['text']
    print(f'PASS {source.stem}: {words} words, {len(h2s)} H2, {len(faqs)} FAQs')
assert len(set(titles)) == len(titles) and len(set(descriptions)) == len(descriptions)
redirects = all_redirects()
for old, new in ARTICLE_MOVES.items():
    assert redirects[old] == new and new not in redirects and new in CANONICAL_ROUTES
    assert not (ROOT / old.strip('/') / 'index.html').exists()
print('PASS: distinct metadata, Article/FAQ parity, required internal links, and direct old-article redirects.')
