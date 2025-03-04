package server.src;

import java.util.concurrent.ConcurrentHashMap;

public class SessionTracker {
    // Tracks active sessions on the server
    private ConcurrentHashMap<String, String> activeSessions;

    public SessionTracker() {
        activeSessions = new ConcurrentHashMap<>();
    }

    public void addSession(String sessionId) {
        activeSessions.put(sessionId, "Active");
        System.out.println("Session added: " + sessionId);
    }

    public void removeSession(String sessionId) {
        activeSessions.remove(sessionId);
        System.out.println("Session removed: " + sessionId);
    }

    public boolean isSessionActive(String sessionId) {
        return activeSessions.containsKey(sessionId);
    }
}
