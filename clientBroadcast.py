import socket
import threading

LOCAL_TUNNEL_HOST = 'localhost'
LOCAL_TUNNEL_PORT = 12345
DESTINATION_PORT = 10000

def receive_messages(sock):
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            print(f"\n📩 Mesaj primit: {data.decode('utf-8')}\n> Introduceti un mesaj: ", end="")
    except Exception as e:
        print(f"Eroare primire: {e}")
    finally:
        print("Conexiune închisă.")


def run_client_broadcast():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((LOCAL_TUNNEL_HOST, LOCAL_TUNNEL_PORT))
    
        init_payload = f"{DESTINATION_PORT}:"
        s.sendall(init_payload.encode('utf-8'))

        print("=== Client Broadcast Chat ===")
        print("Client Broadcast conectat.")
        
        threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

        while True:
            msg = input("> Introduceti un mesaj: ")
            if msg.lower() == 'exit':
                print("Client: Conexiune închisă.")
                break
            payload = f"{msg}"
            s.sendall(payload.encode('utf-8'))

if __name__ == "__main__":
    run_client_broadcast()
