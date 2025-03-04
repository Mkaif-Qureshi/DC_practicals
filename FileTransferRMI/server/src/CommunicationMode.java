package server.src;

public class CommunicationMode {
    // Allows switching between persistent and transient communication modes
    public enum Mode {
        PERSISTENT,
        TRANSIENT
    }

    private Mode currentMode;

    public CommunicationMode() {
        currentMode = Mode.PERSISTENT; // default mode
    }

    public Mode getCurrentMode() {
        return currentMode;
    }

    public void setCurrentMode(Mode mode) {
        currentMode = mode;
        System.out.println("Communication mode set to: " + mode);
    }
}
