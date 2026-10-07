"""Локален сървър за макетите. Стандартният `python -m http.server` приема твърде
малко едновременни връзки и на Windows сваля част от корицата и скриптовете.
Пускане:  python _mockups/serve.py   ->  http://127.0.0.1:8041/_mockups/g-prozhektor/index.html
"""
import os, sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')   # български в конзолата на Windows
except Exception:
    pass
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # папката на krvoden
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8041

class Server(ThreadingHTTPServer):
    request_queue_size = 256
    daemon_threads = True

class Handler(SimpleHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    def log_message(self, *a): pass
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

os.chdir(ROOT)
print(f'Макети: http://127.0.0.1:{PORT}/_mockups/g-prozhektor/index.html  (Ctrl+C за спиране)')
Server(('127.0.0.1', PORT), Handler).serve_forever()
