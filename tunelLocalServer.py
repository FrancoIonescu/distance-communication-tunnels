import socket
import threading

LOCAL_HOST = '127.0.0.1'
LOCAL_PORT_TUNNEL = 12345
REMOTE_HOST = '127.0.0.1'
REMOTE_PORT_TUNNEL = 54321

def handle_client(client_socket, client_address):
    print(f"Conexiune de la {client_address}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            destination_port = 8080
            payload = f"{destination_port}:{data.decode()}".encode('utf-8')
            print(f"Server local: Redirecționare către {REMOTE_HOST}:{REMOTE_PORT_TUNNEL} - {payload.decode()}")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_to_remote:
                sock_to_remote.connect((REMOTE_HOST, REMOTE_PORT_TUNNEL))
                sock_to_remote.sendall(payload)
                response = sock_to_remote.recv(1024)
                client_socket.sendall(response)
    except ConnectionResetError:
        print(f"Conexiune resetată de clientul {client_address}")
    except Exception as e:
        print(f"Eroare în comunicarea cu clientul {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Conexiune închisă cu {client_address}")

def start_local_tunnel_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((LOCAL_HOST, LOCAL_PORT_TUNNEL))
        server_socket.listen()
        print(f"Serverul de tunelare local ascultă pe {LOCAL_HOST}:{LOCAL_PORT_TUNNEL}")
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

if __name__ == "__main__":
    start_local_tunnel_server()