// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('@grpc/grpc-js');
var binary_converter_pb = require('./binary_converter_pb.js');

function serialize_binaryconverter_BinaryRequest(arg) {
  if (!(arg instanceof binary_converter_pb.BinaryRequest)) {
    throw new Error('Expected argument of type binaryconverter.BinaryRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_binaryconverter_BinaryRequest(buffer_arg) {
  return binary_converter_pb.BinaryRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_binaryconverter_BinaryResponse(arg) {
  if (!(arg instanceof binary_converter_pb.BinaryResponse)) {
    throw new Error('Expected argument of type binaryconverter.BinaryResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_binaryconverter_BinaryResponse(buffer_arg) {
  return binary_converter_pb.BinaryResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


// The service definition
var BinaryConverterService = exports.BinaryConverterService = {
  // Unary RPC
convertToBinary: {
    path: '/binaryconverter.BinaryConverter/ConvertToBinary',
    requestStream: false,
    responseStream: false,
    requestType: binary_converter_pb.BinaryRequest,
    responseType: binary_converter_pb.BinaryResponse,
    requestSerialize: serialize_binaryconverter_BinaryRequest,
    requestDeserialize: deserialize_binaryconverter_BinaryRequest,
    responseSerialize: serialize_binaryconverter_BinaryResponse,
    responseDeserialize: deserialize_binaryconverter_BinaryResponse,
  },
};

exports.BinaryConverterClient = grpc.makeGenericClientConstructor(BinaryConverterService);
