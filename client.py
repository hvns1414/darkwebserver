import socket
import threading
from optparse import OptionParser

# Setting up command-line arguments using optparse
parser = OptionParser()
parser.add_option("-i", "--ip", dest="ip", default="127.0.0.1",
                  help="IP address of the server to connect to (default: 127.0.0.1)")
parser.add_option("-p", "--port", dest="port", type="int", default=8000,
                  help="Port of the server to connect to (default: 8000)")
parser.add_option("-s", "--password", dest="password", default="ntf2",
                  help="Password for the server (default: ntf2)")

(options, args) = parser.parse_args()

# Prompting the user for a nickname
nickname = input("Enter your nickname: ")

# Connecting to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((options.ip, options.port))

# Sending the password to the server
client.send(options.password.encode('ascii'))
response = client.recv(1024).decode('ascii')
if response == "WRONG_PASSWORD":
    print("Incorrect password! Could not connect to the server.")
    client.close()
    exit()

# Function to receive messages from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred! Connection closed.")
            client.close()
            break

# Function to send messages to the server
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

# Starting threads for receiving and writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
