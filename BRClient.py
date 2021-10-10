import socket

def connect():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 8000        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)
        print('Received', repr(data))
        s.sendall(b'1')
        data = s.recv(1024)
    return data


