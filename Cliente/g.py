import sys
import socket
import select


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


    print(
    'Connected to remote host. You can start sending messages')
    sys.stdout.write('[Me] ');
    sys.stdout.flush()


    while 1:
        socket_list = [sys.stdin,s]


        for sock in socket_list:
            if sock == s:
                print(1)
                # incoming message from remote server, s
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

            else:

                # user entered a message
                msg = sys.stdin.readline()
                s.send(str.encode(msg))
                sys.stdout.write('[Me] ');
                sys.stdout.flush()


if __name__ == "__main__":
    sys.exit(chat_client())