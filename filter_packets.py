import re

# check if file exist and is pcap, then create filtered txt
def filter(file, layer) :
	directory, filename, extension = split_file(file)

	if not file_exist(file):
		print(file, "does not exist!")
		return False
	
	with open(directory + filename + "_filtered.txt", "w") as output_file:
		index = 0
		while True:
			packet, index = extract_packet(file, index)
			if packet == "":
				break
			if re.search(layer, packet):
				print(packet)
				output_file.write(packet)			

def file_exist(file):
    try:
        with open(file, "r"):
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

	return directory, filename, extension

# extracts packet starting from header
def extract_packet(file, index = 0):
	start_extract = False
	packet = ""
	with open(file) as file:
		for _ in range(index):
			next(file)
		for line in file:
			header_match = bool(re.search("^No\.", line))
			# start extracting if header match and is not extracting. Stop when header match and is extracting
			if not start_extract and header_match:
				start_extract=True
			elif start_extract and header_match:
				return packet, index
			if start_extract:
				packet += line
				index += 1

	return packet, index

def main() :
	directory = "./Captures/"
	file = "Node1.txt"
	layer="ICMP"

	filter(directory + file, layer)


if __name__=="__main__":
	main()
	# split_file("./testing/Project 2/version_96/.The.dothere.txt")
	
