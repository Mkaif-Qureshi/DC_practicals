#!/usr/bin/env python3
import time
import logging
from concurrent import futures
import grpc
import converter_pb2
import converter_pb2_grpc
import sys

# Configure logging to include timestamps
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

def decimal_to_binary(num: int) -> str:
    """Converts an integer to its binary representation (as a string without the '0b' prefix)."""
    return bin(num)[2:]

class ConverterServicer(converter_pb2_grpc.ConverterServicer):
    def __init__(self, server_id: str):
        self.server_id = server_id

    def ServerStreamingConvert(self, request, context):
        """Server streaming RPC: streams one binary digit at a time."""
        binary_str = decimal_to_binary(request.number)
        logging.info(f"Server {self.server_id}: Received server streaming request for number {request.number} -> {binary_str}")
        # Stream each character with a small delay
        for ch in binary_str:
            response = converter_pb2.BinaryResponse(binary=ch, server_id=self.server_id)
            logging.info(f"Server {self.server_id}: Streaming response chunk: {ch}")
            time.sleep(0.5)
            yield response

    def ClientStreamingConvert(self, request_iterator, context):
        """Client streaming RPC: receives a stream of numbers and returns one combined binary string."""
        binaries = []
        for req in request_iterator:
            binary_str = decimal_to_binary(req.number)
            logging.info(f"Server {self.server_id}: Received number {req.number} -> {binary_str}")
            binaries.append(binary_str)
        # Combine the binary strings (separated by spaces)
        combined = ' '.join(binaries)
        logging.info(f"Server {self.server_id}: Sending combined response: {combined}")
        return converter_pb2.BinaryResponse(binary=combined, server_id=self.server_id)

    def BidirectionalStreamingConvert(self, request_iterator, context):
        """Bidirectional streaming RPC: for every request, immediately replies with its binary conversion."""
        for req in request_iterator:
            binary_str = decimal_to_binary(req.number)
            logging.info(f"Server {self.server_id}: Received number {req.number} -> {binary_str}")
            response = converter_pb2.BinaryResponse(binary=binary_str, server_id=self.server_id)
            logging.info(f"Server {self.server_id}: Sending response: {binary_str}")
            yield response

def serve(port: int, server_id: str):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    converter_pb2_grpc.add_ConverterServicer_to_server(ConverterServicer(server_id), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"Server {server_id} started on port {port}.")
    try:
        while True:
            time.sleep(86400)  # Keep server alive for one day intervals
    except KeyboardInterrupt:
        logging.info("Server stopping...")
        server.stop(0)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python server.py <port> <server_id>")
        sys.exit(1)
    port = int(sys.argv[1])
    server_id = sys.argv[2]
    serve(port, server_id)
