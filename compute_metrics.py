import statistics


def between(string: str, char1: str, char2: str) -> str:
    bet = ""
    reading = False
    for c in string:
        if c == char1:
            reading = True
            continue
        elif c == char2:
            break
        if reading:
            bet += c
    return bet


def find_packet_from_seq(packets: list, seq: int):
    for packet in packets:
        split_info = packet["Info"].split(" ")
        if int(between(split_info[4], "=", "/")) == seq:
            return packet


def find_no(packets: list, no: int):
    for packet in packets:
        if int(packet["No."]) == no:
            return packet


def compute(packets: list, ip: str):
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

    # inputs: ['No.', 'Time', 'Source', 'Destination', 'Protocol', 'Length', 'Info', 'Hex']
    HEADER_SIZE = 42
    for packet in packets:
        split_info = packet["Info"].split(" ")
        # Data size metrics
        # ==========================
        # num echo requests sent, request bytes sent, request data sent
        if split_info[2] == "request" and packet["Source"] == ip:
            num_echo_requests_sent += 1
            # Total request bytes sent
            request_bytes_sent.append(int(packet["Length"]))
            request_data_sent.append(int(packet["Length"]) - HEADER_SIZE)
            open_request_packets.append(packet)


        # num echo requests received, request bytes received, request data received
        if split_info[2] == "request" and packet["Destination"] == ip:
            num_echo_requests_received += 1
            # total request bytes received
            request_bytes_received.append(int(packet["Length"]))
            request_data_received.append(int(packet["Length"]) - HEADER_SIZE)
            rec_request_packets.append(packet)


        # num echo replies sent
        if split_info[2] == "reply" and packet["Source"] == ip:
            num_echo_replies_sent += 1
            other = find_no(rec_request_packets, int(split_info[8][:-1]))
            delays.append(float(other["Time"]) - float(packet["Time"]))

        # num echo replies received
        if split_info[2] == "reply" and packet["Destination"] == ip:
            num_echo_replies_received += 1
            other = find_no(open_request_packets, int(split_info[8][:-1]))
            round_trips.append(float(other["Time"]) - float(packet["Time"]))
            # Distance metric
            # ============================
            # average number of hops per echo request
            hops.append(128 - int(split_info[5][4::1]) + 1)  # adding 1, prof that made it worded things weird i think




        # Time-based metrics
        # ============================
        # average round trip time in ms (computed at end)
        # time between echo request and corresponding reply (ms)

    # throughput
    thruput = sum(request_bytes_sent) / sum(round_trips)

    # goodput
    goodput = sum(request_data_sent) / sum(round_trips)

    # temp

    # average reply delay in microseconds
    # time between receiving request and sending corresponding reply
    return (num_echo_requests_sent, num_echo_requests_received, num_echo_replies_sent, num_echo_replies_received,
            sum(request_bytes_sent), sum(request_bytes_received), sum(request_data_sent),
            sum(request_data_received), statistics.mean(round_trips)*-1000, thruput/-1000, goodput/-1000, statistics.mean(delays)*-1000000,
            statistics.mean(hops))
