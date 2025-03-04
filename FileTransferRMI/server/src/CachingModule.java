package server.src;

import java.util.concurrent.ConcurrentHashMap;

public class CachingModule {
    // Implements a simple in-memory cache for idempotent procedure replies
    private ConcurrentHashMap<String, Object> cache;

    public CachingModule() {
        cache = new ConcurrentHashMap<>();
    }

    public void cacheReply(String requestId, Object reply) {
        cache.put(requestId, reply);
        System.out.println("Cached reply for request: " + requestId);
    }

    public Object getCachedReply(String requestId) {
        return cache.get(requestId);
    }
}
