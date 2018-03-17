import socket
import select
HOST=''
PORT=5000
BUFFER_SIZE = 1024
SOCKET_LIST=[]


servidor_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
servidor_socket.bind((HOST,PORT))
servidor_socket.listen(10)

SOCKET_LIST.append(servidor_socket)

#Empieza el chat
# broadcast chat messages to all connected clients
def broadcast(server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock:
            try:
                socket.send(str.encode(message))
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)


while True:
    ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)
    for sockets in ready_to_read:
        #Solicitud de nueva coneccion
        if sockets == servidor_socket:
            newSocket,addr= servidor_socket.accept()
            SOCKET_LIST.append(newSocket)
            print("Cliente (%s, %s) connectado" % addr)
        else:
            try:
                data= sockets.recv(BUFFER_SIZE)
                if data:
                    broadcast(servidor_socket,sockets,"\r"+'[' + str(sockets.getpeername()) + ']'+data.decode())
                else:
                    if sockets in SOCKET_LIST:
                        SOCKET_LIST.remove(sockets)
                    broadcast(servidor_socket, sockets, "Cliente (%s, %s) se desconecto\n" % addr)

            except:
                ##broadcast(servidor_socket, sockets, "Cliente (%s, %s) se desconecto\n" % addr)
                continue


servidor_socket.close()

