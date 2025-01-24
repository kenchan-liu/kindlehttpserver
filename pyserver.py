import http.server
import socketserver
import os
import urllib.parse
import html
import io

PORT = 8080
DIRECTORY = "/mnt/c/Users/kentl/kindleserv"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(404, "Directory listing not allowed")
            return None
        list.sort(key=lambda a: a.lower())
        f = io.BytesIO()
        displaypath = html.escape(urllib.parse.unquote(self.path))
        f.write(f'<!DOCTYPE html>\n<html>\n<head>\n<title>Directory listing for {displaypath}</title>\n</head>\n<body>\n'.encode())
        f.write(f'<h2>Directory listing for {displaypath}</h2>\n'.encode())
        f.write(b'<hr>\n<ul>\n')
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
            # Append / for directories or @ for symbolic links
            # Change to make each link a direct download
            f.write(f'<li><a href="{urllib.parse.quote(linkname)}" download="{html.escape(displayname)}">{html.escape(displayname)}</a></li>\n'.encode())
        f.write(b'</ul>\n<hr>\n</body>\n</html>\n')
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == "__main__":
    handler_class = CustomHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler_class) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
