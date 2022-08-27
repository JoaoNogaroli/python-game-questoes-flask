import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'disc'
SERVER = "192.168.15.43"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


msg_recebida_servidor = client.recv(2048).decode(FORMAT)
#print(msg_recebida_servidor)


# def send(msg):
#     message = msg.encode(FORMAT)
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b' ' * (HEADER - len(send_length))
#     #print(f"send lenf: {send_length}")
#     client.send(send_length)
#     client.send(message)
#     print(client.recv(2048).decode(FORMAT)) 

# send("OLÀ SERVIDOR")

# send(DISCONNECT_MESSAGE)
