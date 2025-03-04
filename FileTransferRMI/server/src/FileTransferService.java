package server.src;

import common.src.RemoteInterfaces;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.io.File;
import java.nio.file.Files;
import java.io.FileOutputStream;

public class FileTransferService extends UnicastRemoteObject implements RemoteInterfaces {
    private static FileTransferService instance;
    private final String FILE_DIR = "server_files";

    private FileTransferService() throws RemoteException {
        super();
        // Create the directory for storing files if it doesn't exist
        File dir = new File(FILE_DIR);
        if (!dir.exists()) {
            dir.mkdir();
        }
    }

    public static synchronized FileTransferService getInstance() throws RemoteException {
        if (instance == null) {
            instance = new FileTransferService();
        }
        return instance;
    }

    @Override
    public byte[] downloadFile(String fileName) throws RemoteException {
        try {
            File file = new File(FILE_DIR + File.separator + fileName);
            if (!file.exists()) {
                System.out.println("File not found: " + fileName);
                return null;
            }
            System.out.println("Downloading file: " + fileName);
            return Files.readAllBytes(file.toPath());
        } catch (Exception e) {
            System.out.println("Error downloading file: " + e.getMessage());
            return null;
        }
    }

    @Override
    public boolean uploadFile(String fileName, byte[] fileData) throws RemoteException {
        try {
            File file = new File(FILE_DIR + File.separator + fileName);
            FileOutputStream fos = new FileOutputStream(file);
            fos.write(fileData);
            fos.close();
            System.out.println("Uploaded file: " + fileName);
            return true;
        } catch (Exception e) {
            System.out.println("Error uploading file: " + e.getMessage());
            return false;
        }
    }
}
