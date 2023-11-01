# sudo pip3 install scapy
from scapy.all import *

WIRESHARK_EXTENSION = ".pcap"

# check if file exist and is pcap, then create filtered txt
def filter(file, layer) :
	directory, filename, extension = split_file(file)

	if not file_exists(file):
		print(file, "does not exist!")
		return False
	elif WIRESHARK_EXTENSION != extension:
		print(filename + extension, "must contain", WIRESHARK_EXTENSION, "extension!")
		return False
	
	with open(directory + filename + "_filtered.txt", "w") as output_file:
		packets = rdpcap(file)
		# filtered_packets=[]
		for packet in packets:
			if packet.haslayer(layer):
				# filtered_packets.append(packet)
				pass
				# need to manually convert the raw info from scapy to human readeable format like Node1.txt

def file_exists(file):
    try:
        with open(file, 'r'):
            return True
    except FileNotFoundError:
        return False

# split input into directory, filename, and extension
def split_file(file):
	"""
		For testing purpose
		# print("last slash dot index:", last_slash, last_dot)
		# print(file)
		# print ("directory", directory,"\nfilename:", filename, "\nextension:", extension)
	"""

	last_slash = file.rfind("/") + 1
	# end at specific index
	directory = file[:last_slash]
	filename_extension = file[last_slash:]

	last_dot = filename_extension.rfind(".")
	if (last_dot == -1):
		last_dot = len(filename_extension)
	filename = filename_extension[:last_dot]
	extension = filename_extension[last_dot:]

	print ("\nfile:", file, "\ndirectory:", directory,"\nfilename:", filename, "\nextension:", extension)
	return directory, filename, extension

def main() :
	directory = "./Captures/"
	file = "Node1.pcap"
	packets = rdpcap(directory + file)
	layer="ICMP"

	filter(directory + file, layer)

	# for packet in filteredPackets:
		# print(hexdump(packet))
	

if __name__=="__main__":
	main()
	# split_file("./testing/Project 2/version_96/.The.dothere.txt")
	
