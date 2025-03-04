package client.src;

import java.io.File;
import java.nio.file.Files;
import common.src.RemoteInterfaces;

public class TransientTransfer {
    // Handles a one-shot file transfer for small files
    public boolean transferSmallFile(String filePath, RemoteInterfaces fileService) {
        try {
            File file = new File(filePath);
            byte[] fileData = Files.readAllBytes(file.toPath());
            boolean result = fileService.uploadFile(file.getName(), fileData);
            return result;
        } catch (Exception e) {
            System.out.println("Error in transient transfer: " + e.getMessage());
            return false;
        }
    }
}
