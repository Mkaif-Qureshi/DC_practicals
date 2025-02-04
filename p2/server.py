import grpc
import time
import random
from concurrent import futures
import converter_pb2
import converter_pb2_grpc
from registry import Registry  # Importing Registry

class ConverterServicer(converter_pb2_grpc.ConverterServicer):
    def ConvertServerStream(self, request, context):
        binary_representation = bin(request.number)[2:]
        for digit in binary_representation:
            yield converter_pb2.BinaryResponse(binary=digit)
            time.sleep(0.2)  # Simulate delay

    def ConvertClientStream(self, request_iterator, context):
        binary_results = []
        for request in request_iterator:
            binary_results.append(bin(request.number)[2:])
        return converter_pb2.BinaryResponse(binary=" ".join(binary_results))

    def ConvertBidirectional(self, request_iterator, context):
        for request in request_iterator:
            yield converter_pb2.BinaryResponse(binary=bin(request.number)[2:])

def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    converter_pb2_grpc.add_ConverterServicer_to_server(ConverterServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()

    # Register the server in the registry
    registry = Registry()
    registry.register(port)

    print(f"Server started on port {port}")
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print(f"Shutting down server on port {port}")
        registry.deregister(port)
        server.stop(0)

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 50051
    serve(port)
