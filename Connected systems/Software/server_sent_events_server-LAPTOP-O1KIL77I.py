from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep

HOST = "localhost"
PORT = 8000

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Connection accepted from {self.client_address}")
        if self.path == "/messages":
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-type", "text/event-stream")
            self.end_headers()
            i = 0
            while True:
                try:
                    self.wfile.write(bytes(f"data: Here is message number {i}\n\n", "utf-8"))
                    self.wfile.flush()
                except:
                    print(f"Connection lost to {self.client_address}")
                    return
                i += 1
                sleep(1)

webServer = HTTPServer((HOST, PORT), MyServer)
print(f"Server started http://{HOST}:{PORT}")

try:
    webServer.serve_forever()
except:
    webServer.server_close()
    print("Server stopped")