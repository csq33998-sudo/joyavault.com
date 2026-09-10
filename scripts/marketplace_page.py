"""Render marketplace guides from the shared finds collection, without inventing sources."""
from collections import Counter
from urllib.parse import urlencode
from find_card import card, e, popular_categories
from finds_data import ROOT
from category_page import NEXT_STEPS, links

MARKETPLACE_CONTENT = {
    'taobao': {
        'name': 'Taobao',
        'title': 'Taobao Finds Spreadsheet for Joyagoo | JoyaVault',
        'description': 'Explore the Taobao finds route on JoyaVault, compare clothing and accessory ideas, and prepare listing, QC, and shipping checks before Joyagoo.',
        'intro': 'Use the Taobao route to organize product ideas when your research starts with a Taobao listing. JoyaVault helps you move from a broad category to a shortlist, keeping the original source and selected options beside the questions you still need to answer.',
        'direction': 'Start with the type of item you need, then compare its details on the original listing. Clothing, shoes, and accessories are useful routes for building a focused shortlist rather than opening unrelated saved rows.',
        'categories': [
            ('Clothing', 'Compare the intended layer, garment measurements, and selected size before choosing a clothing candidate.'),
            ('Shoes', 'Narrow the intended use and silhouette, then record the size and variation you want to inspect.'),
            ('Accessories', 'Compare dimensions, included pieces, and how the accessory fits your planned order.'),
        ],
        'checks': [
            ('Keep the original listing', 'Save the full Taobao product URL and seller reference. A discovery card gives you a starting point; reopen the actual listing before relying on its information.'),
            ('Match the selected options', 'Record the size, color, and quantity together. Check that the displayed price refers to the combination you intend to buy.'),
            ('Use measurements for comparison', 'Compare the relevant measurements with an item that suits you. A familiar size label does not answer every fit question.'),
            ('Prepare the next decision', 'Write down the photos or details you will want to review and reserve a separate shipping budget before expanding your shortlist.'),
        ],
        'faq': [
            ('What is this Taobao finds page useful for?', 'Use it to choose a category, organize Taobao-related research, and prepare questions for the original listing. JoyaVault supplies discovery context and guides; the marketplace and your shopping agent handle the actual transaction.'),
            ('Which category should I browse first?', 'Start with your intended use. Clothing is a useful route when fit and measurements lead the decision; shoes and accessories provide narrower alternatives when you already know the type of item you need.'),
            ('Does a saved price confirm what I will pay?', 'No. Confirm the price for your selected variation and quantity on the live listing. Example prices are illustrative, and product spending should remain separate from the later parcel budget.'),
            ('How do I continue from a Taobao shortlist?', 'Keep the original link and exact options, read the buying guide, and continue to your chosen agent. Confirm that the loaded product matches your notes before taking an ordering action.'),
        ],
    },
    'weidian': {
        'name': 'Weidian',
        'title': 'Weidian Finds Spreadsheet for Joyagoo | Source & QC Notes',
        'description': 'Browse the Weidian finds route with shoes, clothing, and accessory ideas, plus seller, variant, QC, and parcel questions to check before buying.',
        'intro': 'The Weidian route is useful when a saved product or seller link is your starting point. Use JoyaVault to keep that source identifiable while you compare product direction, selected versions, and the details you want to check before continuing to Joyagoo.',
        'direction': 'Keep each candidate tied to its own seller and options. Begin with shoes if footwear is your goal, or explore clothing and accessories when another part of your shortlist needs attention.',
        'categories': [
            ('Shoes', 'Compare the exact version, selected size, and visible details that matter to your footwear choice.'),
            ('Clothing', 'Record measurements and option names rather than combining information from similar-looking listings.'),
            ('Accessories', 'Check the intended dimensions, construction details, and included pieces before adding another item.'),
        ],
        'checks': [
            ('Identify the seller and item', 'Keep the original Weidian link with the seller and product reference. Do not combine details from separate listings into one assumed offer.'),
            ('Distinguish similar versions', 'Check the description and selected variation even when images look alike. Similar photos do not establish that two listings describe the same product.'),
            ('Make QC expectations specific', 'Write down the label, color, quantity, and visible details you will compare with received-item photos. Resolve missing listing information before ordering.'),
            ('Keep replacements separate', 'If the saved link stops opening, investigate the original source before choosing another candidate. Review the replacement as a new listing.'),
        ],
        'faq': [
            ('Should I browse Weidian only for shoes?', 'No. Use the category that matches your needs. This page includes shoes, clothing, and accessory routes, and the grid reflects the records currently labeled Weidian in the JoyaVault collection.'),
            ('Do similar product photos mean the versions are identical?', 'No. Compare the seller, description, selected options, measurements, and included pieces. Mark unclear differences as questions rather than treating the listings as interchangeable.'),
            ('What if a Weidian link no longer loads?', 'Check the original URL and record what fails. If you have already paid, review the existing order before buying a replacement. Use the dead product link guide to organize the comparison.'),
            ('Where do I review an actual order?', 'Use the account of the agent handling your purchase. JoyaVault provides research notes and QC checklists but does not hold your order, inspect your warehouse item, or arrange dispatch.'),
        ],
    },
    '1688': {
        'name': '1688',
        'title': '1688 Finds Spreadsheet for Joyagoo | Quantity & Cost Guide',
        'description': 'Explore 1688 finds by category and compare quantity, selected options, price assumptions, QC needs, and shipping plans before continuing to Joyagoo.',
        'intro': 'Use the 1688 route when your product research needs a careful comparison of quantity, selected options, and the amount shown for that combination. JoyaVault helps you organize these questions before you carry an original listing into the Joyagoo buying flow.',
        'direction': 'Choose a category first, then confirm that the intended quantity and variation suit your needs. A low displayed amount is only useful when it describes the order you actually want to make.',
        'categories': [
            ('Clothing', 'Check sizes and quantity choices together, especially when comparing more than one intended variation.'),
            ('Accessories', 'Record whether the listing describes an individual piece, a set, or another quantity before comparing costs.'),
            ('Electronics', 'Compare the exact model, compatibility, and included pieces, then clarify parcel eligibility for the intended item.'),
        ],
        'checks': [
            ('Check the quantity condition', 'Read the quantity choices or requirements shown on the specific 1688 listing. Confirm that they fit your intended purchase rather than assuming a displayed amount applies to one item.'),
            ('Compare the selected total', 'Use the same quantity and equivalent options when comparing candidates. Keep product cost and delivery estimates on separate lines.'),
            ('Resolve specifications', 'Record measurements, material descriptions, compatibility, or included pieces relevant to the category. Ask about missing details before treating the item as ready to buy.'),
            ('Consider the complete parcel', 'Think about the bulk and packaging of the intended quantity. Check available shipping options for the actual contents before increasing an order to chase a lower unit price.'),
        ],
        'faq': [
            ('Should I assume every 1688 item has the same quantity requirement?', 'No. Read the conditions and quantity choices on the individual listing. If a requirement or price tier is unclear, confirm what applies to your intended selection before paying.'),
            ('How should I compare an 1688 price with another find?', 'Compare equivalent variations and the quantity you actually need. Record which costs are included and keep unknown delivery amounts visible instead of treating them as zero.'),
            ('Should I buy extra items to lower the unit price?', 'Compare the complete expanded order with your original plan, including the added items and parcel budget. A lower unit price does not automatically mean lower overall spending.'),
            ('Can JoyaVault place an 1688 order for me?', 'No. JoyaVault helps with discovery and preparation. Continue to the shopping platform or agent you choose for the actual order, payment, warehouse questions, and shipping arrangements.'),
        ],
    },
}


def marketplace_outputs(data, shell):
    outputs = {}
    for slug, content in MARKETPLACE_CONTENT.items():
        name = content['name']
        records = [item for item in data if item['marketplace'] == name and not item['isPlaceholder'] and item['sourceUrl'] != '#']
        counts = Counter(item['category'] for item in records)
        examples = sum(item['isPlaceholder'] for item in records)
        saved = len(records) - examples
        route = f'/en/marketplaces/{slug}/'
        categories = ''.join(f'<a class="home-category-card" href="{e("/en/best-joyagoo-finds/?" + urlencode({"category": category, "marketplace": name}) + "#finds")}"><h3>{e(category)}</h3><p>{e(copy)}</p><span>{counts[category]} matching directory records</span></a>' for category, copy in content['categories'])
        cards = ''.join(card(item).replace('</h3>', '</h3><p class="marketplace-card-note">' + e('Research prompt: ' + item['qcNotes'][0]) + '</p>', 1) for item in records)
        status = f'{len(records)} records filtered by the {name} label: {saved} saved listings and {examples} examples.'
        if not records:
            status = f'No product listings from {name} are available in this directory yet.'
            cards = '<div class="finds-empty"><h3>Explore available finds</h3><p>Choose another category or read the buying guide while this collection is being prepared.</p>'+popular_categories()+'</div>'
        else:
            status += ' Saved listings are unverified, not live offers. Examples have illustrative prices and marketplace assignments and no seller link.'
        status += ' Record dates refer to directory maintenance.'
        faq = [*content['faq'], ('Are these cards verified products I can buy?', 'Read each record label before continuing. Example records illustrate browsing and have no seller source. Saved listings, when supplied, still need checking against the original product page. JoyaVault does not guarantee availability or a live price.')]
        table_rows = [
            ('When to start here', 'Your shortlist already points to a Taobao item.', 'A Weidian product or seller link is your starting point.', 'An 1688 listing needs a quantity and option comparison.'),
            ('Useful research focus', 'Fit, selected variation, and current listing details.', 'Seller reference, exact version, and visible item details.', 'Intended quantity, specifications, and the selected total.'),
            ('Compare before deciding', 'Measurements and options for your candidate.', 'Descriptions of similar-looking versions.', 'Equivalent options at the quantity you need.'),
            ('What the label cannot establish', 'Availability, fit, or the final delivered cost.', 'Quality, authenticity, or equivalence between sellers.', 'A universally cheaper price or a fixed quantity rule.'),
        ]
        table = ''.join('<tr><th scope="row">'+e(row[0])+'</th>'+''.join('<td>'+e(cell)+'</td>' for cell in row[1:])+'</tr>' for row in table_rows)
        main = f'''<main id="main" class="home-main marketplace-page">
<section class="catalog-intro"><div class="home-shell"><nav class="catalog-breadcrumb" aria-label="Breadcrumb"><a href="/en/">Home</a><span>/</span><a href="/en/best-joyagoo-finds/">Finds</a><span>/</span><span aria-current="page">{e(name)}</span></nav>
<p class="home-eyebrow">MARKETPLACE DISCOVERY</p><h1>{e(name)} Finds Spreadsheet for Joyagoo</h1><p class="catalog-intro-copy">{e(content['intro'])}</p><p class="category-copy">JoyaVault is an independent discovery and guide site. Continue to your chosen agent for account access, orders, payments, QC, warehouse services, and shipping.</p><div class="catalog-intro-links"><a href="#featured-finds">Explore {e(name)} records ↓</a><a href="#source-checks">Read the source checklist</a></div></div></section>
<section class="home-section home-category-band"><div class="home-shell"><h2>Best categories to browse from this marketplace</h2><p class="category-copy">{e(content['direction'])}</p><div class="category-signals">{categories}</div></div></section>
<section id="featured-finds" class="home-section home-shell"><h2>Featured {e(name)} finds</h2><p class="home-section-note" id="marketplace-record-status">{e(status)}</p><div class="home-product-grid" data-marketplace-grid="{e(name)}" aria-describedby="marketplace-record-status">{cards}</div></section>
<section id="source-checks" class="home-section home-guide-band"><div class="home-shell"><h2>What to check before opening source links</h2><p>Use the record label first. A pending source is not a purchase link; for a supplied source, compare the live listing with your notes.</p><div class="category-checks">{''.join('<article><h3>'+e(title)+'</h3><p>'+e(copy)+'</p></article>' for title, copy in content['checks'])}</div></div></section>
<section class="home-section home-shell"><h2>Taobao vs Weidian vs 1688</h2><p class="category-copy">Compare the research question, not a blanket ranking. The specific seller, listing, and chosen options matter more than assuming one marketplace suits every purchase.</p><div class="comparison-table-wrap" role="region" aria-label="Marketplace comparison" tabindex="0"><table class="comparison-table"><caption>Choose a marketplace route for your next check</caption><thead><tr><th scope="col">Research need</th><th scope="col"><a href="/en/marketplaces/taobao/">Taobao</a></th><th scope="col"><a href="/en/marketplaces/weidian/">Weidian</a></th><th scope="col"><a href="/en/marketplaces/1688/">1688</a></th></tr></thead><tbody>{table}</tbody></table></div><p class="category-copy">Read the <a href="/en/articles/taobao-weidian-1688-finds-guide/">marketplace finds guide</a> for a fuller comparison, or use the <a href="/en/articles/dead-product-link-fix/">dead product link guide</a> when a saved source stops opening.</p></section>
<section class="home-section home-shell"><h2>Next steps</h2><div class="category-signals">{links(NEXT_STEPS)}</div></section>
<section class="home-section home-faq-band"><div class="home-shell faq-layout"><div><p class="home-eyebrow">MARKETPLACE QUESTIONS</p><h2>{e(name)} FAQ</h2></div><div class="home-faq">{''.join('<details open><summary>'+e(q)+'</summary><p>'+e(a)+'</p></details>' for q,a in faq)}</div></div></section>
</main>'''
        graph = {'@context': 'https://schema.org', '@graph': [
            {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': i, 'name': label, 'item': 'https://joyavault.com'+url} for i,(label,url) in enumerate([('Home','/en/'),('Finds','/en/best-joyagoo-finds/'),(name,route)],1)]},
            {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer','text':a}} for q,a in faq]},
        ]}
        outputs[ROOT / route.strip('/') / 'index.html'] = shell(content['title'], content['description'], route, main, indexable=True, structured_data=graph)
    return outputs
