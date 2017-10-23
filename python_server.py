import socket
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
    while True:
        msg = id.recv(1024).decode('utf-8')
        print("MENSAGEM RECEBIDA: " + msg)
        if not msg:
            break
        elif msg == "GET\n":
            id.send(file.encode('utf-8'))
        else:
            id.sendall(b'Mensagem incorreta!\n')
            break

    id.close()
    exit()

def run(filename, port=8080):
    f = open(filename,'r')
    l = f.read(1024)
    run_server(l, port)