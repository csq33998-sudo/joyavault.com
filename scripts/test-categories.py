"""Check category content, crawlable cards, and category-specific image descriptions."""
import json
import re
import unittest
from category_content import CATEGORIES
from category_page import category_records, NEXT_STEPS
from finds_data import ROOT, load_finds
from html.parser import HTMLParser

class Tags(HTMLParser):
    def __init__(self, html):
        super().__init__(); self.tags=[]; self.feed(html)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag,dict(attrs)))

class CategoryTests(unittest.TestCase):
    def test_indexability_threshold(self):
        base = next(row for row in load_finds() if row['category'] == 'Shoes' and not row['isPlaceholder'])
        approved = [{**base, 'id': f'approved-{i}', 'isIndexable': True} for i in range(8)]
        demo = {**base, 'isPlaceholder': True, 'isIndexable': False}
        self.assertFalse(category_records(approved[:7] + [demo], 'Shoes')[1])
        records, indexable = category_records(approved + [demo], 'Shoes')
        self.assertTrue(indexable)
        self.assertEqual(records, approved)
        self.assertFalse(category_records(approved, 'Clothing')[1])

    def test_category_contract(self):
        data=load_finds(); descriptions=[]
        for slug,c in CATEGORIES.items():
            with self.subTest(category=slug):
                html=(ROOT / f'en/best-joyagoo-finds/{slug}/index.html').read_text(encoding='utf-8')
                tags=Tags(html).tags
                self.assertEqual(sum(t=='h1' for t,a in tags),1)
                self.assertLessEqual(len(c['title']),60)
                descriptions.append(c['description'])
                main_tags=Tags(re.search(r'<main\b[^>]*>(.*?)</main>',html,re.S).group(1)).tags
                self.assertEqual(sum(t=='details' for t,a in main_tags),len(c['faq']))
                self.assertGreaterEqual(len(c['faq']),4)
                self.assertIn('CATEGORY GUIDE', html)
                self.assertIn('id="shipping-notes"', html)
                self.assertIn('QC checklist</h2>', html)
                self.assertIn('Browse more in this category</a>', html)
                for url, title, _ in NEXT_STEPS:
                    self.assertTrue(any(t == 'a' and a.get('href') == url for t,a in main_tags))
                for title, copy in c['shipping']:
                    self.assertIn(copy, html)
                indexable = category_records(data, c['name'])[1]
                self.assertEqual('content="noindex, follow"' in html, not indexable)
                sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
                self.assertEqual(f'<loc>https://joyavault.com/en/best-joyagoo-finds/{slug}/</loc>' in sitemap, indexable)
                cards=[a for t,a in tags if 'data-find-id' in a]
                expected=category_records(data, c['name'])[0]
                self.assertTrue(len(cards) >= 8 or not indexable)
                self.assertEqual({a['data-find-id'] for a in cards},{x['id'] for x in expected})
                self.assertTrue(all(a['data-category']==c['name'] for a in cards))
                product_images=[a for t,a in tags if t=='img' and a.get('width')=='450']
                self.assertEqual(len(product_images),len(expected))
                self.assertTrue(all(c['name'] in a['alt'] for a in product_images))
                self.assertTrue(all(any(x['title'] in a['alt'] for x in expected) for a in product_images))
                schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',html).group(1))
                schema=next(node for node in schema['@graph'] if node['@type']=='BreadcrumbList')
                self.assertEqual(schema['itemListElement'][-1]['item'],f'https://joyavault.com/en/best-joyagoo-finds/{slug}/')
        self.assertEqual(len(set(descriptions)),5)

if __name__=='__main__': unittest.main()
