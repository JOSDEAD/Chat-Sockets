import socket

HOST='localhost'
PORT=5000
BUFFER_SIZE = 20

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1)

conn,addr=s.accept()

print("Connection address", addr)
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    decodedData=data.decode()
    print("received data: "+ decodedData)
    conn.send(data)  # echo
conn.close()