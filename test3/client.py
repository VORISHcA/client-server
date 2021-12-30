import json
import sys
import socket
import time

if '-p' in sys.argv:
    server_port = int(sys.argv[sys.argv.index('-p') + 1])
else:
    server_port = 7777
if '-a' in sys.argv:
    server_address = sys.argv[sys.argv.index('-a') + 1]
else:
    server_address = "127.7.7.7"

transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
transport.connect((server_address, server_port))

message = {
    'action': "presence",
    'time': time.time(),
}

json_message = json.dumps(message)
response = json_message.encode("utf-8")
transport.send(response)
response = transport.recv(1024)
json_response = response.decode("utf-8")
response = json.loads(json_response)
if response['action'] == "response":
    print('200')
print(response)


