#!/usr/bin/env python
import scapy.all as scapy
import argparse
def scapy_way_to_do_it(ip):
    scapy.arping(ip)
    scapy.scan("192.168.18.2/24")
# THERE IS A MODULE FOR THIS, AKA SCAPY
# You can use scapy.ls to learn what variables can be used
# ----------------------- THE HANDS-ON IMPLEMENTATION ------------------------

def get_arguments():
    parser = argparse.ArgumentParser() # ADD A () AT THE END GOD FUCKING DAMMIT
    parser.add_argument("-t", "--target", dest="target", help="The IP range of your target")
    options = parser.parse_args()
    return options

def scan(ip):
    # This is an object-like structure. A custom packet(?) (OSI Layer 3?)
    arp_request = scapy.ARP(pdst = ip)
    # This is an Ethernet frame (OSI Layer 2?)
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request # Combine two packets into one
    # srp = send/receive (sr is used if you don't have )
    answered_list = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)[0]
    clients_list = [] # [] for lists (aka arrays) {} for dictionaries (aka hashmaps(?))

    # create a list of dictionaries
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
        # The first element of answered_list is the package sent, second is received
    return clients_list

def print_result (results_list):
    print("IP\t\t\tMAC Address\n----------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])

options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)


# print(answered_list.summary())
# print(arp_request.summary())
# print(broadcast.summary())
# print(arp_request_broadcast.summary())
# arp_request_broadcast.show()