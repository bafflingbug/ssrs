import os
import sys
import yaml
from py3 import py3
if py3:
    import socketserver
else:
    import SocketServer as socketserver

dir_path = os.path.dirname(os.path.realpath(__file__))
config = None

class Server(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        while True:
            try:
                data = int(conn.recv(10).strip())
                if data == 0:
                    pass
                elif 0 < data <= 65535:
                    pass
                else:
                    import time
                    error_file = open(dir_path + '/error.log', 'a')
                    error_file.write('[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']' + str(data) + '\n')
                    error_file.close()
            except:
                pass

if __name__ == '__main__':
    if not py3:
        reload(sys)
        sys.setdefaultencoding('utf-8')
    config_file = open(dir_path + '/config.yaml')
    config = yaml.load(config_file)
    config_file.close()
    server = socketserver.ThreadingTCPServer((config['server']['host'], config['server']['port']), Server)
    server.serve_forever()