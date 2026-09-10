"""One-time migration. Existing destination pages are never overwritten."""
from collections import Counter
from html import escape, unescape
from html.parser import HTMLParser
import hashlib
import json
import re
from urllib.parse import urljoin, urlsplit, urlunsplit

from site_routes import ROOT, ORIGIN, LEGACY_PAGES, page_path, legacy_redirects


class Text(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.parts = []
        self.feed(html)

    def handle_data(self, data):
        self.parts.extend(data.split())


def main_body(html):
    return re.search(r'<main\b[^>]*>(.*?)</main>', html, re.S).group(1)


def migrate_links(html, old):
    def replace(match):
        attr, quote, value = match.groups()
        value = unescape(value)
        if not value or value.startswith(('#', 'mailto:', 'tel:', 'data:')):
            return match.group()
        url = urlsplit(urljoin(ORIGIN + '/' + old, value))
        if url.netloc != 'joyavault.com':
            return match.group()
        target = legacy_redirects().get(url.path, url.path)
        if url.path.startswith('/assets/'):
            target = url.path
        # Keep social images absolute; other assets and internal links are root-relative.
        absolute = attr.lower() == 'content' and url.path.startswith('/assets/')
        out = urlunsplit(('https' if absolute else '', 'joyavault.com' if absolute else '', target, url.query, url.fragment))
        return f'{attr}={quote}{escape(out, quote=True)}{quote}'
    # Only URL-valued attributes, not prose descriptions.
    html = re.sub(r'\b(href|src|action)=([\"\'])(.*?)\2', replace, html, flags=re.I)
    html = re.sub(r'\b(content)=([\"\'])(https://joyavault\.com/.*?)\2', replace, html, flags=re.I)
    canonical = ORIGIN + LEGACY_PAGES[old]
    html = re.sub(r'(<link\b[^>]*rel=[\"\']canonical[\"\'][^>]*href=)[\"\'][^\"\']*[\"\']', lambda m: m[1] + '"' + canonical + '"', html)
    html = re.sub(r'(<meta\b[^>]*property=[\"\']og:url[\"\'][^>]*content=)[\"\'][^\"\']*[\"\']', lambda m: m[1] + '"' + canonical + '"', html)
    return html


def card(route, title, copy):
    return f'<a class="resource-card" href="{route}"><h3>{title}</h3><p>{copy}</p></a>'


def new_page(route, title, description, body):
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title} | JoyaVault</title>
<meta name="description" content="{description}" />
<link rel="canonical" href="{ORIGIN}{route}" />
<meta property="og:site_name" content="JoyaVault" />
<meta property="og:type" content="website" />
<meta property="og:title" content="{title} | JoyaVault" />
<meta property="og:description" content="{description}" />
<meta property="og:url" content="{ORIGIN}{route}" />
<meta property="og:image" content="{ORIGIN}/assets/social/joyagoo-spreadsheet-og.jpg" />
<link rel="icon" type="image/svg+xml" href="/assets/icons/joyavault.svg" />
<link rel="stylesheet" href="/styles.css" />
</head><body><a class="skip-link" href="#main">Skip to content</a>
<header></header>
<main id="main" class="section-shell"><h1>{title}</h1><p>{description}</p>{body}</main>
<footer></footer><script src="/js/theme.js"></script><script src="/js/i18n.js"></script>
</body></html>
'''


def migrate():
    actual = {str(p.relative_to(ROOT)).replace('\\', '/') for p in [*ROOT.glob('*.html'), *ROOT.glob('articles/*.html'), *ROOT.glob('blog/*.html')]}
    if actual != set(LEGACY_PAGES):
        raise SystemExit(f'Legacy inventory changed or migration already ran: {actual ^ set(LEGACY_PAGES)}')
    if (ROOT / 'en').exists():
        raise SystemExit('Destination en/ already exists; refusing to overwrite.')
    originals = {old: (ROOT / old).read_text(encoding='utf-8') for old in LEGACY_PAGES}
    output = {}
    for old, html in originals.items():
        if old != 'guides.html':
            output[LEGACY_PAGES[old]] = migrate_links(html, old)

    # Preserve the guide directory as a section within the full buying guide.
    guide = LEGACY_PAGES['guide.html']
    extra = main_body(migrate_links(originals['guides.html'], 'guides.html'))
    extra = extra.replace('<h1>', '<h2>').replace('</h1>', '</h2>')
    output[guide] = output[guide].replace('</main>', '<section id="guide-routes">' + extra + '</section></main>')

    categories = [
        ('shoes', 'Shoes', 'Sneakers, Nike, Jordan, and footwear discovery.'),
        ('clothing', 'Clothing', 'Hoodies, shorts, T-shirts, jerseys, and polo shirts.'),
        ('accessories', 'Accessories', 'Bags, jewelry, and outfit accessories.'),
        ('beauty-fragrance', 'Beauty &amp; Fragrance', 'Product information and fragrance discovery notes.'),
        ('electronics', 'Electronics', 'Compatibility, specifications, and device discovery notes.'),
    ]
    cards = ''.join(card('/en/best-joyagoo-finds/' + slug + '/', title, copy) for slug, title, copy in categories)
    hub = LEGACY_PAGES['finds-spreadsheet.html']
    output[hub] = output[hub].replace('<section id="categories" class="section-shell">', '<section id="categories" class="section-shell"><h2>Browse finds by category</h2><div class="resource-grid">' + cards + '</div>')

    clothing = '/en/best-joyagoo-finds/clothing/'
    cards = ''.join(card(clothing + slug + '/', title, copy) for slug, title, copy in (
        ('hoodies', 'Hoodies', 'Compare logo hoodies and zip-up layers.'),
        ('shorts', 'Shorts', 'Browse summer and relaxed streetwear shorts.'),
        ('t-shirts', 'T-Shirts', 'Explore graphic tees and everyday tops.'),
        ('jerseys', 'Jerseys', 'Browse sport-inspired jersey routes.'),
        ('polo-shirts', 'Polo Shirts', 'Compare polos and street-prep styles.'),
    ))
    output[clothing] = new_page(clothing, 'Clothing Finds', 'Browse Joyagoo clothing finds by garment type, then compare measurements, materials, and product options.', '<div class="resource-grid">' + cards + '</div>')

    for slug, title, description, body in (
        ('beauty-fragrance', 'Beauty &amp; Fragrance Finds', 'Organize beauty and fragrance product research before opening external listings.',
         '<h2>Build a useful product shortlist</h2><p>Record the product name, size, variant, ingredients or product information supplied by the manufacturer, seller, and listing date. Keep fragrance concentration and bottle size separate when comparing listings.</p><h2>Check the source information</h2><p>Compare the listing with manufacturer information and retain photographs of labels and packaging. A product link alone does not establish authenticity.</p><h2>Plan the next step</h2><p>Before adding a liquid, spray, or fragrance to a shipment, ask your chosen service whether it accepts that exact item and destination.</p>'),
        ('electronics', 'Electronics Finds', 'Organize electronics research around model numbers, compatibility, and listed specifications.',
         '<h2>Compare the exact model</h2><p>Save the manufacturer, model number, included accessories, plug type, voltage specification, and regional version. Similar product names can refer to different configurations.</p><h2>Check compatibility</h2><p>Compare connectors, operating-system requirements, supported networks, and the specifications published by the manufacturer. Record the seller\'s warranty and return information before ordering.</p><h2>Plan shipping</h2><p>Ask your chosen service about batteries, packaging, and acceptance of the exact device before adding it to a haul.</p>'),
    ):
        route = '/en/best-joyagoo-finds/' + slug + '/'
        body += '<h2>Product availability</h2><p>No curated product listings are published in this category yet.</p><div class="resource-grid">'
        body += card('/en/best-joyagoo-finds/', 'Browse all finds', 'Explore the currently available categories.')
        body += card('/en/articles/joyagoo-spreadsheet-shipping-planning/', 'Shipping planning', 'Organize questions before choosing a shipping service.') + '</div>'
        output[route] = new_page(route, title, description, body)

    # Verify every original body word survives, including both merged guide pages.
    audit = []
    for old, html in originals.items():
        before = Text(main_body(html)).parts
        after = Counter(Text(main_body(output[LEGACY_PAGES[old]])).parts)
        if Counter(before) - after:
            raise ValueError(f'Content lost: {old}')
        audit.append({'source': old, 'destination': LEGACY_PAGES[old], 'body_words': len(before), 'body_sha256': hashlib.sha256(' '.join(before).encode()).hexdigest(), 'preserved': True})
    for route, html in output.items():
        dest = page_path(route)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding='utf-8', newline='\n')
    # Remove only the verified individual source files after every page has been written.
    for old in originals:
        source = (ROOT / old).resolve()
        source.relative_to(ROOT.resolve())
        if not page_path(LEGACY_PAGES[old]).is_file():
            raise ValueError(f'Missing destination for {old}')
        source.unlink()
    for name in ('header', 'footer'):
        path = ROOT / 'components' / f'{name}.html'
        html = path.read_text(encoding='utf-8').replace('{{root}}', '')
        path.write_text(migrate_links(html, 'index.html'), encoding='utf-8', newline='\n')
    (ROOT / 'scripts' / 'migration-audit.json').write_text(json.dumps(audit, indent=2) + '\n', encoding='utf-8')
    print(f'Migrated {len(originals)} source pages to {len(output)} canonical pages; all original body text preserved.')


if __name__ == '__main__':
    migrate()
