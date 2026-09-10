"""Archive public shop listings using the endpoint used by Weidian's shop page.

No login, cookies, private APIs, or publication changes. Re-running refreshes
the snapshot; item IDs deduplicate products. Raw data is kept for review.
"""
import json
from datetime import datetime, timezone
from pathlib import Path
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SHOP_ID = 1663319819
ENDPOINT = 'https://thor.weidian.com/decorate/shopDetail.open.getCateItemList/1.0'
DEST = ROOT / 'src/data/imports/weidian-1663319819.json'


def fetch_page(page):
    params = dict(shopId=SHOP_ID, ctx=f'0;0;0;{SHOP_ID};0;0;0;0;0;-1;-1;0;0;0;0',
                  sectionId=501, cateId='0', pageNum=page, pageSize=20, sort=0)
    request = Request(ENDPOINT + '?' + urlencode({'param': json.dumps(params)}),
                      headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://weidian.com/'})
    with urlopen(request, timeout=25) as response:
        payload = json.load(response)
    if payload.get('status', {}).get('code') != 0:
        raise RuntimeError(f'Public endpoint returned {payload.get("status")}')
    return payload.get('result', {}).get('itemList', [])


if __name__ == '__main__':
    DEST.parent.mkdir(parents=True, exist_ok=True)
    records = {}
    complete = False
    for page in range(200):
        rows = fetch_page(page)
        if not rows:
            complete = True
            break
        before = len(records)
        for row in rows:
            item_id = str(row['itemId'])
            if row['itemUrl'] != f'https://weidian.com/item.html?itemID={item_id}':
                raise ValueError('Unexpected product destination')
            records[item_id] = {key: row.get(key) for key in
                               ('itemId', 'itemName', 'itemImg', 'itemUrl', 'price', 'status', 'stock')}
        if len(records) == before:
            raise RuntimeError('Pagination repeated; refusing to claim a complete snapshot')
        DEST.write_text(json.dumps(dict(shopId=SHOP_ID, fetchedAt=datetime.now(timezone.utc).isoformat(),
                                        complete=False, items=list(records.values())), ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'Page {page + 1}: {len(records)} unique products', flush=True)
        time.sleep(.25)
    snapshot = json.loads(DEST.read_text(encoding='utf-8'))
    snapshot['complete'] = complete
    DEST.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Saved {len(records)} products; reached end: {complete}')

