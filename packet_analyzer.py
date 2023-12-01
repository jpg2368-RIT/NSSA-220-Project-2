from filter_packets import *
from packet_parser import *
from compute_metrics import *

# find highest character count of a particular column and add spacing
def variable_col_width(table_format, col_index, space_between=5):
    max_col_width = 0
    for cols in table_format:
        if len(cols) > col_index and len(str(cols[col_index])) > max_col_width:
            max_col_width = len(cols[col_index])
    return max_col_width + space_between


def main():
    # setup
    num_nodes = 4
    node_ips = ["192.168.100.1", "192.168.100.2", "192.168.200.1", "192.168.200.2"]
    if num_nodes != len(node_ips):
        print(f"Number of nodes ({num_nodes}) does not equal number of IPs ({len(node_ips)})")
        exit(1)

    # compute and output data for each node
    for i in range(num_nodes):
        filtered_packets_file = filter(f"./Captures/Node{i + 1}.txt", "ICMP")
        parsed_metrics = parse(filtered_packets_file)
        parse_info(parsed_metrics)
        computed_metrics = compute(parsed_metrics, node_ips[i])

        node_format = (
            ('Echo Requests Sent', 'Echo Requests Received'),
            (computed_metrics[0], computed_metrics[1]),
            ('Echo Replies Sent', 'Echo Replies Received'),
            (computed_metrics[2], computed_metrics[3]),
            ('Echo Request Bytes Sent', 'Echo Request Data Sent'),
            (computed_metrics[4], computed_metrics[5]),
            ('Echo Request Bytes Received', 'Echo Request Data Received'),
            (computed_metrics[6], computed_metrics[7]),
            (),
            ('Average RTT (milliseconds)', f'{computed_metrics[8]:.3f}'),
            ('Echo Request Throughput (kB/sec)', f'{computed_metrics[9]:.2f}'),
            ('Echo Request Goodput (kB/sec)', f'{computed_metrics[10]:.2f}'),
            ('Average Reply Delay (microseconds)', f'{computed_metrics[11]:.3f}'),
            ('Average Echo Request Hop Count', f'{computed_metrics[12]:.3f}'))

        print(f"Node {i + 1} metrics:")
        for row in node_format:
            print("\t", end="")
            for i, col in enumerate(row):
                print(f"{col:<{variable_col_width(node_format, i)}}", end="")
            print()
        print(" ========================================================\n")


if __name__ == "__main__":
    main()
