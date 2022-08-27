from concurrent.futures import thread
import socket
import threading
import csv
# from pegardado import pegardado2

HEADER = 64
PORT = 5050
# SERVER = "192.168.15.43"
# or
SERVER = socket.gethostbyname(socket.gethostname())
print("meu ip é: ", SERVER)
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'disc'

lista_client = []


lista = ['0',
 'adm_geral',
 'Questão 1:',
 ' Liderança',
 'O Jornal O Estado de São Paulo publicou reportagem denominada “De Nobel da Paz a líder de guerra, Abiy Ahmed encara eleição na Etiópia”, em que discutia como o primeiro-ministro do país africano enfrenta a vontade das urnas pela primeira vez, desde que chegou ao cargo, em um processo eleitoral bastante questionado a partir do seguinte quadro:\n“Mesmo a votação desta segunda-feira, antes anunciada como a primeira eleição livre do país, e uma chance de virar a página em décadas de governos autocráticos, apenas reforçou as divisões internas e alimentou advertências sombrias de que o futuro da Etiópia está em dúvida.”\n  (O Estado de São Paulo. “De Nobel da Paz a líder de guerra, Abiy Ahmed encara eleição na Etiópia”. Internacional, São Paulo, ano 2021. Disponível em: https://internacional.estadao.com.br/noticias/geral)\n  No contexto desta publicação, a liderança de governos autocráticos é caracterizada por',
 ' a)  busca da popularidade com os liderados.\n b)  divisão dos poderes de decisão entre chefe e grupo.\n c)  delegação do poder de decisão ao grupo.\n d)  abuso de autoridade e delegação de poder.\n e)  centralização de poder de decisão no chefe.',
 'E']

lista = [s.replace('\n', '<br>') for s in lista]
#print(lista)
import pickle

data=pickle.dumps(lista)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def globalmessage(message):
    for cc in lista_client:
        cc.send(message).encode(FORMAT)    


def handle_client(conn, addr):
    print(f"[Nova conexão: {addr} conectado]")

    connected = True
    while connected:

        # conn.send("Primeira Mensagem ->Servidor mandando msg para cliente".encode(FORMAT))
        conn.send(data)
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            globalmessage(msg)
            # if msg == DISCONNECT_MESSAGE:
            #     connected = False
            # print(f"{addr}: {msg}")
            
            # # mensagem do SERVIDOR para o CLIENTE
        else:
            conn.send("Aguardando msg: ".encode(FORMAT))


            

        # conn.close()    

def start():
    server.listen(2)
    print(f"[Servidor no ip: {SERVER}]...")
    while True:
        conn, addr= server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[Conexoes ativas: {threading.activeCount()-1}]")
        lista_client.append(conn)
        print(lista_client)

print("[Iniciando servidor....]")
start()