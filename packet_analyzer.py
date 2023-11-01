from filter_packets import *
from packet_parser import *
from compute_metrics import *


def main():
    num_nodes = 4
    for i in range(num_nodes):
        filtered_packets = filter(f"./Captures/Node{i}.pcap", "ICMP")
        parsed_metrics = parse(filtered_packets)
        computed_metrics = compute(parsed_metrics)
        print(f"Node {i} metrics:")
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
