package client.src;

import common.src.RemoteInterfaces;
import common.src.SystemConstants;
import java.rmi.Naming;
import java.util.Scanner;
import java.io.File;
import java.nio.file.Files;

public class FileTransferClient {
    private RemoteInterfaces fileService;
    private SessionManager sessionManager;
    private PersistentTransfer persistentTransfer;
    private TransientTransfer transientTransfer;

    public FileTransferClient() {
        try {
            // Lookup the remote file transfer service
            fileService = (RemoteInterfaces) Naming.lookup("rmi://localhost/FileTransferService");
            sessionManager = new SessionManager();
            persistentTransfer = new PersistentTransfer();
            transientTransfer = new TransientTransfer();
        } catch (Exception e) {
            System.out.println("Error connecting to RMI server: " + e.getMessage());
            e.printStackTrace();
        }
    }

    public void run() {
        Scanner scanner = new Scanner(System.in);
        while (true) {
            System.out.println("\nSelect option:\n1. Download File\n2. Upload File\n3. Exit");
            String option = scanner.nextLine();
            if (option.equals("1")) {
                System.out.print("Enter filename to download: ");
                String fileName = scanner.nextLine();
                downloadFile(fileName);
            } else if (option.equals("2")) {
                System.out.print("Enter file path to upload: ");
                String filePath = scanner.nextLine();
                uploadFile(filePath);
            } else if (option.equals("3")) {
                System.out.println("Exiting client...");
                break;
            } else {
                System.out.println("Invalid option, please try again.");
            }
        }
        scanner.close();
    }

    private void downloadFile(String fileName) {
        try {
            byte[] fileData = fileService.downloadFile(fileName);
            if (fileData != null && fileData.length > 0) {
                // Save file to current directory with a prefix
                File outFile = new File("downloaded_" + fileName);
                Files.write(outFile.toPath(), fileData);
                System.out.println("File downloaded and saved as: " + outFile.getAbsolutePath());
            } else {
                System.out.println("File not found or empty.");
            }
        } catch (Exception e) {
            System.out.println("Error downloading file: " + e.getMessage());
        }
    }

    private void uploadFile(String filePath) {
        try {
            File file = new File(filePath);
            if (!file.exists()) {
                System.out.println("File does not exist: " + filePath);
                return;
            }
            long fileSize = file.length();
            boolean result;
            // Choose persistent or transient transfer based on file size threshold
            if (fileSize > Configurations.FILE_SIZE_THRESHOLD) {
                System.out.println("Using persistent transfer for large file (" + fileSize + " bytes).");
                result = persistentTransfer.transferLargeFile(filePath, fileService);
            } else {
                System.out.println("Using transient transfer for small file (" + fileSize + " bytes).");
                result = transientTransfer.transferSmallFile(filePath, fileService);
            }
            if (result) {
                System.out.println("File uploaded successfully.");
            } else {
                System.out.println("File upload failed.");
            }
        } catch (Exception e) {
            System.out.println("Error uploading file: " + e.getMessage());
        }
    }
}
