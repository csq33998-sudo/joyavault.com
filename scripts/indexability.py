"""Shared publication gates for robots and sitemap; no network assumptions."""
from urllib.parse import urlsplit

CATEGORY_NAMES = {'shoes':'Shoes','clothing':'Clothing','accessories':'Accessories','beauty-fragrance':'Beauty & Fragrance','electronics':'Electronics'}
SUBCATEGORY_NAMES = {'bags':'Bags','hoodies':'Hoodies','t-shirts':'Tops','polo-shirts':'Tops','jerseys':'Tops','shorts':'Bottoms'}


def exclusion_reason(route, data):
    parsed = urlsplit(route)
    if parsed.query or parsed.fragment:
        return 'parameter-or-fragment'
    parts = parsed.path.strip('/').split('/')
    if any(part in ('test','tests','demo','demos','preview') for part in parts):
        return 'test-or-demo-route'
    record = next((row for row in data if row['detailUrl'] == parsed.path), None)
    if record:
        return 'unapproved-product' if record['isPlaceholder'] or not record['isIndexable'] else None
    lang = parts[0]
    tail = '/'.join(parts[1:])
    if lang != 'en':
        from localization import PAGE_PATHS, ready
        key = next((key for key,value in PAGE_PATHS.items() if value.rstrip('/') == tail), None)
        if key is None or not ready(lang, key):
            return 'translation-not-ready'
    approved = [row for row in data if row['isIndexable'] and not row['isPlaceholder']]
    if tail == 'best-joyagoo-finds' and not approved:
        return 'demo-directory'
    if tail.startswith('best-joyagoo-finds/'):
        category = CATEGORY_NAMES.get(parts[2])
        rows = [row for row in approved if row['category'] == category]
        if len(parts) > 3:
            subcategory = SUBCATEGORY_NAMES.get(parts[3])
            rows = [row for row in rows if row['subcategory'] == subcategory]
        if len(rows) < 8:
            return 'insufficient-approved-category-finds'
    if tail.startswith('marketplaces/') and not any(row['marketplace'].lower() == parts[2] for row in approved):
        return 'demo-marketplace'
    return None
