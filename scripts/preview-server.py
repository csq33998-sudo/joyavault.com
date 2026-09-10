"""Local static preview with the exact redirect table from vercel.json.

This checks application routing locally; Vercel's edge must also be tested after deployment.
"""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from urllib.parse import urlsplit, urlunsplit

from site_routes import ROOT


class PreviewHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def send_head(self):
        # A preview always returns current files, even when a browser retained
        # validators from an earlier run of the standard Python HTTP server.
        for header in ('If-Modified-Since', 'If-None-Match'):
            if header in self.headers:
                del self.headers[header]
        url = urlsplit(self.path)
        config = json.loads((ROOT / 'vercel.json').read_text(encoding='utf-8'))
        for rule in config.get('redirects', []):
            if url.path == rule['source']:
                target = urlsplit(rule['destination'])
                location = urlunsplit((target.scheme, target.netloc, target.path, url.query, target.fragment))
                self.send_response(rule['statusCode'])
                self.send_header('Location', location)
                self.send_header('Content-Length', '0')
                self.end_headers()
                return None
        return super().send_head()

    def list_directory(self, path):
        self.send_error(404, 'Page not found')
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5190)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(PreviewHandler, directory=str(ROOT)))
    print(f'JoyaVault preview: http://127.0.0.1:{args.port}/en/', flush=True)
    server.serve_forever()
