package client.src;

import java.io.File;
import java.nio.file.Files;
import common.src.SystemConstants;
import common.src.RemoteInterfaces;

public class PersistentTransfer {
    // Simulated persistent transfer (e.g., sending in chunks)
    public boolean transferLargeFile(String filePath, RemoteInterfaces fileService) {
        try {
            File file = new File(filePath);
            long fileSize = file.length();
            int chunkSize = SystemConstants.CHUNK_SIZE;
            int numChunks = (int) Math.ceil((double) fileSize / chunkSize);

            // For simplicity, read the entire file.
            // In a real implementation, you would send and reassemble chunks.
            byte[] fileData = Files.readAllBytes(file.toPath());
            boolean result = fileService.uploadFile(file.getName(), fileData);
            System.out.println("Large file transferred in " + numChunks + " chunks.");
            return result;
        } catch (Exception e) {
            System.out.println("Error in persistent transfer: " + e.getMessage());
            return false;
        }
    }
}
