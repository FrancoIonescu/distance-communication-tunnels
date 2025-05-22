import socket
import threading
import sys
import os

LOCAL_HOST = 'localhost'
LOCAL_PORT_TUNNEL = 12345

def receive_messages(client_socket):
    while True:
        try:
            response = client_socket.recv(1024)
            if not response:
                print("\nClient: Conexiune închisă de server.")
                break
            
            if os.name == 'nt': 
                print('\r' + ' ' * 60 + '\r', end='', flush=True)
            else:  
                print('\r\033[K', end='', flush=True)
            print(f"Client: Mesaj primit: {response.decode()}")
            
            sys.stdout.write("Introduceți mesajul: (scrie 'exit' pentru a ieși): ")
            sys.stdout.flush()
        except Exception as e:
            print(f"\nClient: Eroare la recepționarea mesajului: {e}")
            break

def run_client():
    print("=== Client Chat ===")
    print(f"Conectare la {LOCAL_HOST}:{LOCAL_PORT_TUNNEL}...")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((LOCAL_HOST, LOCAL_PORT_TUNNEL))
            print("Conectat cu succes!")
            
            threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
            
            sys.stdout.write("Introduceți mesajul: (scrie 'exit' pentru a ieși): ")
            sys.stdout.flush()
            
            while True:
                message = sys.stdin.readline().strip()
                if message.lower() == 'exit':
                    print("Client: Conexiune închisă.")
                    break
                
                client_socket.sendall(message.encode('utf-8'))
                
                sys.stdout.write("Introduceți mesajul: (scrie 'exit' pentru a ieși): ")
                sys.stdout.flush()
                
        except ConnectionRefusedError:
            print(f"Client: Nu s-a putut conecta la {LOCAL_HOST}:{LOCAL_PORT_TUNNEL}")
        except Exception as e:
            print(f"Client: Eroare: {e}")

if __name__ == "__main__":
    try:
        run_client()
    except KeyboardInterrupt:
        print("\nClient închis.")