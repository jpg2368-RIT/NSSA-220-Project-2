# sudo pip3 install scapy
from scapy.all import *

def filter(packets, layer) :
	filteredPackets=[]
	for packet in packets:
		if (packet.haslayer(layer)):
			filteredPackets.append(packet)
	return filteredPackets


def main() :
	filePath = "./Captures/"
	filename = "Node1.pcap"
	packets = rdpcap(filePath + filename)
	layer="ICMP"

	filteredPackets = filter(packets, layer)

	for packet in filteredPackets:
		print(packet)
	

if __name__=="__main__":
	main()
	
