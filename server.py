import socket


# Creating socket
def create_socket():
    try:
        global host
        global port
        global s
        host = socket.gethostname()
        print(" server will start on host : ", host)
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding + listening for connections
def bind_socket():
    try:
        global host
        global port
        global s

        s.bind((host, port))
        print("Binding the Port: " + str(port))

        s.listen(1)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Establish connection with a client
# Send message and receive message from the client
def socket_accept():
    conn, address = s.accept()
    print("Connected to server at: " + " IP " + address[0] + " | Port" + str(address[1]))

    while True:
        message = input(str(">> "))
        message = message.encode()
        conn.send(message)
        print("message has been sent...\n")

        incoming_message = conn.recv(1024)
        incoming_message = incoming_message.decode()
        print(" Client : " + incoming_message + "\n")

    conn.close()


def main():
    create_socket()
    bind_socket()
    socket_accept()


main()
