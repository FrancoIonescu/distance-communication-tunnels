import socket
import threading

REMOTE_HOST = 'localhost'
REMOTE_PORT_TUNNEL = 54321
SERVICE_HOST = 'localhost'
ECHO_PORT = 8080

def forward_data(source_socket, destination_socket, description):
    try:
        while True:
            data = source_socket.recv(1024)
            if not data:
                break
            destination_socket.sendall(data)
    except Exception as e:
        print(f"Eroare în transmiterea datelor {description}: {e}")
    finally:
        source_socket.close()
        destination_socket.close()

def handle_remote_connection(client_socket, client_address):
    print(f"Server de la distanță: Conexiune de la {client_address}")
    try:
        first_data = client_socket.recv(1024).decode('utf-8')
        if not first_data:
            return

        if ':' in first_data:
            port_str, msg = first_data.split(':', 1)
            try:
                destination_port = int(port_str)
            except ValueError:
                destination_port = ECHO_PORT
                msg = first_data
        else:
            destination_port = ECHO_PORT
            msg = first_data

        print(f"Redirecționare către {SERVICE_HOST}:{destination_port} - {msg}")

        svc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        svc_sock.connect((SERVICE_HOST, destination_port))
        svc_sock.sendall(msg.encode('utf-8'))

        threading.Thread(target=forward_data, args=(client_socket, svc_sock, "client -> serviciu"), daemon=True).start()
        threading.Thread(target=forward_data, args=(svc_sock, client_socket, "serviciu -> client"), daemon=True).start()

    except Exception as e:
        print(f"Eroare în conexiune remote: {e}")

def start_remote_tunnel_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((REMOTE_HOST, REMOTE_PORT_TUNNEL))
        server_socket.listen()
        print(f"Serverul de tunelare de la distanță ascultă pe {REMOTE_HOST}:{REMOTE_PORT_TUNNEL}")
        while True:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=handle_remote_connection, args=(client_socket, client_address), daemon=True).start()

if __name__ == "__main__":
    start_remote_tunnel_server()
