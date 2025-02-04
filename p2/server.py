from concurrent import futures
import grpc
import time
import logging
import converter_pb2
import converter_pb2_grpc

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ConverterServicer(converter_pb2_grpc.ConverterServicer):
    # Server streaming RPC: stream each binary digit.
    def ConvertServerStream(self, request, context):
        logging.info(f"Received Server Stream request: {request.number}")
        binary = bin(request.number)[2:]  # remove the '0b' prefix
        for digit in binary:
            logging.info(f"Streaming binary digit: {digit}")
            yield converter_pb2.BinaryResponse(binary=digit)
            time.sleep(0.5)  # simulate a delay for streaming

    # Client streaming RPC: accumulate requests and return a single response.
    def ConvertClientStream(self, request_iterator, context):
        binaries = []
        for req in request_iterator:
            logging.info(f"Received Client Stream request: {req.number}")
            binaries.append(bin(req.number)[2:])
        result = ','.join(binaries)
        logging.info(f"Returning combined binary response: {result}")
        return converter_pb2.BinaryResponse(binary=result)

    # Bidirectional streaming RPC: for each request, respond immediately.
    def ConvertBidirectional(self, request_iterator, context):
        for req in request_iterator:
            logging.info(f"Received Bidirectional request: {req.number}")
            binary = bin(req.number)[2:]
            logging.info(f"Sending binary response: {binary}")
            yield converter_pb2.BinaryResponse(binary=binary)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    converter_pb2_grpc.add_ConverterServicer_to_server(ConverterServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Server started on port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        logging.info("Shutting down server...")
        server.stop(0)

if __name__ == '__main__':
    serve()
