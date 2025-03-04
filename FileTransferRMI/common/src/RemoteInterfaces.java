package common.src;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface RemoteInterfaces extends Remote {
    byte[] downloadFile(String fileName) throws RemoteException;

    boolean uploadFile(String fileName, byte[] fileData) throws RemoteException;
}
