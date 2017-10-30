import socket
import platform
import os
import sys
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
from threading import Thread


def run_server(file, port):
    hostIp = ''

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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
            req = file + req.partition(" ")[0]
            is_valid_file = os.path.isfile(req)
            if is_valid_file:
                if not req.endswith('jpg') or req.endswith('png'):
                    f = open(req, 'r')
                    file = f.read(10000)
                    response = "HTTP/1.1 200 OK\n" \
                               "Date: " + format_date_time(stamp) + "\n" \
                               "Server: " + platform.system() + "/" + platform.release() + "\n" \
                               "Content-Type: text/html\n" \
                               "Connection: close\n\n"
                    response = response + file
                    id.send(response.encode('utf-8'))
                else:
                    if req.endswith('jpg'):
                        type = 'jpg'
                    else:
                        type = 'png'
                    f = open(req, 'rb')
                    file = f.read(10000)
                    response = "HTTP/1.1 200 OK\n" \
                               "Date: " + format_date_time(stamp) + "\n" \
                               "Server: " + platform.system() + "/" + platform.release() + "\n" \
                               "Content-Type: image/" + type + "\n" \
                               "Connection: close\n\n"
                    id.send(response.encode('utf-8'))
                    id.send(file)

            elif os.path.isdir(req):
                response = "HTTP/1.1 200 OK\n" \
                           "Date: " + format_date_time(stamp) + "\n" \
                           "Server: " + platform.system() + "/" + platform.release() + "\n" \
                           "Content-Type: text/html\n" \
                           "Connection: close\n\n"
                response = response + \
                           "<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 2.0//EN\"><html><head><title>Arquivos</title>" \
                           "</head><body><ol>" \
                           "<h1>Arquivos em " + req.partition("/")[1] + req.partition("/")[2] + "</h1>"
                for f in os.listdir(req):
                    if not os.path.isdir(f):
                        response = response + "<li><a href=\"" + req.partition("/")[2] + "/" + f + "\">" + f + "</a></li>"
                response = response + "</ol></body>"
                id.send(response.encode('utf-8'))
            else:
                response = "HTTP/1.1 200 OK\n" \
                           "Date: " + format_date_time(stamp) + "\n" \
                           "Server: " + platform.system() + "/" + platform.release() + "\n" \
                           "Content-Type: text/html\n" \
                           "Connection: close\n\n" \
                           "<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 2.0//EN\"><html><head><title>404 Not Found</title>" \
                           "</head><body><h1>Not Found</h1>" \
                           "<p>The requested URL " + req.partition("/")[2] + " was not found on this server.</p><hr>" \
                           "<address>" + platform.system() + "/" + platform.release() + " Server at localhost Port 80</address>" \
                           "</body></html>"
                id.send(response.encode('utf-8'))

        id.close()
        exit()


def run(filename, port=8080):
    run_server(filename, port)


if sys.argv[2]:
    run(sys.argv[1], sys.argv[2])
else:
    run(sys.argv[1])
