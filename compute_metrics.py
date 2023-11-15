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
        split_info = packet.split(" ")
        if packet.between(split_info[4], "=", "/") == seq:
            return packet


def find_no(packets, no):
    for packet in packets:
        if packet.No == no:
            return packet


# geth the # from "request in ###"
def get_req_in(packet):
    info = packet.Info.split(" ")


# gets the # from "reply in ###"
def get_rep_in(packet):
    info = packet.Info.split(" ")


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
    open_reply_packets = []

    # input: ['No.', 'Time', 'Source', 'Destination', 'Protocol', 'Length', 'Info', 'Hex']

    for packet in packets:
        split_info = packet.Info.split(" ")
        # Data size metrics
        # ==========================
        # num echo requests sent, request bytes sent, request data sent
        if "request" in packet.Info and packet.Source == ip:
            num_echo_requests_sent += 1
            # Total request bytes sent
            request_bytes_sent.append(int(packet.Length))
            request_data_sent.append(int(packet.Length - 42))
            open_request_packets.append(packet)

        # num echo requests received, request bytes received, request data received
        if "request" in packet.Info and packet.Destination is ip:
            num_echo_requests_received += 1
            # total request bytes received
            request_bytes_received.append(int(packet.Length))
            request_data_received.append(int(packet.Length) - 42)
            open_reply_packets.append(packet)

        # num echo replies sent
        if "reply" in packet.Info and packet.Source is ip:
            num_echo_replies_sent += 1
            # other = find_packet_from_seq(packets, between(split_info[4], "=", "/"))
            other = find_no(open_reply_packets, get_rep_in(packet))
            round_trips.append(float(other.Time) - float(packet.Time))

        # num echo replies received
        if "reply" in packet.Info and packet.Destination is ip:
            num_echo_replies_received += 1
            # other = find_packet_from_seq(packets, between(split_info[4], "=", "/"))
            round_trips.append(float(other.Time) - float(packet.Time))

        # Time-based metrics
        # ============================
        # TODO: average round trip time in ms (computed at end)
        # time between echo request and corresponding reply (ms)

        # throughput
        thruput = sum(request_bytes_sent) / sum(round_trips)

        # goodput
        goodput = sum(request_data_sent) / sum(round_trips)

        # TODO: average reply delay in microseconds
        # time between receiving request and sending corresponding reply

        # Distance metric
        # ============================
        # average number of hops per echo request
        hops.append(255 - int(split_info[5][4::1]))

    return (num_echo_requests_sent, num_echo_requests_received, num_echo_replies_sent, num_echo_replies_received,
            request_bytes_sent, request_bytes_received, request_data_sent, request_data_received,
            statistics.mean(round_trips), thruput, goodput, statistics.mean(delays), statistics.mean(hops))
