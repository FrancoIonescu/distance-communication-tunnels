import socket
import threading

REMOTE_HOST = '127.0.0.1'
REMOTE_PORT_TUNNEL = 54321
SERVICE_HOST = '127.0.0.1'
ECHO_PORT = 8080
TIME_PORT = 9090

def handle_remote_connection(client_socket, client_address):
    print(f"Server de la distanță: Conexiune de la {client_address}")
    try:
        while True:
            data_received = client_socket.recv(1024).decode('utf-8').strip()
            if not data_received:
                break

            if data_received.lower().startswith("timp"):
                destination_port = TIME_PORT
                print(f"Server de la distanță: Redirecționare către serviciul de timp ({SERVICE_HOST}:{destination_port}) - {data_received}")
            else:
                destination_port = ECHO_PORT
                print(f"Server de la distanță: Redirecționare către serviciul echo ({SERVICE_HOST}:{destination_port}) - {data_received}")

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_to_service:
                    sock_to_service.connect((SERVICE_HOST, destination_port))
                    sock_to_service.sendall(data_received.encode('utf-8'))
                    response = sock_to_service.recv(1024)
                    client_socket.sendall(response)
            except socket.error as e:
                print(f"Server de la distanță: Eroare de socket: {e}")
            except Exception as e:
                print(f"Server de la distanță: Eroare generală: {e}")

    except ConnectionResetError:
        print(f"Server de la distanță: Conexiune resetată de {client_address}")
    except socket.error as e:
        print(f"Server de la distanță: Eroare de rețea cu {client_address}: {e}")
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
