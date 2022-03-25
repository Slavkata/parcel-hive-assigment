from http.server import BaseHTTPRequestHandler, HTTPServer
from subprocess import Popen
import websocket

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open('index.html', 'r') as file:
            self.wfile.write(bytes(file.read(), 'utf-8'))


if __name__ == "__main__":
    Popen(['python3', 'websocket.py'])
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f'Server started http://{hostName}:{serverPort}')
    webServer.serve_forever()
