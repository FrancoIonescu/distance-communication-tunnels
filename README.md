# 🔀 Distance Communication Tunnels

This project is about creating a simple communication tunnel using Python sockets. A message goes from the client to a local server, then to a remote server, and finally to the appropriate service, such as an echo service that replies with the same message. If the message is "time", the system connects to a time service to retrieve and return the current time.

## 📁 Project Structure

```plaintext
.
├── clientEcho.py           # Sends a message to the echo service
├── clientTime.py           # Sends a request for time to the time service
├── clientBroadcast.py      # Sends and receives broadcast messages from the broadcast server
├── broadcastServer.py      # Sends messages to all connected broadcast clients
├── tunelLocalServer.py     # Forwards messages from the client to the remote tunnel server
├── tunelRemoteServer.py    # Sends messages to the final service (echo, time or broadcast server)
├── echoServer.py           # Test service that replies with the same message received
└── timeServer.py           # Provides the current time to the client
```

## 🔧 Requirements

- Python 3.x
- No extra libraries

## 🚀 How It Works

1. **client.py**: sends a message (e.g., "hello" for Echo Server, "9090:time" for Time Server and "10000:hello" for Broadcast Server)
2. **clientTime.py**: connects to the time service, receiving every minute the local time.
3. **clientBroadcast.py**: connects to the broadcast service, sends messages, and listens for messages from other clients.
4. **serverTunelLocal.py**: forwards the message to the remote tunnel server.
5. **serverTunelRemote.py**: if the message starts with a known port prefix (e.g. `9090:`, `10000:`), it forwards the message to the corresponding service (time or broadcast). Otherwise, it defaults to the echo service.
6. **serverEcho.py**: replies with the same message it receives.
7. **serverTime.py**: sends the current time every minute.
8. **serverBroadcast.py**: receives a message from any client and broadcasts it to all other connected clients.


## 🧪 How to Run

> Open **8 terminals**, and run these:

### 1. Start the Remote Tunnel Server

```bash
python serverTunelRemote.py
```

### 2. Start the Local Tunnel Server

```bash
python serverTunelLocal.py
```

### 3. Start the Echo Server

```bash
python serverEcho.py
```

### 4. Start the Time Server

```bash
python serverTime.py
```

### 5. Start the Broadcast Server

```bash
python serverBroadcast.py
```

### 6. Run the General Client

```bash
python client.py
```

### 7. Run the Time Client
```bash
python clientTime.py
```

### 8. Run the Broadcast Client (you can open multiple)
```bash
python clientBroadcast.py
```

You can now type messages into the client. Based on the message content, the system will automatically determine which remote service you're trying to access. This demonstrates how the client connects to the local tunneling server, which in turn forwards the request through the only accessible port to the remote tunneling server. The remote server then connects to the appropriate service (such as the echo, time or broadcast server) based on the message.

For example, if you type a regular message, the system recognizes it as an echo request and forwards it to the echo server. If the message is prefixed with 9090:, it understands that you're requesting the current time and automatically connects to the time server to retrieve and return the time. If the message is prefixed with 10000:, it will be routed to the broadcast server.


## 📄 License

This project is open-source and free to use for educational purposes.
