const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const readline = require('readline');

const PROTO_PATH = __dirname + '/converter.proto';

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
});

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const converter_proto = grpc.loadPackageDefinition(packageDefinition).converter;

// Create a client using round-robin load balancing
const client = new converter_proto.Converter(
    'localhost:50051,localhost:50052,localhost:50053',
    grpc.credentials.createInsecure(),
    { 'grpc.lb_policy_name': 'round_robin' }
);

function serverStreamingCall() {
    rl.question('Enter a decimal number for server streaming: ', (input) => {
        const number = parseInt(input);
        if (isNaN(number)) {
            console.log('Invalid number! Please enter a valid decimal.');
            showMenu();
            return;
        }
        const call = client.ConvertServerStream({ number });
        console.log('Server streaming response:');
        call.on('data', (response) => {
            console.log('Received binary digit:', response.binary);
        });
        call.on('end', () => {
            console.log('Server streaming ended.');
            showMenu();
        });
        call.on('error', (e) => {
            console.error('Error in server streaming:', e);
            showMenu();
        });
    });
}

function clientStreamingCall() {
    const call = client.ConvertClientStream((error, response) => {
        if (error) {
            console.error('Error in client streaming:', error);
        } else {
            console.log('Client streaming response:', response.binary);
        }
        showMenu();
    });

    console.log('Enter decimal numbers one by one (type "done" to send):');
    rl.on('line', (input) => {
        if (input.toLowerCase() === 'done') {
            call.end();
            rl.removeAllListeners('line');
        } else {
            const number = parseInt(input);
            if (!isNaN(number)) {
                console.log('Sending decimal:', number);
                call.write({ number });
            } else {
                console.log('Invalid number! Enter a valid decimal or type "done".');
            }
        }
    });
}

function bidirectionalStreamingCall() {
    const call = client.ConvertBidirectional();
    console.log('Enter decimal numbers for bidirectional streaming (type "done" to stop):');

    call.on('data', (response) => {
        console.log('Received binary:', response.binary);
    });

    call.on('end', () => {
        console.log('Bidirectional call ended.');
        showMenu();
    });

    rl.on('line', (input) => {
        if (input.toLowerCase() === 'done') {
            call.end();
            rl.removeAllListeners('line');
        } else {
            const number = parseInt(input);
            if (!isNaN(number)) {
                console.log('Sending decimal:', number);
                call.write({ number });
            } else {
                console.log('Invalid number! Enter a valid decimal or type "done".');
            }
        }
    });
}

function showMenu() {
    rl.question(
        '\nSelect RPC type:\n1. Server Streaming\n2. Client Streaming\n3. Bidirectional Streaming\nQ. Quit\nEnter choice: ',
        (choice) => {
            switch (choice.toLowerCase()) {
                case '1':
                    serverStreamingCall();
                    break;
                case '2':
                    clientStreamingCall();
                    break;
                case '3':
                    bidirectionalStreamingCall();
                    break;
                case 'q':
                    console.log('Exiting...');
                    rl.close();
                    process.exit(0);
                    break;
                default:
                    console.log('Invalid choice! Try again.');
                    showMenu();
            }
        }
    );
}

// Start the loop
showMenu();
