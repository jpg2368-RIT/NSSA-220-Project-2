from filter_packets import extract_packet


def parse(path):
    packets = []
    with open(path) as file:
        packet_generator = extract_packet(file)
        for packet in packet_generator:
            packets.append(packet_dictionary(packet))
    return packets


# Only parse when packet is either request or reply for successfull ICMP
def parse_info(packets, parse_type = True):
    for packet in packets:
        info_dict = {}
        split_info = packet["Info"].split(" ")
        if "request" in split_info or "reply" in split_info:
            info_dict["Packet Type"] = split_info[2]
            info_dict["id"] = split_info[3][3:-1]
            info_dict["seq"] = split_info[4][4:-1].split("/")
            info_dict["ttl"] = split_info[5][4:]
            info_dict["No. pointer"] = split_info[8][:-1]
            if parse_type:
                for i in range(len(info_dict["seq"])):
                    info_dict["seq"][i] = int(info_dict["seq"][i])
                info_dict["ttl"] = int(info_dict["ttl"])
                info_dict["No. pointer"] = int(info_dict["No. pointer"])

            packet["Info"] = info_dict


# Parsed Packet: {
# 'No.': int, 
# 'Time': float, 
# 'Source': str, 
# 'Destination': str, 
# 'Protocol': str, 
# 'Length': int, 
# 'Info': {}, <- Parsed Info only if successful. Else str
# 'Hex': str}
def packet_dictionary(packet, parse_type = True):
    lines = packet.split("\n")
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line.split())

    header = None
    packet_dict = {}
    for i in range(len(cleaned_lines)):
        if i < 2:
            if i == 0:
                header = cleaned_lines[i]
                continue
            if i == 1:
                for j in range(len(cleaned_lines[i])):
                    # The rest of array will output to Info since Info contain whitespaces. 
                    if j < len(header):
                        packet_dict[header[j]] = cleaned_lines[i][j]
                    else:
                        packet_dict[header[len(header) - 1]] += " " + cleaned_lines[i][j]
        else:
            if "Hex" not in packet_dict:
                packet_dict["Hex"] = ""
            for j in range(1, len(cleaned_lines[i]) - 1):
                packet_dict["Hex"] += cleaned_lines[i][j] + " "
        if parse_type:
            packet_dict["No."] = int(packet_dict["No."])
            packet_dict["Time"] = float(packet_dict["Time"])
            packet_dict["Length"] = float(packet_dict["Length"])

    return packet_dict


def main():
    packets = parse("./Captures/Node1_filtered.txt")
    parse_info(packet)

    for packet in packets:
        for key, value in packet.items():
            if key == "Hex":
                continue
            print(key + ":", value)
        

if __name__ == "__main__":
    main()
