package server.src;

public class MultiThreadHandler implements Runnable {
    // Wraps a task to execute it concurrently
    private Runnable task;

    public MultiThreadHandler(Runnable task) {
        this.task = task;
    }

    @Override
    public void run() {
        task.run();
    }
}
