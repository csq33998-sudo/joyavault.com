"""Publication gates and sitemap must agree, including language alternates."""
import copy
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch
from finds_data import ROOT, load_finds
from indexability import exclusion_reason

class PublicationTests(unittest.TestCase):
    def test_discovery_gates_across_locales(self):
        data=load_finds()
        for route in ('/en/best-joyagoo-finds/', '/zh/best-joyagoo-finds/', '/en/best-joyagoo-finds/shoes/', '/de/best-joyagoo-finds/shoes/', '/en/marketplaces/taobao/'):
            self.assertIsNotNone(exclusion_reason(route,data))
        approved={**next(r for r in data if not r['isPlaceholder'] and r['category']=='Shoes'),'isIndexable':True}
        rows=[{**approved,'id':f'valid-{i}'} for i in range(8)]
        self.assertIsNone(exclusion_reason('/en/best-joyagoo-finds/shoes/',rows))
        self.assertIsNotNone(exclusion_reason('/en/best-joyagoo-finds/shoes/',rows[:7]))
        self.assertIsNotNone(exclusion_reason('/en/best-joyagoo-finds/clothing/',rows))

    def test_parameters_demo_and_unready_translations(self):
        data=load_finds()
        for route in ('/en/?q=shoes','/en/best-joyagoo-finds/?category=Shoes','/en/test/example/', '/en/demo/example/'):
            self.assertIsNotNone(exclusion_reason(route,data))
        for row in data:
            self.assertIsNotNone(exclusion_reason(row['detailUrl'],data))
        with patch('localization.ready',return_value=False):
            self.assertEqual(exclusion_reason('/zh/joyagoo-spreadsheet/',data),'translation-not-ready')

    def test_sitemap_alternates_are_indexable(self):
        root=ET.parse(ROOT/'sitemap.xml').getroot()
        urls={node.text for node in root.findall('{*}url/{*}loc')}
        data=load_finds()
        for url in urls:
            self.assertIsNone(exclusion_reason(url.removeprefix('https://joyavault.com'),data))
        for node in root.findall('{*}url/{*}link'):
            self.assertIn(node.attrib['href'],urls)

if __name__=='__main__': unittest.main()
