class PercolatorEngine:
    """
    Google Percolator Distributed Snapshot Transaction Protocol.
    Uses primary lock resolution over multi-versioned columnar storage.
    """
    def __init__(self):
        self.data = {}
        self.lock = {}
        self.write = {}
        self.global_ts = 1

    def get_ts(self):
        ts = self.global_ts
        self.global_ts += 1
        return ts

    def write_transaction(self, key, value):
        start_ts = self.get_ts()
        if key in self.lock:
            return False, "LOCKED"
        self.data[(key, start_ts)] = value
        self.lock[key] = {"primary": (key, start_ts), "ts": start_ts}

        commit_ts = self.get_ts()
        del self.lock[key]
        self.write[(key, commit_ts)] = start_ts
        return True, "COMMITTED"

    def read_transaction(self, key):
        ts = self.get_ts()
        latest_commit = -1
        latest_start = -1
        for (k, c_ts), s_ts in self.write.items():
            if k == key and c_ts <= ts and c_ts > latest_commit:
                latest_commit = c_ts
                latest_start = s_ts

        if latest_start != -1:
            return self.data.get((key, latest_start))
        return None
