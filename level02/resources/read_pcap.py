import scapy.all as scapy

pcap = scapy.rdpcap('level02.pcap')

for packet in pcap:
    if packet.haslayer(scapy.Raw):
        print(packet[scapy.Raw].load.decode('utf-8', errors='ignore'))
