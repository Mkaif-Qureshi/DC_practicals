package client.src;

public class MainClient {
    public static void main(String[] args) {
        System.out.println("Starting RMI File Transfer Client...");
        FileTransferClient client = new FileTransferClient();
        client.run();
    }
}
