import socket

HOST = ""
PORT = 1024

s = socket.create_server((HOST, PORT))
s.listen()
conn, addr = s.accept()
print("Connection accepted from", addr)
data = conn.recv(1024).decode()
print("Received: " + data)
