import statistics


def compute(entries):
    num_echo_requests_sent = 0
    num_echo_replies_received = 0
    num_echo_replies_sent = 0
    num_echo_replies_received = 0
    request_bytes_sent = 0
    request_bytes_received = 0
    request_data_sent = 0
    request_data_received = 0

    for entry in entries:
        # Data size metrics
        # ==========================
        # num echo requests sent
        # if "request" in entry and source_ip is this one:
        #     num_echo_requests_sent += 1
        # # num echo requests received
        # if "request" in entry and dest_ip is this one:
        #     num_echo_requests_received += 1
        # num echo replies sent
        # if "reply" in entry and source_ip is this one:
        # num_echo_replies_sent += 1
        # num echo replies received
        # if "reply" in entry and dest_ip is this one:
        # num_echo_replies_received += 1
        # Total request bytes sent
        # total request bytes received
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
        pass
