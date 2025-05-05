import socket
import threading

SERVICE_HOST = '127.0.0.1'
SERVICE_PORT = 10000

clients = []
clients_lock = threading.Lock()

def broadcast(message, sender_socket=None):
    with clients_lock:
        for client in clients:
            if client is not sender_socket:
                try:
                    client.sendall(message.encode('utf-8'))
                except Exception:
                    pass


def handle_client(client_socket, client_address):
    print(f"Broadcast Service: Conexiune nouă de la {client_address}")
    with clients_lock:
        clients.append(client_socket)
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            text = data.decode('utf-8')
            print(f"Broadcast Service: Mesaj de la {client_address}: {text}")
            broadcast(f"{client_address}: {text}", sender_socket=client_socket)
    except Exception as e:
        print(f"Broadcast Service: Eroare cu {client_address}: {e}")
    finally:
        with clients_lock:
            clients.remove(client_socket)
        client_socket.close()
        print(f"Broadcast Service: Conexiune închisă cu {client_address}")


def start_broadcast_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((SERVICE_HOST, SERVICE_PORT))
        server.listen()
        print(f"Broadcast Server ascultă pe {SERVICE_HOST}:{SERVICE_PORT}")
        while True:
            client_sock, client_addr = server.accept()
            threading.Thread(target=handle_client, args=(client_sock, client_addr), daemon=True).start()

if __name__ == "__main__":
    start_broadcast_server()
