from filter_packets import extract_packet


def parse(file):
    packets = []
    with open(file) as file:
        packet_generator = extract_packet(file)
        for packet in packet_generator:
            packets.append(packet_dictionary(packet))
    return packets


def packet_dictionary(packet):
    """
	For testing purpose:

	"""
    lines = packet.split("\n")
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line.split())

    # ['No.', 'Time', 'Source', 'Destination', 'Protocol', 'Length', 'Info', 'Hex']
    header = None
    packet_dict = {"Hex": ""}
    for i in range(len(cleaned_lines)):
        if i < 2:
            if i == 0:
                header = cleaned_lines[i]
                continue
            if i == 1:
                for j in range(len(cleaned_lines[i])):
                    # The rest of array will output to Info since Info contain whitespaces
                    if j < len(header):
                        packet_dict[header[j]] = cleaned_lines[i][j]
                    else:
                        packet_dict[header[len(header) - 1]] += cleaned_lines[i][j] + " "
        else:
            for j in range(1, len(cleaned_lines[i]) - 1):
                packet_dict["Hex"] += cleaned_lines[i][j] + " "

    return packet_dict


def main():
    packets = parse("./Captures/example_filtered.txt")


# for packet in packets:
# 	print()
# 	print(packet["Hex"])

# print(packets[0]["Hex"])


if __name__ == "__main__":
    main()
