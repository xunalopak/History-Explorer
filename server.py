"""Local, read-only Chromium history explorer. Standard library only."""
import argparse
import json
import sqlite3
import threading
import webbrowser
from contextlib import closing
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent


def read_history(path):
    with closing(sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True)) as db:
        rows = db.execute('''SELECT v.id, u.url, u.title, v.visit_time,
            (SELECT k.term FROM keyword_search_terms k WHERE k.url_id=u.id LIMIT 1)
            FROM visits v JOIN urls u ON u.id=v.url
            WHERE v.visit_time > 11644473600000000 ORDER BY v.visit_time''')
        result = []
        for ident, url, title, timestamp, term in rows:
            try:
                domain = urlsplit(url).hostname or '(local / autre)'
            except ValueError:
                domain = '(adresse invalide)'
            result.append([ident, url, title or '', (timestamp // 1000) - 11644473600000, domain, term or ''])
        return result


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.headers.get('Host') != f'127.0.0.1:{self.server.server_port}' or self.headers.get('Sec-Fetch-Site') == 'cross-site':
            self.send_error(403)
            return
        if self.path == '/api/history':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(self.server.history)))
            self.end_headers()
            self.wfile.write(self.server.history)
        elif self.path.split('?')[0] in ('/', '/index.html', '/app.js', '/style.css'):
            super().do_GET()
        else:
            self.send_error(404)

    def end_headers(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'")
        super().end_headers()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', type=Path, default=ROOT.parent / 'History')
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--open', action='store_true')
    args = parser.parse_args()
    payload = json.dumps(read_history(args.database), ensure_ascii=False).encode('utf-8')
    server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(Handler, directory=str(ROOT)))
    server.history = payload
    print(f'History Explorer: http://127.0.0.1:{args.port}', flush=True)
    if args.open:
        threading.Timer(0.5, webbrowser.open, args=(f'http://127.0.0.1:{args.port}',)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
