"""Validate the finds collection before generating any public pages."""
from datetime import date
import json
import math
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
TAXONOMY = {
    'Shoes': ['Sneakers', 'Boots', 'Loafers', 'Clogs'],
    'Clothing': ['Tops', 'Hoodies', 'Outerwear', 'Bottoms'],
    'Accessories': ['Bags', 'Eyewear', 'Jewelry', 'Watches'],
    'Beauty & Fragrance': ['Perfume'],
    'Electronics': ['Audio', 'Phone Accessories'],
}
MARKETPLACES = ['Taobao', 'Weidian', '1688', 'Unknown']
REQUIRED = ['id', 'title', 'category', 'subcategory', 'brand', 'marketplace', 'priceCny', 'image', 'sourceUrl', 'detailUrl', 'tags', 'qcNotes', 'shippingNotes', 'updatedAt', 'isIndexable', 'sourceType', 'isPlaceholder', 'featured', 'imageAlt', 'description', 'sourceName']


def validate(data):
    if not isinstance(data, list) or not data:
        raise ValueError('finds.json must contain a non-empty array')
    ids, routes = set(), set()
    for i, item in enumerate(data):
        label = f'finds[{i}]'
        if not isinstance(item, dict) or any(key not in item for key in REQUIRED):
            raise ValueError(f'{label}: missing required fields')
        if set(item) != set(REQUIRED):
            raise ValueError(f'{label}: unsupported fields {set(item) - set(REQUIRED)}')
        for key in REQUIRED:
            if key not in ('priceCny', 'tags', 'qcNotes', 'shippingNotes', 'isPlaceholder', 'featured', 'isIndexable'):
                if not isinstance(item[key], str) or not item[key].strip():
                    raise ValueError(f'{label}.{key}: expected non-empty text')
        for key in ('tags', 'qcNotes', 'shippingNotes'):
            if not isinstance(item[key], list) or not item[key] or any(not isinstance(v, str) or not v.strip() for v in item[key]):
                raise ValueError(f'{label}.{key}: expected non-empty text array')
        if item['category'] not in TAXONOMY or item['subcategory'] not in TAXONOMY[item['category']]:
            raise ValueError(f'{label}: category/subcategory mismatch')
        if item['marketplace'] not in MARKETPLACES:
            raise ValueError(f'{label}: unsupported marketplace')
        if type(item['priceCny']) not in (int, float) or not math.isfinite(item['priceCny']) or item['priceCny'] < 0:
            raise ValueError(f'{label}: invalid priceCny')
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', item['updatedAt']):
            raise ValueError(f'{label}: updatedAt must be YYYY-MM-DD')
        date.fromisoformat(item['updatedAt'])
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', item['id']) or item['id'] in ids:
            raise ValueError(f'{label}: invalid or duplicate id')
        if not re.fullmatch(r'/en/finds/[a-z0-9-]+/', item['detailUrl']) or item['detailUrl'] in routes:
            raise ValueError(f'{label}: invalid or duplicate detailUrl')
        ids.add(item['id']); routes.add(item['detailUrl'])
        for key in ('isPlaceholder', 'featured', 'isIndexable'):
            if type(item[key]) is not bool:
                raise ValueError(f'{label}.{key}: expected boolean')
        source = urlsplit(item['sourceUrl'])
        if item['sourceUrl'] != '#' and (source.scheme != 'https' or not source.netloc or source.username or source.password):
            raise ValueError(f'{label}: sourceUrl must be # or a public HTTPS URL')
        if item['sourceUrl'] != '#':
            segments = [part.lower() for part in source.path.split('/') if part]
            if not segments or (len(segments) == 1 and len(segments[0]) == 2) or any(part in ('search', 'products', 'categories', 'category') for part in segments):
                raise ValueError(f'{label}: sourceUrl must identify a specific product, not a homepage or listing')
            if source.hostname and source.hostname.endswith('maisonlooks.com') and (source.hostname != 'maisonlooks.com' or not re.fullmatch(r'/[a-z]{2}/p/[a-z0-9-]+', source.path)):
                raise ValueError(f'{label}: use the current MaisonLooks product detail URL')
        if item['sourceType'] not in ('commercial', 'affiliate', 'editorial', 'unavailable'):
            raise ValueError(f'{label}: invalid sourceType')
        if (item['sourceUrl'] == '#') != (item['sourceType'] == 'unavailable'):
            raise ValueError(f'{label}: sourceUrl/sourceType mismatch')
        if item['isPlaceholder'] and item['sourceUrl'] != '#':
            raise ValueError(f'{label}: example records cannot claim a seller source')
        if item['isIndexable'] and (item['isPlaceholder'] or item['sourceType'] == 'unavailable'):
            raise ValueError(f'{label}: demo records and records without a source cannot be indexable')
        image = urlsplit(item['image'])
        if not (image.scheme == 'https' and image.netloc) and not (item['image'].startswith('/assets/') and '..' not in item['image'] and (ROOT / item['image'].lstrip('/')).is_file()):
            raise ValueError(f'{label}: invalid image path')
    if sum(item['featured'] for item in data) < 8:
        raise ValueError('Select at least eight featured records')
    return data


def load_finds():
    return validate(json.loads((ROOT / 'src/data/finds.json').read_text(encoding='utf-8')))


if __name__ == '__main__':
    data = load_finds()
    print(f'PASS: {len(data)} valid finds; {len({x["category"] for x in data})} categories; {sum(x["isPlaceholder"] for x in data)} example records.')


def catalog_records(data):
    """Publish approved finds, or a clearly separated demo catalogue."""
    approved = [item for item in data if item['isIndexable'] and not item['isPlaceholder']]
    if approved:
        return approved, True
    sourced = [item for item in data if not item['isPlaceholder'] and item['sourceUrl'] != '#']
    return sourced, False
