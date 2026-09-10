"""Generate crawlable homepage cards and detail pages from local finds data."""
import importlib.util
import json
import re
import sys
from html import escape
from pathlib import Path
from finds_data import load_finds, TAXONOMY, MARKETPLACES, catalog_records
from find_card import card, facts, source_link, popular_categories
from category_page import category_outputs
from marketplace_page import marketplace_outputs
from brand_page import brand_output
from buying_guide import buying_output

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('layout', ROOT / 'scripts/sync-layout.py')
layout = importlib.util.module_from_spec(spec)
spec.loader.exec_module(layout)
TITLE = 'Joyagoo Spreadsheet 2026 | Finds, Categories & Buying Guide'
DESCRIPTION = 'Browse Joyagoo spreadsheet finds, categories, QC notes, shipping planning, and buying guides before opening product links.'


def e(value):
    return escape(str(value), quote=True)


def shell(title, description, route, main, *, home=False, indexable=False, structured_data=None):
    structured_markup = '<script type="application/ld+json">' + json.dumps(structured_data, ensure_ascii=False).replace('<', '\\u003c') + '</script>' if structured_data else ''
    return f'''<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}" />
  <link rel="canonical" href="https://joyavault.com{route}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="JoyaVault" />
  <meta property="og:title" content="{e(title)}" />
  <meta property="og:description" content="{e(description)}" />
  <meta property="og:url" content="https://joyavault.com{route}" />
  <meta property="og:image" content="https://joyavault.com/assets/social/joyagoo-spreadsheet-og.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{e(title)}" />
  <meta name="twitter:description" content="{e(description)}" />
  <meta name="twitter:image" content="https://joyavault.com/assets/social/joyagoo-spreadsheet-og.jpg" />
  {'' if home or indexable else '<meta name="robots" content="noindex, follow" />'}
  <link rel="icon" type="image/svg+xml" href="/assets/icons/joyavault.svg" />
  <link rel="stylesheet" href="/styles.css" />
  <link rel="stylesheet" href="/home.css" />
  {structured_markup}
</head><body class="discovery-page{' homepage' if home else ''}">
<a class="skip-link" href="#main">Skip to content</a><header></header>
{main}
<footer></footer>
<script src="/js/finds-filter.js" defer></script><script src="/js/finds-search.js" defer></script>
</body></html>
'''


def outputs():
    data = load_finds()
    featured = sorted([item for item in data if not item['isPlaceholder'] and item['sourceUrl'] != '#'], key=lambda item: not item['featured'])
    main = (ROOT / 'components/home.html').read_text(encoding='utf-8').replace('{{find_cards}}', '\n'.join(card(item, hidden=i >= 8) for i, item in enumerate(featured))).replace('{{total}}', str(len(featured))).replace('{{popular_categories}}', popular_categories())
    result = {ROOT / 'en/index.html': shell(TITLE, DESCRIPTION, '/en/', main, home=True)}
    options = lambda values: ''.join(f'<option value="{e(value)}">{e(value if value != "Unknown" else "Marketplace unverified")}</option>' for value in values)
    catalog_data, catalog_indexable = catalog_records(data)
    has_real = any(not item['isPlaceholder'] for item in catalog_data)
    catalog = f'''<section id="finds" class="home-section home-shell" aria-labelledby="all-finds-title">
      <p class="home-eyebrow">THE FINDS DIRECTORY</p><h2 id="all-finds-title">{'All Joyagoo Finds' if has_real else 'Demo finds — explore the directory'}</h2>
      <p class="home-section-note">{('Browse ' + str(len(catalog_data)) + ' saved product listings with source links. Prices are snapshots, not live quotes. Check the selected option at the source. These listings have not been independently QC tested.') if has_real else 'Demo directory: examples only. Prices and marketplaces are illustrative and there are no purchasable sources.'}</p>
      <form id="finds-search-form" class="catalog-filters" action="/en/best-joyagoo-finds/#finds" method="get" role="search">
        <div><label for="finds-search">Search finds</label><input id="finds-search" name="q" type="search" placeholder="Search finds, styles, QC notes, or shipping..." aria-controls="featured-grid" /></div>
        <div><label for="finds-category">Category</label><select id="finds-category" name="category" aria-controls="featured-grid"><option value="">All categories</option>{options(sorted({item["category"] for item in catalog_data}))}</select></div>
        <div><label for="finds-subcategory">Subcategory</label><select id="finds-subcategory" name="subcategory" aria-controls="featured-grid"><option value="">All subcategories</option>{options(sorted({item["subcategory"] for item in catalog_data}))}</select></div>
        <div><label for="finds-marketplace">Marketplace</label><select id="finds-marketplace" name="marketplace" aria-controls="featured-grid"><option value="">All marketplaces</option>{options(sorted({item["marketplace"] for item in catalog_data}))}</select></div>
        <div><label for="finds-brand">Brand / style</label><select id="finds-brand" name="brand" aria-controls="featured-grid"><option value="">All brands and styles</option>{options(sorted({value for item in catalog_data for value in [item['brand'], *item['tags']]}))}</select></div>
        <fieldset class="catalog-price"><legend>Price range (CNY)</legend><div class="catalog-price-inputs"><div><label for="finds-min-price">Min ¥</label><input id="finds-min-price" name="minPrice" type="number" min="0" step="0.01" placeholder="0" /></div><div><label for="finds-max-price">Max ¥</label><input id="finds-max-price" name="maxPrice" type="number" min="0" step="0.01" placeholder="Any" /></div></div></fieldset>
        <a class="home-button" href="/en/best-joyagoo-finds/#finds">Reset filters</a>
      </form>
      <p id="finds-status" class="finds-status" role="status" aria-live="polite">Showing all {len(catalog_data)} finds.</p>
      <div class="home-product-grid" id="featured-grid" data-mode="catalog" data-page-size="24">{''.join(card(item) for item in catalog_data)}</div>
      <div id="finds-empty" class="finds-empty" hidden><h3>No finds match these filters.</h3><p>Try a broader search, reset the filters, or explore these popular categories.</p>{popular_categories()}<a class="home-text-link" href="/en/best-joyagoo-finds/#finds">Reset all filters</a></div>
      <nav class="finds-pagination" aria-label="Finds result pages"><a id="finds-prev" class="home-button" href="/en/best-joyagoo-finds/#finds" hidden>Previous finds</a><span id="finds-page" aria-live="polite"></span><a id="finds-next" class="home-button" href="/en/best-joyagoo-finds/?page=2#finds"{' hidden' if len(catalog_data) <= 24 else ''}>Next finds →</a></nav>
      <noscript><p>All {len(catalog_data)} cards are displayed without JavaScript. Enable JavaScript for 24-card pages and combined search, category, subcategory, marketplace, brand/style, and price filters.</p></noscript>
    </section>'''
    catalog_main = (ROOT / 'components/finds-catalog.html').read_text(encoding='utf-8').replace('{{catalog}}', catalog)
    breadcrumb = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'https://joyavault.com/en/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Best Joyagoo Finds', 'item': 'https://joyavault.com/en/best-joyagoo-finds/'},
    ]}
    result[ROOT / 'en/best-joyagoo-finds/index.html'] = shell('Best Joyagoo Finds Spreadsheet | Shoes, Clothing, Accessories', 'Browse Joyagoo-style finds by category, marketplace, price, QC notes, and shipping considerations before opening product links.', '/en/best-joyagoo-finds/', catalog_main, indexable=catalog_indexable, structured_data=breadcrumb)
    for item in data:
        route = item['detailUrl']
        path = ROOT / route.strip('/') / 'index.html'
        if item['isPlaceholder']:
            main = '<main id="main" class="home-shell find-detail"><h1>Example listing retired</h1><p>This demonstration record is no longer part of the product catalogue. Browse saved product listings with actual source links instead.</p><p id="product-source">No product source is available for this retired example.</p><a class="home-button" href="/en/best-joyagoo-finds/">Browse available finds</a>'+popular_categories()+'</main>'
            result[path] = shell('Example listing retired | JoyaVault', 'This demonstration record has been retired. Browse available product listings and buying guides.', route, main, indexable=False)
            continue
        main = f'''<main id="main" class="home-shell find-detail">
          <a class="home-text-link" href="/en/best-joyagoo-finds/#finds">← Back to all finds</a>
          <div class="detail-layout"><img src="{e(item['image'])}" alt="{e(item['imageAlt'])}" width="600" height="600" />
          <article><p class="home-eyebrow">{e(item['category'])} / {e(item['subcategory'])}</p><h1>{e(item['title'])}</h1>
          <p>{e(item['description'])}</p>{facts(item)}<p>Marketplace: {e(item['marketplace'])}{' (example only)' if item['isPlaceholder'] else ''}</p>
          <p class="record-note">{'This is an example record, not an available product offer. Its price and marketplace are illustrative.' if item['isPlaceholder'] else 'This is a saved listing, not an independently verified recommendation. Its price is a saved reference, not a live quote.'} Record updated refers to this directory entry. Brand names do not establish authenticity or official affiliation.</p>
          {source_link(item, 'home-button primary')}
          <p id="product-source">Source: {e(item['sourceName'])}. {'No product source is available for this demo record. This page does not link to a purchasable listing.' if item['isPlaceholder'] else ''}</p><h2>QC notes</h2><ul>{''.join('<li>' + e(note) + '</li>' for note in item['qcNotes'])}</ul><h2>Shipping notes</h2><ul>{''.join('<li>' + e(note) + '</li>' for note in item['shippingNotes'])}</ul><a class="home-text-link" href="/en/articles/joyagoo-spreadsheet-qc-checklist/">Read the QC Photo Checklist →</a></article></div></main>'''
        result[path] = shell(item['title'] + ' | JoyaVault', item['description'], route, main, indexable=item['isIndexable'])
    spreadsheet = (ROOT / 'components/spreadsheet-guide.html').read_text(encoding='utf-8-sig')
    result[ROOT / 'en/joyagoo-spreadsheet/index.html'] = shell(
        'Joyagoo Spreadsheet 2026 Guide | Finds, QC & Buying Steps',
        'Learn what a Joyagoo Spreadsheet is, how to use it for Taobao, Weidian, and 1688 finds, and when to move into QC, shipping, and buying guides.',
        '/en/joyagoo-spreadsheet/', spreadsheet, indexable=True)
    result.update(buying_output(shell))
    result.update(category_outputs(data, shell))
    result.update(marketplace_outputs(data, shell))
    result.update(brand_output(shell))
    return {path: layout.render_layout(path, html) for path, html in result.items()}


if __name__ == '__main__':
    changed = []
    for path, html in outputs().items():
        if not path.exists() or path.read_text(encoding='utf-8') != html:
            changed.append(str(path.relative_to(ROOT)))
            if '--check' not in sys.argv:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(html, encoding='utf-8', newline='\n')
    print(f'Homepage + catalogue + {len(load_finds())} detail pages; {len(changed)} ' + ('out of sync' if '--check' in sys.argv else 'updated'))
    sys.exit(bool(changed) if '--check' in sys.argv else 0)
