# OmniStream - Architecture & Design Diagrams

This document contains a series of diagrams generated with Mermaid to visually represent the architecture, interactions, and design of the OmniStream gRPC project.

## Table of Contents
1.  [High-Level Architecture Diagram](#1-high-level-architecture-diagram)
2.  [C4 Component Diagram](#2-c4-component-diagram)
3.  [Sequence Diagrams](#3-sequence-diagrams)
    *   [User Service (Unary RPC)](#user-service-unary-rpc)
    *   [Event Service (Server Streaming RPC)](#event-service-server-streaming-rpc)
    *   [Chat Service (Bidirectional Streaming RPC)](#chat-service-bidirectional-streaming-rpc)
4.  [Class Diagram](#4-class-diagram)
5.  [Conceptual Entity Relationship Diagram](#5-conceptual-entity-relationship-diagram)
6.  [State Diagram (Chat Client Lifecycle)](#6-state-diagram-chat-client-lifecycle)


---

### 1. High-Level Architecture Diagram

This diagram provides a simple, high-level overview of the system's components and their primary interactions. It's useful for quickly understanding the overall structure.

```mermaid
graph TD
    subgraph Client-Side
        A[Client Application]
    end

    subgraph "Server-Side (Docker Network)"
        B["User Service (gRPC Unary)"]
        C["Event Service (gRPC Server-Streaming)"]
        D["Chat Service (gRPC Bidirectional-Streaming)"]
    end

    A -- "gRPC: GetUser" --> B
    A -- "gRPC: SubscribeToEvents" --> C
    A -- "gRPC: Chat Stream" --> D
```

### 2. C4 Component Diagram

The C4 model helps to describe a system at different levels of detail. This C2-level (Container/Component) diagram shows our services as running components within the OmniStream system boundary and how a client interacts with them.

```mermaid
C4Component
    title Component Diagram for OmniStream System

    Person(client_app, "Client Application", "A test script or future UI.")

    System_Boundary(omni_stream, "OmniStream gRPC Backend") {
        Component(user_service, "User Service", "Python/gRPC", "Manages user profiles. <br> [Unary RPC]")
        Component(event_service, "Event Service", "Python/gRPC", "Streams real-time game events. <br> [Server Streaming]")
        Component(chat_service, "Chat Service", "Python/gRPC", "Handles real-time, two-way chat. <br> [Bidirectional Streaming]")
    }

    Rel(client_app, user_service, "Requests user data", "gRPC")
    Rel(client_app, event_service, "Subscribes to game events", "gRPC")
    Rel(client_app, chat_service, "Opens a chat stream", "gRPC")
```

### 3. Sequence Diagrams

These diagrams show the step-by-step flow of messages for each of the three gRPC communication patterns.

#### User Service (Unary RPC)

This shows the simple request-response flow of getting a user's profile.

```mermaid
sequenceDiagram
    participant Client
    participant UserService

    Client->>UserService: GetUser(user_id: "1")
    activate UserService
    Note right of UserService: Fetch user data
    UserService-->>Client: User(id: "1", name: "Alice", ...)
    deactivate UserService

    Client->>UserService: GetUser(user_id: "99")
    activate UserService
    Note right of UserService: User not found
    UserService-->>Client: RpcError(StatusCode.NOT_FOUND)
    deactivate UserService
```

#### Event Service (Server Streaming RPC)

This illustrates the client making one request and the server sending back multiple messages over time.

```mermaid
sequenceDiagram
    participant Client
    participant EventService

    Client->>EventService: SubscribeToGameEvents(game_id: "game-123")
    activate EventService
    Note right of EventService: Subscription is active

    loop Stream of Events
        EventService-->>Client: stream GameEvent(event_id: "event-1", ...)
        Note right of EventService: Waits 2s
        EventService-->>Client: stream GameEvent(event_id: "event-2", ...)
        Note right of EventService: Waits 2s
        EventService-->>Client: stream GameEvent(event_id: "event-3", ...)
    end
    Note right of EventService: Server closes the stream
    deactivate EventService
```

#### Chat Service (Bidirectional Streaming RPC)

This diagram shows the concurrent, two-way flow of messages in the chat service.

```mermaid
sequenceDiagram
    participant Client
    participant ChatService

    Client->>ChatService: Establish Chat() Stream
    activate ChatService
    Note over Client, ChatService: Persistent connection is open

    par Client Sends Messages AND Server Responds
        Client->>ChatService: stream ChatMessage(user: "Chris", msg: "Hello!")
        ChatService-->>Client: stream ChatMessage(user: "Server", msg: "[Echo]: Hello!")
    and
        Client->>ChatService: stream ChatMessage(user: "Chris", msg: "How are you?")
        ChatService-->>Client: stream ChatMessage(user: "Server", msg: "[Echo]: How are you?")
    end

    Client->>ChatService: Client closes stream (e.g., sends 'quit')
    deactivate ChatService
```

### 4. Class Diagram

This diagram shows the key classes we implemented (`*Servicer`, `*Client`) and their relationships with the gRPC-generated stubs and message classes.

```mermaid
classDiagram
    direction LR

    class user_pb2_grpc.UserServiceServicer {
        <<Generated>>
        +GetUser()
    }
    class user_pb2_grpc.UserServiceStub {
        <<Generated>>
        +GetUser()
    }
    class user_pb2.User {
        <<Generated Message>>
    }

    class UserServiceServicer {
        +GetUser(request, context)
    }
    class user_client {
        +run_client()
    }

    user_pb2_grpc.UserServiceServicer <|-- UserServiceServicer
    UserServiceServicer ..> user_pb2.User : Returns
    user_client ..> user_pb2_grpc.UserServiceStub : Uses
```

### 5. Conceptual Entity Relationship Diagram

Since this project does not use a database, this ERD visualizes the primary data *entities* (our Protobuf messages) and their attributes in a conceptual way. It is **not** a database schema.

```mermaid
erDiagram
    USER {
        string user_id PK
        string name
        int32 level
    }

    GAME_EVENT {
        string event_id PK
        string description
        string timestamp
    }

    CHAT_MESSAGE {
        string user_id
        string message
        string timestamp
    }
```

### 6. State Diagram (Chat Client Lifecycle)

This diagram models the different states of the interactive chat client, from connecting to disconnecting.

```mermaid
stateDiagram-v2
    [*] --> Disconnected

    Disconnected --> Connecting: run_client()
    Connecting --> Chatting: Connection Established
    Connecting --> Disconnected: Connection Failed

    Chatting --> Chatting: Receive Message
    Chatting --> Disconnecting: User types 'quit'
    Chatting --> Disconnecting: RPC Error

    Disconnecting --> Disconnected: Stream Closed
```
