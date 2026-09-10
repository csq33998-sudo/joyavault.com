"""Build the first localized page collection from authored, ready-only locale files."""
from html import escape as e
import json
import sys
from localization import ROOT, ORIGIN, LANGUAGES, PAGE_PATHS, load_locale, ready, decorate, locale_chrome
from finds_data import load_finds


def render(lang, key, data):
    data = [item for item in data if not item['isPlaceholder'] and item['sourceUrl'] != '#']
    content = load_locale(lang)
    ui, page = content['ui'], content['pages'][key]
    route = f'/{lang}/{PAGE_PATHS[key]}'
    url = ORIGIN + route
    sections = []
    for i, section in enumerate(page['sections'],1):
        sections.append(f'<section class="local-section" id="section-{i}"><h2>{e(section["heading"])}</h2>'+''.join(f'<p>{e(p)}</p>' for p in section['paragraphs'])+'</section>')
    if page.get('checks'):
        tag = 'ol' if key=='buying' else 'ul'
        sections.append(f'<section class="local-section"><h2>{e(page["checks_heading"])}</h2><{tag}>'+''.join(f'<li>{e(item)}</li>' for item in page['checks'])+f'</{tag}></section>')
    if page.get('table'):
        table = page['table']
        sections.append(f'<section class="local-section"><h2>{e(table["heading"])}</h2><div class="comparison-table-wrap" role="region" aria-label="{e(table["heading"])}" tabindex="0"><table class="comparison-table"><thead><tr>'+''.join(f'<th scope="col">{e(cell)}</th>' for cell in table['headers'])+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+e(row[0])+'</th>'+''.join('<td>'+e(cell)+'</td>' for cell in row[1:])+'</tr>' for row in table['rows'])+'</tbody></table></div></section>')
    if key in ('home','finds','shoes','clothing','accessories'):
        selected = [item for item in data if key not in ('shoes','clothing','accessories') or item['category'].lower()==key]
        if key=='home':
            selected = sorted(selected,key=lambda item:not item['featured'])[:8]
        cards = []
        for item in selected:
            category = content['categories'][item['category']]
            label = ui['example'] if item['isPlaceholder'] else ui['saved']
            title = content['subcategories'][item['subcategory']]+' — '+ui['example'] if item['isPlaceholder'] else item['title']
            title_lang = lang if item['isPlaceholder'] else 'en'
            source = f'<span>{e(ui["pending"])}</span>' if item['sourceUrl']=='#' else f'<a data-product-source data-product-find-id="{e(item["id"])}" href="{e(item["sourceUrl"])}" target="_blank" rel="noopener sponsored nofollow">{e(ui["source"])}</a>'
            cards.append(f'<article class="local-product" data-find-id="{e(item["id"])}" data-title="{e(item["title"])}" data-marketplace="{e(item["marketplace"])}" data-category="{e(item["category"])}" data-search="{e(title+" "+category+" "+item["title"])}"><img src="{e(item["image"])}" alt="{e(title)}" lang="{title_lang}" width="450" height="450" loading="lazy" /><p>{e(category)} · {e(label)}</p><h3 lang="{title_lang}" dir="auto">{e(title)}</h3><p>{e(ui["example_price"] if item["isPlaceholder"] else ui["saved_price"])}: <bdi>¥{item["priceCny"]:,.2f}</bdi></p>{source}</article>')
        filters = ''
        if key=='finds':
            filters = f'<label for="local-search">{e(ui["search"])}</label><input id="local-search" type="search" aria-controls="local-products" /><label for="local-category">{e(ui["category"])}</label><select id="local-category" aria-controls="local-products"><option value="">{e(ui["all"])}</option>'+''.join(f'<option value="{e(original)}">{e(label)}</option>' for original,label in content['categories'].items())+'</select>'+f'<p id="local-results" role="status" data-label="{e(ui["results"])}" data-empty="{e(ui["empty"])}">{e(ui["results"])}: {len(selected)}</p>'
        sections.append(f'<section class="local-section" id="finds"><h2>{e(ui["records"])}</h2><p class="local-note">{e(ui["data_note"])}</p>{filters}<div class="local-products" id="local-products">'+''.join(cards)+'</div></section>')
    related_keys = ['shoes','clothing','accessories','spreadsheet','buying','qc','shipping'] if key in ('home','finds') else ['finds','spreadsheet','buying','qc','shipping']
    links = ''.join(f'<a class="local-link-card" href="/{lang}/{PAGE_PATHS[k]}"><h3>{e(content["pages"][k]["nav"])}</h3><p>{e(content["pages"][k]["description"])}</p></a>' for k in related_keys if k!=key and ready(lang,k))
    sections.append(f'<section class="local-section" id="categories"><h2>{e(ui["next"])}</h2><div class="local-link-grid">{links}</div></section>')
    sections.append(f'<section class="local-section faq-list" id="faq"><h2>{e(ui["faq"])}</h2>'+''.join(f'<details open><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in page['faq'])+'</section>')
    header,footer = locale_chrome(lang,route)
    graph = [{'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in page['faq']]}]
    if key in ('qc','shipping'):
        graph.append({'@type':'Article','headline':page['h1'],'description':page['description'],'inLanguage':lang,'mainEntityOfPage':url,'publisher':{'@type':'Organization','name':'JoyaVault','url':ORIGIN+f'/{lang}/'}})
    jsonld = json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')
    markup = f'''<!doctype html><!-- generated-localization --><html lang="{lang}" dir="{'rtl' if lang=='ar' else 'ltr'}"><head>
<meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><title>{e(page['title'])}</title><meta name="description" content="{e(page['description'])}" />
<link rel="canonical" href="{url}" /><meta property="og:type" content="{'article' if key in ('qc','shipping') else 'website'}" /><meta property="og:site_name" content="JoyaVault" /><meta property="og:url" content="{url}" /><meta property="og:title" content="{e(page['title'])}" /><meta property="og:description" content="{e(page['description'])}" /><meta property="og:image" content="{ORIGIN}/assets/social/joyagoo-spreadsheet-og.jpg" />
<meta name="twitter:card" content="summary_large_image" /><meta name="twitter:title" content="{e(page['title'])}" /><meta name="twitter:description" content="{e(page['description'])}" /><link rel="icon" type="image/svg+xml" href="/assets/icons/joyavault.svg" /><link rel="stylesheet" href="/styles.css" /><script type="application/ld+json">{jsonld}</script>
</head><body class="localized-page"><a class="skip-link" href="#main">{e(ui['skip'])}</a>{header}<main id="main" class="local-shell"><div class="local-hero"><nav aria-label="{e(ui['breadcrumb'])}"><a href="/{lang}/">{e(ui['home'])}</a> / <span aria-current="page">{e(page['nav'])}</span></nav><h1>{e(page['h1'])}</h1><p class="local-intro">{e(page['intro'])}</p></div>{''.join(sections)}</main>{footer}<script src="/js/i18n.js" defer></script><script src="/js/local-finds.js" defer></script></body></html>'''
    path = ROOT / route.strip('/') / 'index.html'
    return path,decorate(path,markup)


if __name__=='__main__':
    changed = []
    data = load_finds()
    for lang in LANGUAGES:
        if lang=='en': continue
        for key in PAGE_PATHS:
            if not ready(lang,key):
                stale = ROOT / lang / PAGE_PATHS[key] / 'index.html'
                if stale.exists():
                    if '<!-- generated-localization -->' not in stale.read_text(encoding='utf-8'):
                        raise ValueError(f'Refusing to remove unmanaged page: {stale}')
                    changed.append(str(stale.relative_to(ROOT)))
                    if '--check' not in sys.argv:
                        assert stale.resolve().is_relative_to((ROOT / lang).resolve())
                        stale.unlink()
                continue
            path,text = render(lang,key,data)
            if not path.exists() or path.read_text(encoding='utf-8')!=text:
                changed.append(str(path.relative_to(ROOT)))
                if '--check' not in sys.argv:
                    path.parent.mkdir(parents=True,exist_ok=True)
                    path.write_text(text,encoding='utf-8',newline='\n')
    print(f'Localized pages: {len(changed)} '+('out of sync' if '--check' in sys.argv else 'updated'))
    sys.exit(bool(changed) if '--check' in sys.argv else 0)
