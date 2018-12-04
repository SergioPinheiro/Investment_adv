from http.server import HTTPServer, BaseHTTPRequestHandler
from Serv import Serv

def run(server_class=HTTPServer, handler_class=Serv, port=8080):
        # web_dir = os.path.join(os.path.dirname(__file__), './atividade 4/')
        # print(web_dir)
        # os.chdir(web_dir)
        server_address = ('localhost', port)
        httpd = server_class(server_address, handler_class)
        print ('Starting httpd...')
        httpd.serve_forever()

run()
