import statistics


# finds a packet in a list based on it's number
def find_no(packets, no):
    for packet in packets:
        if packet["No."] == no:
            return packet


# does all the computing, returns a list with all the info
def compute(packets, ip):
    num_echo_requests_sent = 0
    num_echo_requests_received = 0
    num_echo_replies_sent = 0
    num_echo_replies_received = 0
    request_bytes_sent = []
    request_bytes_received = []
    request_data_sent = []
    request_data_received = []
    round_trips = []
    delays = []
    hops = []
    open_request_packets = []
    rec_request_packets = []

    # Parsed Packet: {
    # 'No.': int, 
    # 'Time': float, 
    # 'Source': str, 
    # 'Destination': str, 
    # 'Protocol': str, 
    # 'Length': int, 
    # 'Info': {}, <- Parsed Info only if successful. Else str
    # 'Hex': str}
    
    # Parsed Info: {
    # 'Packet Type': str, 
    # 'id': str, 
    # 'seq': [int, int], 
    # 'ttl': int, 
    # 'No. pointer': int}

    HEADER_SIZE = 42
    for packet in packets:
        # skip if Info is not parsed
        if isinstance(packet["Info"], str):
            continue
        # Data size metrics
        # ==========================
        # num echo requests sent, request bytes sent, request data sent
        if packet["Info"]["Packet Type"] == "request" and packet["Source"] == ip:
            num_echo_requests_sent += 1
            # Total request bytes sent
            request_bytes_sent.append(packet["Length"])
            request_data_sent.append(packet["Length"] - HEADER_SIZE)
            open_request_packets.append(packet)

        # num echo requests received, request bytes received, request data received
        if packet["Info"]["Packet Type"] == "request" and packet["Destination"] == ip:
            num_echo_requests_received += 1
            # total request bytes received
            request_bytes_received.append(packet["Length"])
            request_data_received.append(packet["Length"] - HEADER_SIZE)
            rec_request_packets.append(packet)

        # num echo replies sent
        if packet["Info"]["Packet Type"] == "reply" and packet["Source"] == ip:
            num_echo_replies_sent += 1
            other = find_no(rec_request_packets, packet["Info"]["No. pointer"])
            delays.append(other["Time"] - packet["Time"])

        # num echo replies received
        if packet["Info"]["Packet Type"] == "reply" and packet["Destination"] == ip:
            num_echo_replies_received += 1
            other = find_no(open_request_packets, packet["Info"]["No. pointer"])
            round_trips.append(other["Time"] - packet["Time"])
            # Distance metric
            # ============================
            # average number of hops per echo request
            hops.append(128 - packet["Info"]["ttl"] + 1)  # adding 1, prof that made it worded things weird i think

        # Time-based metrics
        # ============================
        # average round trip time in ms (computed at end)
        # time between echo request and corresponding reply (ms)

    # throughput
    thruput = sum(request_bytes_sent) / sum(round_trips)

    # goodput
    goodput = sum(request_data_sent) / sum(round_trips)

    # average reply delay in microseconds
    # time between receiving request and sending corresponding reply

    return (
        num_echo_requests_sent, num_echo_requests_received, num_echo_replies_sent, num_echo_replies_received,
        sum(request_bytes_sent), sum(request_bytes_received), sum(request_data_sent),
        sum(request_data_received), statistics.mean(round_trips) * -1000, thruput / -1000, goodput / -1000,
        statistics.mean(delays) * -1000000,
        statistics.mean(hops))
