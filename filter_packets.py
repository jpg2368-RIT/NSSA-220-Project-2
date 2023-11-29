import re
import os


# check if file exist and is pcap, then create filtered txt
def filter(path, layer):
    if not os.path.isfile:
        return False
    
    directory, filename_and_extension = os.path.split(path)
    filename, extension = os.path.splitext(filename_and_extension)
    filtered_file = os.path.join(directory, filename + "_filtered.txt")

    with open(path) as input_file:
        packet_generator = extract_packet(input_file)
        with open(filtered_file, "w") as output_file:
            for packet in packet_generator:
                if re.search(layer, packet):
                    output_file.write(packet)
    return filtered_file

# extracts packet starting from header
def extract_packet(file):
    start_extract = False
    packet = ""
    for line in file:
        header_match = bool(re.search("^No\.", line))
        # start extracting if header match and is not extracting. Stop when header match and is extracting
        if not start_extract and header_match:
            start_extract = True
        elif start_extract and header_match:
            yield packet
            packet = ""
        if start_extract:
            packet += line

    yield packet

def main():
    directory = "./Captures/"
    file = "Node1.txt"
    layer = "ICMP"

    filter(directory + file, layer)

if __name__ == "__main__":
    main()

