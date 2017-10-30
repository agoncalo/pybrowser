import socket
import sys


def connect(addr, port):
    print("INICIALIZANDO SOCKET ...")
    port = int(port)
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
        client.connect((hostIp, port))
    except socket.gaierror:
        print("NÃO FOI POSSÍVEL ENCONTRAR O ENDEREÇO IP PARA " + addr + "!")
        sys.exit()

    msg = "GET /" + dir + " HTTP/1.1\nHost: " + addr + ":" + str(port) + "\n" + \
            "Connection: keep-alive\n" \
            "Cache-Control: max-age=0\n" \
            "User-Agent: Mozilla/5.0(X11;Linux x86_64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/62.0.3202.75Safari/537.36\n" \
            "Upgrade-Insecure-Requests: 1\n" \
            "Accept: text/html, application/xhtml + xml, application/xml;q=0.9, image/webp, image/apng, */*;q=0.8\n" \
            "Accept-Encoding: gzip, deflate, br\n" \
            "Accept-Language: pt-BR, pt;q=0.9, en-US;q=0.8, en;q=0.7\n" \
            "\n\n"
    msg = msg.encode('utf-8')
    client.sendall(msg)
    code = 'latin-1'
    recv = client.recv(1024).decode(code)
    print(recv)
    while len(recv) > 0:
        recv = client.recv(1024).decode(code)
        print(recv)

    print("FECHANDO CONEXÃO!")
    client.close()


def run(addr, port=80):
    connect(addr, port)


if len(sys.argv) == 3:
    run(sys.argv[1], sys.argv[2])
elif len(sys.argv) != 1:
    run(sys.argv[1])
else:
    run('https://www.w3.org/Protocols/rfc2616/rfc2616.html')