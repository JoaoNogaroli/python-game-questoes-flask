from copyreg import pickle
import socket
import pickle

def conexao_cliente_primeira_msg():
    HEADER = 64
    PORT = 5050
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = 'disc'
    SERVER = "192.168.15.43"
    ADDR = (SERVER, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)


    msg_recebida_servidor = client.recv(4096)
    #msg_recebida_servidor.replace('\n','<br>')
   
    msg = pickle.loads(msg_recebida_servidor)
    #print(msg)
    # def send(msg):
    #     message = msg.encode(FORMAT)
    #     msg_length = len(message)
    #     send_length = str(msg_length).encode(FORMAT)
    #     send_length += b' ' * (HEADER - len(send_length))
    #     #print(f"send lenf: {send_length}")
    #     client.send(send_length)
    #     client.send(message)
    # send("disc")
    client.close()    
    return {'msg':msg}