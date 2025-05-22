import socket

LOCAL_TUNNEL_HOST = 'localhost'
LOCAL_TUNNEL_PORT = 12345
DESTINATION_PORT = 9090

def run_time_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((LOCAL_TUNNEL_HOST, LOCAL_TUNNEL_PORT))

        print("=== Client Time Chat ===")
        print("Client Time conectat. Așteptând mesaje de timp...")
        
        payload = f"{DESTINATION_PORT}:timp"
        s.sendall(payload.encode('utf-8'))
        
        try:
            while True:
                data = s.recv(1024)
                if not data:
                    break
                print(f"Timpul primit: {data.decode('utf-8')}")
        except Exception as e:
            print(f"Eroare: {e}")
        finally:
            print("Conexiune închisă.")

if __name__ == "__main__":
    run_time_client()