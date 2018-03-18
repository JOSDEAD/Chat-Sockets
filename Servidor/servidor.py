import socket
import select
import urllib.request
import json
HOST=''
PORT=5000
BUFFER_SIZE = 1024
SOCKET_LIST=[]

#Obtener lista de paises y sus zonas horarias
response = urllib.request.Request('http://api.timezonedb.com/v2/list-time-zone?key=07T61XN44HZU&format=json')
r = urllib.request.urlopen(response).read()
jsonPaises = r.decode('utf8').replace("'", '"')
# Load the JSON to a Python list & dump it back out as formatted JSON
paises = json.loads(jsonPaises)



""""port = input("Escriba el Puerto(default=5000):")
port = int(port) if (len(port) > 0) else 5000"""""
servidor_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
servidor_socket.bind((HOST,PORT))
servidor_socket.listen(10)
SOCKET_LIST.append(servidor_socket)




##Obtener hora de algun pais
def obtenerHora(server_socket,pais):
    pais = pais.replace("\n", '')
    zonename = ""
    for i in paises["zones"]:
        if i["countryName"] == pais:
            zonename = i["zoneName"]
            break;

    if zonename != "":
        url = 'http://api.timezonedb.com/v2/get-time-zone?key=07T61XN44HZU&by=zone&format=json&zone=' + zonename
        response = urllib.request.Request(url)
        r = urllib.request.urlopen(response).read()
        my_json = r.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        broadcast(server_socket,server_socket,"\r[Server] Hora en "+pais+' '+data["formatted"]+'\n')
    else:
        broadcast(server_socket, server_socket, "\r[Server] Pais no encontrado\n")



#Empieza el chat
# envia mensajes a todos los clientes, menos al que envia
def broadcast(server_socket, sock, message):
    for socket in SOCKET_LIST:
        # enviar solo a receptores
        if socket != server_socket and socket != sock:
            try:
                socket.send(str.encode(message))
            except:
                socket.close()
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

def enviarATodos(server_socket,msg):
    for socket in SOCKET_LIST:
        # enviar solo a receptores
        if socket != server_socket:
            try:
                socket.send(str.encode(msg))
            except:
                socket.close()
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
            broadcast(servidor_socket, sockets, "\r[%s:%s] entro al chat\n" % addr)
        else:
            try:
                data= sockets.recv(BUFFER_SIZE)
                if data:
                    broadcast(servidor_socket, sockets, "\r" + '[' + str(sockets.getpeername()) + ']' + data.decode())
                    decodedData = data.decode()
                    if "@" == decodedData[0]:
                        if "@hora " in decodedData:
                            pais=decodedData.replace("@hora ", '')
                            obtenerHora(servidor_socket,pais)
                        if "@IP" in decodedData:
                            enviarATodos(servidor_socket,"@IP")
                        if "@ip" in decodedData:
                            enviarATodos(servidor_socket, "@IP")
                        if "@procesos" in decodedData:
                            enviarATodos(servidor_socket,"\rHay "+str(len(SOCKET_LIST)-1)+" procesos en el servidor\n")


                else:
                    if sockets in SOCKET_LIST:
                        SOCKET_LIST.remove(sockets)
                    broadcast(servidor_socket, sockets, "Cliente (%s, %s) se desconecto\n" % addr)

            except:

                continue


servidor_socket.close()

