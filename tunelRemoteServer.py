import socket
import threading

REMOTE_HOST = '127.0.0.1'
REMOTE_PORT_TUNNEL = 54321 
SERVICE_HOST = '127.0.0.1' 

def handle_remote_connection(client_socket, client_address):
    print(f"Server de la distanță: Conexiune de la {client_address}")
    try:
        while True:
            data_received = client_socket.recv(1024).decode('utf-8')
            if not data_received:
                break
            try:
                destination_port_str, payload = data_received.split(':', 1)
                destination_port = int(destination_port_str)
                print(f"Server de la distanță: Forwarding către {SERVICE_HOST}:{destination_port} - {payload}")
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_to_service:
                    sock_to_service.connect((SERVICE_HOST, destination_port))
                    sock_to_service.sendall(payload.encode('utf-8'))
            except ValueError:
                print(f"Server de la distanță: Format de date invalid primit: {data_received}")
            except ConnectionRefusedError:
                print(f"Server de la distanță: Conexiune refuzată pe {SERVICE_HOST}:{destination_port}")
    except ConnectionResetError:
        print(f"Server de la distanță: Conexiune resetată de {client_address}")
    except Exception as e:
        print(f"Server de la distanță: Eroare în comunicare: {e}")
    finally:
        client_socket.close()
        print(f"Server de la distanță: Conexiune închisă cu {client_address}")

def start_remote_tunnel_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((REMOTE_HOST, REMOTE_PORT_TUNNEL))
        server_socket.listen()
        print(f"Serverul de tunelare de la distanță ascultă pe {REMOTE_HOST}:{REMOTE_PORT_TUNNEL}")
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_remote_connection, args=(client_socket, client_address))
            client_thread.start()

if __name__ == "__main__":
    start_remote_tunnel_server()