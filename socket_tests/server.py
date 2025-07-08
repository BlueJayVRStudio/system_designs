import socket, selectors

sel = selectors.DefaultSelector()
client_info = {}  # maps conn → client metadata (like IP address)

def accept(sock):
    conn, addr = sock.accept()
    print("Accepted from", addr)
    conn.setblocking(False)

    client_info[conn] = {
        "addr": addr,
        "buffer": b""
    }

    sel.register(conn, selectors.EVENT_READ, read)

def read(conn):
    try:
        data = conn.recv(1024)
        if data:
            info = client_info[conn]
            print(f"Received from {info['addr']}: {data!r}")
            info['buffer'] += data
        else:
            # connection closed
            print(f"Closing {client_info[conn]['addr']}")
            sel.unregister(conn)
            conn.close()
            del client_info[conn]
    except ConnectionResetError:
        print(f"Reset by {client_info[conn]['addr']}")
        sel.unregister(conn)
        conn.close()
        del client_info[conn]

# setup server socket
server = socket.socket()
server.bind(("localhost", 12345))
server.listen()
server.setblocking(False)
sel.register(server, selectors.EVENT_READ, accept)

while True:
    for key, _ in sel.select():
        callback = key.data
        callback(key.fileobj)