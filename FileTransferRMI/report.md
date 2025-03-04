## Overview

The project implements a file transfer system using Java RMI (Remote Method Invocation) to allow remote communication between clients and a centralized server. It supports both large and small file transfers by selecting either a persistent or transient communication mode. Additionally, it is designed with stateful session management so that interrupted transfers can be resumed and to ensure secure, authenticated operations.

---

## Key Components and Their Roles

### 1. Client Module

**FileTransferClient:**

- **Purpose:** Acts as the primary entry point for the client application.
- **Responsibilities:**
  - Provides a command-line interface (CMD-based) that prompts the user for actions like file upload or download.
  - Looks up the remote service from the RMI Registry.
  - Delegates file transfer operations to either persistent or transient transfer strategies based on file size.

**SessionManager:**

- **Purpose:** Manages session data on the client side.
- **Responsibilities:**
  - Keeps track of active sessions, which is critical when transfers are interrupted.
  - Provides the capability to resume file transfers without starting from scratch.

**PersistentTransfer & TransientTransfer:**

- **Purpose:** Provide two modes of file transfer.
- **PersistentTransfer:**
  - Designed for large files.
  - Splits the file into chunks and ensures that if a transfer is interrupted, it can resume from the last successful chunk.
- **TransientTransfer:**
  - Used for small files where a quick, one-shot transfer is sufficient.
  - Initiates a temporary session that doesn’t maintain prolonged state.

**Configurations:**

- **Purpose:** Houses configurable parameters such as timeout values and file size thresholds.
- **Responsibilities:**
  - Determines whether the file should be transferred persistently or transiently based on its size.

---

### 2. Server Module

**FileTransferService (Singleton):**

- **Purpose:** Implements the core remote service methods for file transfers.
- **Key Characteristics:**
  - **Singleton Pattern:** Ensures that only one instance handles all requests, simplifying synchronization and resource management.
  - **Methods:**
    - `downloadFile(fileName)`: Reads a file from the server’s file system and returns its content as a byte array.
    - `uploadFile(fileName, fileData)`: Writes the uploaded data to the server’s file system.

**SessionTracker:**

- **Purpose:** Tracks active file transfer sessions on the server.
- **Responsibilities:**
  - Monitors which transfers are in progress.
  - Helps enforce access controls and manage the state for resuming transfers if needed.

**MultiThreadHandler:**

- **Purpose:** Enables concurrent handling of client requests.
- **Responsibilities:**
  - Wraps tasks in a Runnable, ensuring that multiple client operations can be processed in parallel, improving overall throughput.

**TimeoutManager:**

- **Purpose:** Manages the timeout settings for file transfers.
- **Responsibilities:**
  - Prevents processes from hanging indefinitely during slow or failed transfers.
  - Provides the possibility to set adaptive timeouts based on the context (like file size or network latency).

**CommunicationMode:**

- **Purpose:** Offers flexibility in switching between persistent and transient communication.
- **Responsibilities:**
  - Ensures that the correct transfer strategy is employed based on the file size or the network condition.

**CachingModule (Planned/Placeholder):**

- **Purpose:** Indicates a future enhancement for caching replies of idempotent remote procedures.
- **Responsibilities:**
  - Aims to reduce server load by storing responses of repetitive requests.
  - Although not fully implemented, it sets the stage for performance optimization.

---

### 3. Common Layer

**RemoteInterfaces:**

- **Purpose:** Defines the contract between the client and the server.
- **Responsibilities:**
  - Declares remote methods such as `downloadFile` and `uploadFile`.
  - Ensures that both the client and server adhere to a standardized communication protocol.

**FileChunk, FileMetadata, SystemConstants:**

- **FileChunk:**
  - Represents a portion of a file. Useful for chunked transfers in persistent mode.
- **FileMetadata:**
  - Holds details about the file (e.g., file name, file size).
- **SystemConstants:**
  - Contains global constants such as default timeouts and the chunk size used for splitting large files.

---

### 4. Build, Deployment, and Testing

**Build Scripts:**

- **build.cmd:**
  - Compiles all Java source files for the client, server, and common modules.
  - Organizes the compiled classes into respective `bin` directories.
- **deploy.cmd:**
  - Prepares the environment for deployment, sets up classpaths, or performs other necessary configuration steps.

**CMD-based Start-up Scripts:**

- **startServer.cmd:**
  - Initiates the RMI Registry and starts the FileTransferService.
- **startClient.cmd:**
  - Launches the client application that connects to the server.

**Test Suites:**

- **ClientTestSuite, ServerTestSuite, Integration Tests:**
  - Validate individual components as well as the overall integration between client and server.
  - Ensure that file uploads, downloads, and session management function as expected.

---

## Overall Flow and Communication

1. **Client Initialization:**

   - A physical client (via CMD) starts and creates an instance of `FileTransferClient`.
   - It also instantiates `SessionManager` to manage file transfer sessions.

2. **RMI Setup:**

   - The client uses the RMI registry (on default port 1099) to look up the `FileTransferService` remote object.
   - The `FileTransferService` is a singleton on the server, ensuring all requests are handled centrally.

3. **File Transfer Operation:**

   - When a user initiates a file upload or download, the client first determines the size of the file.
   - Based on the size, it either uses `PersistentTransfer` (for large files) or `TransientTransfer` (for small files).
   - The chosen transfer module reads the file (or its chunks) and calls the corresponding remote method (`uploadFile` or `downloadFile`) via RMI.

4. **Server Processing:**

   - Upon receiving a request, the server’s `FileTransferService` processes it.
   - For uploads, the service writes the file data to the server’s file system; for downloads, it reads the file and returns the data.
   - The server uses `MultiThreadHandler` to handle multiple simultaneous requests.

5. **Session and Timeout Management:**

   - Both client and server maintain session data. This allows for resuming interrupted transfers.
   - The `TimeoutManager` ensures that operations do not hang indefinitely.

6. **Response and User Feedback:**
   - The server returns a success or failure status through the RMI stub.
   - The client then provides feedback to the user and, if necessary, updates session status.

---

## Conclusion

This project demonstrates a robust design for a file transfer system using Java RMI. Its key strengths include:

- **Stateful Transfers:** Allowing for interruption recovery and session management.
- **Dual Transfer Modes:** Optimized strategies for both small and large files.
- **Singleton Server Design:** Simplifies concurrency and resource management.
- **Scalability Considerations:** With multi-threaded request handling and placeholders for caching and load balancing.

Each component—from the client’s interactive file selection to the server’s efficient file handling—plays a crucial role in ensuring reliable, scalable, and secure file transfers. The overall architecture, as depicted in our diagrams and described above, provides a clear blueprint for further enhancements and real-world deployment.
