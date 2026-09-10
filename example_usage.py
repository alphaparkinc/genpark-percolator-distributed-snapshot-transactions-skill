from client import PercolatorEngine

def main():
    print("=== Testing Percolator Distributed Transactions ===")
    perc = PercolatorEngine()
    ok, st = perc.write_transaction("user:alice", "Balance: 500")
    print("Write transaction status:", st)
    assert ok and st == "COMMITTED"

    val = perc.read_transaction("user:alice")
    print("Read value:", val)
    assert val == "Balance: 500"
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
