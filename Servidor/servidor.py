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
                    print("["+str(addr)+"]: "+data.decode())
                    for rectores in SOCKET_LIST:
                        if rectores != sockets and rectores != servidor_socket:
                            print(rectores)
                            rectores.send(data)
                else:
                    if sockets in SOCKET_LIST:
                        SOCKET_LIST.remove(sockets)
            except:
                continue

servidor_socket.close()

