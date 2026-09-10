"""Write shared layout into static pages so navigation works without JavaScript.

Run: python scripts/sync-layout.py
Check committed output: python scripts/sync-layout.py --check
"""
from pathlib import Path
import re
import sys
from localization import LANGUAGES, decorate, locale_chrome

ROOT = Path(__file__).resolve().parents[1]


def pages():
    return sorted(path for lang in LANGUAGES for path in (ROOT / lang).rglob('index.html'))


def render_layout(path, text):
    lang = path.relative_to(ROOT).parts[0]
    if lang != 'en':
        route = '/' + path.relative_to(ROOT).as_posix().removesuffix('index.html')
        header, footer = locale_chrome(lang, route)
        for tag, template in [('header',header),('footer',footer)]:
            text = re.sub(rf'<{tag}\b[^>]*>.*?</{tag}>', lambda _: template, text, flags=re.S)
        return decorate(path, text)
    for tag in ('header', 'footer'):
        template = (ROOT / 'components' / f'{tag}.html').read_text(encoding='utf-8').strip()
        # Discovery pages are English and expose only crawlable link CTAs.
        if 'class="discovery-page' in text and tag == 'header':
            template = re.sub(r'<button\b[^>]*data-theme-toggle[^>]*>.*?</button>', '', template, flags=re.S)
        text, count = re.subn(rf'<{tag}\b[^>]*>.*?</{tag}>', lambda _: template, text, flags=re.S)
        if count != 1:
            raise ValueError(f'{path}: expected one {tag}, found {count}')
    return decorate(path, text)


if __name__ == '__main__':
    changed = []
    for path in pages():
        original = path.read_text(encoding='utf-8')
        updated = render_layout(path, original)
        if updated != original:
            changed.append(str(path.relative_to(ROOT)))
            if '--check' not in sys.argv:
                path.write_text(updated, encoding='utf-8', newline='\n')
    print(f'{len(pages())} pages checked; {len(changed)} ' + ('out of sync' if '--check' in sys.argv else 'updated'))
    if '--check' in sys.argv and changed:
        print('\n'.join(changed))
        sys.exit(1)
