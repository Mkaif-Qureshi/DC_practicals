package server.src;

import java.rmi.Naming;
import java.rmi.registry.LocateRegistry;

public class MainServer {
    public static void main(String[] args) {
        try {
            // Create RMI registry on port 1099
            LocateRegistry.createRegistry(1099);
            // Get the singleton instance of FileTransferService
            FileTransferService service = FileTransferService.getInstance();
            Naming.rebind("rmi://localhost/FileTransferService", service);
            System.out.println("RMI File Transfer Server started.");
        } catch (Exception e) {
            System.out.println("Error starting server: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
