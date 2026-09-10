from indexability import exclusion_reason
from finds_data import load_finds
"""Audit locale availability, reciprocal metadata, navigation, RTL, and draft gates."""
from html.parser import HTMLParser
import importlib.util
import json
import re
import unittest
from unittest.mock import patch
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

import localization as loc
from site_routes import CANONICAL_ROUTES


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.tags=[]; self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag,dict(attrs)))


class LocaleTests(unittest.TestCase):
    def test_ready_collection(self):
        self.assertEqual(len(loc.localized_routes()),63)
        for lang in loc.LANGUAGES:
            if lang=='en': continue
            data=loc.load_locale(lang)
            self.assertEqual(set(data['pages']),set(loc.PAGE_PATHS))
            for key in loc.PAGE_PATHS:
                self.assertTrue(loc.ready(lang,key))
                self.assertNotIn('\ufffd',json.dumps(data,ensure_ascii=False))
                self.assertGreater(len(data['pages'][key]['checks']),2)

    def test_heads_and_navigation(self):
        for route in CANONICAL_ROUTES:
            text=(loc.ROOT/route.strip('/')/'index.html').read_text(encoding='utf-8')
            tags=Document(text).tags
            actual={a['hreflang']:a['href'] for t,a in tags if t=='link' and a.get('rel')=='alternate'}
            self.assertEqual(actual,loc.alternates(route),route)
            self.assertEqual(sum(t=='link' and a.get('rel')=='alternate' for t,a in tags),len(actual))
            canonical=[a['href'] for t,a in tags if t=='link' and a.get('rel')=='canonical']
            self.assertEqual(canonical,[loc.ORIGIN+route])
            self.assertIn('class="locale-switcher"',text)
            self.assertNotIn('{{language_switcher}}',text)
            for code,target in actual.items():
                target_route=urlsplit(target).path
                self.assertIn(target_route,CANONICAL_ROUTES)
                if code!='x-default':
                    self.assertIn(loc.ORIGIN+route,loc.alternates(target_route).values())

    def test_localized_content(self):
        for route in loc.localized_routes():
            lang,tail=loc.split_route(route)
            text=(loc.ROOT/route.strip('/')/'index.html').read_text(encoding='utf-8')
            tags=Document(text).tags
            html=next(a for t,a in tags if t=='html')
            self.assertEqual(html['lang'],lang)
            self.assertEqual(html['dir'],'rtl' if lang=='ar' else 'ltr')
            self.assertEqual(sum(t=='h1' for t,a in tags),1)
            self.assertEqual('noindex' in text, bool(exclusion_reason(route, load_finds())))
            self.assertNotIn('ml_language',text)
            self.assertGreaterEqual(sum(t=='h2' for t,a in tags),5)
            key=next(k for k,v in loc.PAGE_PATHS.items() if v==tail)
            page=loc.load_locale(lang)['pages'][key]
            schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',text,re.S).group(1))
            faq=next(x for x in schema['@graph'] if x['@type']=='FAQPage')['mainEntity']
            self.assertEqual([(x['name'],x['acceptedAnswer']['text']) for x in faq],[tuple(row) for row in page['faq']])
            if key=='buying': self.assertEqual(len(page['checks']),9)
            if key in ('qc','shipping'):
                self.assertTrue(any(x['@type']=='Article' and x['inLanguage']==lang for x in schema['@graph']))

    def test_sitemap(self):
        root=ET.parse(loc.ROOT/'sitemap.xml').getroot()
        entries={url.find('{*}loc').text:url for url in root.findall('{*}url')}
        for route in loc.localized_routes():
            url=loc.ORIGIN+route
            if exclusion_reason(route, load_finds()):
                self.assertNotIn(url, entries)
                continue
            self.assertIn(url,entries)
            links={x.attrib['hreflang']:x.attrib['href'] for x in entries[url].findall('{http://www.w3.org/1999/xhtml}link')}
            self.assertEqual(links,{code:target for code,target in loc.alternates(route).items() if target in entries})

    def test_draft_missing_and_incomplete(self):
        data=json.loads(json.dumps(loc.load_locale('de')))
        original=loc.load_locale
        with patch.object(loc,'load_locale',side_effect=lambda lang:data if lang=='de' else original(lang)):
            data['pages']['buying']['status']='draft'
            self.assertFalse(loc.ready('de','buying'))
            self.assertNotIn('/de/joyagoo-buying-guide/',loc.localized_routes())
            self.assertNotIn('de',loc.alternates('/en/joyagoo-buying-guide/'))
            self.assertIn('href="/de/"',loc.switcher('/en/joyagoo-buying-guide/'))
            data['pages']['buying']['status']='ready'
            data['pages']['buying']['intro']=''
            with self.assertRaises(ValueError): loc.ready('de','buying')
        with patch.object(loc,'load_locale',return_value=None):
            self.assertFalse(loc.ready('de','home'))


if __name__=='__main__': unittest.main()
