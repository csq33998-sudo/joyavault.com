"""Check trust routes, global footer navigation and policy content."""
import json
from localization import ROOT, LANGUAGES
from seo import Document
from site_routes import CANONICAL_ROUTES, all_redirects

slugs = ('about', 'editorial-policy', 'contact', 'privacy-policy', 'terms')
required = {f'/en/{slug}/' for slug in slugs}
assert required <= set(CANONICAL_ROUTES)
assert '/en/terms-of-service/' not in CANONICAL_ROUTES
assert all_redirects()['/en/terms-of-service/'] == '/en/terms/'
count = 0
for lang in LANGUAGES:
    for path in (ROOT / lang).rglob('index.html'):
        doc = Document(path.read_text(encoding='utf-8')).root
        footer = doc.all('footer')[0]
        assert required <= {a.attrs.get('href') for a in footer.all('a')}, path
        count += 1
for slug in slugs:
    text = (ROOT / 'en' / slug / 'index.html').read_text(encoding='utf-8')
    doc = Document(text).root
    main = doc.all('main')[0]
    assert len(main.all('h1')) == 1 and len(main.all('h2')) >= 4
    assert '2026-09-09' in text
    assert 'not the official Joyagoo website' in main.text()
    assert 'warehouse QC' in main.text() and 'international shipping' in main.text()
    if slug != 'contact':
        assert 'being prepared' not in main.text() and 'not yet been published' not in main.text()
privacy = (ROOT / 'en/privacy-policy/index.html').read_text(encoding='utf-8')
assert 'ml_theme' in privacy and 'Google Analytics 4' in privacy
assert 'stores your selected theme and language' not in privacy
for a in Document(privacy).root.all('a'):
    if 'google.com' in a.attrs.get('href',''):
        assert 'sponsored' not in a.attrs.get('rel','')
data = json.loads((ROOT / 'src/content/trust.json').read_text(encoding='utf-8'))
contact = (ROOT / 'en/contact/index.html').read_text(encoding='utf-8')
if data['contact_email']:
    assert 'mailto:' + data['contact_email'] in contact
    assert 'Report a broken link by email' in contact
else:
    assert 'mailto:' not in contact
    assert 'id="report-link"' in contact or "id='report-link'" in contact
    assert 'cannot send a report yet' in contact
    print('PENDING: owner must supply a real contact email; no address has been invented.')
print(f'PASS: 5 trust pages, {count} footers, direct Terms redirect and policy content.')
