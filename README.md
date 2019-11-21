# Arp_spoof
arp_spoof - ARP spoofing attack against someone else on your local unencrypted network.

## Desclaimer
arp_spoof is intented ONLY for EDUCATIONAL PURPOSES.

## Requirements
Python

## Install
```
# git clone https://github.com/LeuvaApurv/arp_spoof
# cd arp_spoof
```

## Usage
Run the python script and MITM attack performed. 

## Help
```
# python arp_spoof.py -h
Usage: arp_spoof.py [options]

Options:
  -h, --help            show this help message and exit
  -t TARGET_IP, --target-ip=TARGET_IP
                        Target IP for spoofing gateway.
  -g GATEWAY_IP, --gateway-ip=GATEWAY_IP
                        Gateway IP for spoofing Target.
```

## Sample output:
```
#python arp_spoof.py -t 10.*.*.10 -g 10.*.*.1
[+] Packets sent: 6^C 
[+] Detected CTRL + C ....... Resetting ARP tables...... Please wait.

```
