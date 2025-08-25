# OmniStream

A Python project demonstrating Unary, Server-Streaming, and Bidirectional gRPC patterns through a practical microservices backend.

## Core Concepts Demonstrated

This project implements three distinct microservices, each showcasing a primary gRPC use case:

1.  **👤 User Service (Unary RPC)**
    *   A simple request/response pattern.
    *   The client sends a request for a user, and the server returns a single user object.

2.  **🎮 Event Service (Server Streaming RPC)**
    *   A one-to-many data push pattern.
    *   The client subscribes to a game's event feed, and the server streams multiple event messages back over time.

3.  **💬 Chat Service (Bidirectional Streaming RPC)**
    *   A fully interactive, two-way communication pattern.
    *   The client and server open a persistent connection and can send messages to each other asynchronously.

## Tech Stack

*   **Language:** Python 3.12
*   **RPC Framework:** gRPC & Protocol Buffers
*   **Containerization:** Docker & Docker Compose
*   **Package Management:** `uv`

---

## Getting Started

Follow these steps to get the project running.

### 1. Clone the Repository

```bash
git clone https://github.com/zhu-weijie/omni-stream.git
cd omni-stream
```

### 2. Generate Protobuf Code

The Python gRPC code is generated from the `.proto` files. This command runs the protoc compiler inside a Docker container, ensuring the correct environment and dependencies are used.

```bash
docker compose run --rm user_service ./scripts/generate_protos.sh
```

### 3. Running the Services

You can run and test each service independently.

#### Testing the User Service (Unary)

```bash
# In your terminal, start the user service in the background
docker compose up -d user_service

# Run the client to make a request
docker compose run --rm user_service python clients/user_client.py

# Stop the service when you're done
docker compose down
```

#### Testing the Event Service (Server Streaming)

```bash
# Start the event service in the background
docker compose up -d event_service

# Run the client to subscribe to the event stream
docker compose run --rm event_service python clients/event_client.py

# Stop the service
docker compose down
```

#### Testing the Chat Service (Bidirectional Streaming)

This requires two terminals.

**In Terminal 1 (Server):**
```bash
# Start the chat service in the foreground to see live logs
docker compose up chat_service
```

**In Terminal 2 (Client):**
```bash
# Run the interactive client
docker compose run --rm -it chat_service python clients/chat_client.py

# You will be prompted for your name.
# Type messages and press Enter. Type 'quit' to exit.
```

When you are finished, press `Ctrl+C` in Terminal 1 and then run `docker compose down` to clean up.
