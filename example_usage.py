from client import MultiPaxosCluster

def main():
    print("=== Multi-Paxos Distributed Consensus Cluster ===")
    cluster = MultiPaxosCluster(num_nodes=5)

    res = cluster.propose(prop_num=101, client_val="TX_TRANSFER_$500")
    print("Proposal Result:", res)
    assert res["status"] == "COMMITTED"
    assert res["value"] == "TX_TRANSFER_$500"
    assert res["quorum"] >= 3

    print("Multi-Paxos Cluster verified successfully!")

if __name__ == "__main__":
    main()
