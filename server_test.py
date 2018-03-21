import socket
import threading
import time

def client_handler(sock):
    data = sock.recv(1024)
    time.sleep(0.3)
    sock.sendall(
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/html\r\n"
        b"Content-Length: 71\r\n\r\n"
        b"<html><head><title>Success</title></head><body>Index page</body></html>"
    )
    sock.close()

host = '127.0.0.1'
port = 9090
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
sock.bind((host, port))
sock.listen(128)

try:
    while True:
        client_sock, _ = sock.accept()
        client_thread = threading.Thread(target=client_handler, args=(client_sock,))
        client_thread.daemon = True
        client_thread.start()
except KeyboardInterrupt:
    print("Shutting down")
finally:
    sock.close()