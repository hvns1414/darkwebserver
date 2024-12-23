import socket
import threading
from optparse import OptionParser

# Setting up command-line arguments using optparse
parser = OptionParser()
parser.add_option("-i", "--ip", dest="ip", default="127.0.0.1",
                  help="IP address for the server to bind to (default: 127.0.0.1)")
parser.add_option("-p", "--port", dest="port", type="int", default=8000,
                  help="Port for the server to listen on (default: 8000)")
parser.add_option("-s", "--password", dest="password", default="ntf2",
                  help="Password for the server (default: ntf2)")

(options, args) = parser.parse_args()

# Connection data
host = options.ip
port = options.port
server_password = options.password

# Starting the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists to hold clients and their nicknames
clients = []
nicknames = []

# Function to broadcast messages to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle a single client
def handle(client):
    while True:
        try:
            # Broadcasting messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing and closing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left!'.encode('ascii'))
            nicknames.remove(nickname)
            break

# Function to receive new connections
def receive():
    print(f"Server is running on {host}:{port}")
    while True:
        # Accepting connection
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Password verification
        client.send("PASSWORD".encode('ascii'))
        password = client.recv(1024).decode('ascii')
        if password != server_password:
            client.send("WRONG_PASSWORD".encode('ascii'))
            client.close()
            print(f"Incorrect password attempt from {str(address)}")
            continue

        # Requesting and storing nickname
        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Announcing the new client
        print(f"Nickname is {nickname}")
        broadcast(f"{nickname} joined!".encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        # Starting thread to handle the client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Starting the server
receive()
