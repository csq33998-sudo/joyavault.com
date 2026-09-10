"""Canonical public routes and the complete pre-migration page inventory."""
from pathlib import Path
import json
from finds_data import load_finds
from localization import localized_routes

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://joyavault.com'
LEGACY_PAGES = {
    'index.html': '/en/',
    'joyagoo-spreadsheet.html': '/en/joyagoo-spreadsheet/',
    'joyagoo-spreadsheet-updates.html': '/en/joyagoo-spreadsheet-updates/',
    'guide.html': '/en/joyagoo-buying-guide/',
    'guides.html': '/en/joyagoo-buying-guide/',
    'finds-spreadsheet.html': '/en/best-joyagoo-finds/',
    'sneaker-finds-spreadsheet.html': '/en/best-joyagoo-finds/shoes/',
    'accessories-finds-spreadsheet.html': '/en/best-joyagoo-finds/accessories/',
    'bag-finds-spreadsheet.html': '/en/best-joyagoo-finds/accessories/bags/',
    'hoodie-finds-spreadsheet.html': '/en/best-joyagoo-finds/clothing/hoodies/',
    'shorts-finds-spreadsheet.html': '/en/best-joyagoo-finds/clothing/shorts/',
    't-shirt-finds-spreadsheet.html': '/en/best-joyagoo-finds/clothing/t-shirts/',
    'polo-shirt-finds-spreadsheet.html': '/en/best-joyagoo-finds/clothing/polo-shirts/',
    'jersey-finds-spreadsheet.html': '/en/best-joyagoo-finds/clothing/jerseys/',
    'brands.html': '/en/brands/',
    'nike-finds-spreadsheet.html': '/en/brands/nike/',
    'jordan-finds-spreadsheet.html': '/en/brands/jordan/',
    'taobao-finds-spreadsheet.html': '/en/marketplaces/taobao/',
    'weidian-finds-spreadsheet.html': '/en/marketplaces/weidian/',
    '1688-finds-spreadsheet.html': '/en/marketplaces/1688/',
    'articles.html': '/en/articles/',
    'contact.html': '/en/contact/',
    'privacy-policy.html': '/en/privacy-policy/',
    'terms-of-service.html': '/en/terms/',
    'editorial-policy.html': '/en/editorial-policy/',
    'blog/index.html': '/en/blog/',
}
for slug in (
    'best-sneaker-finds', 'joyagoo-spreadsheet-coupon-fee-checklist',
    'joyagoo-spreadsheet-qc-checklist', 'joyagoo-spreadsheet-shipping-planning',
    'joyagoo-spreadsheet-vs-traditional-spreadsheet', 'taobao-weidian-1688-finds-guide',
):
    LEGACY_PAGES[f'articles/{slug}.html'] = f'/en/articles/{slug}/'
for slug in (
    'routes', 'category-discovery-notes-for-joyagoo-haul-planning',
    'choosing-an-agent-route-after-category-research',
    'how-to-use-trending-lists-in-a-joyagoo-haul',
    'joyagoo-haul-guide-workflow-from-list-to-shipping',
    'qc-notes-before-warehouse-consolidation',
    'review-notes-that-keep-haul-finds-organized',
    'shipping-route-planning-for-a-joyagoo-haul',
):
    LEGACY_PAGES[f'blog/{slug}.html'] = f'/en/blog/{slug}/'

NEW_CATEGORIES = {
    '/en/best-joyagoo-finds/clothing/',
    '/en/best-joyagoo-finds/beauty-fragrance/',
    '/en/best-joyagoo-finds/electronics/',
}
FINDS_DATA = ROOT / 'src/data/finds.json'
FIND_ROUTES = {item['detailUrl'] for item in load_finds()} if FINDS_DATA.exists() else set()
ARTICLE_MOVES = {
    '/en/terms-of-service/': '/en/terms/',
    '/en/articles/joyagoo-spreadsheet-vs-traditional-spreadsheet/': '/en/articles/joyagoo-spreadsheet-vs-raw-spreadsheet/',
    '/en/articles/joyagoo-spreadsheet-dead-link-replacement-guide/': '/en/articles/dead-product-link-fix/',
}
LEGACY_PAGES = {old: ARTICLE_MOVES.get(route, route) for old, route in LEGACY_PAGES.items()}
NEW_ARTICLES = {
    '/en/articles/joyagoo-spreadsheet-vs-raw-spreadsheet/',
    '/en/articles/dead-product-link-fix/',
    '/en/articles/warehouse-consolidation-checklist/',
}
CANONICAL_ROUTES = sorted(set(LEGACY_PAGES.values()) | NEW_CATEGORIES | FIND_ROUTES | NEW_ARTICLES | {'/en/about/', '/en/terms/'} | localized_routes())


def page_path(route):
    return ROOT / route.strip('/') / 'index.html'


def legacy_redirects():
    redirects = {}
    for old, new in LEGACY_PAGES.items():
        stem = '/' + old.removesuffix('.html')
        for alias in ('/' + old, stem, stem + '/'):
            redirects[alias] = new
        if old.endswith('index.html'):
            directory = '/' + old.removesuffix('index.html')
            redirects[directory] = new
            if directory != '/':
                redirects[directory.rstrip('/')] = new
    return redirects


def all_redirects():
    redirects = legacy_redirects()
    for old, new in ARTICLE_MOVES.items():
        for alias in (old, old.rstrip('/'), old + 'index.html', old + 'index', old.rstrip('/') + '.html'):
            redirects[alias] = new
    for route in CANONICAL_ROUTES:
        for alias in (route.rstrip('/'), route + 'index.html', route + 'index', route.rstrip('/') + '.html'):
            redirects[alias] = route
    return redirects
