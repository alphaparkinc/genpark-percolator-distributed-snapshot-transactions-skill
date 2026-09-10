import sys
import json
from client import PercolatorEngine

def main():
    perc = PercolatorEngine()
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        if method == "write":
            ok, st = perc.write_transaction(params.get("key"), params.get("value"))
            res = {"success": ok, "status": st}
        elif method == "read":
            val = perc.read_transaction(params.get("key"))
            res = {"value": val}
        else:
            res = {"error": "unknown method"}
        sys.stdout.write(json.dumps({"id": req.get("id"), "result": res}) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
