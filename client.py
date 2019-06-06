import socket

# Creating socket
s = socket.socket()
host = input(str("Enter hostname of the server: "))
port = 9999

# Connecting socket
s.connect((host, port))

print(" Connected to chat server")

# Send message and receive message from the server
while True:
    incoming_message = s.recv(1024)
    incoming_message = incoming_message.decode()
    print(" Server: " + incoming_message + "\n")

    message = input(str(">> "))
    message = message.encode()
    s.send(message)
    print("message has been sent...\n")