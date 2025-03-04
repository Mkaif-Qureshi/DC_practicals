package server.src;

public class TimeoutManager {
    // Manages timeout values for server-side operations
    private int timeout;

    public TimeoutManager(int timeout) {
        this.timeout = timeout;
    }

    public int getTimeout() {
        return timeout;
    }

    public void setTimeout(int timeout) {
        this.timeout = timeout;
        System.out.println("Timeout updated to: " + timeout + " ms");
    }
}
