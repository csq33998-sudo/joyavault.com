"""Shared FindCard rendering for the homepage, catalogue, and detail pages."""
from html import escape
import re
from finds_data import ROOT


def e(value):
    return escape(str(value), quote=True)


def source_link(item, css_class=''):
    if item['sourceUrl'] == '#':
        return f'<a class="source-pending {e(css_class)}" href="{e(item["detailUrl"])}#product-source">Source unavailable <small>View explanation</small></a>'
    rel = 'sponsored nofollow noopener noreferrer' if item['sourceType'] in ('commercial', 'affiliate') else 'noopener noreferrer'
    return f'<a class="{e(css_class)}" data-product-source data-product-find-id="{e(item["id"])}" href="{e(item["sourceUrl"])}" target="_blank" rel="{rel}">Open product source <span aria-hidden="true">↗</span></a>'


def facts(item):
    price = f'¥{item["priceCny"]:,.2f}'
    label = 'Example price' if item['isPlaceholder'] else 'Saved price'
    return f'''<dl class="find-facts">
      <div><dt>Brand</dt><dd>{e(item['brand'])}</dd></div>
      <div><dt>{label}</dt><dd>{price}</dd></div>
      <div><dt>Record updated</dt><dd><time datetime="{e(item['updatedAt'])}">{e(item['updatedAt'])}</time></dd></div>
    </dl>'''


def card(item, hidden=False):
    if item['isPlaceholder'] or item['sourceUrl'] == '#':
        return ''
    search = ' '.join([item['title'], item['brand'], item['category'], item['subcategory'], item['marketplace'], *item['tags'], *item['qcNotes'], *item['shippingNotes']])
    values = {key: e(item[key]) for key in ('id', 'category', 'subcategory', 'marketplace', 'brand', 'detailUrl', 'image', 'imageAlt', 'title')}
    values.update(priceCny=e(item['priceCny']), styles=e('|'.join(item['tags'])))
    values.update(search=e(search), hidden=' hidden' if hidden else '', recordLabel='Example record' if item['isPlaceholder'] else 'Saved listing · unverified', marketplaceLabel=e('Marketplace unverified' if item['marketplace'] == 'Unknown' else item['marketplace'] + (' · example' if item['isPlaceholder'] else '')), facts=facts(item), sourceLink=source_link(item))
    for key in ('qcNotes', 'shippingNotes'):
        note = item[key][0]
        values[key] = e(note if len(note) <= 140 else note[:137].rsplit(' ', 1)[0] + '…')
    template = (ROOT / 'components/FindCard.html').read_text(encoding='utf-8')
    return re.sub(r'\{\{(\w+)\}\}', lambda match: values[match[1]], template)


def popular_categories():
    return '<nav class="empty-recommendations" aria-label="Popular categories">' + ''.join(f'<a class="home-button" href="/en/best-joyagoo-finds/{slug}/">{label}</a>' for slug, label in [('shoes', 'Shoes'), ('clothing', 'Clothing'), ('accessories', 'Accessories')]) + '</nav><p>Need help choosing? <a class="home-text-link" href="/en/joyagoo-buying-guide/">Read the Buying Guide →</a></p>'
