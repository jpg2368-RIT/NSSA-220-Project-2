from filter_packets import extract_packet


def parse(path):
    packets = []
    with open(path) as file:
        packet_generator = extract_packet(file)
        for packet in packet_generator:
            packets.append(packet_dictionary(packet))
    return packets

def parse_info(packet, parse_type = True):
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
        
        print(info_dict)

        packet["Info"] = info_dict

def packet_dictionary(packet, parse_type = True):
    lines = packet.split("\n")
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line.split())

    # {'No.', 'Time', 'Source', 'Destination', 'Protocol', 'Length', 'Info', 'Hex'}
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
                    # - 1 will end early in order to place whitespace initially 
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

    # for packet in packets:
    #     parse_info(packet)

    for packet in packets:
        # for key, value in packet.items():
        #     if key == "Hex":
        #         continue
        #     print(key + ":", value)
        parse_info(packet)


if __name__ == "__main__":
    main()
