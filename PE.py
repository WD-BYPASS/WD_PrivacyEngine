import sys
import os
import requests
from netmiko import ConnectHandler
import psutil

addrs = psutil.net_if_addrs()

for interface_name, interface_addresses in addrs.items():
    print(f"Interface: {interface_name}")
    for address in interface_addresses:
        print(f"  Family: {address.family.name}")
        if address.family == psutil.AF_LINK: # MAC address
            print(f"  MAC Address: {address.address}")
        else: # IP address (IPv4 or IPv6)
            print(f"  Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast: {address.broadcast}")
    print("-" * 20)
