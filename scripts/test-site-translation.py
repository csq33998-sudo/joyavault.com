"""Tests use fixture translations, never live APIs or fake public translations."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import site_translation as st
import localization as loc

spec=importlib.util.spec_from_file_location('translate_site',Path(__file__).with_name('translate-site.py'))
cli=importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


class TranslationTests(unittest.TestCase):
    def render(self, source, mapping, lang='de', available=('/de/shoes/',)):
        cache={st.key(s):{'source':s,'translation':t} for s,t in mapping.items()}
        return st.Page(source,cache,lang,available).render()

    def test_html_entities_structure_urls_and_script_preserved(self):
        source='<html lang="en"><head><title>Shoes &amp; bags</title></head><body><a href="/en/shoes/?brand=Nike#finds">Shop now</a><p>One <strong>pair</strong> &amp; more.</p><script>const label = "Do not translate code";</script><style>.x{color:red}</style><input value="All" placeholder="Search shoes"></body></html>'
        mapping={'Shoes & bags':'Schuhe und Taschen','Shop now':'Jetzt kaufen','One':'Ein','pair':'Paar','& more.':'und mehr.','Search shoes':'Schuhe suchen'}
        output=self.render(source,mapping)
        self.assertIn('<html lang="de" dir="ltr">',output)
        self.assertIn('/de/shoes/?brand=Nike#finds',output)
        self.assertIn('<p>Ein <strong>Paar</strong> und mehr.</p>',output)
        self.assertIn('const label = "Do not translate code";',output)
        self.assertIn('value="All" placeholder="Schuhe suchen"',output)

    def test_metadata_and_schema_match_locale(self):
        source='<html><head><meta name="description" content="Shoe guide"><link rel="canonical" href="https://joyavault.com/en/shoes/"><script type="application/ld+json">{"@type":"WebPage","name":"Shoe guide","inLanguage":"en","url":"https://joyavault.com/en/shoes/"}</script></head></html>'
        output=self.render(source,{'Shoe guide':'دليل الأحذية'},'ar',('/ar/shoes/',))
        self.assertIn('dir="rtl"',output)
        self.assertIn('content="دليل الأحذية"',output)
        self.assertIn('"inLanguage": "ar"',output)
        self.assertNotIn('https://joyavault.com/en/shoes/',output)

    def test_missing_translation_is_error(self):
        with self.assertRaisesRegex(ValueError,'Missing'):
            self.render('<p>Untranslated text</p>',{})

    def test_placeholders_and_protected_names(self):
        text='Open Nike on Joyagoo: {count} https://weidian.com/item.html?id=1'
        protected,saved=st.protect(text)
        self.assertNotIn('Nike',protected)
        self.assertEqual(st.restore(protected,saved),text)
        with self.assertRaises(ValueError):st.restore('broken',saved)
        with self.assertRaisesRegex(ValueError,'placeholders'):
            self.render('<p>{count} shoes</p>',{'{count} shoes':'Schuhe'})

    def test_external_and_unavailable_links_are_not_rewritten(self):
        self.assertEqual(st.local_url('https://other.com/en/shoes/','de',{'/de/shoes/'}),'https://other.com/en/shoes/')
        self.assertEqual(st.local_url('/en/absent/','de',{'/de/shoes/'}),'/en/absent/')
        menu=loc.switcher('/en/shoes/')
        self.assertNotIn('href="/de/"',menu)
        self.assertIn('aria-disabled="true"',menu)
        self.assertNotIn('lang="zh"',menu)

    def test_chrome_is_idempotent_and_preserves_custom_header(self):
        path=loc.ROOT/'en/index.html'
        original=path.read_text(encoding='utf-8')
        once=loc.sync_language_menu(path,original)
        twice=loc.sync_language_menu(path,once)
        self.assertEqual(once,twice)
        self.assertIn('class="shell header-inner"',once)
        self.assertEqual(once.count('class="locale-switcher"'),1)
        self.assertEqual(st.fingerprint(once),st.fingerprint(twice))

    def test_budget_and_missing_credentials_never_call_network(self):
        with patch.object(cli,'load_environment'),patch.dict(cli.os.environ,{},clear=True),patch.object(cli,'google_translate') as request:
            with self.assertRaisesRegex(ValueError,'GOOGLE_TRANSLATE_API_KEY'):
                cli.translate(['de'],{st.key('Hello'):'Hello'},100)
            request.assert_not_called()
        with patch.object(cli,'load_environment'),patch.dict(cli.os.environ,{'GOOGLE_TRANSLATE_API_KEY':'fixture'}),patch.object(cli,'cache_for',return_value={}),patch.object(cli,'google_translate') as request:
            with self.assertRaisesRegex(ValueError,'no request was sent'):
                cli.translate(['de'],{st.key('Hello'):'Hello'},1)
            request.assert_not_called()

    def test_cached_work_is_not_billed_again(self):
        cache={st.key('Hello'):{'source':'Hello','translation':'Hallo'}}
        self.assertEqual(cli.missing_strings({st.key('Hello'):'Hello'},cache),{})

    def test_build_is_atomic_when_translations_missing(self):
        with patch.object(cli,'cache_for',return_value={}),patch.object(cli,'write_json') as write:
            with self.assertRaisesRegex(ValueError,'No pages were generated'):
                cli.build(['de'],{'/en/':{}},{st.key('Hello'):'Hello'})
            write.assert_not_called()

    def test_complete_fixture_build_produces_independent_page(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            source=root/'en/shoes/index.html'
            source.parent.mkdir(parents=True)
            source.write_text('<html lang="en"><head><title>Shoes</title><link rel="canonical" href="https://joyavault.com/en/shoes/"></head><body><header>{{language_switcher}}</header><main><h1>Shoes</h1><a href="/en/shoes/">Browse shoes</a></main></body></html>',encoding='utf-8')
            cache={st.key(s):{'source':s,'translation':t} for s,t in {'Shoes':'Schuhe','Browse shoes':'Schuhe ansehen'}.items()}
            strings={identifier:row['source'] for identifier,row in cache.items()}
            with patch.object(cli,'ROOT',root),patch.object(cli,'DATA',root/'src/translations'),patch.object(cli,'cache_for',return_value=cache),patch.object(cli.subprocess,'run') as run:
                cli.build(['de'],{'/en/shoes/':{}},strings)
                output=(root/'de/shoes/index.html').read_text(encoding='utf-8')
                self.assertIn('<h1>Schuhe</h1>',output)
                self.assertIn('href="https://joyavault.com/de/shoes/"',output)
                self.assertIn('href="/de/shoes/"',output)
                self.assertIn('/assets/locales/de.js',output)
                self.assertEqual(run.call_count,2)
                manifest=json.loads((root/'src/translations/published.json').read_text(encoding='utf-8'))
                self.assertEqual(manifest['/de/shoes/']['sourceHash'],st.fingerprint(source.read_text(encoding='utf-8')))

    def test_service_batches_keep_order_and_cache_results(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(cli,'DATA',Path(directory)),patch.object(cli,'load_environment'),patch.dict(cli.os.environ,{'GOOGLE_TRANSLATE_API_KEY':'fixture'}),patch.object(cli,'google_translate',return_value=['Hallo','Schuhe']) as request:
                strings={st.key('Hello'):'Hello',st.key('Shoes'):'Shoes'}
                cli.translate(['de'],strings,100)
                cli.translate(['de'],strings,100)
                request.assert_called_once()
                self.assertEqual(cli.cache_for('de')[st.key('Hello')]['translation'],'Hallo')

    def test_all_real_pages_round_trip_and_have_menus(self):
        for path in sorted((loc.ROOT/'en').rglob('index.html')):
            source=st.source_html(path.read_text(encoding='utf-8'))
            page=st.Page(source)
            identity={st.key(s):{'source':s,'translation':s} for s in page.strings}
            rendered=st.Page(source,identity,'en',()).render()
            # Identity fixture must keep the same text inventory, scripts and CSS.
            self.assertEqual(st.Page(rendered).strings,page.strings,str(path))
            import re
            scripts=lambda s:re.findall(r'<script(?![^>]*application/ld\+json)[^>]*>.*?</script>',s,re.S)
            self.assertEqual(scripts(source),scripts(rendered),str(path))
            original=path.read_text(encoding='utf-8')
            self.assertIn('class="locale-switcher"',original,str(path))
            self.assertIn('/js/i18n.js',original,str(path))


if __name__=='__main__':unittest.main()
