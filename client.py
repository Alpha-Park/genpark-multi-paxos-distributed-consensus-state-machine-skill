class PaxosAcceptor:
    def __init__(self, node_id: int):
        self.node_id = node_id
        self.promised_prop_num = -1
        self.accepted_prop_num = -1
        self.accepted_value = None

    def prepare(self, prop_num: int) -> dict:
        if prop_num > self.promised_prop_num:
            self.promised_prop_num = prop_num
            return {"ok": True, "highest_accepted_prop": self.accepted_prop_num, "highest_accepted_val": self.accepted_value}
        return {"ok": False, "highest_accepted_prop": self.promised_prop_num, "highest_accepted_val": None}

    def accept(self, prop_num: int, value) -> bool:
        if prop_num >= self.promised_prop_num:
            self.promised_prop_num = prop_num
            self.accepted_prop_num = prop_num
            self.accepted_value = value
            return True
        return False

class MultiPaxosCluster:
    def __init__(self, num_nodes: int = 5):
        self.nodes = [PaxosAcceptor(i) for i in range(num_nodes)]
        self.quorum_size = (num_nodes // 2) + 1
        self.committed_log = []

    def propose(self, prop_num: int, client_val) -> dict:
        # Phase 1: Prepare
        prepare_res = [node.prepare(prop_num) for node in self.nodes]
        successes = [r for r in prepare_res if r["ok"]]
        if len(successes) < self.quorum_size:
            return {"status": "REJECTED_PHASE_1", "promises": len(successes)}

        # Find if any value was previously accepted by highest proposal
        chosen_val = client_val
        highest_prop = -1
        for r in successes:
            if r["highest_accepted_prop"] > highest_prop and r["highest_accepted_val"] is not None:
                highest_prop = r["highest_accepted_prop"]
                chosen_val = r["highest_accepted_val"]

        # Phase 2: Accept
        accept_res = [node.accept(prop_num, chosen_val) for node in self.nodes]
        acc_count = sum(1 for a in accept_res if a)
        if acc_count >= self.quorum_size:
            self.committed_log.append({"proposal": prop_num, "value": chosen_val})
            return {"status": "COMMITTED", "proposal": prop_num, "value": chosen_val, "quorum": acc_count}

        return {"status": "REJECTED_PHASE_2", "accepts": acc_count}
