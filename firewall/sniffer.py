from scapy.all import sniff
from datetime import datetime

def log_packet(packet):
	try:
	    src=packet[0][1].src
	    dst=packet[0][1].dst
	    proto=packet[0][1].proto if hasattr(packet[0][1], 'proto') else 'N/A'
	    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	    log_entry=f"[{timestamp}] SRC:{src} DST:{dst} PROTO:{proto}"
	    print(log_entry)

	    with open("logs/packet_logs.txt","a") as f:
	       f.write(log_entry + "\n")

	except:
	    pass

def start_sniffing(interface="eth0"):
	print(f"[STARTED] Sniffing on interface: {interface}")
	sniff(iface=interface,prn=log_packet,store=False)
