import sys
import socket
import _thread


def recibirMsg(sock):

    while True:
        data = sock.recv(4096)
        if not data:
            print(
                '\nDisconnected from chat server')
            sys.exit()
        else:
            # print data
            sys.stdout.write(data.decode())
            sys.stdout.write('[Me] ');
            sys.stdout.flush()

def chat_client():


    host = "localhost"
    port = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print(
        'Unable to connect')
        sys.exit()

    _thread.start_new_thread(recibirMsg, (s,))

    print(
    'Connected to remote host. You can start sending messages')
    sys.stdout.write('[Me] ');
    sys.stdout.flush()


    while 1:
        # user entered a message
        msg = sys.stdin.readline()
        s.send(str.encode(msg))
        sys.stdout.write('[Me] ');
        sys.stdout.flush()


chat_client()