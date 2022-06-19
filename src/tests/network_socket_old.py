from network.network_socket import NetworkSocket

# Examples
net_a = NetworkSocket("172.27.97.46", "8768")
net_b = NetworkSocket("172.27.97.46", "8769")

net_a.send("172.27.97.46", "8769", "hallo b")
net_b.send("172.27.97.46", "8768", "hey a")
net_a.send("172.27.97.46", "8769", "nice to meet u")
