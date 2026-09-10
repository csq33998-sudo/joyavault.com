"""Render original article sources and matching Article/FAQ JSON-LD.

Sources use title/description on the first two lines, followed by a small
Markdown subset: headings, paragraphs, lists, links, and pipe tables.
Run with --check to verify the generated pages without writing them.
"""
from pathlib import Path
import html
import json
import re
import sys
from localization import decorate

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://joyavault.com'


def inline(value):
    value = html.escape(value)
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', value)


def plain(value):
    return re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', value)


def render(source):
    title, description, body = source.read_text(encoding='utf-8').split('\n', 2)
    route = f'/en/articles/{source.stem}/'
    url = ORIGIN + route
    blocks = body.strip().split('\n\n')
    headline = blocks.pop(0).removeprefix('# ')
    result, faqs, sections = [], [], []
    in_section = False
    in_faq = False
    i = 0
    while i < len(blocks):
        block = blocks[i].strip()
        if block.startswith('## '):
            if in_section:
                result.append('</section>')
            name = block[3:]
            anchor = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
            faq_class = ' class="faq-list"' if name == 'FAQ' else ''
            result.append(f'<section id="{anchor}"{faq_class}><h2>{inline(name)}</h2>')
            sections.append((anchor, name))
            in_section, in_faq = True, name == 'FAQ'
        elif block.startswith('### ') and in_faq:
            question, answer = block[4:], blocks[i + 1].strip()
            faqs.append({'@type': 'Question', 'name': plain(question), 'acceptedAnswer': {'@type': 'Answer', 'text': plain(answer)}})
            result.append(f'<details open><summary>{inline(question)}</summary><p>{inline(answer)}</p></details>')
            i += 1
        elif block.startswith('- '):
            result.append('<ul class="article-checklist">' + ''.join(f'<li>{inline(line[2:])}</li>' for line in block.splitlines()) + '</ul>')
        elif block.startswith('|'):
            rows = [[cell.strip() for cell in line.strip('|').split('|')] for line in block.splitlines()]
            result.append('<div class="comparison-table-wrap" role="region" aria-label="Decision table" tabindex="0"><table class="comparison-table"><caption>Compare the situation and next action</caption><thead><tr>' + ''.join(f'<th scope="col">{inline(cell)}</th>' for cell in rows[0]) + '</tr></thead><tbody>')
            for row in rows[2:]:
                result.append('<tr><th scope="row">' + inline(row[0]) + '</th>' + ''.join(f'<td>{inline(cell)}</td>' for cell in row[1:]) + '</tr>')
            result.append('</tbody></table></div>')
        else:
            result.append(f'<p>{inline(block)}</p>')
        i += 1
    if in_section:
        result.append('</section>')
    graph = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Article', '@id': url + '#article', 'headline': headline, 'description': description, 'inLanguage': 'en', 'mainEntityOfPage': {'@type': 'WebPage', '@id': url}, 'url': url, 'publisher': {'@type': 'Organization', 'name': 'JoyaVault', 'url': ORIGIN + '/en/'}},
        {'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': faqs},
    ]}
    header = (ROOT / 'components/header.html').read_text(encoding='utf-8').strip()
    footer = (ROOT / 'components/footer.html').read_text(encoding='utf-8').strip()
    nav = ''.join(f'<a href="#{anchor}">{inline(name)}</a>' for anchor, name in sections)
    page = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{inline(title)}</title><meta name="description" content="{html.escape(description)}" />
<link rel="canonical" href="{url}" />
<meta property="og:type" content="article" /><meta property="og:site_name" content="JoyaVault" />
<meta property="og:title" content="{html.escape(title)}" /><meta property="og:description" content="{html.escape(description)}" /><meta property="og:url" content="{url}" />
<meta property="og:image" content="{ORIGIN}/assets/social/joyagoo-spreadsheet-og.jpg" />
<meta name="twitter:card" content="summary_large_image" /><meta name="twitter:title" content="{html.escape(title)}" /><meta name="twitter:description" content="{html.escape(description)}" /><meta name="twitter:image" content="{ORIGIN}/assets/social/joyagoo-spreadsheet-og.jpg" />
<link rel="stylesheet" href="/styles.css" /><link rel="icon" type="image/svg+xml" href="/assets/icons/joyavault.svg" />
<script type="application/ld+json">{json.dumps(graph, indent=2)}</script>
</head><body><a class="skip-link" href="#main">Skip to content</a>
{header}
<main id="main"><div class="section-shell article-layout"><article class="article longform">
<nav aria-label="Breadcrumb"><a href="/en/">Home</a> / <a href="/en/articles/">Articles</a> / <span aria-current="page">{inline(headline)}</span></nav>
<p class="eyebrow">JOYAVAULT BUYER NOTES</p><h1>{inline(headline)}</h1>
{chr(10).join(result)}
</article><aside class="guide-panel"><nav aria-label="On this page"><p><strong>In this article</strong></p>{nav}</nav></aside></div></main>
{footer}
<script src="/js/theme.js"></script><script src="/js/i18n.js"></script></body></html>
'''
    return route, decorate(ROOT / route.strip('/') / 'index.html', page)


if __name__ == '__main__':
    changed = []
    for source in sorted((ROOT / 'src/content/articles').glob('*.md')):
        route, page = render(source)
        target = ROOT / route.strip('/') / 'index.html'
        if not target.exists() or target.read_text(encoding='utf-8') != page:
            changed.append(route)
            if '--check' not in sys.argv:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(page, encoding='utf-8', newline='\n')
    print(f'Article cluster: {len(changed)} ' + ('out of sync' if '--check' in sys.argv else 'updated'))
    sys.exit(bool(changed) if '--check' in sys.argv else 0)
