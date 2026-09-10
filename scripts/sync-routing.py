"""Regenerate Vercel 301 rules and the canonical sitemap; --check never writes."""
import json
import sys
from xml.sax.saxutils import escape

from site_routes import ROOT, ORIGIN, CANONICAL_ROUTES, page_path, all_redirects
from localization import alternates
from seo import Document
from finds_data import load_finds
from indexability import exclusion_reason


def generated_files():
    config = json.loads((ROOT / 'vercel.json').read_text(encoding='utf-8'))
    config['$schema'] = 'https://openapi.vercel.sh/vercel.json'
    # Automatic URL normalization uses 308. Explicit rules below require 301.
    config['cleanUrls'] = False
    config.pop('trailingSlash', None)
    config['redirects'] = [
        {'source': old, 'destination': new, 'statusCode': 301}
        for old, new in sorted(all_redirects().items())
    ]
    config['rewrites'] = [
        {'source': route, 'destination': route + 'index.html'}
        for route in CANONICAL_ROUTES
    ]
    for rule in config.get('headers', []):
        if rule['source'] == '/(.*).html':
            rule['source'] = '/en/:path*'
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    data = load_finds()
    eligible = set()
    for route in CANONICAL_ROUTES:
        if exclusion_reason(route, data):
            continue
        html = page_path(route).read_text(encoding='utf-8')
        doc = Document(html).root
        noindex = any('noindex' in m.attrs.get('content','').lower() for m in doc.all('meta') if m.attrs.get('name','').lower() in ('robots','googlebot'))
        if not noindex:
            eligible.add(ORIGIN + route)
    for route in CANONICAL_ROUTES:
        if ORIGIN + route not in eligible:
            continue
        alternate_xml = ''.join(f'<xhtml:link rel="alternate" hreflang="{code}" href="{escape(url)}" />' for code,url in alternates(route).items() if url in eligible)
        sitemap.append(f'  <url><loc>{escape(ORIGIN + route)}</loc>{alternate_xml}</url>')
    sitemap.append('</urlset>')
    return {'vercel.json': json.dumps(config, indent=2) + '\n', 'sitemap.xml': '\n'.join(sitemap) + '\n', 'robots.txt': 'User-agent: *\nAllow: /\n\nSitemap: https://joyavault.com/sitemap.xml\n'}


if __name__ == '__main__':
    changed = []
    for name, text in generated_files().items():
        path = ROOT / name
        if not path.exists() or path.read_text(encoding='utf-8') != text:
            changed.append(name)
            if '--check' not in sys.argv:
                path.write_text(text, encoding='utf-8', newline='\n')
    print(f'{len(all_redirects())} explicit 301 rules; {len(CANONICAL_ROUTES)} canonical pages; changed: {changed}')
    sys.exit(bool(changed) if '--check' in sys.argv else 0)
