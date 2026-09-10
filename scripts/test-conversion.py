"""Verify stage CTAs and disclosures in static HTML."""
import re
from pathlib import Path
from conversion import NOTICE, STAGES, QC, SHIPPING, BUYING, FINDS
from finds_data import ROOT, load_finds
from find_card import source_link
from seo import Document

for route, links in STAGES.items():
    html=(ROOT / route.strip('/') / 'index.html').read_text(encoding='utf-8')
    for label,url in links:
        assert f'href="{url}">{label}</a>' in html, (route,label)
for slug in ('shoes','clothing','accessories','beauty-fragrance','electronics'):
    html=(ROOT / f'en/best-joyagoo-finds/{slug}/index.html').read_text(encoding='utf-8')
    for label in ('Browse more in this category','Read Shipping Planning','Open Buying Guide'):
        assert label in html
checked=0
for path in (ROOT / 'en').rglob('index.html'):
    html=path.read_text(encoding='utf-8')
    for match in re.finditer(r'<a\b[^>]*data-product-source[^>]*>.*?</a>',html,re.S):
        attrs=Document(match.group()).root.all('a')[0].attrs
        assert attrs['target']=='_blank'
        assert {'noopener','noreferrer'} <= set(attrs['rel'].split())
        assert html[match.end():].startswith('<span class="external-cta-note" lang="en">'+NOTICE)
        checked+=1
item=next(r for r in load_finds() if r['sourceUrl']!='#')
for kind in ('commercial','affiliate','editorial'):
    attrs=Document(source_link({**item,'sourceType':kind})).root.all('a')[0].attrs
    expected='sponsored nofollow noopener noreferrer' if kind!='editorial' else 'noopener noreferrer'
    assert attrs['rel']==expected
    assert attrs['target']=='_blank'
print(f'PASS: stage CTA labels, category actions, {checked} external product handoffs, and commercial/affiliate/editorial link policy.')
