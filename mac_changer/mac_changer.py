#!/usr/bin/env python

import subprocess # This is for system calls (ifconfig etc.)
import optparse # This is for command line arguments
import re # This is for regular expressions

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="The new MAC address to change to")
    (options, arguments) = parser.parse_args()  # parse_args() function returns two variables, options and arguments
    if not options.interface:
        parser.error("[-] Please specify an interface, use -- help for info!")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use -- help for info!")
    return options

def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    # Needs utf-8 decoding, or else can't be searched later
    # Or cast ifconfig_result into string (str(ifconfig_result))
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)  # Pay attention to the groups!
    else:
        print("[-] Could not read MAC address")


options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC address is: " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not change")

# input is a python3 function and is meant to run using python3 in terminal
# if you change input into raw_input, then it can be used in python2
# interface = input("interface > ")
# new_mac = input("new MAC > ")