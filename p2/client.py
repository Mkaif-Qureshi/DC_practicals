import grpc
import random
import time
import converter_pb2
import converter_pb2_grpc
from registry import Registry

def get_available_server():
    registry = Registry()
    servers = registry.get_servers()
    if not servers:
        raise Exception("No available servers found.")
    return random.choice(servers)  # Load balancing: pick a random server

def server_streaming(stub, port):
    number = int(input("Enter decimal number for server streaming: "))
    print(f"Connecting to server on port {port}...")
    response_stream = stub.ConvertServerStream(converter_pb2.DecimalRequest(number=number))
    print("Binary Representation (streamed):", end=" ")
    for response in response_stream:
        print(response.binary, end=" ", flush=True)
        time.sleep(0.5)  # Simulate streaming delay
    print("\n")

def client_streaming(stub, port):
    print(f"Connecting to server on port {port}...")
    print("Enter decimal numbers (type 'q' to stop):")
    requests = []
    while True:
        user_input = input("Enter number: ")
        if user_input.lower() == 'q':
            break
        try:
            requests.append(converter_pb2.DecimalRequest(number=int(user_input)))
        except ValueError:
            print("Invalid input, enter a valid number.")
    
    response = stub.ConvertClientStream(iter(requests))
    print(f"Client Streaming Response from server {port}: {response.binary}")

def bidirectional_streaming(stub, port):
    def request_generator():
        print(f"Connecting to server on port {port}...")
        print("Enter decimal numbers (type 'q' to stop):")
        while True:
            user_input = input("Enter number: ")
            if user_input.lower() == 'q':
                return
            try:
                yield converter_pb2.DecimalRequest(number=int(user_input))
            except ValueError:
                print("Invalid input, enter a valid number.")
    
    response_stream = stub.ConvertBidirectional(request_generator())
    print(f"Bidirectional Stream Responses from server {port}:")
    for response in response_stream:
        print(response.binary)

def run():
    port = get_available_server()
    channel = grpc.insecure_channel(f'localhost:{port}')
    stub = converter_pb2_grpc.ConverterStub(channel)
    
    while True:
        print("\nSelect an option:")
        print("1. Client Streaming")
        print("2. Server Streaming")
        print("3. Bidirectional Streaming")
        print("q. Quit")
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            client_streaming(stub, port)
        elif choice == '2':
            server_streaming(stub, port)
        elif choice == '3':
            bidirectional_streaming(stub, port)
        elif choice.lower() == 'q':
            print("Exiting client.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 'q'.")

if __name__ == '__main__':
    run()
