package tests.clientTests;

import client.src.FileTransferClient;

public class ClientTestSuite {
    public static void main(String[] args) {
        System.out.println("Running Client Test Suite...");
        FileTransferClient client = new FileTransferClient();
        // For testing, run the interactive client (manual tests can be performed)
        client.run();
    }
}
