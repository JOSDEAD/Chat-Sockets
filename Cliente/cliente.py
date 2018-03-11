import socket

TCP_IP = 'localhost'
TCP_PORT = 5000
BUFFER_SIZE = 1024
MESSAGE = str.encode( "Hello, World!")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()
print("received data: "+ data.decode())