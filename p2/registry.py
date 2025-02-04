import json
import threading

class Registry:
    REGISTRY_FILE = "registry.json"
    LOCK = threading.Lock()

    def __init__(self):
        self._load_registry()

    def _load_registry(self):
        try:
            with open(self.REGISTRY_FILE, "r") as f:
                self.servers = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.servers = []

    def _save_registry(self):
        with open(self.REGISTRY_FILE, "w") as f:
            json.dump(self.servers, f)

    def register(self, port):
        with self.LOCK:
            if port not in self.servers:
                self.servers.append(port)
                self._save_registry()

    def deregister(self, port):
        with self.LOCK:
            if port in self.servers:
                self.servers.remove(port)
                self._save_registry()

    def get_servers(self):
        with self.LOCK:
            return list(self.servers)
