from filter_packets import *
from packet_parser import *
from compute_metrics import *


def main():
    num_nodes = 4
    node_ips = ["192.168.100.1", "192.168.100.2", "192.168.200.1", "192.168.200.2"]
    if num_nodes != len(node_ips):
        print(f"Number of nodes ({num_nodes}) does not equal number of IPs ({len(node_ips)})")
        exit(1)
    for i in range(num_nodes):
        filtered_packets_file = filter(f"./Captures/Node{i+1}.txt", "ICMP")
        parsed_metrics = parse(filtered_packets_file)
        computed_metrics = compute(parsed_metrics, node_ips[i])
        print(f"Node {i+1} metrics:")
        print(f"\tNumber of echo requests sent:\t{computed_metrics[0]}")
        print(f"\tNumber of echo requests received:\t{computed_metrics[1]}")
        print(f"\tNumber of Echo replies sent:\t{computed_metrics[2]}")
        print(f"\tNumber of echo replies received:\t{computed_metrics[3]}")
        print(f"\tTotal request bytes sent:\t{computed_metrics[4]}")
        print(f"\tTotal request bytes received:\t{computed_metrics[5]}")
        print(f"\tTotal request data sent:\t{computed_metrics[6]}")
        print(f"\tTotal request data received:\t{computed_metrics[7]}")
        print("")
        print(f"\tAverage round trip time:\t{computed_metrics[8]}ms")
        print(f"\tThroughput:\t{computed_metrics[9]}")
        print(f"\tGoodput:\t{computed_metrics[10]}")
        print(f"\tAverage reply delay:\t{computed_metrics[11]} microseconds")
        print("")
        print(f"\tAverage hops:{computed_metrics[12]}")
        print("\n")


if __name__ == "__main__":
    main()
