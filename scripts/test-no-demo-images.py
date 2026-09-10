"""Prevent placeholder product images/cards from returning to public pages."""
import json
from html.parser import HTMLParser
from finds_data import ROOT, load_finds
from localization import LANGUAGES

data = load_finds()
demos = [row for row in data if row['isPlaceholder']]
images = {row['image'] for row in demos}
ids = {row['id'] for row in demos}


class Audit(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        assert attrs.get('data-find-id') not in ids, f'{path}: demo card'
        if tag == 'img':
            assert attrs.get('src') not in images, f'{path}: placeholder image'
            assert not any(image in attrs.get('srcset', '') for image in images), path


pages = [p for lang in LANGUAGES for p in (ROOT / lang).rglob('index.html')]
for path in pages:
    Audit().feed(path.read_text(encoding='utf-8'))
for row in demos:
    text = (ROOT / row['detailUrl'].strip('/') / 'index.html').read_text(encoding='utf-8')
    assert 'noindex, follow' in text
    assert 'Example listing retired' in text
for slug in ('beauty-fragrance', 'electronics'):
    text = (ROOT / f'en/best-joyagoo-finds/{slug}/index.html').read_text(encoding='utf-8')
    category = 'Beauty & Fragrance' if slug == 'beauty-fragrance' else 'Electronics'
    real = [row for row in data if row['category'] == category and not row['isPlaceholder'] and row['sourceUrl'] != '#']
    assert len(real) >= 8, f'{category}: needs at least eight source-backed listings'
    assert 'No product listings in this category yet' not in text
    for row in real:
        assert row['image'] in text and row['sourceUrl'].replace('&', '&amp;') in text
    assert 'noindex, follow' in text
print(f'PASS: {len(pages)} pages; zero demo cards or placeholder product images; beauty and electronics have at least eight sourced listings.')
