import sys
import json
from client import MultiPaxosCluster

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    if method == "propose":
        cluster = MultiPaxosCluster(params.get("num_nodes", 5))
        return cluster.propose(params.get("prop_num", 1), params.get("value", "DEFAULT"))
    return {"error": "Unknown method"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_request(req)
        print(json.dumps(res))
        sys.stdout.flush()

if __name__ == "__main__":
    main()
