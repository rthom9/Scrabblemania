# Author: Robert Thom
# GitHub username: rthom9
# Description: Client-side code to interact with randomizer microservice via websocket.

import socket
import json

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)

# Send a message
def send(msg):
    # Encode messages to byte format to be sent through socket
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    
    # Send_length needs to be padded to 64 bytes
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    if msg != DISCONNECT_MESSAGE:   
        received_msg = client.recv(2048).decode(FORMAT)
        received_msg_json = json.loads(received_msg)
        return received_msg_json
    
def randomize_request(values, num):
    """Accepts an array of values and requested number of random values to be returned"""
    return send(json.dumps({"values": values, "num": num}))
