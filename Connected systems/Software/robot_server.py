import socket
import threading

HOST = ""
PORT = 1024

messages = {}
clientCount = 0

def echo(conn):
    global messages, clientCount
    while True:
        data = conn.recv(1024).decode()
        if data == "":
            print("Connection lost to", conn.getpeername())
            break
        name, msg = data.split(": ")
        messages[name] = msg
        try:
            conn.sendall(str(messages).encode("ascii"))
        except:
            print("Connection lost to", conn.getpeername())
            break
    clientCount -= 1
    if clientCount == 0:
        print("All clients disconnected; resetting")
        messages = {}

s = socket.create_server((HOST, PORT))
s.listen()
while True:
    conn, addr = s.accept()
    clientCount += 1
    print("Connection accepted from", addr)
    t = threading.Thread(target = echo, args = (conn,))
    t.start()
