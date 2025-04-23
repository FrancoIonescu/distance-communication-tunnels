import socket

LOCAL_HOST = '127.0.0.1'
LOCAL_PORT_TUNNEL = 12345
DESTINATION_PORT = 9090

def run_time_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((LOCAL_HOST, LOCAL_PORT_TUNNEL))
            print("Client Timp: Conectat. Așteaptă răspunsuri periodice...")

            payload = f"{DESTINATION_PORT}:"
            client_socket.sendall(payload.encode('utf-8'))

            while True:
                response = client_socket.recv(1024)
                if not response:
                    print("Client Timp: Conexiune închisă de server.")
                    break
                print(f"Client Timp: {response.decode()}")
        except Exception as e:
            print(f"Client Timp: Eroare: {e}")

if __name__ == "__main__":
    run_time_client()
