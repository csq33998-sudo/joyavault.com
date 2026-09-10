"""Audit delivered image and external-link contracts across all locales."""
from urllib.parse import urlsplit, parse_qs
from localization import ROOT, LANGUAGES
from seo import Document
import json

records = json.loads((ROOT / 'src/data/finds.json').read_text(encoding='utf-8'))
def supported_image(url):
    source = urlsplit(url)
    if source.path.endswith(('.webp', '.avif')) or parse_qs(source.query).get('fm') == ['webp']:
        return True
    # Imported seller originals deliberately retain their supplied encoding.
    if source.path.startswith('/assets/products/weidian/'):
        asset = ROOT / source.path.lstrip('/')
        return asset.is_file() and 0 < asset.stat().st_size <= 3_000_000 and asset.suffix in ('.jpg', '.png', '.gif')
    return False

assert all(supported_image(item['image']) for item in records)
pages = images = links = 0
for lang in LANGUAGES:
    for path in (ROOT / lang).rglob('index.html'):
        text = path.read_text(encoding='utf-8')
        doc = Document(text).root
        assert text.count('class="site-menu"') == 1, path
        sheets = [n.attrs.get('href') for n in doc.all('link') if n.attrs.get('rel') == 'stylesheet']
        assert sheets[-1] == '/performance.css', (path, sheets)
        for image in doc.all('img'):
            attrs = image.attrs
            assert int(attrs['width']) > 0 and int(attrs['height']) > 0, path
            if '/icons/' not in attrs['src']:
                images += 1
                source = urlsplit(attrs['src'])
                assert supported_image(attrs['src']), (path, source)
                assert attrs.get('loading') in ('lazy','eager'), path
                if attrs.get('fetchpriority') == 'high':
                    assert attrs['loading'] == 'eager'
                else:
                    assert attrs['loading'] == 'lazy'
        for link in doc.all('a'):
            attrs = link.attrs
            host = urlsplit(attrs.get('href','')).hostname
            if host and host != 'joyavault.com':
                links += 1
                assert attrs.get('target') == '_blank', path
                assert {'noopener','noreferrer'} <= set(attrs.get('rel','').split()), path
                if any(host == d or host.endswith('.'+d) for d in ('joyagoo.com','maisonlooks.com','taobao.com','weidian.com','1688.com')):
                    assert {'sponsored','nofollow'} <= set(attrs['rel'].split()), path
        pages += 1
print(f'PASS: {pages} pages, {images} supported content images, dimensions/loading, native menus, and {links} safe external links.')
