import socket
import sys

def connect(addr, port):
    print("INICIALIZANDO SOCKET ...")
    if addr.startswith("http://") or addr.startswith("https://"):
        addr = addr.split("//")[1]
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

    client.sendall(b'GET\n')
    rec = client.recv(1024).decode('utf-8')
    print(rec)

    print("FECHANDO CONEXÃO!")
    client.close()


def run(addr,port=80):
    connect(addr,port)

run('localhost',8080)