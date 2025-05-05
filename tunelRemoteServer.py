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
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            if ':' in data:
                port_str, msg = data.split(':', 1)
                try:
                    destination_port = int(port_str)
                except ValueError:
                    destination_port = ECHO_PORT
                    msg = data
            else:
                destination_port = ECHO_PORT
                msg = data

            print(f"Server de la distanță: Redirecționare către serviciul de la {SERVICE_HOST}:{destination_port} - {msg}")
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as svc_sock:
                    svc_sock.connect((SERVICE_HOST, destination_port))
                    svc_sock.sendall(msg.encode('utf-8'))
                    response = svc_sock.recv(1024)
                    client_socket.sendall(response)
            except Exception as e:
                print(f"Server de la distanță: Eroare conectare la serviciu: {e}")

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
            threading.Thread(target=handle_remote_connection, args=(client_socket, client_address), daemon=True).start()

if __name__ == "__main__":
    start_remote_tunnel_server()
