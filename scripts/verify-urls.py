"""Audit local HTML and optionally HTTP routing via --base-url (local or deployed)."""
import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from urllib.error import HTTPError
from urllib.parse import urlsplit, unquote
from urllib.request import build_opener, HTTPRedirectHandler, Request
import xml.etree.ElementTree as ET

from site_routes import ROOT, ORIGIN, CANONICAL_ROUTES, LEGACY_PAGES, page_path, all_redirects


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.resources, self.ids, self.canonicals, self.og_urls = [], [], [], [], []
        self.noindex = False
        self.h1s = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
            assert 'onclick' not in attrs, 'Navigation must use href'
        if tag in ('script', 'img') and 'src' in attrs:
            self.resources.append(attrs['src'])
        if tag == 'link':
            if attrs.get('rel') == 'canonical':
                self.canonicals.append(attrs.get('href'))
            elif attrs.get('rel') in ('stylesheet', 'icon'):
                self.resources.append(attrs.get('href', ''))
        if tag == 'meta':
            if attrs.get('property') == 'og:url':
                self.og_urls.append(attrs.get('content'))
            if attrs.get('name') == 'robots' and 'noindex' in attrs.get('content', ''):
                self.noindex = True
        if tag == 'h1':
            self.h1s += 1


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def verify(base_url=None):
    documents = {route: Document(page_path(route).read_text(encoding='utf-8')) for route in CANONICAL_ROUTES}
    config = json.loads((ROOT / 'vercel.json').read_text(encoding='utf-8'))
    rules = {r['source']: r for r in config['redirects']}
    assert len(rules) == len(config['redirects']), 'Duplicate redirect sources'
    assert config.get('cleanUrls') is False and 'trailingSlash' not in config, 'Avoid automatic 308 normalization'
    expected = {
        '/': '/en/', '/joyagoo-spreadsheet': '/en/joyagoo-spreadsheet/',
        '/joyagoo-spreadsheet-updates': '/en/joyagoo-spreadsheet-updates/',
        '/finds-spreadsheet': '/en/best-joyagoo-finds/', '/brands': '/en/brands/',
        '/guides': '/en/joyagoo-buying-guide/', '/articles': '/en/articles/', '/blog': '/en/blog/',
        '/sneaker-finds-spreadsheet': '/en/best-joyagoo-finds/shoes/',
        '/taobao-finds-spreadsheet': '/en/marketplaces/taobao/',
        '/weidian-finds-spreadsheet': '/en/marketplaces/weidian/',
        '/1688-finds-spreadsheet': '/en/marketplaces/1688/',
    }
    for source, target in expected.items():
        assert rules[source]['destination'] == target, source
    for source, target in all_redirects().items():
        assert rules[source] == {'source': source, 'destination': target, 'statusCode': 301}, source
        assert target not in rules and target in documents, f'Chain, loop or missing target: {source}'
    links = 0
    for route, doc in documents.items():
        assert doc.canonicals == [ORIGIN + route], f'Canonical: {route}'
        assert doc.og_urls == [ORIGIN + route], f'og:url: {route}'
        assert doc.h1s == 1, f'Expected one h1: {route}'
        assert not [value for value, count in Counter(doc.ids).items() if count > 1], f'Duplicate IDs: {route}'
        for href in doc.links:
            url = urlsplit(href)
            if url.netloc and url.netloc != 'joyavault.com' or url.scheme in ('mailto', 'tel'):
                continue
            assert href and href != '#' and url.scheme not in ('javascript',), f'Empty or JS href: {route}'
            target = url.path or route
            assert target in documents, f'Old or missing internal link: {route} -> {href}'
            if url.fragment:
                assert unquote(url.fragment) in documents[target].ids, f'Missing fragment: {route} -> {href}'
            links += 1
        for src in doc.resources:
            url = urlsplit(src)
            if url.netloc and url.netloc != 'joyavault.com':
                continue
            assert url.path.startswith('/') and (ROOT / url.path.lstrip('/')).is_file(), f'Missing resource: {route} -> {src}'
    sitemap = ET.parse(ROOT / 'sitemap.xml')
    locations = [node.text for node in sitemap.findall('.//{*}loc')]
    assert len(locations) == len(set(locations)), 'Duplicate sitemap URLs'
    assert set(locations) == {ORIGIN + route for route, doc in documents.items() if not doc.noindex}, 'Sitemap differs from indexable canonical pages'
    assert not any((ROOT / old).exists() for old in LEGACY_PAGES), 'Old HTML still published'
    print(f'PASS: {len(documents)} pages, {links} internal links, {len(rules)} direct 301 rules, {len(locations)} sitemap URLs.')
    if base_url:
        opener = build_opener(NoRedirect())
        count = 0
        for source, rule in rules.items():
            try:
                response = opener.open(Request(base_url.rstrip('/') + source, method='HEAD'), timeout=20)
            except HTTPError as response_error:
                response = response_error
            with response:
                assert response.status == 301, f'{source}: HTTP {response.status}, expected 301'
                target = urlsplit(response.headers['Location'])
                assert target.path == rule['destination'], f'{source}: wrong Location'
            count += 1
        for route, doc in documents.items():
            with opener.open(base_url.rstrip('/') + route, timeout=20) as response:
                assert response.status == 200, f'{route}: HTTP {response.status}'
                actual = Document(response.read().decode('utf-8'))
                assert actual.canonicals == doc.canonicals, f'{route}: wrong served page'
        with_http_query = base_url.rstrip('/') + '/finds-spreadsheet.html?utm_source=migration-check'
        try:
            opener.open(Request(with_http_query, method='HEAD'), timeout=20)
        except HTTPError as response:
            assert response.code == 301 and urlsplit(response.headers['Location']).query == 'utm_source=migration-check'
        else:
            raise AssertionError('Query-string URL must return 301')
        try:
            opener.open(base_url.rstrip('/') + '/en/not-a-real-page/', timeout=20)
        except HTTPError as response:
            assert response.code == 404
        else:
            raise AssertionError('Missing page must return 404')
        print(f'PASS HTTP at {base_url}: {count} redirects return 301, {len(documents)} pages return 200; query preserved; unknown page returns 404.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url', help='Optional preview or deployed origin to test actual HTTP responses.')
    verify(parser.parse_args().base_url)
