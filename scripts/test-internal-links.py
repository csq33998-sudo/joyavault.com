"""Audit actual HTML against the requested internal-link contract, without JS."""
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlsplit
from localization import LANGUAGES
from internal_links import render_internal_links

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.current = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.current = [dict(attrs).get('href', ''), '']

    def handle_data(self, value):
        if self.current is not None:
            self.current[1] += value

    def handle_endtag(self, tag):
        if tag == 'a' and self.current is not None:
            self.links.append(self.current)
            self.current = None


count = articles = edges = 0
for lang in LANGUAGES:
    for path in sorted((ROOT / lang).rglob('index.html')):
        text = path.read_text(encoding='utf-8')
        assert render_internal_links(path, text) == text, f'Unsynced: {path}'
        main = re.search(r'<main\b[^>]*>(.*?)</main>', text, re.S).group(1)
        tail = path.relative_to(ROOT / lang).as_posix().removesuffix('index.html')
        hrefs = {href for href, label in Links(main).links}
        required = []
        if not tail:
            required = ['joyagoo-spreadsheet/', 'joyagoo-buying-guide/', 'best-joyagoo-finds/',
                        'best-joyagoo-finds/shoes/', 'best-joyagoo-finds/clothing/', 'best-joyagoo-finds/accessories/',
                        'articles/joyagoo-spreadsheet-qc-checklist/', 'articles/joyagoo-spreadsheet-shipping-planning/']
        elif tail == 'joyagoo-spreadsheet/':
            required = ['best-joyagoo-finds/', 'joyagoo-buying-guide/', 'joyagoo-spreadsheet-updates/', 'articles/joyagoo-spreadsheet-qc-checklist/', 'articles/joyagoo-spreadsheet-shipping-planning/']
            required += [p.parent.relative_to(ROOT / lang).as_posix() + '/'
                         for p in (ROOT / lang / 'best-joyagoo-finds').rglob('index.html')
                         if p.parent.name != 'best-joyagoo-finds']
        elif tail == 'best-joyagoo-finds/':
            required = ['joyagoo-spreadsheet/', 'joyagoo-buying-guide/',
                        'articles/joyagoo-spreadsheet-qc-checklist/', 'articles/joyagoo-spreadsheet-shipping-planning/']
            required += ['best-joyagoo-finds/' + slug + '/' for slug in ('shoes', 'clothing', 'accessories', 'beauty-fragrance', 'electronics')]
            required += ['marketplaces/' + slug + '/' for slug in ('taobao', 'weidian', '1688')]
        elif tail == 'joyagoo-buying-guide/':
            required = ['joyagoo-spreadsheet/', 'articles/joyagoo-spreadsheet-qc-checklist/',
                        'articles/joyagoo-spreadsheet-shipping-planning/', 'articles/joyagoo-spreadsheet-coupon-fee-checklist/']
        elif tail.startswith('best-joyagoo-finds/') and tail != 'best-joyagoo-finds/':
            required = ['best-joyagoo-finds/', 'joyagoo-spreadsheet/', 'joyagoo-buying-guide/',
                        'articles/joyagoo-spreadsheet-qc-checklist/', 'articles/joyagoo-spreadsheet-shipping-planning/']
        for target in required:
            code = lang if (ROOT / lang / target / 'index.html').exists() else 'en'
            assert f'/{code}/{target}' in hrefs, (path, target)
        module = re.search(r'<!-- internal-links:start -->(.*?)<!-- internal-links:end -->', main, re.S)
        article = tail.startswith(('articles/', 'blog/')) and tail not in ('articles/', 'blog/', 'blog/routes/')
        if article:
            articles += 1
            assert module and '>Next Pages</h2>' in module[1], path
            assert 3 <= len(Links(module[1]).links) <= 5, path
            body = re.search(r'<article\b[^>]*>(.*?)</article>', main, re.S)
            ending = body[1] if body else main
            assert ending.rstrip().endswith('<!-- internal-links:end -->'), path
        if module:
            count += 1
            assert main.count('id="internal-links-heading"') == 1, path
            links = Links(module[1]).links
            assert len({h for h, _ in links}) == len(links), path
            for href, label in links:
                assert len(label.strip()) >= 2 and label.lower().strip() != 'click here', path
                assert href != '/' + path.relative_to(ROOT).as_posix().removesuffix('index.html'), path
                assert (ROOT / urlsplit(href).path.strip('/') / 'index.html').exists(), (path, href)
                edges += 1
print(f'PASS: {count} navigation modules, {articles} articles, {edges} crawlable links; all required destinations and article endings verified.')
