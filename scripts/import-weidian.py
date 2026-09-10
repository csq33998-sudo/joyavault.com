"""Import the first manually categorized selection from the public shop snapshot."""
import json
from pathlib import Path
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from finds_data import ROOT, validate

# Neutral English descriptions of seller titles, not inferred brands or quality claims.
SELECTION = [
    ('7632057229', 'Running shoes 1', 'Shoes', 'Sneakers'),
    ('7632169241', 'LXD zip-neck knitted sweater', 'Clothing', 'Tops'),
    ('7632217737', 'Outdoor casual sports shoes 70', 'Shoes', 'Sneakers'),
    ('7632057227', 'Couple sweatshirt', 'Clothing', 'Tops'),
    ('7635193722', 'Summer shorts SQ002', 'Clothing', 'Bottoms'),
    ('7632171167', 'Crew-neck sweatshirt 006', 'Clothing', 'Tops'),
    ('7635115516', 'Autumn sweater', 'Clothing', 'Tops'),
    ('7632217731', 'Casual hooded sweatshirt', 'Clothing', 'Hoodies'),
    ('7635195732', 'BQQ casual sports shoes', 'Shoes', 'Sneakers'),
    ('7632177081', 'Casual sports shoes 18', 'Shoes', 'Sneakers'),
    ('7635109580', 'Sports shoes ab88', 'Shoes', 'Sneakers'),
    ('7635129468', 'L home hoodie', 'Clothing', 'Hoodies'),
    ('7632145463', 'Casual sneakers 031', 'Shoes', 'Sneakers'),
    ('7635037222', 'Summer short-sleeved top FF01', 'Clothing', 'Tops'),
    ('7635135436', 'Casual jacket KK10', 'Clothing', 'Outerwear'),
    ('7632203803', 'Casual sweater pc', 'Clothing', 'Tops'),
    ('7635160048', 'Casual hooded top', 'Clothing', 'Hoodies'),
    ('7635125476', 'Winter padded jacket YZX01', 'Clothing', 'Outerwear'),
    ('7632161419', 'Short-sleeved T-shirt', 'Clothing', 'Tops'),
    ('7635155070', 'Bag collection KK10', 'Accessories', 'Bags'),
    ('7635197704', 'Jeans — seller style AM1R1', 'Clothing', 'Bottoms'),
    ('7635115502', 'Short-sleeved top 005', 'Clothing', 'Tops'),
    ('7635133392', 'Bracelet 001', 'Accessories', 'Jewelry'),
    ('7635133388', 'Bag BS177', 'Accessories', 'Bags'),
    ('7631314185', 'Perfume collection LL55', 'Beauty & Fragrance', 'Perfume'),
    ('7631369795', 'Woody fragrance — seller listing', 'Beauty & Fragrance', 'Perfume'),
    ('7633734032', 'Fragrance collection — multiple scent options', 'Beauty & Fragrance', 'Perfume'),
    ('7632833718', '100ml perfume collection FC888', 'Beauty & Fragrance', 'Perfume'),
    ('7632681538', 'Perfume collection — check return conditions', 'Beauty & Fragrance', 'Perfume'),
    ('7628005287', 'Perfume q1', 'Beauty & Fragrance', 'Perfume'),
    ('7629848005', 'Woody and fruit fragrance collection D', 'Beauty & Fragrance', 'Perfume'),
    ('7630917446', '100ml fragrance — seller listing', 'Beauty & Fragrance', 'Perfume'),
    ('7631699819', 'Earphones m1GS5', 'Electronics', 'Audio'),
    ('7632879812', 'Phone case 006', 'Electronics', 'Phone Accessories'),
    ('7629755579', 'Phone case P', 'Electronics', 'Phone Accessories'),
    ('7629811701', 'Over-ear headphones', 'Electronics', 'Audio'),
    ('7629039785', 'Earphones DS', 'Electronics', 'Audio'),
    ('7630915444', 'Phone case collection', 'Electronics', 'Phone Accessories'),
    ('7634603260', 'Bluetooth speaker — seller listing', 'Electronics', 'Audio'),
    ('7631935566', 'Speaker and watch collection OO01', 'Electronics', 'Audio'),
    ('7631836909', 'Wallet — seller listing', 'Accessories', 'Bags'),
    ('7634804962', 'Textured bag — seller listing', 'Accessories', 'Bags'),
    ('7634666226', 'Bracelet and necklace collection OO01', 'Accessories', 'Jewelry'),
    ('7634605352', 'Casual messenger bag 01', 'Accessories', 'Bags'),
]


def make_record(selection, source, updated):
    item_id, title, category, sub = selection
    row = source[item_id]
    if row['status'] != 1 or float(row['price']) < 0:
        raise ValueError(f'{item_id}: unavailable or invalid listing')
    with urlopen(Request(row['itemImg'], headers={'User-Agent': 'Mozilla/5.0'}), timeout=25) as response:
        content_type = response.headers.get_content_type()
        extension = {'image/jpeg': 'jpg', 'image/png': 'png', 'image/gif': 'gif', 'image/webp': 'webp'}.get(content_type)
        if not extension:
            raise ValueError(f'{item_id}: expected a product image, got {content_type}')
        image = f'/assets/products/weidian/{item_id}.{extension}'
        path = ROOT / image.lstrip('/')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(response.read())
    qc = {
        'Shoes': ['Ask for size-label and insole measurements for the selected size.', 'Check both shoes, outsole edges and stitching in QC photos.'],
        'Clothing': ['Compare chest, length and sleeve measurements with clothing you already own.', 'Check seams, closures and the selected color in QC photos.'],
        'Accessories': ['Confirm dimensions, material description and the exact selected option.', 'Inspect closures, hardware and surface finish in QC photos.'],
        'Beauty & Fragrance': ['Confirm the selected scent, bottle volume, ingredients and batch information with the seller.', 'Check seals, packaging and signs of leaks; photos cannot establish authenticity or skin safety.'],
        'Electronics': ['Confirm the exact model, compatibility and included accessories for your selected option.', 'Request a function check for powered devices; for phone cases, check dimensions and camera cutouts.'],
    }[category]
    shipping = {
        'Shoes': 'Ask for packed weight and dimensions with and without the shoe box before comparing shipping quotes.',
        'Clothing': 'Request packed weight for your selected quantity; bulky layers can increase parcel volume.',
        'Accessories': 'Ask about protective packaging and packed dimensions; rigid hardware and delicate surfaces may need extra protection.',
        'Beauty & Fragrance': 'Confirm liquid and alcohol acceptance with the shipping provider before paying. Ask about leak protection and the seller return conditions.',
        'Electronics': 'Declare any batteries and confirm route eligibility before paying. Ask for packed weight and protective packaging; phone cases require model confirmation.',
    }[category]
    return dict(id='weidian-'+item_id, title=title, category=category, subcategory=sub,
                brand='Not specified', marketplace='Weidian', priceCny=float(row['price']),
                image=image, sourceUrl=row['itemUrl'], detailUrl=f'/en/finds/weidian-{item_id}/',
                tags=[sub, 'Weidian shop 1663319819'], qcNotes=qc, shippingNotes=[shipping],
                updatedAt=updated, isIndexable=False, sourceType='commercial', isPlaceholder=False,
                featured=True, imageAlt=title+' — seller product photo',
                description=f'Seller listing from Weidian shop 1663319819. Original listing title: {row["itemName"]}. The saved price may depend on the selected option. Confirm specifications and current availability at the source; this listing has not been independently QC tested.',
                sourceName='Weidian · 夕阳的刻痕 (1663319819)')


if __name__ == '__main__':
    snapshot = json.loads((ROOT / 'src/data/imports/weidian-1663319819.json').read_text(encoding='utf-8'))
    source = {str(row['itemId']): row for row in snapshot['items']}
    updated = datetime.fromisoformat(snapshot['fetchedAt']).date().isoformat()
    with ThreadPoolExecutor(max_workers=4) as pool:
        imported = list(pool.map(lambda selection: make_record(selection, source, updated), SELECTION))
    path = ROOT / 'src/data/finds.json'
    existing = json.loads(path.read_text(encoding='utf-8'))
    imported_ids = {row['id'] for row in imported}
    data = imported + [{**row, 'featured': False} for row in existing if row['id'] not in imported_ids]
    validate(data)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f'Imported {len(imported)} listings with local seller images; existing records retained.')
