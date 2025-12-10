#!/usr/bin/env python3
"""
Target HTTP Server with CPU-intensive operations
Простий HTTP сервер для тестування навантаження
"""
import http.server
import socketserver
import hashlib
import sys

PORT = 80 if len(sys.argv) < 2 else int(sys.argv[1])

class CPUIntensiveHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # CPU-intensive операція: хешування для створення навантаження
        data = self.path.encode('utf-8') * 1000
        for _ in range(100):
            hashlib.sha256(data).hexdigest()

        # Відповідь
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'OK')

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
