from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from userDB import userDB

# Holds User information on DataBase
users = userDB()

# CLIENTS holds {socket: client_name}
# ADDRESSES holds {socket: (IP, PORT)}
CLIENTS = {}
ADDRESSES = {}
ONLINE_USERS = {}

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
        client_socket, client_address = SERVER.accept()
        print("{}:{} has connected.".format(client_address[0],client_address[1]))
        ADDRESSES[client_socket] = client_address

        # When a client connects, clicking register or login will send to the server a string of either
        # REGISTER or LOGIN
        userOption = client_socket.recv(BUFFERSIZE).decode()
        print("User option is {}".format(userOption))

        if userOption == "REGISTER":
            username = client_socket.recv(BUFFERSIZE).decode()
            password = client_socket.recv(BUFFERSIZE).decode()
            check_user = users.username_query(username)
            if check_user:
                client_socket.send("FAILED_TO_REGISTER".encode())
                print("{} failed to register, already exists in database".format(username))
            else:
                users.user_insert(username, password)
                client_socket.send("REGISTER_SUCCESS".encode())
                print("{} registered".format(username))


        elif userOption == "LOGIN":
            username = client_socket.recv(BUFFERSIZE).decode()
            password = client_socket.recv(BUFFERSIZE).decode()
            check_user = users.user_query(username, password)
            if check_user:
                ONLINE_USERS[client_socket] = username
                client_socket.send("PASS_LOGIN".encode())
                Thread(target=handle_client, args=(client_socket,)).start()
                print("{} logged in".format(username))
            else:
                client_socket.send("FAILED_LOGIN".encode())
                print("{} does not exist in database".format(username))

        else:
            pass

# Takes client socket as argument and handles a single client connection
def handle_client(client):
    name = ONLINE_USERS[client]
    CLIENTS[client] = name
    welcome = "Welcome {}! Type QUIT to exit.".format(name)
    msg = "{} has joined the chat!".format(name)

    try:
        client.send(welcome.encode())
        broadcast(msg.encode())
    except:
        pass

    while True:
        try:
            msg = client.recv(BUFFERSIZE)
            if msg != "QUIT":
                broadcast(msg, name + ": ")
            else:
                close_connection(client)
                break

        except:
            continue

def close_connection(client):
    client.send(bytes("QUIT".encode()))
    print("{}:{} has disconnected.".format(ADDRESSES[client][0], ADDRESSES[client][1]))
    client.close()
    del ADDRESSES[client]
    del ONLINE_USERS[client]

# Prefix is for name identification
# Broadcasts a message to all clients
# TODO change to broadcast to single client
def broadcast(msg, prefix=""):
    try:
        for client in ONLINE_USERS:
            client.send("{}{}".format(prefix, msg).encode())
    except:
        pass


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_connections())
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
