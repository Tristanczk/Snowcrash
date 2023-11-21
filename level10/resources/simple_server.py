import socket

HOST, PORT = '', 6969

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print(f"Server listening on port {PORT}")
while True:
    client_connection, client_address = listen_socket.accept()
    request_data = client_connection.recv(1024)
    while request_data:
        s = request_data.decode('utf-8')
        if (s != "trying\n" and s != ".*( )*.\n"):
            print(f"Message received: {s}")
        request_data = client_connection.recv(1024)
