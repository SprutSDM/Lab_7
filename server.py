import socket

def main(host='localhost', port=9090):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    serversocket.bind((host, port))
    serversocket.listen(5)
    
    print('Starting Echo Server at ' + str(host) + ':' + str(port))
    try:
        while True:
            clientsocket, (client_address, client_port) = serversocket.accept()
            print('New client ' + str(client_address) + ':' + str(client_port))
            
            while True:
                try:
                    data = clientsocket.recv(1024)
                except OSError:
                    break
            
                if not data:
                    break
                sent_data = data
                while True:
                    sent_len = clientsocket.send(sent_data)
                    if sent_len == len(data):
                        break
                    sent_data = sent_data[sent_len:]
                print('Send:', data)
            clientsocket.close()
            print('Bye-Bye: ' + client_address + ':' + client_port)
    except KeyboardInterrupt:
        print('Shutting down')
    finally:
        serversocket.close()

if __name__ == '__main__':
    main()