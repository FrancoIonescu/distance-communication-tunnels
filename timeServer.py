import socket
import threading
import time
from datetime import datetime

SERVICE_HOST = '127.0.0.1'
SERVICE_PORT = 9090  

def send_time_to_client(client_socket, client_address):
    print(f"Server de timp: Conexiune de la {client_address}")
    try:
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            message = f"Timpul curent este: {current_time}"
            client_socket.sendall(message.encode('utf-8'))
            print(f"Server de timp: Mesaj trimis către {client_address}: {message}")
            time.sleep(5)
    except ConnectionAbortedError:
        print(f"Server de timp: Conexiunea a fost închisă de clientul {client_address}")
    except socket.timeout:
        print(f"Server de timp: Timeout cu {client_address}")
    finally:
        client_socket.close()
        print(f"Server de timp: Conexiune închisă cu {client_address} la {datetime.now()}")

def start_time_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVICE_HOST, SERVICE_PORT))
        server_socket.listen()
        print(f"Serverul de timp ascultă pe {SERVICE_HOST}:{SERVICE_PORT}")
        
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                thread = threading.Thread(target=send_time_to_client, args=(client_socket, client_address))
                thread.daemon = True  
                thread.start()
            except Exception as e:
                print(f"Server de timp: Eroare la acceptarea unei noi conexiuni: {e}")

if __name__ == "__main__":
    start_time_server()
