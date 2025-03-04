package tests.serverTests;

import server.src.FileTransferService;

public class ServerTestSuite {
    public static void main(String[] args) {
        System.out.println("Running Server Test Suite...");
        try {
            FileTransferService service = FileTransferService.getInstance();
            // Test upload and download functionality
            byte[] testData = "Test data".getBytes();
            boolean uploadResult = service.uploadFile("test.txt", testData);
            byte[] downloadedData = service.downloadFile("test.txt");
            System.out.println("Upload result: " + uploadResult);
            System.out.println("Downloaded data: " + new String(downloadedData));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
