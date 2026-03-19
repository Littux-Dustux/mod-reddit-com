import http.server
import socketserver
import os
from sys import argv

# Get the absolute directory where this script (serve.py) is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, 'index.html')

class SPAServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Instead of modifying self.path (which looks in the CWD),
        # we manually serve the specific file from the script's directory.
        try:
            with open(INDEX_PATH, 'rb') as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.copyfile(f, self.wfile)
        except FileNotFoundError:
            self.send_error(404, "index.html not found in script directory")

PORT = int(argv[1]) if len(argv) > 1 else 44444
# "allow_reuse_address" prevents the "Address already in use" error on restarts
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), SPAServer) as httpd:
    print(f"Serving Modmail Archive at http://localhost:{PORT}")
    print(f"Target file: {INDEX_PATH}")
    httpd.serve_forever()
