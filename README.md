# 🔀 Distance Communication Tunnels

This project is about creating a simple communication tunnel using Python sockets. A message goes from the client to a local server, then to a remote server, and finally to the appropriate service, such as an echo service that replies with the same message. If the message is "time", the system connects to a time service to retrieve and return the current time.

## 📁 Project Structure

```plaintext
.
├── clientEcho.py           # Sends a message to the echo service
├── clientTime.py           # Sends a request for time to the time service
├── tunelLocalServer.py     # Forwards messages from the client to the remote tunnel server
├── tunelRemoteServer.py    # Sends messages to the final service (echo or time server)
├── echoServer.py           # Test service that replies with the same message received
└── timeServer.py           # Provides the current time to the client
```

## 🔧 Requirements

- Python 3.x
- No extra libraries

## 🚀 How It Works

1. **client.py**: sends a message (e.g., "hello" or "time")
2. **tunelLocalServer.py**: forwards the message to the remote tunnel server.
3. **tunelRemoteServer.py**: if it's "time", connects to timeServer; otherwise, to echoServer.
4. **echoServer.py**: replies with the same message it receives.
5. **timeServer.py**: sends the current time every minute.

## 🧪 How to Run

> Open **6 terminal windows**, and run these:

### 1. Start the Remote Tunnel Server

```bash
python tunelRemoteServer.py
```

### 2. Start the Local Tunnel Server

```bash
python tunelLocalServer.py
```

### 3. Start the Echo Server

```bash
python echoServer.py
```

### 4. Start the Time Server

```bash
python timeServer.py
```

### 5. Run the Client

```bash
python client.py
```

### 6. Run the Time Client

```bash
python timeClient.py
```

You can now type messages into the client. Based on the message content, the system will automatically determine which remote service you're trying to access. This demonstrates how the client connects to the local tunneling server, which in turn forwards the request through the only accessible port to the remote tunneling server. The remote server then connects to the appropriate service (such as the echo server or time server) based on the message.

For example, if you type a regular message, the system recognizes it as an echo request and forwards it to the echo server. If you type the word "time", it understands that you're requesting the current time and automatically connects to the time server to retrieve and return the time.

## 📄 License

This project is open-source and free to use for educational purposes.
