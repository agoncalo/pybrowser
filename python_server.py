import socket
import platform
import os
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
from threading import Thread

def run_server(file, port):
    hostIp = ''

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    addr = srv.bind((hostIp, port))

    print("SOCKET CRIADO PARA A PORTA " + str(port) + "!")

    srv.listen(1)

    while True:
        id, client = srv.accept()
        thread = Thread(target=connect, args=(id, file))
        thread.start()
        print("NOVA CONEXÃO!")


def connect(id, file):
    now = datetime.now()
    stamp = mktime(now.timetuple())

    while True:
        msg = id.recv(1024).decode('utf-8')
        print("MENSAGEM RECEBIDA: " + msg)
        if not msg:
            break
        elif msg.startswith("GET "):
            req = msg.partition("/")[2]
            req = req.partition(" ")[0]
            is_valid_file = os.path.isfile(req)
            if is_valid_file:
                response = "HTTP/1.1 200 OK\n" \
                           "Date: " + format_date_time(stamp) + "\n" \
                           "Server: " + platform.system() + "/" + platform.release() + "\n" \
                           "Content-Type: text/html\n" \
                           "Connection: close\n\n"

                response = response + file
            else:
                response = "HTTP/1.1 200 OK\n" \
                           "Date: " + format_date_time(stamp) + "\n" \
                           "Server: " + platform.system() + "/" + platform.release() + "\n" \
                           "Content-Type: text/html\n" \
                           "Connection: close\n\n" \
                           "<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 2.0//EN\"><html><head><title>404 Not Found</title>" \
                           "</head><body><h1>Not Found</h1>" \
                           "<p>The requested URL " + req + " was not found on this server.</p><hr>" \
                           "<address>" + platform.system() + "/" + platform.release() + " Server at localhost Port 80</address>" \
                           "</body></html>"

            id.send(response.encode('utf-8'))
        else:
            id.sendall(response)
            break

    id.close()
    exit()

def run(filename, port=8480):
    f = open(filename,'r')
    l = f.read(1024)
    run_server(l, port)

run('README.md')