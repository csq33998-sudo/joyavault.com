"""Whole-site translation: estimate -> translate -> build. No third-party SDK.

python scripts/translate-site.py estimate
python scripts/translate-site.py translate --languages de --max-characters 400000
python scripts/translate-site.py build --languages de
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from html import unescape
from site_translation import (ROOT, DATA, TARGETS, MARKER, Page, DYNAMIC,
    inventory, key, source_html, fingerprint, read_json, write_json, protect, restore,
    published_routes)


def load_environment():
    path = ROOT / '.env.translation.local'
    if path.exists():
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            if line.strip() and not line.lstrip().startswith('#') and '=' in line:
                name,value = line.split('=',1)
                if name.strip() == 'GOOGLE_TRANSLATE_API_KEY':
                    os.environ.setdefault(name.strip(),value.strip().strip('\"\''))


def cache_for(lang):
    return read_json(DATA / f'{lang}.json', {})


def missing_strings(strings, cache):
    return {identifier:source for identifier,source in strings.items()
            if not cache.get(identifier,{}).get('translation') or cache[identifier].get('source') != source}


def batches(items, max_chars=4000):
    group=[]; size=0
    for item in items:
        if group and (size+len(item[1])>max_chars or len(group)>=50):
            yield group; group=[]; size=0
        group.append(item);size+=len(item[1])
    if group: yield group


def google_translate(texts, lang, secret):
    # Header authentication avoids putting credentials in URLs/log messages.
    body=json.dumps({'q':texts,'source':'en','target':lang,'format':'text','model':'nmt'}).encode()
    request=urllib.request.Request('https://translation.googleapis.com/language/translate/v2',
        data=body, headers={'Content-Type':'application/json; charset=utf-8','X-Goog-Api-Key':secret},method='POST')
    try:
        with urllib.request.urlopen(request,timeout=45) as response:
            result=json.load(response)
    except urllib.error.HTTPError as error:
        # Do not print service response bodies or credentials. Completed batches
        # are cached; retry is explicit so a timeout never silently doubles cost.
        raise ValueError(f'Google Translation returned HTTP {error.code}; check API activation, key restrictions, billing and quota.') from None
    except (urllib.error.URLError,TimeoutError):
        raise ValueError('Translation connection failed; completed batches are saved. Retry after checking the connection.') from None
    rows=result.get('data',{}).get('translations',[])
    if len(rows)!=len(texts): raise ValueError('Translation service returned an incomplete batch')
    return [unescape(row['translatedText']) for row in rows]


def estimate(languages, pages, strings):
    rows={}
    for lang in languages:
        missing=missing_strings(strings,cache_for(lang))
        rows[lang]={'pendingStrings':len(missing),'requestCharacters':sum(len(protect(s)[0]) for s in missing.values())}
    report={'englishPages':len(pages),'uniqueStrings':len(strings),'languages':rows,
            'totalRequestCharacters':sum(r['requestCharacters'] for r in rows.values())}
    write_json(DATA / 'inventory.json', {'pages':pages,'strings':strings})
    write_json(DATA / 'estimate.json',report)
    print(json.dumps(report,indent=2))
    return report


def translate(languages, strings, limit):
    load_environment()
    secret=os.environ.get('GOOGLE_TRANSLATE_API_KEY','')
    if not secret: raise ValueError('Set GOOGLE_TRANSLATE_API_KEY in .env.translation.local. No request was sent.')
    pending={lang:missing_strings(strings,cache_for(lang)) for lang in languages}
    total=sum(len(protect(s)[0]) for rows in pending.values() for s in rows.values())
    if limit is None or total>limit:
        raise ValueError(f'Pending requests contain {total} characters. Pass --max-characters at least this value to run; no request was sent.')
    for lang,rows in pending.items():
        cache=cache_for(lang)
        for batch in batches(list(rows.items())):
            protected=[protect(source) for _,source in batch]
            results=google_translate([row[0] for row in protected],lang,secret)
            additions={}
            for (identifier,source),translated,(_,saved) in zip(batch,results,protected):
                value=restore(translated,saved)
                if not value.strip(): raise ValueError('Empty translation; batch was not saved')
                additions[identifier]={'source':source,'translation':value,'provider':'google-nmt'}
            cache.update(additions)
            write_json(DATA / f'{lang}.json',cache)
            print(f'{lang}: saved {len(additions)} translations',flush=True)


def build(languages, pages, strings):
    caches={lang:cache_for(lang) for lang in languages}
    missing={lang:len(missing_strings(strings,cache)) for lang,cache in caches.items()}
    if any(missing.values()):
        raise ValueError('No pages were generated: missing translations '+json.dumps(missing))
    from localization import localized_routes
    available=localized_routes() | set(pages)
    available.update(f'/{lang}/'+route[4:] for lang in languages for route in pages)
    manifest=read_json(DATA / 'published.json',{})
    outputs={}
    for lang,cache in caches.items():
        for route in pages:
            source_path=ROOT / route.strip('/') / 'index.html'
            text=source_html(source_path.read_text(encoding='utf-8'))
            target=f'/{lang}/'+route[4:]
            output=Page(text,cache,lang,available).render()
            output=output.replace('</head>',f'<script src="/assets/locales/{lang}.js"></script>\n</head>')
            # The shared helper is loaded before any page-specific defer scripts.
            output=output.replace('</head>', '<script src="/js/i18n.js"></script>\n</head>')
            outputs[ROOT / target.strip('/') / 'index.html']=MARKER+'\n'+output
            manifest[target]={'sourceHash':fingerprint(text),'language':lang,'sourceRoute':route}
        # Only UI phrases are downloaded at runtime; article translations remain
        # in the HTML and require no browser translation service.
        ui={row['source']:row['translation'] for row in cache.values()
            if row['source'] in DYNAMIC or len(row['source'])<90}
        payload=json.dumps(ui,ensure_ascii=False).replace('<','\\u003c')
        outputs[ROOT / f'assets/locales/{lang}.js']='window.ML_TRANSLATIONS='+payload+';\n'
    # Validate every page before writing any output; missing strings never ship.
    for path,text in outputs.items():
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(text,encoding='utf-8',newline='\n')
    write_json(DATA / 'published.json',manifest)
    published_routes.cache_clear()
    for script in ('sync-language-menus.py','sync-routing.py'):
        subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,check=True)
    print(f'Generated {len(pages)*len(languages)} translated pages. Nothing deployed.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('estimate','translate','build'))
    parser.add_argument('--languages',nargs='+',choices=TARGETS,default=list(TARGETS))
    parser.add_argument('--max-characters',type=int)
    args=parser.parse_args()
    pages,strings=inventory()
    if args.command=='estimate': estimate(args.languages,pages,strings)
    elif args.command=='translate': translate(args.languages,strings,args.max_characters)
    else: build(args.languages,pages,strings)


if __name__=='__main__':
    try: main()
    except ValueError as error:
        print(str(error),file=sys.stderr)
        sys.exit(1)
