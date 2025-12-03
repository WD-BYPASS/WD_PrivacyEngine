import sys
import os
import requests
from netmiko import ConnectHandler, SSHDetect
import psutil
import socket

usrnm = input("Enter username: ")
pswrd = input("Enter password: ")
addrs = psutil.net_if_addrs()

def print_network_interfaces():
    for interface, addresses in addrs.items():
        for addr in addresses:
            if addr.family == socket.AF_INET:
                print(f"Interface: {interface}, IP Address: {addr.address}")

def print_process_info():
    current_process = psutil.Process(os.getpid())
    print(f"Current Process ID: {current_process.pid}")
    print(f"Process Name: {current_process.name()}")
    print(f"Executable Path: {current_process.exe()}")
    print(f"Command Line: {' '.join(current_process.cmdline())}")

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def get_device_type(ip, username, password):
    device = {
        'device_type': 'autodetect',
        'host': ip,
        'username': username,
        'password': password,
    }
    try:
        guesser = SSHDetect(**device)
        best_match = guesser.autodetect()
        return best_match
    except Exception as e:
        print(f"Error detecting device type for {ip}: {e}")
        return None
    
def connect_and_execute(ip, device_type, username, password):
    device = {
        'device_type': device_type,
        'host': ip,
        'username': username,
        'password': password,
    }
    try:
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_command("show version")
            print(f"Output from {ip}:\n{output}\n")
    except Exception as e:
        print(f"Error connecting to {ip}: {e}")

local_ip = get_local_ip()
subnet = '.'.join(local_ip.split('.')[:-1]) + '.0/24'
for i in range(1, 255):
    ip = f"{subnet[:-4]}{i}"
    device_type = get_device_type(ip, usrnm, pswrd)
    if device_type:
        print(f"Detected device type {device_type} for IP {ip}")
        connect_and_execute(ip, device_type, usrnm, pswrd)
    else:
        print(f"No device detected at IP {ip}")

print_network_interfaces()
print_process_info()
get_local_ip()
get_device_type()
connect_and_execute()
