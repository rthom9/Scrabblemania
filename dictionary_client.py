# Author: Robert Thom
# GitHub username: rthom9
# Description: Client-side code for use of dictionary microservice. Microservice will access Merriam-Webster API.

import socket
import json

HEADER = 64
PORT = 5060
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client.connect(ADDR)

# Send a message
def send(msg):
    """Accepts msg string and encodes to byte format to send to dictionary_lookup microservice server. Returns word definition."""
    # Encode messages to byte format to be sent through socket
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    
    # Pad send_length to 64 bytes
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    if msg != DISCONNECT_MESSAGE:   
        received_msg = client.recv(2048).decode(FORMAT)
        received_msg_json = json.loads(received_msg)
        return received_msg_json
    
def dictionary_lookup(word, number_of_definitions=2):
    """Accepts word as an array and number of definitions requested. If word not found, returns invalid word."""
    
    word_request = [word, number_of_definitions]
    word_request_string = json.dumps(word_request)
    word_definition = send(word_request_string)
    return word_definition
