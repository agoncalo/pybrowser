import socket
import sys
from threading import Thread

def connect(addr, port):
    print("INICIALIZANDO SOCKET ...")
    if addr.startswith("http://") or addr.startswith("https://"):
        if addr.startswith("http"):
            port = 80
        elif addr.startswith("https"):
            port = 443
        addr = addr.split("//")[1]
    dir = addr.partition("/")[2]
    addr = addr.split("/")[0]

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("SOCKET CRIADO!")
    except socket.error:
        print("FALHA AO CRIAR SOCKET!")
        sys.exit()
    print("OBTENDO ENDEREÇO DE IP ...")
    try:
        hostIp = socket.gethostbyname(addr)
        print("O IP PARA " + addr + " É " + hostIp + ". ESTABELECENDO CONEXÃO ...")
        client.connect((hostIp,port))
    except socket.gaierror:
        print("NÃO FOI POSSÍVEL ENCONTRAR O ENDEREÇO IP PARA " + addr + "!")
        sys.exit()

    msg = "GET /" + dir + " HTTP/1.1\nHost: " + addr + "\n\n"
    msg = msg.encode('utf-8')
    client.sendall(msg)
    rec = client.recv(1024).decode('utf-8')
    print(rec)

    print("FECHANDO CONEXÃO!")
    client.close()


def run(addr,port=80):
    connect(addr,port)

thread = []
thread_1 = Thread(target=run, args=('http://dcomp.ufsj.edu.br/~fls/redes/tp1.txt', 80))
thread_1.start()