import socket
import time

HOST = 'localhost'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))  # Blocking connect
    print(f"Connected to {HOST}:{PORT}")
    
    while True:
        message = "Hello, server this is from the fifth client!\n"
        sock.sendall(message.encode())
        time.sleep(2)
    # Wait for response (if server sends anything back)
    # data = sock.recv(1024)
    # print(f"Received: {data.decode()}")