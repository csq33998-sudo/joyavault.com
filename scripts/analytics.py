"""Keep analytics assets present once in all generated and manually authored pages."""
import re


def render_analytics(text):
    text = re.sub(r'\s*<script src="/js/analytics(?:-config)?\.js" defer></script>\s*', '', text)
    scripts = '<script src="/js/analytics-config.js" defer></script>\n<script src="/js/analytics.js" defer></script>\n'
    # Keep SEO's managed block last so both renderers remain idempotent.
    return re.sub(r'<head>\s*', '<head>\n' + scripts, text, count=1)


if __name__ == '__main__':
    from localization import ROOT, LANGUAGES
    for lang in LANGUAGES:
        for path in (ROOT / lang).rglob('index.html'):
            text = path.read_text(encoding='utf-8')
            updated = render_analytics(text)
            if text != updated:
                path.write_text(updated, encoding='utf-8', newline='\n')
