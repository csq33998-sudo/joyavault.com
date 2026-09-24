"""Static locale registry. Only complete, explicitly ready pages become public routes."""
from functools import lru_cache
from pathlib import Path
import json
import re
from html import escape

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://joyavault.com'
LANGUAGES = {'en':'English', 'zh':'中文', 'de':'Deutsch', 'fr':'Français', 'pt':'Português', 'pl':'Polski', 'it':'Italiano', 'ar':'العربية'}
MENU_LANGUAGES = {code: label for code, label in LANGUAGES.items() if code != 'zh'}
UNAVAILABLE = {'en':'Translation not available yet', 'zh':'Translation not available yet', 'de':'Übersetzung noch nicht verfügbar', 'fr':'Traduction pas encore disponible', 'pt':'Tradução ainda não disponível', 'pl':'Tłumaczenie nie jest jeszcze dostępne', 'it':'Traduzione non ancora disponibile', 'ar':'الترجمة غير متاحة بعد'}
PAGE_PATHS = {
    'home':'', 'spreadsheet':'joyagoo-spreadsheet/', 'buying':'joyagoo-buying-guide/',
    'finds':'best-joyagoo-finds/', 'shoes':'best-joyagoo-finds/shoes/',
    'clothing':'best-joyagoo-finds/clothing/', 'accessories':'best-joyagoo-finds/accessories/',
    'qc':'articles/joyagoo-spreadsheet-qc-checklist/', 'shipping':'articles/joyagoo-spreadsheet-shipping-planning/',
}


@lru_cache
def load_locale(lang):
    path = ROOT / 'src/locales' / f'{lang}.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else None


def ready(lang, key):
    if lang == 'en':
        return True
    content = load_locale(lang)
    page = content and content.get('pages', {}).get(key)
    if not page or page.get('status') != 'ready':
        return False
    if key != 'home' and not ready(lang,'home'):
        return False
    required = ('title','description','h1','intro','sections','faq')
    if any(not page.get(k) for k in required):
        raise ValueError(f'{lang}/{key}: a ready translation is incomplete')
    if len(page['sections']) < 2 or len(page['faq']) < 2:
        raise ValueError(f'{lang}/{key}: missing localized sections or FAQs')
    if any(not section.get('heading') or not section.get('paragraphs') for section in page['sections']):
        raise ValueError(f'{lang}/{key}: incomplete section')
    if any(not isinstance(q,str) or not q.strip() or not isinstance(a,str) or not a.strip() for q,a in page['faq']):
        raise ValueError(f'{lang}/{key}: incomplete FAQ')
    if not page.get('checks') or not page.get('checks_heading'):
        raise ValueError(f'{lang}/{key}: missing localized checklist')
    return True


def localized_routes():
    from site_translation import published_routes
    return {f'/{lang}/{tail}' for lang in LANGUAGES if lang != 'en' for key,tail in PAGE_PATHS.items() if ready(lang,key)} | published_routes()


def split_route(route):
    parts = route.strip('/').split('/',1)
    lang = parts[0]
    tail = parts[1]+'/' if len(parts)>1 else ''
    return lang, tail


def alternates(route):
    from site_translation import published_routes
    lang, tail = split_route(route)
    key = next((k for k,v in PAGE_PATHS.items() if v == tail),None)
    choices = {code:ORIGIN+f'/{code}/{tail}' for code in LANGUAGES if key is not None and ready(code,key)}
    for code in MENU_LANGUAGES:
        if f'/{code}/{tail}' in published_routes():
            choices[code] = ORIGIN+f'/{code}/{tail}'
    if choices and (ROOT / 'en' / tail / 'index.html').exists():
        choices['en'] = ORIGIN+f'/en/{tail}'
    if not choices:
        choices = {lang:ORIGIN+route}
    choices['x-default'] = ORIGIN+f'/en/{tail}'
    return choices


def switcher(route):
    lang,tail = split_route(route)
    content = load_locale(lang) if lang!='en' else None
    ui = content['ui'] if content else {'language':'Language','home':'Home'}
    available = alternates(route)
    items = []
    for code,label in MENU_LANGUAGES.items():
        target = available.get(code)
        if target is None:
            items.append(f'<span class="locale-unavailable" aria-disabled="true"><span lang="{code}" dir="auto">{escape(label)}</span><small>{escape(UNAVAILABLE[lang])}</small></span>')
            continue
        href = target.removeprefix(ORIGIN)
        current = ' aria-current="page"' if code==lang else ''
        items.append(f'<a href="{href}" lang="{code}" dir="auto"{current}>{escape(label)}</a>')
    globe = '<svg class="locale-globe" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/></svg>'
    return f'<details class="locale-switcher"><summary aria-label="{escape(ui["language"])}: {escape(LANGUAGES[lang])}">{globe}<span class="locale-label">{escape(ui["language"])}</span><span class="locale-chevron" aria-hidden="true"></span></summary><div class="locale-options">'+''.join(items)+'</div></details>'


def sync_language_menu(path, text):
    """Update language chrome without replacing independently authored headers."""
    route = '/' + Path(path).relative_to(ROOT).as_posix().removesuffix('index.html')
    menu = switcher(route)
    if 'class="locale-switcher"' in text:
        text = re.sub(r'<details class="locale-switcher">.*?</details>', lambda _: menu, text, flags=re.S)
    elif '{{language_switcher}}' in text:
        text = text.replace('{{language_switcher}}', menu)
    elif 'class="shell header-inner"' in text:
        text, count = re.subn(r'(</details>)(\s*</div>\s*</header>)', lambda m: m[1] + menu + m[2], text, count=1)
        if count != 1:
            raise ValueError(f'{route}: cannot locate authored header insertion point')
    else:
        raise ValueError(f'{route}: missing language menu insertion point')
    if '/locale.css' not in text:
        text = text.replace('</head>', '<link rel="stylesheet" href="/locale.css" />\n</head>')
    if '/js/i18n.js' not in text:
        text = text.replace('</body>', '<script src="/js/i18n.js" defer></script>\n</body>')
    text = re.sub(r'<link\b[^>]*hreflang=[^>]*>\s*', '', text)
    meta = '\n'.join(f'<link rel="alternate" hreflang="{code}" href="{url}" />' for code,url in alternates(route).items())
    return text.replace('</head>', meta+'\n</head>')


def locale_chrome(lang, route):
    content = load_locale(lang)
    ui = content['ui']
    nav = ''.join(f'<a href="/{lang}/{tail}">{escape(content["pages"][key]["nav"])}</a>' for key,tail in PAGE_PATHS.items() if ready(lang,key))
    header = f'''<header class="site-header"><nav class="nav" aria-label="{escape(ui['navigation'])}"><a class="brand" href="/{lang}/" translate="no"><span class="brand-mark"><img src="/assets/icons/joyavault.svg" alt="" width="42" height="42" /></span><span><strong>JoyaVault</strong><small>{escape(ui['tagline'])}</small></span></a><div class="nav-links">{nav}</div><div class="nav-actions">{switcher(route)}</div></nav></header>'''
    legal = ''.join(f'<a href="/en/{slug}/" lang="en">{escape(label)} (English)</a>' for slug,label in [('about','About JoyaVault'),('contact','Contact'),('privacy-policy','Privacy Policy'),('terms','Terms of Use'),('editorial-policy','Editorial Policy')])
    footer = f'<footer class="site-footer"><div class="footer-brand"><a href="/{lang}/"><strong>JoyaVault</strong></a><p>{escape(ui["independent"])}</p></div><nav class="footer-links" aria-label="{escape(ui["footer"])}">{nav}{legal}</nav></footer>'
    return header,footer


def decorate(path, text):
    text = text.replace('/assets/icons/joyagoo-spreadsheet.png', '/assets/icons/joyagoo-spreadsheet-transparent.png')
    text = text.replace('/assets/icons/joyavault.svg', '/assets/icons/joyagoo-spreadsheet-transparent.png')
    text = text.replace('type="image/svg+xml" href="/assets/icons/joyagoo-spreadsheet-transparent.png"', 'type="image/png" href="/assets/icons/joyagoo-spreadsheet-transparent.png"')
    text = text.replace('src="/assets/icons/joyagoo-spreadsheet-transparent.png" alt=""', 'src="/assets/icons/joyagoo-spreadsheet-transparent.png" alt="Joyagoo spreadsheet"')
    relative = Path(path).relative_to(ROOT).as_posix().removesuffix('index.html')
    route = '/' + relative
    lang,_ = split_route(route)
    text = re.sub(r'<link\b[^>]*hreflang=[^>]*>\s*', '', text)
    text = re.sub(r'<link rel="stylesheet" href="/locale.css" />\s*', '', text)
    meta = '\n'.join(f'<link rel="alternate" hreflang="{code}" href="{url}" />' for code,url in alternates(route).items())
    text = text.replace('</head>', '<link rel="stylesheet" href="/locale.css" />\n'+meta+'\n</head>')
    text = text.replace('{{language_switcher}}', switcher(route))
    if 'class="locale-switcher"' in text and '/js/i18n.js' not in text:
        text = text.replace('</body>', '<script src="/js/i18n.js" defer></script>\n</body>')
    from seo import render_seo
    from internal_links import render_internal_links
    from analytics import render_analytics
    from performance import render_performance
    from conversion import render_conversion
    from back_to_top import render_back_to_top
    result = render_analytics(render_seo(path, render_performance(render_internal_links(path, render_back_to_top(render_conversion(path, text))))))
    return re.sub(r'\s*<link rel="stylesheet" href="/locale.css" />', '\n<link rel="stylesheet" href="/locale.css" />', result)
