from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from userDB import userDB

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
    while 1:
        client_socket, client_address = SERVER.accept()
        print("{}:{} has connected.".format(client_address[0], client_address[1]))
        ADDRESSES[client_socket] = client_address
        users = userDB()
        while 1:
            option = client_socket.recv(BUFFERSIZE)
            option = option.decode("utf8")
            if option == "register":
                username = client_socket.recv(BUFFERSIZE).decode("utf8")
                password = client_socket.recv(BUFFERSIZE).decode("utf8")
                check_user = users.username_query(username)
                users.mycursor.execute("SELECT * FROM USERS")
                temp = users.mycursor.fetchall()
                for x in temp:
                    print(x)
                if check_user:
                    client_socket.send(bytes("FAILED_TO_REGISTER", "utf8"))
                    print("{} failed to register, already exists in database".format(username))
                else:
                    users.user_insert(username, password)
                    client_socket.send(bytes("REGISTER_SUCCESS", "utf8"))
                    print("{} registered".format(username))

            elif option == "login":
                username = client_socket.recv(BUFFERSIZE).decode("utf8")
                password = client_socket.recv(BUFFERSIZE).decode("utf8")
                check_user = users.user_query(username, password)
                if check_user:
                    ONLINE_USERS[client_socket] = username
                    client_socket.send(bytes("PASS_LOGIN", "utf8"))
                    Thread(target=handle_client, args=(client_socket,)).start()
                    print("{} logged in".format(username))
                    break
                else:
                    client_socket.send(bytes("FAILED_LOGIN", "utf8"))
                    print("{} does not exist in database".format(username))


# Takes client.py socket as argument and handles a single client.py connection
def handle_client(client):
    name = ONLINE_USERS[client]
    CLIENTS[client] = name
    welcome = "Welcome {}! Type QUIT to exit.".format(name)
    msg = "{} has joined the chat!".format(name)
    client.send(bytes(welcome, "utf8"))
    broadcast(msg)

    while True:
        try:
            msg = client.recv(BUFFERSIZE).decode('utf8')
            broadcast(msg, name + ": ")
            if msg == "QUIT":
                close_connection(client)
                break
        except:
            continue


def close_connection(client):
    client.send(bytes("QUIT", "utf8"))
    print("{}:{} has disconnected.".format(ADDRESSES[client][0], ADDRESSES[client][1]))
    client.close()
    del ADDRESSES[client]
    del ONLINE_USERS[client]


# Prefix is for name identification
# Broadcasts a message to all clients
# TODO change to broadcast to single client.py
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
