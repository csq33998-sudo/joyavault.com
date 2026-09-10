"""Build authored trust pages with the shared layout, SEO and analytics."""
from html import escape
import json
import re
import sys
from urllib.parse import urlencode
from datetime import date
from localization import ROOT, decorate


def outputs():
    data = json.loads((ROOT / 'src/content/trust.json').read_text(encoding='utf-8'))
    email = data['contact_email'].strip()
    if email and not re.fullmatch(r'[^\s<>@]+@[^\s<>@]+\.[^\s<>@]+', email):
        raise ValueError('A valid contact email is required')
    contact = (f'<p><a href="mailto:{escape(email, quote=True)}">{escape(email)}</a></p>' if email else
               '<p>The contact address is awaiting confirmation by the site owner.</p>')
    report_query = urlencode({'subject': 'JoyaVault broken link report', 'body': 'JoyaVault page URL:\nAffected source URL:\nIssue observed:\nDate checked:\n'})
    broken_link_contact = (f'<p><a href="mailto:{escape(email)}?{escape(report_query)}">Report a broken link by email</a></p>' if email else '<p>A reporting email has not yet been published. Please retain the page URL and issue details; this page cannot send a report yet.</p>')
    analytics_config = (ROOT / 'js/analytics-config.js').read_text(encoding='utf-8')
    analytics_enabled = bool(re.search(r'"measurementId"\s*:\s*"G-[A-Z0-9]+"', analytics_config))
    analytics_status = '<p>Google Analytics 4 is enabled in this site build.</p>' if analytics_enabled else '<p>No Google Analytics 4 measurement ID is configured in this site build, so the bundled analytics code does not load GA4 or send analytics events.</p>'
    updated_label = date.fromisoformat(data['updated']).strftime('%B %d, %Y')
    header = (ROOT / 'components/header.html').read_text(encoding='utf-8')
    footer = (ROOT / 'components/footer.html').read_text(encoding='utf-8')
    for slug, page in data['pages'].items():
        sections = ''.join(f'<section><h2>{escape(title)}</h2>{body.replace("{{contact}}", contact).replace("{{broken_link_contact}}", broken_link_contact).replace("{{analytics_status}}", analytics_status)}</section>' for title, body in page['sections'])
        related = ''.join(f'<li><a href="/en/{key}/">{escape(value["heading"])}</a></li>' for key, value in data['pages'].items() if key != slug)
        markup = f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{escape(page['title'])}</title><meta name="description" content="{escape(page['description'], quote=True)}" />
<link rel="stylesheet" href="/styles.css" /><link rel="icon" type="image/svg+xml" href="/assets/icons/joyavault.svg" />
</head><body><a class="skip-link" href="#main">Skip to content</a>{header}
<main id="main" class="section-shell"><article class="article longform">
<nav aria-label="Breadcrumb"><a href="/en/">Home</a> / <span aria-current="page">{escape(page['heading'])}</span></nav>
<p class="eyebrow">ABOUT JOYAVAULT</p><h1>{escape(page['heading'])}</h1>
<p>Last updated: <time datetime="{data['updated']}">{updated_label}</time></p>
{sections}<nav class="internal-links" aria-label="Related site policies"><h2>Related pages</h2><ul>{related}</ul></nav>
</article></main>{footer}<script src="/js/theme.js" defer></script><script src="/js/i18n.js" defer></script></body></html>
'''
        path = ROOT / 'en' / slug / 'index.html'
        yield path, decorate(path, markup)


if __name__ == '__main__':
    changed = []
    for path, text in outputs():
        if not path.exists() or path.read_text(encoding='utf-8') != text:
            changed.append(str(path.relative_to(ROOT)))
            if '--check' not in sys.argv:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding='utf-8', newline='\n')
    print(f'Trust pages: {len(changed)} ' + ('out of sync' if '--check' in sys.argv else 'updated'))
    if '--check' in sys.argv and changed:
        sys.exit(1)
