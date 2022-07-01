import socket

HOST = "localhost"
PORT = 1024
s = socket.socket()
try:
    s.connect((HOST, PORT))
except:
    print("Connection refused")
    exit()
s.sendall(b"Hello, world")
