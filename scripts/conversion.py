"""Build crawlable stage-specific CTAs and explain external handoffs."""
from html import escape
from pathlib import Path
import re
from urllib.parse import urlsplit
from finds_data import ROOT

NOTICE = 'JoyaVault helps with discovery and preparation. Orders, payments, warehouse, QC, and international shipping are handled outside JoyaVault.'
QC = '/en/articles/joyagoo-spreadsheet-qc-checklist/'
SHIPPING = '/en/articles/joyagoo-spreadsheet-shipping-planning/'
BUYING = '/en/joyagoo-buying-guide/'
FINDS = '/en/best-joyagoo-finds/'
STAGES = {
    FINDS: [('Read QC Checklist', QC)],
    QC: [('Browse Finds', FINDS), ('Plan Shipping', SHIPPING), ('Continue to Buying Guide', BUYING)],
    SHIPPING: [('Browse Finds', FINDS), ('Read Coupon and Fee Checklist', '/en/articles/joyagoo-spreadsheet-coupon-fee-checklist/'), ('Continue to Buying Guide', BUYING)],
}


def render_conversion(path, text):
    from seo import Document
    route = '/' + Path(path).relative_to(ROOT).as_posix().removesuffix('index.html')
    text = re.sub(r'<!-- stage-cta:start -->.*?<!-- stage-cta:end -->\n?', '', text, flags=re.S)
    text = re.sub(r'<span class="external-cta-note" lang="en">.*?</span>', '', text, flags=re.S)
    links = STAGES.get(route)
    if route.startswith(FINDS) and route != FINDS and 'class="home-main category-page"' not in text:
        links = [('Browse more in this category', FINDS), ('Read Shipping Planning', SHIPPING), ('Open Buying Guide', BUYING)]
    if links:
        actions = ''.join(f'<a href="{escape(url)}">{escape(label)}</a>' for label,url in links)
        block = '<!-- stage-cta:start --><nav class="stage-cta" aria-label="Continue your research"><p><strong>Continue your research</strong></p><div>'+actions+'</div></nav><!-- stage-cta:end -->\n'
        if '<article' in text and route in (QC, SHIPPING):
            # Keep the article's Next Pages module at its end on every rebuild.
            marker = '<!-- internal-links:start -->'
            if marker in text:
                text = text.replace(marker, block + marker, 1)
            else:
                text = text.replace('</article>', block + '</article>', 1)
        else:
            text = text.replace('</main>', block + '</main>')
    def external(match):
        raw = match.group()
        attrs = Document(raw).root.all('a')[0].attrs
        parsed = urlsplit(attrs.get('href', ''))
        if parsed.scheme not in ('https', 'http') or parsed.hostname == 'joyavault.com':
            return raw
        classes = set(attrs.get('class', '').split())
        if 'nav-cta' in classes:
            # Keep the compact header layout: explain the external handoff in
            # the link's tooltip rather than adding a full-width flex item.
            raw = re.sub(r'\s+title="[^"]*"', '', raw, count=1)
            return raw.replace('<a ', '<a title="' + escape(NOTICE + ' Opens in a new tab.', quote=True) + '" ', 1)
        cta = 'data-product-source' in attrs or bool(classes & {'nav-cta', 'home-button', 'button'}) or parsed.hostname in ('joyagoo.com', 'www.joyagoo.com')
        return raw + f'<span class="external-cta-note" lang="en">{NOTICE}</span>' if cta else raw
    return re.sub(r'<a\b[^>]*>.*?</a>', external, text, flags=re.S)
