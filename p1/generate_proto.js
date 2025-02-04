const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

// Load the proto file
const packageDefinition = protoLoader.loadSync('binary_converter.proto', {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
});

// Load the gRPC package
const binaryConverterProto = grpc.loadPackageDefinition(packageDefinition).binary_converter;

module.exports = binaryConverterProto;
