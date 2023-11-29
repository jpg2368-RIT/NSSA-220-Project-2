import statistics


def between(string, char1, char2):
    num = ""
    reading = False
    for c in string:
        if c == char1:
            reading = True
            continue
        elif c == char2:
            break
        if reading:
            num += c
    return int(num)


def find_packet_from_seq(packets, seq):
    for packet in packets:
        split_info = packet["Info"].split(" ")
        if between(split_info[3], "=", "/") == seq:
            return packet


def find_no(packets, no):
    for packet in packets:
        if packet["No."] == no:
            return packet


def compute(packets, ip):
    num_echo_requests_sent = 0
    num_echo_requests_received = 0
    num_echo_replies_sent = 0
    num_echo_replies_received = 0
    request_bytes_sent = []
    request_bytes_received = []
    request_data_sent = []
    request_data_received = []
    thruput = 0
    goodput = 0
    round_trips = []
    delays = []
    hops = []
    open_request_packets = []
    rec_request_packets = []

    # input: {'No.', 'Time', 'Source', 'Destination', 'Protocol', 'Length', 'Info', 'Hex'}

    for packet in packets:
        split_info = packet["Info"].split(" ")
        # Data size metrics
        # ==========================
        if split_info[1] == "request":
            # num echo requests sent, request bytes sent, request data sent
            if packet["Source"] == str(ip):
                num_echo_requests_sent += 1
                request_bytes_sent.append(int(packet["Length"]))
                request_data_sent.append(int(packet["Length"]) - 42)
                open_request_packets.append(packet)
            # num echo requests received, request bytes received, request data received
            elif packet["Destination"] == str(ip):
                num_echo_requests_received += 1
                request_bytes_received.append(int(packet["Length"]))
                request_data_received.append(int(packet["Length"]) - 42)
                rec_request_packets.append(packet)

        # # num echo requests sent, request bytes sent, request data sent
        # if split_info[1] == "request" and packet["Source"] == str(ip):
        #     num_echo_requests_sent += 1
        #     # Total request bytes sent
        #     request_bytes_sent.append(int(packet["Length"]))
        #     request_data_sent.append(int(packet["Length"]) - 42)
        #     open_request_packets.append(packet)

        # # num echo requests received, request bytes received, request data received
        # if split_info[1] == "request" and packet["Destination"] == str(ip):
        #     num_echo_requests_received += 1
        #     # total request bytes received
        #     request_bytes_received.append(int(packet["Length"]))
        #     request_data_received.append(int(packet["Length"]) - 42)
        #     rec_request_packets.append(packet)

        if split_info[1] == "reply":
            # num echo replies sent
            if packet["Source"] == str(ip):
                num_echo_replies_sent += 1
                other = find_packet_from_seq(rec_request_packets, split_info[7][:-1])
                delays.append(float(other["Time"]) - float(packet["Time"]))
            # num echo replies received
            elif packet["Destination"] == str(ip):
                num_echo_replies_received += 1
                other = find_no(open_request_packets, split_info[7][:-1])
                round_trips.append(float(other["Time"]) - float(packet["Time"]))

        # # num echo replies sent
        # if split_info[1] == "reply" and packet["Source"] == str(ip):
        #     num_echo_replies_sent += 1
        #     other = find_packet_from_seq(rec_request_packets, split_info[7][:-1])
        #     delays.append(float(other["Time"]) - float(packet["Time"]))

        # # num echo replies received
        # if split_info[1] == "reply" and packet["Destination"] == str(ip):
        #     num_echo_replies_received += 1
        #     other = find_no(open_request_packets, split_info[7][:-1])
        #     round_trips.append(float(other["Time"]) - float(packet["Time"]))

        # Distance metric
        # ============================
        # average number of hops per echo request
        try:
            hops.append(255 - int(split_info[5][4::1]) + 1)  # adding 1, prof that made it worded things weird i think
        except:
            pass

        # Time-based metrics
        # ============================
        # TODO: average round trip time in ms (computed at end)
        # time between echo request and corresponding reply (ms)
        #

    # throughput
    # TODO: Add specific exception for good coding practice
    try:
        thruput = sum(request_bytes_sent) / sum(round_trips)
    except:
        thruput = "placeholder"

    # goodput
    # TODO: Add specific exception for good coding practice
    try:
        goodput = sum(request_data_sent) / sum(round_trips)
    except:
        goodput = "placeholder"

    # temp

    # TODO: average reply delay in microseconds
    # time between receiving request and sending corresponding reply
    try:
        return (num_echo_requests_sent, num_echo_requests_received, num_echo_replies_sent, num_echo_replies_received,
                sum(request_bytes_sent), sum(request_bytes_received), sum(request_data_sent),
                sum(request_data_received),
                statistics.mean(round_trips), thruput, goodput, statistics.mean(delays), statistics.mean(hops))
    except:
        return (num_echo_requests_sent, num_echo_requests_received, num_echo_replies_sent, num_echo_replies_received,
                sum(request_bytes_sent), sum(request_bytes_received), sum(request_data_sent),
                sum(request_data_received),
                "placeholder", thruput, goodput, "placeholder", "placeholder")
