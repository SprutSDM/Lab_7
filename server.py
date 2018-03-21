import socket
import threading
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s'
    )

def client_handler(sock, address, port):
    while True:
        try:
            data = sock.recv(1024)
            print(data)
            logging.debug('Recv: ' + str(data) + ' from ' + address + ':' + str(port))
        except OSError:
            break
        
        if len(data) == 0:
            break
        
        sent_data = data
        while True:
            sent_len = sock.send(data)
            if sent_len == len(data):
                break
            sent_data = sent_data[sent_len:]
        logging.debug('Send: ' + str(data) + ' from ' + address + ':' + str(port))
    
    sock.close()
    logging.debug('Bye-bye: ' + address + ':' + str(port))

def main(host='localhost', port=9090):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    serversocket.bind((host, port))
    serversocket.listen(128)
    print("Starting TCP Echo Server at", str(host) + ":" + str(port))
    try:
        while True:
            client_sock, (client_address, client_port) = serversocket.accept()
            logging.debug('New client ' + client_address + ':' + str(port))
            client_thread = threading.Thread(target=client_handler,
                            args=(client_sock, client_address, client_port))   
            client_thread.daemon = False
            client_thread.start()
    except KeyboardInterrupt:
        print('Shutting down')
    finally:
        sock.close()

if __name__ == '__main__':
    main()