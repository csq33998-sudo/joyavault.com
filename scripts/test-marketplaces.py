"""Check marketplace filtering, honest example labels, links, and FAQ parity."""
from html import unescape
from html.parser import HTMLParser
import json
import re
import unittest
from urllib.parse import urlsplit, parse_qs
from finds_data import ROOT, load_finds
from marketplace_page import MARKETPLACE_CONTENT
from category_page import NEXT_STEPS


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.tags = []; self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class MarketplaceTests(unittest.TestCase):
    def test_marketplace_pages(self):
        data = load_finds()
        titles, descriptions = [], []
        for slug, content in MARKETPLACE_CONTENT.items():
            with self.subTest(marketplace=slug):
                text = (ROOT / f'en/marketplaces/{slug}/index.html').read_text(encoding='utf-8')
                tags = Tags(text).tags
                self.assertEqual(re.findall(r'<h1>(.*?)</h1>', text), [content['name'] + ' Finds Spreadsheet for Joyagoo'])
                titles.append(unescape(re.search(r'<title>(.*?)</title>', text).group(1)))
                descriptions.append(next(a['content'] for t,a in tags if t == 'meta' and a.get('name') == 'description'))
                self.assertEqual(titles[-1], content['title'])
                self.assertEqual(descriptions[-1], content['description'])
                records = {item['id']:item for item in data if item['marketplace'] == content['name'] and not item['isPlaceholder'] and item['sourceUrl'] != '#'}
                cards = [a for t,a in tags if 'data-find-id' in a]
                if not records:
                    self.assertIn('No product listings from', text)
                    self.assertIn('noindex, follow', text)
                self.assertEqual({a['data-find-id'] for a in cards}, set(records))
                self.assertTrue(all(a['data-marketplace'] == content['name'] and 'hidden' not in a for a in cards))
                self.assertEqual(len(cards), len(re.findall('class="marketplace-card-note"', text)))
                for markup in re.findall(r'<article class="find-card".*?</article>', text, re.S):
                    item = records[Tags(markup).tags[0][1]['data-find-id']]
                    self.assertIn(item['detailUrl'], markup)
                    self.assertIn('<img ', markup)
                    if item['isPlaceholder']:
                        self.assertIn('Example record', markup)
                        self.assertIn('Example price', markup)
                        self.assertIn('Source pending', markup)
                        self.assertNotIn('href="#"', markup)
                links = [a for t,a in tags if t == 'a']
                for url,_,_ in NEXT_STEPS:
                    self.assertTrue(any(a.get('href') == url for a in links))
                categories = [a for a in links if a.get('class') == 'home-category-card' and '?' in a.get('href','')]
                self.assertEqual(len(categories), 3)
                for a in categories:
                    query = parse_qs(urlsplit(a['href']).query)
                    self.assertEqual(query['marketplace'], [content['name']])
                    self.assertIn(query['category'][0], {name for name, _ in content['categories']})
                self.assertIn('<table class="comparison-table">', text)
                graph = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', text).group(1))['@graph']
                faq = next(x for x in graph if x['@type'] == 'FAQPage')['mainEntity']
                visible = re.findall(r'<details open><summary>(.*?)</summary><p>(.*?)</p></details>', text)
                self.assertEqual(len(faq), len(visible))
                self.assertGreaterEqual(len(faq), 4)
                for (q,a), entity in zip(visible, faq):
                    self.assertEqual(unescape(q), entity['name'])
                    self.assertEqual(unescape(a), entity['acceptedAnswer']['text'])
        self.assertEqual(len(set(titles)), 3)
        self.assertEqual(len(set(descriptions)), 3)


if __name__ == '__main__':
    unittest.main()
