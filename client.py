import socket

LOCAL_HOST = '127.0.0.1'
LOCAL_PORT_TUNNEL = 12345

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((LOCAL_HOST, LOCAL_PORT_TUNNEL))
            while True:
                message = input("Introduceți mesajul: (scrie 'exit' pentru a ieși): ")
                if message.lower() == 'exit':
                    print("Client: Conexiune închisă.")
                    break
                client_socket.sendall(message.encode('utf-8'))
                response = client_socket.recv(1024)
                if not response:
                    print("Client: Conexiune închisă de server.")
                    break
                print(f"Client: Răspuns primit: {response.decode()}")
        except ConnectionRefusedError:
            print(f"Client: Nu s-a putut conecta la {LOCAL_HOST}:{LOCAL_PORT_TUNNEL}")
        except Exception as e:
            print(f"Client: Eroare: {e}")

if __name__ == "__main__":
    run_client()
