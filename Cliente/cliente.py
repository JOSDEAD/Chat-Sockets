import sys
import socket
import select

from threading import *

from socket import *
import _thread, time
import msvcrt as m


def recvMsg(sock):
    while True:
        recvmsg = sock.recv(1024)
        print(
        '<Server>>> ' + recvmsg.decode())


if __name__ == '__main__':

    host = "localhost"
    port = 5000

    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))

        _thread.start_new_thread(recvMsg, (s,))

        time.sleep(1)
        nickmsg = input('My Nickname: ')
        s.send(nickmsg)

        time.sleep(2)
        print(
        'Wait!...')

        while True:
            if m.getch() != '\r':
                continue
            sendmsg = input(' - Send: ')
            if sendmsg == 'exit()':
                break
            s.send(sendmsg)

        s.close()
    except:
        print(
        'Wrong address!')

    input('Exit client (Press any key!)')