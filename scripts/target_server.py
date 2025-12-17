#!/usr/bin/env python3
"""
Target HTTP Server with CPU-intensive operations
Простий HTTP сервер для тестування навантаження
"""
import http.server
import socketserver
import hashlib
import sys
import os

PORT = 80 if len(sys.argv) < 2 else int(sys.argv[1])

# Шлях до HTML файлу (відносно розташування скрипта)
HTML_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'index.html')

# Завантаження HTML сторінки з файлу або використання дефолтної
def load_html_page():
    try:
        with open(HTML_FILE_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # Fallback на просту сторінку якщо файл не знайдено
        return """<!DOCTYPE html>
<html><head><title>Test Server</title></head>
<body><h1>Test Server Online</h1><p>DDoS Research Laboratory</p></body>
</html>"""

HTML_PAGE = load_html_page()

class CPUIntensiveHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # CPU-intensive операція: хешування для створення навантаження
        data = self.path.encode('utf-8') * 1000
        for _ in range(100):
            hashlib.sha256(data).hexdigest()

        # Відповідь з HTML сторінкою
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(HTML_PAGE.encode('utf-8')))
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode('utf-8'))

    def do_POST(self):
        self.do_GET()

    def do_PUT(self):
        self.do_GET()

    def do_DELETE(self):
        self.do_GET()

    def do_HEAD(self):
        self.do_GET()

    def do_OPTIONS(self):
        self.do_GET()

    def do_PATCH(self):
        self.do_GET()

    def log_message(self, format, *args):
        # Відключаємо логування для продуктивності
        pass

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), CPUIntensiveHandler) as httpd:
        print(f"[+] Target server running on port {PORT}")
        print(f"[*] Waiting for requests...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Server stopped")
            sys.exit(0)
