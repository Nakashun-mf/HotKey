from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from urllib.parse import parse_qs
import os
import sys
import threading

class ConfigHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/config.json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            try:
                with open('config.json', 'r') as f:
                    self.wfile.write(f.read().encode())
            except FileNotFoundError:
                self.wfile.write(json.dumps({"hotkeys": []}).encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/save_config':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                config = json.loads(post_data.decode())
                with open('config.json', 'w') as f:
                    json.dump(config, f, indent=4)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"message": "設定を保存しました"}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        elif self.path == '/shutdown':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "サーバーを終了します"}).encode())
            # サーバーを別スレッドで安全に終了
            threading.Thread(target=self.server.shutdown).start()
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=ConfigHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'サーバーを起動しました - http://localhost:{port}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nサーバーを終了します')
    finally:
        httpd.server_close()

if __name__ == '__main__':
    run() 