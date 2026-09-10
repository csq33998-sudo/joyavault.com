"""Shared, server-rendered internal navigation for every publishing pipeline."""
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    'spreadsheet': ('joyagoo-spreadsheet/', 'Joyagoo Spreadsheet Guide'),
    'buying': ('joyagoo-buying-guide/', 'How to Buy With Joyagoo'),
    'finds': ('best-joyagoo-finds/', 'Best Joyagoo Finds'),
    'qc': ('articles/joyagoo-spreadsheet-qc-checklist/', 'QC Photo Checklist'),
    'shipping': ('articles/joyagoo-spreadsheet-shipping-planning/', 'Shipping Planning Guide'),
    'coupon': ('articles/joyagoo-spreadsheet-coupon-fee-checklist/', 'Coupon and Fee Guide'),
    'updates': ('joyagoo-spreadsheet-updates/', 'Joyagoo Spreadsheet Updates'),
    'warehouse': ('articles/warehouse-consolidation-checklist/', 'Warehouse Consolidation Checklist'),
    'marketplaces': ('articles/taobao-weidian-1688-finds-guide/', 'Taobao, Weidian and 1688 Finds Guide'),
    'taobao': ('marketplaces/taobao/', 'Taobao Finds'),
    'weidian': ('marketplaces/weidian/', 'Weidian Finds'),
    '1688': ('marketplaces/1688/', '1688 Finds'),
    'dead-links': ('articles/dead-product-link-fix/', 'How to Fix Dead Product Links'),
}
CATEGORIES = {
    'shoes': 'Shoes Finds', 'clothing': 'Clothing Finds',
    'accessories': 'Accessories Finds', 'electronics': 'Electronics Finds',
    'beauty-fragrance': 'Beauty and Fragrance Finds',
    'accessories/bags': 'Bag Finds', 'clothing/hoodies': 'Hoodie Finds',
    'clothing/t-shirts': 'T-Shirt Finds', 'clothing/shorts': 'Shorts Finds',
    'clothing/polo-shirts': 'Polo Shirt Finds', 'clothing/jerseys': 'Jersey Finds',
}
PAGES.update({key: ('best-joyagoo-finds/' + key + '/', label) for key, label in CATEGORIES.items()})

# Authored relationships: the next step depends on the subject of the article.
ARTICLE_LINKS = {
    'joyagoo-spreadsheet-qc-checklist': ['buying', 'warehouse', 'shipping', 'shoes'],
    'joyagoo-spreadsheet-shipping-planning': ['qc', 'warehouse', 'coupon', 'buying'],
    'joyagoo-spreadsheet-coupon-fee-checklist': ['buying', 'shipping', 'spreadsheet', 'finds'],
    'warehouse-consolidation-checklist': ['qc', 'shipping', 'coupon', 'buying'],
    'dead-product-link-fix': ['updates', 'marketplaces', 'finds', 'spreadsheet'],
    'taobao-weidian-1688-finds-guide': ['spreadsheet', 'finds', 'buying', 'dead-links'],
    'joyagoo-spreadsheet-vs-raw-spreadsheet': ['spreadsheet', 'finds', 'buying', 'updates'],
    'best-sneaker-finds': ['shoes', 'finds', 'qc', 'shipping'],
    'qc-notes-before-warehouse-consolidation': ['qc', 'warehouse', 'shipping', 'buying'],
    'shipping-route-planning-for-a-joyagoo-haul': ['shipping', 'warehouse', 'coupon', 'qc'],
    'category-discovery-notes-for-joyagoo-haul-planning': ['finds', 'shoes', 'clothing', 'accessories', 'spreadsheet'],
    'choosing-an-agent-route-after-category-research': ['buying', 'marketplaces', 'shipping', 'coupon'],
    'how-to-use-trending-lists-in-a-joyagoo-haul': ['finds', 'spreadsheet', 'updates', 'qc'],
    'joyagoo-haul-guide-workflow-from-list-to-shipping': ['spreadsheet', 'buying', 'qc', 'shipping'],
    'review-notes-that-keep-haul-finds-organized': ['spreadsheet', 'qc', 'dead-links', 'updates'],
}
MARKER = re.compile(r'<!-- internal-links:start -->.*?<!-- internal-links:end -->\n?', re.S)


def render_internal_links(path, text):
    from localization import PAGE_PATHS, load_locale, ready
    relative = Path(path).relative_to(ROOT)
    lang = relative.parts[0]
    tail = '/'.join(relative.parts[1:-1])
    text = MARKER.sub('', text)
    article = tail.startswith(('articles/', 'blog/')) and tail != 'blog/routes'
    if article:
        keys = ARTICLE_LINKS.get(tail.split('/')[-1], ['spreadsheet', 'finds', 'buying', 'qc'])
    elif tail == '':
        keys = ['spreadsheet', 'buying', 'finds', 'shoes', 'clothing', 'accessories', 'qc', 'shipping']
    elif tail == 'joyagoo-spreadsheet':
        keys = ['finds', *[k for k in CATEGORIES if lang == 'en' or k in ('shoes', 'clothing', 'accessories')], 'buying', 'qc', 'shipping', 'updates']
    elif tail == 'best-joyagoo-finds':
        keys = ['spreadsheet', 'shoes', 'clothing', 'accessories', 'beauty-fragrance', 'electronics', 'taobao', 'weidian', '1688', 'buying', 'qc', 'shipping']
    elif tail == 'joyagoo-buying-guide':
        keys = ['spreadsheet', 'qc', 'shipping', 'coupon']
    elif tail.startswith('best-joyagoo-finds/'):
        keys = ['finds', 'spreadsheet', 'buying', 'qc', 'shipping']
    else:
        return text
    content = load_locale(lang) if lang != 'en' else None
    links = []
    for key in keys:
        target, label = PAGES[key]
        local = key in PAGE_PATHS and ready(lang, key)
        code = lang if lang == 'en' or local else 'en'
        if target.rstrip('/') == tail and code == lang:
            continue
        if content and local:
            label = content['pages'][key]['nav']
        elif code != lang:
            label += ' (English)'
        links.append(f'<li><a href="/{code}/{target}" lang="{code}">{escape(label)}</a></li>')
    heading = 'Next Pages' if article else (content['ui']['next'] if content else 'Explore related guides and finds')
    heading_lang = ' lang="en"' if article else ''
    block = ('<!-- internal-links:start -->'
             '<nav class="internal-links" aria-labelledby="internal-links-heading">'
             f'<h2 id="internal-links-heading"{heading_lang}>{escape(heading)}</h2>'
             '<ul>' + ''.join(links) + '</ul></nav><!-- internal-links:end -->\n')
    # Longform pages place navigation inside the article, after its final section.
    if article and re.search(r'<article\b', text):
        return text.replace('</article>', block + '</article>', 1)
    if text.count('</main>') != 1:
        raise ValueError(f'{path}: expected one main landmark')
    return text.replace('</main>', block + '</main>')


if __name__ == '__main__':
    import sys
    from localization import LANGUAGES
    changed = []
    for lang in LANGUAGES:
        for path in sorted((ROOT / lang).rglob('index.html')):
            original = path.read_text(encoding='utf-8')
            result = render_internal_links(path, original)
            if result != original:
                changed.append(str(path.relative_to(ROOT)))
                if '--check' not in sys.argv:
                    path.write_text(result, encoding='utf-8', newline='\n')
    print(f'Internal links: {len(changed)} pages ' + ('out of sync' if '--check' in sys.argv else 'updated'))
    if '--check' in sys.argv and changed:
        sys.exit(1)
