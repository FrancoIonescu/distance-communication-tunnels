import socket
import threading

SERVICE_HOST = '127.0.0.1'
SERVICE_PORT = 8080  

def handle_service(client_socket, client_address):
    print(f"Server de serviciu (Echo): Conexiune de la {client_address}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Server de serviciu (Echo): Primit: {data.decode()}")
            client_socket.sendall(f"Ai trimis: {data.decode()}".encode('utf-8'))
    except ConnectionResetError:
        print(f"Server de serviciu (Echo): Conexiune resetată de {client_address}")
    except Exception as e:
        print(f"Server de serviciu (Echo): Eroare: {e}")
    finally:
        client_socket.close()
        print(f"Server de serviciu (Echo): Conexiune închisă cu {client_address}")

def start_echo_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVICE_HOST, SERVICE_PORT))
        server_socket.listen()
        print(f"Serverul de serviciu (Echo) ascultă pe {SERVICE_HOST}:{SERVICE_PORT}")
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_service, args=(client_socket, client_address))
            client_thread.start()

if __name__ == "__main__":
    start_echo_server()