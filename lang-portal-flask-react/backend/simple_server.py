from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello, World!\n')

def run(server_class=HTTPServer, handler_class=Handler):
    server_address = ('127.0.0.1', 8000)
    print(f'Starting server on {server_address[0]}:{server_address[1]}')
    print(f'Local hostname: {socket.gethostname()}')
    print(f'Local IP addresses:')
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        print(f'  - {ip}')
    httpd = server_class(server_address, handler_class)
    print('Server is ready')
    httpd.serve_forever()

if __name__ == '__main__':
    run() 