import sys
import socket
import _thread


def recibirMsg(sock):

    while True:
        data = sock.recv(4096)
        if not data:
            print('\nTe has desconectado del servidor')
            sys.exit()
        else:
            # print data
            if(data.decode()=="@IP"):
                sys.stdout.write("\r[Server] IP del servidor= "+str(sock.getpeername()[0])+'\n')
                sys.stdout.write('[Yo] ');
                sys.stdout.flush()
            else:
                sys.stdout.write(data.decode())
                sys.stdout.write('[Yo] ');
                sys.stdout.flush()


def chat_client():

    host = input("Escriba el IP(default=localhost):")
    port = input("Escriba el Puerto(default=5000):")
    host = host if (len(host) > 0) else 'localhost'
    port = int(port) if (len(port) > 0) else 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # conectar con el servidor
    try:
        s.connect((host, port))
    except:
        print('\nImposible conectar')
        sys.exit()

    #hilo para empezar a recibir mensajes
    _thread.start_new_thread(recibirMsg, (s,))
    print('\nSe ha establecido conexion')
    sys.stdout.write('[Yo] ');
    sys.stdout.flush()

    #ciclo para escribir mensajes
    while 1:
        # user entered a message
        msg = sys.stdin.readline()
        s.send(str.encode(msg))
        sys.stdout.write('[Yo] ');
        sys.stdout.flush()


chat_client()