from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# CLIENTS holds {socket: client_name}
# ADDRESSES holds {socket: (IP, PORT)}
CLIENTS = {}
ADDRESSES = {}

HOST = ''
PORT = 9999
BUFFERSIZE = 1024
ADDR = (HOST, PORT)

# Creating the server socket and binds it to ADDR
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# Sets up handling for incoming clients
def accept_connections():
    while True:
        client, addy = SERVER.accept()
        print("%s:%s has connected." % addy)
        ADDRESSES[client] = addy
        Thread(target=handle_client, args=(client,)).start()

# Takes client socket as argument and handles a single client connection
def handle_client(client):
    name = client.recv(BUFFERSIZE).decode("utf8")
    welcome = "Welcome %s! Type QUIT to exit." % name
    msg = "%s has joined the chat!" % name

    try:
        client.send(bytes(welcome,"utf8"))
        CLIENTS[client] = name
        broadcast(bytes(msg,"utf8"))
    except:
        pass

    while True:
        try:
            msg = client.recv(BUFFERSIZE)
            if msg != bytes("QUIT", "utf8"):
                broadcast(msg, name + ": ")
            else:
                client.send(bytes("QUIT", "utf8"))
                client.close
                del CLIENTS[client]
                broadcast(bytes("%s has left the chat." % name, "utf8"))
                break
        except:
            continue

# Prefix is for name identification
# Broadcasts a message to all clients
# TODO change to broadcast to single client
def broadcast(msg, prefix=""):
    try:
        for client in CLIENTS:
            client.send(bytes(prefix, "utf8") + msg)
    except:
        pass

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_connections())
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
