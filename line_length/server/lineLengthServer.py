from http.server import *
import sys
from operator import itemgetter

class PithonRequestHandler(BaseHTTPRequestHandler):
   def do_GET(s):
      s.send_response(200)
      s.send_header('Content-type', 'text/html')
      s.end_headers()
      message = ("{0:.2f} cm".format(s.path))
      s.wfile.write(bytes(message, 'UTF-8'))
      file = open('.lineLength.temp', 'w')
      file.write(message)
      file.close()

def run():
    port = get_arguments()
    server_address = ('', port)
    httpd = HTTPServer(server_address, PithonRequestHandler)
    print("Address: {}\nPort: {}\nWaiting for a response...".format(httpd.server_name, httpd.server_port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

def get_arguments():
    arguments = sys.argv
    if len(arguments) != 2:
        error('Usage: python3 <server>.py <port>\nFor example: python3 server.py 50000')
    try:
        port = int(arguments[1])
        assert(port >= 1)
    except:
        error("Can't convert {} to a port number ({} should be a positive integer)")
    return port

def error(message):
    print(message)
    exit(1)

run()
