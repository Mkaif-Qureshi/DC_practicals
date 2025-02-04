const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");

// Load the protobuf file
const PROTO_PATH = "./binary_converter.proto";
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
});
const binaryConverterProto = grpc.loadPackageDefinition(packageDefinition).binaryconverter;


// Create a gRPC client
const client = new binaryConverterProto.BinaryConverter(
    "localhost:50051",
    grpc.credentials.createInsecure()
);

// Function to call ConvertToBinary RPC
function convertToBinary() {
    const readline = require("readline").createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    readline.question("Enter a decimal number: ", (number) => {
        number = parseInt(number);
        console.log(`Client sending number: ${number}`);

        client.ConvertToBinary({ number: number }, (error, response) => {
            if (error) {
                console.error("Error:", error);
            } else {
                console.log(`Client received binary representation: ${response.binary}`);
            }
            readline.close();
        });
    });
}

// Run the client
convertToBinary();
