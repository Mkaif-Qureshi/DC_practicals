#!/usr/bin/env python3
import grpc
import converter_pb2
import converter_pb2_grpc
import time
import itertools

# List of available server addresses (simulate a registry)
SERVER_ADDRESSES = [
    'localhost:50051',
    'localhost:50052',
    'localhost:50053',
]

# Create a round-robin iterator for load balancing among the servers.
server_cycle = itertools.cycle(SERVER_ADDRESSES)
MAX_RETRIES = 3  # Maximum number of attempts per RPC call

def get_channel():
    """Returns a new gRPC channel to the next server in the registry."""
    address = next(server_cycle)
    print(f"Connecting to server at {address}")
    return grpc.insecure_channel(address)

def rpc_call_with_retry(rpc_function, *args, **kwargs):
    """
    Wraps an RPC call with retry logic. If one server is down (or an error occurs),
    it automatically tries the next server in the round-robin list.
    """
    attempts = 0
    while attempts < MAX_RETRIES:
        channel = get_channel()
        stub = converter_pb2_grpc.ConverterStub(channel)
        try:
            # Call the provided RPC function using the stub.
            return rpc_function(stub, *args, **kwargs)
        except grpc.RpcError as e:
            print(f"Error calling RPC on server: {e}")
            attempts += 1
            print(f"Retrying with a different server (attempt {attempts}/{MAX_RETRIES})...")
            time.sleep(0.5)
    print("All attempts failed. Please try again later.")
    return None

def run_server_streaming(decimal_number):
    print("\n--- Server Streaming RPC ---")
    def server_streaming_call(stub, number):
        request = converter_pb2.DecimalRequest(number=number)
        responses = stub.ServerStreamingConvert(request)
        result = ""
        for response in responses:
            print(f"Received chunk: {response.binary} (from server {response.server_id})")
            result += response.binary
        print(f"Final binary: {result}")
    rpc_call_with_retry(server_streaming_call, decimal_number)

def run_client_streaming(decimal_numbers):
    print("\n--- Client Streaming RPC ---")
    def client_streaming_call(stub, numbers):
        def request_generator():
            for num in numbers:
                print(f"Sending number: {num}")
                yield converter_pb2.DecimalRequest(number=num)
                time.sleep(0.3)  # simulate delay
        response = stub.ClientStreamingConvert(request_generator())
        print(f"Received combined response: {response.binary} (from server {response.server_id})")
    rpc_call_with_retry(client_streaming_call, decimal_numbers)

def run_bidirectional_streaming(decimal_numbers):
    print("\n--- Bidirectional Streaming RPC ---")
    def bidirectional_streaming_call(stub, numbers):
        def request_generator():
            for num in numbers:
                print(f"Sending number: {num}")
                yield converter_pb2.DecimalRequest(number=num)
                time.sleep(0.3)  # simulate delay
        responses = stub.BidirectionalStreamingConvert(request_generator())
        for response in responses:
            print(f"Received response: {response.binary} (from server {response.server_id})")
    rpc_call_with_retry(bidirectional_streaming_call, decimal_numbers)

def get_single_number():
    """Prompts the user for a single number and returns it as an integer."""
    while True:
        try:
            num = int(input("Enter a decimal number: "))
            return num
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_number_list():
    """Prompts the user for a list of numbers (comma-separated) and returns a list of integers."""
    while True:
        try:
            nums_str = input("Enter decimal numbers separated by commas (e.g., 12,7,255): ")
            numbers = [int(x.strip()) for x in nums_str.split(",") if x.strip()]
            if numbers:
                return numbers
            else:
                print("Please enter at least one number.")
        except ValueError:
            print("Invalid input. Please ensure all entries are integers.")

def main():
    print("Choose the type of RPC:")
    print("1. Server Streaming RPC")
    print("2. Client Streaming RPC")
    print("3. Bidirectional Streaming RPC")
    
    choice = input("Enter your choice (1/2/3): ").strip()
    
    if choice == "1":
        num = get_single_number()
        run_server_streaming(num)
    elif choice == "2":
        numbers = get_number_list()
        run_client_streaming(numbers)
    elif choice == "3":
        numbers = get_number_list()
        run_bidirectional_streaming(numbers)
    else:
        print("Invalid choice. Please run the program again and select 1, 2, or 3.")

if __name__ == '__main__':
    main()
