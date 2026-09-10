"""Shared image delivery and native responsive navigation improvements."""
from functools import lru_cache
from html import escape
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@lru_cache
def images():
    return json.loads((ROOT / 'src/data/image-variants.json').read_text(encoding='utf-8'))


def render_performance(text):
    from seo import Document
    def image(match):
        attrs = Document(match.group()).root.all('img')[0].attrs
        original = attrs.get('src', '')
        if original.startswith('https://images.unsplash.com/'):
            attrs['src'] = original.replace('auto=format', 'fm=webp')
        variant = images().get(original)
        if variant:
            attrs.update(src=variant['src'], width=str(variant['width']), height=str(variant['height']))
        if '/icons/' not in original:
            hero = 'hero' in original or 'guide-product-image' in attrs.get('class', '') or attrs.get('fetchpriority') == 'high'
            attrs['loading'] = 'eager' if hero else 'lazy'
            attrs['decoding'] = 'async'
            if hero:
                attrs['fetchpriority'] = 'high'
            attrs.setdefault('width', '600')
            attrs.setdefault('height', '600')
        return '<img ' + ' '.join(f'{k}="{escape(v or "", quote=True)}"' for k, v in attrs.items()) + ' />'
    text = re.sub(r'<img\b[^>]*>', image, text)
    if 'class="site-menu"' not in text:
        match = re.search(r'<html\b[^>]*lang="([^"]+)"', text)
        lang = match.group(1) if match else 'en'
        label = {'en':'Menu','zh':'菜单','de':'Menü','fr':'Menu','pt':'Menu','pl':'Menu','it':'Menu','ar':'القائمة'}.get(lang,'Menu')
        text = re.sub(r'(<div class="nav-links">.*?</div>)',
                      lambda m: f'<details class="site-menu"><summary>{label}</summary>{m[1]}</details>', text, count=1, flags=re.S)
    # Stable position before the final SEO block; no blocking JavaScript is added.
    text = re.sub(r'<link rel="stylesheet" href="/performance.css" />\s*', '', text)
    anchor = '</head>'
    return text.replace(anchor, '<link rel="stylesheet" href="/performance.css" />\n' + anchor, 1)
