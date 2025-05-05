import socket
import threading

LOCAL_TUNNEL_HOST = '127.0.0.1'
LOCAL_TUNNEL_PORT = 12345
DESTINATION_PORT = 10000

def receive_messages(sock):
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode('utf-8'))
    except Exception as e:
        print(f"Eroare primire: {e}")
    finally:
        print("Conexiune închisă.")


def run_client_broadcast():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((LOCAL_TUNNEL_HOST, LOCAL_TUNNEL_PORT))
        print("Client Broadcast conectat. Tastează mesaje (scrie 'exit' pentru a ieși):")
        threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

        while True:
            msg = input()
            if msg.lower() == 'exit':
                break
            payload = f"{DESTINATION_PORT}:{msg}"
            s.sendall(payload.encode('utf-8'))

if __name__ == "__main__":
    run_client_broadcast()
