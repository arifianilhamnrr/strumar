#!/usr/bin/env python3
import json
import os
import sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from api.chord_lib import fetch_song, search_songs


class StrumarHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/search':
            return self._api_search(parsed)
        if parsed.path == '/api/chords':
            return self._api_chords(parsed)
        return super().do_GET()

    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _api_search(self, parsed):
        try:
            qs = parse_qs(parsed.query)
            query = (qs.get('q') or [''])[0]
            results = search_songs(query)
            self._send_json(200, {'results': results})
        except Exception as e:
            self._send_json(500, {'error': str(e), 'results': []})

    def _api_chords(self, parsed):
        try:
            qs = parse_qs(parsed.query)
            url = (qs.get('url') or [''])[0]
            if not url:
                raise ValueError('Parameter url wajib diisi')
            song = fetch_song(url)
            self._send_json(200, {'song': song})
        except Exception as e:
            self._send_json(400, {'error': str(e)})


def _bind_server(preferred):
    for port in range(preferred, preferred + 6):
        try:
            server = ThreadingHTTPServer(('127.0.0.1', port), StrumarHandler)
            return server, port
        except OSError as e:
            if e.errno != 98:
                raise
            print(f'port {port} sudah dipakai, coba berikutnya…')
    raise SystemExit(f'port {preferred}–{preferred + 5} semua penuh. Matikan server lama dulu.')


def main():
    preferred = int(os.environ.get('PORT', '8765'))
    os.chdir(ROOT)
    server, port = _bind_server(preferred)
    print(f'strumar dev server → http://127.0.0.1:{port}')
    print('API: /api/search?q=...  /api/chords?url=...')
    if port != preferred:
        print(f'catatan: port {preferred} bentrok, pakai {port} ya')
    server.serve_forever()


if __name__ == '__main__':
    main()