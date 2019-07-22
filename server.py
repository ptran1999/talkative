from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from userDB import userDB


# CLIENTS holds {socket: client_name}
# ADDRESSES holds {socket: (IP, PORT)}
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
        print("{}:{} has connected.".format(client_address[0], client_address[1]))
        ADDRESSES[client_socket] = client_address

        # When a client connects, clicking register or login will send to the server a string of either
        # REGISTER or LOGIN

        while True:
            userOption = client_socket.recv(BUFFERSIZE).decode('utf8')
            print("User option is {}".format(userOption))
            if userOption == "REGISTER":
                register_thread = Thread(target=register_user, args=(client_socket,))
                register_thread.start()
                register_thread.join()


            elif userOption == "LOGIN":
                users = userDB()
                username = client_socket.recv(BUFFERSIZE).decode('utf8')
                password = client_socket.recv(BUFFERSIZE).decode('utf8')
                check_user = users.user_query(username, password)
                if check_user:
                    ONLINE_USERS[client_socket] = username
                    client_socket.send(bytes("PASS_LOGIN", 'utf8'))
                    Thread(target=handle_client, args=(client_socket,)).start()
                    print("{} logged in".format(username))
                    users.close_connection()
                    break
                else:
                    client_socket.send(bytes("FAILED_LOGIN", 'utf8'))
                    print("{} does not exist in database".format(username))

            else:
                pass



# Create a seperate thread to register the user
def register_user(client):
    flag = False
    newUser = userDB()
    while flag != True :
        username = client.recv(BUFFERSIZE).decode('utf8')
        password = client.recv(BUFFERSIZE).decode('utf8')

        check_user = newUser.username_query(username)
        if check_user:
            client.send(bytes("FAILED_TO_REGISTER", 'utf8'))
        else:
            newUser.user_insert(username, password)
            client.send(bytes("REGISTER_SUCCESS", 'utf8'))
            flag = True
    newUser.close_connection()
    return True

# Takes client socket as argument and handles a single client connection
def handle_client(client):
    name = ONLINE_USERS[client]
    welcome = "Welcome {}! Type QUIT to exit.".format(name)
    msg = "{} has joined the chat!".format(name)

    try:
        print(msg)
        client.send(bytes(welcome, 'utf8'))
        broadcast(msg)
    except:
        pass

    while True:
        try:
            msg = client.recv(BUFFERSIZE).decode('utf8')
            if msg != "QUIT":
                broadcast(msg, name + ": ")
            else:
                close_connection(client)
                break

        except:
            continue


def close_connection(client):
    client.send(bytes("QUIT", 'utf8'))
    print("{}:{} has disconnected.".format(ADDRESSES[client][0], ADDRESSES[client][1]))
    client.close()
    del ADDRESSES[client]
    del ONLINE_USERS[client]


# Prefix is for name identification
# Broadcasts a message to all clients
# TODO change to broadcast to single client
def broadcast(msg, prefix=""):
    sent_message = "{}{}".format(prefix, msg)
    print(sent_message)
    try:
        for client in ONLINE_USERS:
            client.send(bytes(sent_message, 'utf8'))
    except:
        pass


if __name__ == "__main__":
    SERVER.listen(10)
    print("Waiting for connection...")
    accept_connections()
    SERVER.close()
