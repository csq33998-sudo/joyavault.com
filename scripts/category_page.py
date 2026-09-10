"""Generate five category guides with shared markup and category-specific copy."""
import re
from urllib.parse import urlencode
from category_content import CATEGORIES
from find_card import card, e, popular_categories
from finds_data import ROOT

NEXT_STEPS = [
    ('/en/joyagoo-spreadsheet/', 'Joyagoo Spreadsheet Guide', 'Keep source details and comparison notes together.'),
    ('/en/best-joyagoo-finds/', 'Best Joyagoo Finds', 'Compare categories, marketplaces, prices, and research notes.'),
    ('/en/joyagoo-buying-guide/', 'Joyagoo Buying Guide', 'Review the steps between research and an order.'),
    ('/en/articles/joyagoo-spreadsheet-qc-checklist/', 'QC Photo Checklist', 'Prepare questions for the available QC checks.'),
    ('/en/articles/joyagoo-spreadsheet-shipping-planning/', 'Shipping Planning', 'Organize packing questions and a destination-specific quote.')]


def category_records(data, name):
    records = [item for item in data if item['category'] == name and not item['isPlaceholder'] and item['sourceUrl'] != '#']
    approved = [item for item in records if item['isIndexable'] and not item['isPlaceholder']]
    return (approved, True) if len(approved) >= 8 else (records, False)


def links(rows):
    return ''.join(f'<a class="home-category-card" href="{e(url)}"><h3>{e(title)}</h3><p>{e(copy)}</p><span class="route-arrow" aria-hidden="true">↗</span></a>' for url,title,copy in rows)

def category_outputs(data, shell):
    result = {}
    template = (ROOT / 'components/CategoryPage.html').read_text(encoding='utf-8-sig')
    for slug, content in CATEGORIES.items():
        name = content['name']
        records, indexable = category_records(data, name)
        route = f'/en/best-joyagoo-finds/{slug}/'
        values = {key:e(content[key]) for key in ('name','intro','why','cta')}
        values.update(record_note=e('Published finds from this category. Confirm current prices and options at the source.' if indexable else 'Saved seller listings with product photos and source links. Confirm the selected option, current price and availability at the source; these products have not been independently QC tested.'), h1=e('Best Joyagoo '+name+' Finds'),count=str(len(records)),
            signals=''.join(f'<article class="category-signal"><h3>{e(title)}</h3><p>{e(copy)}</p></article>' for title,copy in content['signals']),
            checks=''.join(f'<article><h3>{e(title)}</h3><p>{e(copy)}</p></article>' for title,copy in content['checks']),
            shipping=''.join(f'<article class="category-signal"><h3>{e(title)}</h3><p>{e(copy)}</p></article>' for title,copy in content['shipping']),
            cards=''.join(card({**item, 'imageAlt': name + ': ' + item['title'] + ('; illustrative placeholder, not a product photograph' if item['isPlaceholder'] else '; saved listing image')}) for item in records),
            next_steps=links(NEXT_STEPS), extra=('<h3 class="category-more-title">More category routes</h3><div class="category-signals">'+links(content['extra'])+'</div>') if content['extra'] else '',
            faq=''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in content['faq']),
            browse=e('/en/best-joyagoo-finds/?'+urlencode({'category':name})+'#finds'))
        if not records:
            values['cards'] = '<div class="finds-empty"><h3>No product listings in this category yet</h3><p>Explore available categories or prepare with the buying guide.</p>'+popular_categories()+'</div>'
        main = re.sub(r'\{\{(\w+)\}\}',lambda m:values[m[1]],template)
        breadcrumb = {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i,'name':label,'item':'https://joyavault.com'+url} for i,(label,url) in enumerate([('Home','/en/'),('Finds','/en/best-joyagoo-finds/'),(name,route)],1)]}
        result[ROOT / route.strip('/') / 'index.html'] = shell(content['title'],content['description'],route,main,indexable=indexable,structured_data=breadcrumb)
    return result
