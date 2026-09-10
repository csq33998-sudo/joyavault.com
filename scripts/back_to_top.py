"""Shared scroll-to-top control on every localized page."""
import re

LABELS = {'en': 'Back to top', 'zh': '返回顶部', 'de': 'Nach oben',
          'fr': 'Retour en haut', 'es': 'Volver arriba', 'pt': 'Voltar ao topo',
          'it': 'Torna in alto', 'ja': 'ページの先頭へ', 'ko': '맨 위로',
          'ar': 'العودة إلى الأعلى'}


def render_back_to_top(text):
    if not re.search(r'\bid=[\"\']top[\"\']', text):
        text = re.sub(r'(<body\b[^>]*>)', r'\1\n<div id="top" aria-hidden="true"></div>', text, count=1)
    text = re.sub(r'\s*<link rel="stylesheet" href="/back-to-top.css" />', '', text)
    text = text.replace('</head>', '<link rel="stylesheet" href="/back-to-top.css" />\n</head>')
    text = re.sub(r'<head>.*?</head>', lambda m: re.sub(r'(?m)^[ \t]+', '', re.sub(r'(?m)^[ \t]+\n', '', m[0])), text, flags=re.S)
    text = re.sub(r'\s*<link rel="stylesheet" href="/locale.css" />', '\n<link rel="stylesheet" href="/locale.css" />', text)
    text = re.sub(r'\s*<a\b[^>]*data-back-to-top\b[^>]*>.*?</a>', '', text, flags=re.S)
    text = re.sub(r'\s*<script src="/js/back-to-top.js" defer></script>', '', text)
    match = re.search(r'<html\b[^>]*lang="([^"]+)"', text)
    lang = match[1].split('-')[0] if match else 'en'
    label = LABELS.get(lang, LABELS['en'])
    control = f'''<a class="back-to-top" data-back-to-top href="#top" aria-label="{label}" title="{label}" hidden>
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true" focusable="false"><path d="m5 15 7-7 7 7" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" /></svg>
</a>
<script src="/js/back-to-top.js" defer></script>'''
    return re.sub(r'\s*</body>', lambda _: '\n'+control+'\n</body>', text)
