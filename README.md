# 🔀 Distance Communication Tunnels

This project is about creating a simple communication tunnel using Python sockets. A message goes from the client to a local server, then to a remote server, and finally to an echo service that replies with the same message.

## 📁 Project Structure

```plaintext
.
├── client.py               # Sends messages
├── tunelLocalServer.py     # Sends messages from client to remote server
├── tunelRemoteServer.py    # Sends messages to the final service
└── echoServer.py           # Test service that replies with the same message
```

## 🔧 Requirements

- Python 3.x
- No extra libraries

## 🚀 How It Works

1. **client.py**: sends a message.
2. **tunelLocalServer.py**: forwards it to the remote server.
3. **tunelRemoteServer.py**: reads the port and sends it to the service.
4. **echoServer.py**: replies with the same message it receives.

## 🧪 How to Run

> Open **4 terminal windows**, and run these:

### 1. Start the Echo Server

```bash
python echoServer.py
```

### 2. Start the Remote Tunnel Server

```bash
python tunelRemoteServer.py
```

### 3. Start the Local Tunnel Server

```bash
python tunelLocalServer.py
```

### 4. Run the Client

```bash
python client.py
```

You can now type messages in the client. You’ll get a reply from the echo service.

## 📄 License

This project is open-source and free to use for educational purposes.
