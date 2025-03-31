import socket

def test_server():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the port
    server_address = ('localhost', 3000)
    print(f'Starting up on {server_address[0]} port {server_address[1]}')
    sock.bind(server_address)
    
    # Listen for incoming connections
    sock.listen(1)
    
    while True:
        print('Waiting for a connection...')
        connection, client_address = sock.accept()
        try:
            print(f'Connection from {client_address}')
            connection.send(b'Hello, World!\n')
        finally:
            connection.close()

if __name__ == '__main__':
    test_server() 