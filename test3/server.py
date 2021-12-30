import sys
import socket
import json

if '-p' in sys.argv:
    listen_port = int(sys.argv[sys.argv.index('-p') + 1])
else:
    listen_port = 7777
if '-a' in sys.argv:
    listen_address = sys.argv[sys.argv.index('-a') + 1]
else:
    listen_address = "127.7.7.7"

transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
transport.bind((listen_address, listen_port))
transport.listen(5)
while True:
    client, client_address = transport.accept()
    response = client.recv(512)
    json_response = response.decode('utf-8')
    if json_response['action'] == "presence":
        json_response['action'] = "response"
    response = json_response.encode('utf-8')
    client.send(response)
    client.close()


