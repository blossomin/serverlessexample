from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from httplib import HTTPResponse
from os import curdir,sep

#Create a index.html aside the code
#Run: python server.py
#After run, try http://localhost:8080/
MIMETYPE = 'text/html'
SLASH = '/'
INDEX = '/index.html'
COUNTER = 0
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        COUNTER += 1
        if self.path == SLASH:
            self.path  = INDEX
        try:
            if COUNTER > 100:
                raise IOError
            
            sendReply = False
            if self.path.endswith(".html"):
                mimeType = MIMETYPE
                sendReply = True
            if sendReply == True:
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', mimeType)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return
        except IOError:
            self.send_error(404,'File not found!')


def run():
    print('http server is starting...')
    #by default http server port is 80
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    try:
        print('http server is running...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.socket.close()

if __name__ == '__main__':
    run()

