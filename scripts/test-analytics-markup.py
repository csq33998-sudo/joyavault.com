"""Audit script loading and stable product metadata across every locale."""
from analytics import render_analytics
from finds_data import load_finds
from localization import ROOT, LANGUAGES
from seo import Document

records = {item['id']: item for item in load_finds()}
pages = cards = sources = 0
for lang in LANGUAGES:
    for path in (ROOT / lang).rglob('index.html'):
        pages += 1
        text = path.read_text(encoding='utf-8')
        assert render_analytics(text) == text, path
        document = Document(text)
        assets = [node for node in document.root.all('script')
                  if node.attrs.get('src', '').startswith('/js/analytics')]
        assert [node.attrs['src'] for node in assets] == ['/js/analytics-config.js', '/js/analytics.js'], path
        assert all('defer' in node.attrs for node in assets), path
        for node in document.root.all('article'):
            if 'data-find-id' not in node.attrs:
                continue
            cards += 1
            item = records[node.attrs['data-find-id']]
            for key in ('title', 'category', 'marketplace'):
                assert node.attrs['data-' + key] == item[key], (path, key)
            for anchor in node.all('a'):
                if anchor.attrs.get('href') == item['sourceUrl']:
                    assert 'data-product-source' in anchor.attrs, path
        for anchor in document.root.all('a'):
            attrs = anchor.attrs
            # Anchor IDs must not enter the existing [data-find-id] card filter.
            assert 'data-find-id' not in attrs, path
            if 'data-product-source' in attrs:
                sources += 1
                assert attrs['href'] == records[attrs['data-product-find-id']]['sourceUrl'], path
                assert attrs['href'].startswith('https://'), path
print(f'PASS: {pages} pages load tracking once with defer; {cards} cards and {sources} source links match source records.')
