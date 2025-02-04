import grpc
from concurrent import futures
import binary_converter_pb2
import binary_converter_pb2_grpc

# Define the service implementation
class BinaryConverterServicer(binary_converter_pb2_grpc.BinaryConverterServicer):
    def ConvertToBinary(self, request, context):
        print(f"Server received number: {request.number}")
        binary_representation = bin(request.number)[2:]  # Convert to binary and remove '0b' prefix
        print(f"Server sending binary: {binary_representation}")
        return binary_converter_pb2.BinaryResponse(binary=binary_representation)

def serve():
    print("Starting server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    binary_converter_pb2_grpc.add_BinaryConverterServicer_to_server(BinaryConverterServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Server is running on port 50051")
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Server shutting down...")

if __name__ == "__main__":
    serve()
