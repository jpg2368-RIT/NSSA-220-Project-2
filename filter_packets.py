# sudo pip3 install scapy
from scapy.all import *


def filter(packets, layer):
    filtered_packets = []
    for packet in packets:
        if packet.haslayer(layer):
            filtered_packets.append(packet)
    return filtered_packets


def main():
    file_path = "./Captures/"
    filename = "Node1.pcap"
    packets = rdpcap(file_path + filename)
    layer = "ICMP"

    filtered_packets = filter(packets, layer)

    for packet in filtered_packets:
        print(packet)


if __name__ == "__main__":
    main()
