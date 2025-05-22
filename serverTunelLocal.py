import socket
import threading

LOCAL_HOST = 'localhost'
LOCAL_PORT_TUNNEL = 12345
REMOTE_HOST = 'localhost'
REMOTE_PORT_TUNNEL = 54321

def forward_data(source_socket, destination_socket, description):
    """Transmite date de la un socket la altul continuu"""
    try:
        while True:
            data = source_socket.recv(1024)
            if not data:
                break
            destination_socket.sendall(data)
    except Exception as e:
        print(f"Eroare în transmiterea datelor {description}: {e}")

def handle_client(client_socket, client_address):
    print(f"Conexiune de la {client_address}")
    
    try:
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((REMOTE_HOST, REMOTE_PORT_TUNNEL))
        print(f"Server local: Conectat la serverul de la distanță pentru clientul {client_address}")
        
        client_to_remote = threading.Thread(
            target=forward_data, 
            args=(client_socket, remote_socket, f"client {client_address} -> remote"),
            daemon=True
        )
        
        remote_to_client = threading.Thread(
            target=forward_data, 
            args=(remote_socket, client_socket, f"remote -> client {client_address}"),
            daemon=True
        )
        
        client_to_remote.start()
        remote_to_client.start()
        
        client_to_remote.join()
        remote_to_client.join()
        
    except Exception as e:
        print(f"Eroare la gestionarea clientului {client_address}: {e}")
    finally:
        client_socket.close()
        remote_socket.close()
        print(f"Conexiune închisă cu {client_address}")

def start_local_tunnel_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((LOCAL_HOST, LOCAL_PORT_TUNNEL))
        server_socket.listen()
        print(f"Serverul de tunelare local ascultă pe {LOCAL_HOST}:{LOCAL_PORT_TUNNEL}")
        
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.daemon = True
            client_thread.start()

if __name__ == "__main__":
    start_local_tunnel_server()