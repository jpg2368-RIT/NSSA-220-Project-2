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


def compute(packets, ip):
    computed = []
    num_echo_requests_sent = 0
    num_echo_requests_received = 0
    num_echo_replies_sent = 0
    num_echo_replies_received = 0
    request_bytes_sent = 0
    request_bytes_received = 0
    request_data_sent = 0
    request_data_received = 0
    tot_round_trip_time = 0
    thruput = 0
    goodput = 0
    round_trips = []
    delays = []
    hops = []
    open_packets = []

    for packet in packets:
        split_info = packet.Info.split(" ")
        # Data size metrics
        # ==========================
        # num echo requests sent
        if "request" in packet.Info and packet.Source == ip:
            num_echo_requests_sent += 1
            # Total request bytes sent
            request_bytes_sent += int(packet.Length)
            open_packets.append(packet)
        # num echo requests received
        if "request" in packet.Info and packet.Destination is ip:
            num_echo_requests_received += 1
            # total request bytes received
            request_bytes_received += int(packet.Length)
        # num echo replies sent
        if "reply" in packet.Info and packet.Source is ip:
            num_echo_replies_sent += 1
        # num echo replies received
        if "reply" in packet.Info and packet.Destination is ip:
            num_echo_replies_received += 1
            other = find_packet_from_seq(between(split_info[4], "=", "/"))
            round_trips.append(float(other.Time) - float(packet.Time))
        # total request data sent
        # total request data received

        # Time-based metrics
        # ============================
        # average round trip time in ms
        # use sequence number to find corresponding reply
        # throughput
        # goodput
        # average reply delay in microseconds

        # Distance metric
        # ============================
        # average number of hops per echo request
        hops.append(255 - int(split_info[5][4::1]))

    computed.append(num_echo_requests_sent)
    computed.append(num_echo_requests_received)
    computed.append(num_echo_replies_sent)
    computed.append(num_echo_replies_received)
    computed.append(request_bytes_sent)
    computed.append(request_bytes_received)
    computed.append(request_data_sent)
    computed.append(request_data_received)
    computed.append(statistics.mean(round_trips))
    computed.append(thruput)
    computed.append(goodput)
    computed.append(statistics.mean(delays))
    computed.append(statistics.mean(hops))
    return computed
