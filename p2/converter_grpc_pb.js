// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('@grpc/grpc-js');
var converter_pb = require('./converter_pb.js');

function serialize_converter_BinaryResponse(arg) {
  if (!(arg instanceof converter_pb.BinaryResponse)) {
    throw new Error('Expected argument of type converter.BinaryResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_converter_BinaryResponse(buffer_arg) {
  return converter_pb.BinaryResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_converter_DecimalRequest(arg) {
  if (!(arg instanceof converter_pb.DecimalRequest)) {
    throw new Error('Expected argument of type converter.DecimalRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_converter_DecimalRequest(buffer_arg) {
  return converter_pb.DecimalRequest.deserializeBinary(new Uint8Array(buffer_arg));
}


var ConverterService = exports.ConverterService = {
  // Server streaming: client sends a single decimal; server streams back binary digits.
convertServerStream: {
    path: '/converter.Converter/ConvertServerStream',
    requestStream: false,
    responseStream: true,
    requestType: converter_pb.DecimalRequest,
    responseType: converter_pb.BinaryResponse,
    requestSerialize: serialize_converter_DecimalRequest,
    requestDeserialize: deserialize_converter_DecimalRequest,
    responseSerialize: serialize_converter_BinaryResponse,
    responseDeserialize: deserialize_converter_BinaryResponse,
  },
  // Client streaming: client sends a stream of decimals; server replies with a single response.
convertClientStream: {
    path: '/converter.Converter/ConvertClientStream',
    requestStream: true,
    responseStream: false,
    requestType: converter_pb.DecimalRequest,
    responseType: converter_pb.BinaryResponse,
    requestSerialize: serialize_converter_DecimalRequest,
    requestDeserialize: deserialize_converter_DecimalRequest,
    responseSerialize: serialize_converter_BinaryResponse,
    responseDeserialize: deserialize_converter_BinaryResponse,
  },
  // Bidirectional streaming: both sides exchange streams.
convertBidirectional: {
    path: '/converter.Converter/ConvertBidirectional',
    requestStream: true,
    responseStream: true,
    requestType: converter_pb.DecimalRequest,
    responseType: converter_pb.BinaryResponse,
    requestSerialize: serialize_converter_DecimalRequest,
    requestDeserialize: deserialize_converter_DecimalRequest,
    responseSerialize: serialize_converter_BinaryResponse,
    responseDeserialize: deserialize_converter_BinaryResponse,
  },
};

exports.ConverterClient = grpc.makeGenericClientConstructor(ConverterService);
