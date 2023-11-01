from filter_packets import *
from packet_parser import *
from compute_metrics import *


def main():
    num_nodes = 4
    for i in range(num_nodes):
        filtered_packets = filter(f"./Captures/Node{i}.pcap", "ICMP")
        parsed_metrics = parse(filtered_packets)
        computed_metrics = compute(parsed_metrics)


if __name__ == "__main__":
    main()
