"""Contract tests for editable data, rendered cards, and static fallbacks."""
import copy
import json
import re
from html.parser import HTMLParser
import unittest
from finds_data import ROOT, TAXONOMY, load_finds, validate, catalog_records
from find_card import card, source_link


class Markup(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class FindsTests(unittest.TestCase):
    def setUp(self):
        self.data = load_finds()

    def test_seed_coverage(self):
        self.assertGreaterEqual(len(self.data), 60)
        for category, subs in TAXONOMY.items():
            self.assertTrue(set(subs) <= {row['subcategory'] for row in self.data if row['category'] == category})
        self.assertTrue({'Taobao', 'Weidian', '1688'} <= {row['marketplace'] for row in self.data})

    def test_bad_edits_fail_before_build(self):
        for key, value in [('isIndexable', 'false'), ('priceCny', -1), ('subcategory', 'Typo'), ('updatedAt', '2026-02-31'), ('sourceUrl', 'javascript:alert(1)'), ('detailUrl', '/../outside/'), ('id', self.data[1]['id'])]:
            with self.subTest(key=key):
                bad = copy.deepcopy(self.data)
                bad[0][key] = value
                with self.assertRaises(ValueError):
                    validate(bad)

    def test_source_link_policy(self):
        for row in self.data:
            markup = Markup(source_link(row))
            links = [attrs for tag, attrs in markup.tags if tag == 'a']
            if row['sourceUrl'] == '#':
                self.assertEqual(links[0]['href'], row['detailUrl'] + '#product-source')
                self.assertIn('Source unavailable', source_link(row))
                self.assertNotIn('Open product source', source_link(row))
            else:
                self.assertEqual(links[0]['href'], row['sourceUrl'])
                if row['sourceType'] in ('commercial', 'affiliate'):
                    self.assertTrue({'sponsored', 'nofollow', 'noopener', 'noreferrer'} <= set(links[0]['rel'].split()))
        affiliate = {**self.data[0], 'sourceType': 'affiliate'}
        self.assertIn('sponsored nofollow noopener noreferrer', source_link(affiliate))

    def test_generic_sources_rejected(self):
        for url in ('https://maisonlooks.com/', 'https://maisonlooks.com/en/', 'https://maisonlooks.com/en/products', 'https://maisonlooks.com/en/search?q=shoes', 'https://streetstyle.maisonlooks.com/en/p/example'):
            bad = copy.deepcopy(self.data)
            bad[0]['sourceUrl'] = url
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate(bad)

    def test_catalog_publication_selection(self):
        records, indexable = catalog_records(self.data)
        self.assertFalse(indexable)
        self.assertTrue(all(not row['isPlaceholder'] and row['sourceUrl'] != '#' for row in records))
        demos = [row for row in self.data if row['isPlaceholder']]
        self.assertEqual(catalog_records(demos), ([], False))
        real = {**next(row for row in self.data if not row['isPlaceholder']), 'isIndexable': True}
        records, indexable = catalog_records([*self.data, real])
        self.assertTrue(indexable)
        self.assertEqual(records, [real])
        html = (ROOT / 'en/best-joyagoo-finds/index.html').read_text(encoding='utf-8')
        self.assertIn('noindex, follow', html)
        self.assertNotIn('<loc>https://joyavault.com/en/best-joyagoo-finds/</loc>', (ROOT / 'sitemap.xml').read_text(encoding='utf-8'))
        for field in ('subcategory', 'min-price', 'max-price'):
            self.assertIn('id="finds-' + field + '"', html)

    def test_demo_indexing_guard(self):
        bad = copy.deepcopy(self.data)
        next(row for row in bad if row['isPlaceholder'])['isIndexable'] = True
        with self.assertRaises(ValueError):
            validate(bad)
        missing = copy.deepcopy(self.data)
        del missing[0]['isIndexable']
        with self.assertRaises(ValueError):
            validate(missing)
        sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
        for row in self.data:
            if not row['isIndexable']:
                html = (ROOT / row['detailUrl'].strip('/') / 'index.html').read_text(encoding='utf-8')
                self.assertIn('<meta name="robots" content="noindex, follow"', html)
                self.assertNotIn('https://joyavault.com' + row['detailUrl'] + '</loc>', sitemap)
                if row['sourceUrl'] == '#':
                    self.assertIn('id="product-source"', html)

    def test_card_notes_and_anchor_actions(self):
        for row in self.data:
            html = card(row)
            if row['isPlaceholder']:
                self.assertEqual(html, '')
                continue
            self.assertIn('QC notes:', html)
            self.assertIn('Shipping notes:', html)
            self.assertNotIn('<button', html)
            self.assertRegex(html, r'<a [^>]*href="[^"]+"[^>]*>View details</a>')
            label = 'Source unavailable' if row['sourceUrl'] == '#' else 'Open product source'
            self.assertRegex(html, r'<a [^>]*href="[^"]+"[^>]*>' + label)

    def test_card_escapes_editable_content(self):
        row = {**self.data[0], 'title': '<script>alert(1)</script>', 'tags': ['" onmouseover="alert(1)']}
        output = card(row)
        self.assertNotIn('<script>', output)
        self.assertTrue(all('onmouseover' not in attrs for _, attrs in Markup(output).tags))

    def test_static_home_and_catalog(self):
        for path, visible_count in [('en/index.html', 8), ('en/best-joyagoo-finds/index.html', len(catalog_records(self.data)[0]))]:
            markup = Markup((ROOT / path).read_text(encoding='utf-8'))
            cards = [attrs for _, attrs in markup.tags if 'data-find-id' in attrs]
            self.assertEqual(len(cards), len([row for row in self.data if not row['isPlaceholder']]) if path == 'en/index.html' else len(catalog_records(self.data)[0]))
            self.assertEqual(sum('hidden' not in attrs for attrs in cards), visible_count)
            self.assertEqual(sum(tag == 'h1' for tag, _ in markup.tags), 1)
            self.assertFalse(any(tag == 'a' and attrs.get('href') == '#' for tag, attrs in markup.tags))
            self.assertTrue(all('alt' in attrs for tag, attrs in markup.tags if tag == 'img'))
            self.assertTrue(any(attrs.get('aria-label') == 'Popular categories' for _, attrs in markup.tags))
            html = (ROOT / path).read_text(encoding='utf-8')
            empty = html.split('id="finds-empty"', 1)[1].split('</div>', 1)[0]
            self.assertIn('/en/joyagoo-buying-guide/', empty)
            self.assertIn('Popular categories', empty)
        catalog = (ROOT / 'en/best-joyagoo-finds/index.html').read_text(encoding='utf-8')
        self.assertIn('id="finds-category"', catalog)
        self.assertIn('id="finds-marketplace"', catalog)
        self.assertIn('id="finds-brand"', catalog)
        self.assertIn('data-page-size="24"', catalog)
        self.assertIn('<h1>Best Joyagoo Finds Spreadsheet</h1>', catalog)
        self.assertIn('<title>Best Joyagoo Finds Spreadsheet | Shoes, Clothing, Accessories</title>', catalog)
        breadcrumb = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', catalog).group(1))
        breadcrumb = next(node for node in breadcrumb['@graph'] if node['@type'] == 'BreadcrumbList')
        self.assertEqual(breadcrumb['@type'], 'BreadcrumbList')
        self.assertEqual(breadcrumb['itemListElement'][-1]['item'], 'https://joyavault.com/en/best-joyagoo-finds/')
        self.assertIn('/en/best-joyagoo-finds/?page=2#finds', catalog)


if __name__ == '__main__':
    unittest.main()
