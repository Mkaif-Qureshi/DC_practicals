package client.src;

import java.util.HashMap;
import java.util.Map;

public class SessionManager {
    // Simple session management for demonstration
    private Map<String, String> sessions;

    public SessionManager() {
        sessions = new HashMap<>();
    }

    public void createSession(String sessionId) {
        sessions.put(sessionId, "Active");
        System.out.println("Session created: " + sessionId);
    }

    public void endSession(String sessionId) {
        sessions.remove(sessionId);
        System.out.println("Session ended: " + sessionId);
    }

    public boolean isSessionActive(String sessionId) {
        return sessions.containsKey(sessionId);
    }
}
