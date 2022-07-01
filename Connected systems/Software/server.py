import socket
import threading

HOST = ""
PORT = 1024

def echo(conn):
    connections.append(conn)
    while data := conn.recv(1024):
        for c in connections:
            c.sendall(data)
    print("Connection lost to", conn.getpeername())
    connections.remove(conn)

connections = []
s = socket.create_server((HOST, PORT))
s.listen()
while True:
    conn, addr = s.accept()
    print("Connection accepted from", addr)
    t = threading.Thread(target = echo, args = (conn,))
    t.start()

