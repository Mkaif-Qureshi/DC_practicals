import grpc
import converter_pb2
import converter_pb2_grpc

def server_streaming_call(stub):
    number = input("Enter a decimal number for server streaming: ")
    if not number.isdigit():
        print("Invalid number! Please enter a valid decimal.")
        return
    request = converter_pb2.DecimalRequest(number=int(number))
    print("Server streaming response:")
    for response in stub.ConvertServerStream(request):
        print("Received binary digit:", response.binary)

def client_streaming_call(stub):
    print('Enter decimal numbers one by one (type "done" to send):')
    numbers = []
    while True:
        number = input()
        if number.lower() == 'done':
            break
        if number.isdigit():
            numbers.append(converter_pb2.DecimalRequest(number=int(number)))
        else:
            print("Invalid number! Enter a valid decimal or type 'done'.")

    response = stub.ConvertClientStream(iter(numbers))
    print("Client streaming response:", response.binary)

def bidirectional_streaming_call(stub):
    def request_generator():
        print('Enter decimal numbers for bidirectional streaming (type "done" to stop):')
        while True:
            number = input()
            if number.lower() == 'done':
                break
            if number.isdigit():
                yield converter_pb2.DecimalRequest(number=int(number))
            else:
                print("Invalid number! Enter a valid decimal or type 'done'.")

    responses = stub.ConvertBidirectional(request_generator())
    for response in responses:
        print("Received binary:", response.binary)

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = converter_pb2_grpc.ConverterStub(channel)

    while True:
        print("\nSelect RPC type:")
        print("1. Server Streaming")
        print("2. Client Streaming")
        print("3. Bidirectional Streaming")
        print("Q. Quit")
        choice = input("Enter choice: ").strip().lower()

        if choice == '1':
            server_streaming_call(stub)
        elif choice == '2':
            client_streaming_call(stub)
        elif choice == '3':
            bidirectional_streaming_call(stub)
        elif choice == 'q':
            print("Exiting...")
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
