import grpc
import binary_converter_pb2
import binary_converter_pb2_grpc

def run():
    print("Client is starting...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = binary_converter_pb2_grpc.BinaryConverterStub(channel)
        number = int(input("Enter a decimal number: "))
        print(f"Client sending number: {number}")
        response = stub.ConvertToBinary(binary_converter_pb2.BinaryRequest(number=number))
        print(f"Client received binary representation: {response.binary}")

if __name__ == "__main__":
    run()
