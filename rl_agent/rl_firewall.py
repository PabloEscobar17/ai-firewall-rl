import pandas as pd
import joblib
import random
import os
import subprocess
from datetime import datetime
from scapy.all import sniff, IP, TCP, UDP, ICMP
import pickle

# === Paths ===
Q_TABLE_FILE = "/root/Desktop/ai-firewall-testing/rl_agent/q_table.pkl"
LOG_FILE = "/root/Desktop/ai-firewall-testing/dataset/rl_firewall_log.csv"
MODEL_PATH = "/root/Desktop/ai-firewall-testing/ai_model/firewall_model.pkl"
ENCODER_PATH = "/root/Desktop/ai-firewall-testing/ai_model/encoders.pkl"

# === Load AI model and encoders ===
model = joblib.load(MODEL_PATH)
encoders = joblib.load(ENCODER_PATH)

# === RL Config ===
ACTIONS = ["allow", "block"]
ALPHA = 0.1
GAMMA = 0.9
EPSILON = 1.0
MIN_EPSILON = 0.01
DECAY_RATE = 0.995

# === Load or Create Q-table ===
if os.path.exists(Q_TABLE_FILE):
    with open(Q_TABLE_FILE, "rb") as f:
        q_table = pickle.load(f)
    print("[📂] Q-table loaded from file.")
else:
    q_table = {}
    print("[🆕] New Q-table initialized.")

# === Port Scan Tracker ===
scan_tracker = {}

# === IP Ban Tracker ===
banned_ips = set()

# === Function to block IP via iptables ===
def ban_ip(ip):
    if ip not in banned_ips:
        try:
            subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
            print(f"[🔥] IP {ip} has been blocked via iptables.")
            banned_ips.add(ip)
        except subprocess.CalledProcessError as e:
            print(f"[⚠️] Failed to ban IP {ip}: {e}")

# === Classify packet reason ===
def classify_reason(packet):
    if packet.haslayer(TCP):
        flags = packet.sprintf("%TCP.flags%")
        src_ip = packet[IP].src
        dst_port = packet[TCP].dport
        now = datetime.now()

        # Port scan detection
        if src_ip not in scan_tracker:
            scan_tracker[src_ip] = []

        scan_tracker[src_ip].append((dst_port, now))
        scan_tracker[src_ip] = [(p, t) for p, t in scan_tracker[src_ip] if (now - t).seconds < 5]

        if len(set([p for p, _ in scan_tracker[src_ip]])) > 10:
            return "port_scan"

        if flags in ["S", "SF", "SR", "SU"]:
            return "suspicious_tcp"

    elif packet.haslayer(UDP) and packet[UDP].dport == 53:
        return "dns_query"
    elif packet.haslayer(ICMP):
        return "icmp_ping"
    return "normal"

# === Encode features ===
def extract_features(packet):
    try:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        reason = classify_reason(packet)

        # Encode with saved LabelEncoders
        src_encoded = encoders["src_ip"].transform([src_ip])[0]
        dst_encoded = encoders["dst_ip"].transform([dst_ip])[0]
        reason_encoded = encoders["reason"].transform([reason])[0]

        df = pd.DataFrame([{
            "src_ip": src_encoded,
            "dst_ip": dst_encoded,
            "reason": reason_encoded
        }])

        return df, reason, src_ip, dst_ip
    except Exception as e:
        print(f"[Encoding Error] {e}")
        return pd.DataFrame(), "normal", "0.0.0.0", "0.0.0.0"

# === Build RL state ===
def get_state(packet, reason):
    ip_type = "bad" if "192.168.1" in packet[IP].src else "good"

    if packet.haslayer(TCP):
        protocol = "TCP"
        dst_port = packet[TCP].dport
    elif packet.haslayer(UDP):
        protocol = "UDP"
        dst_port = packet[UDP].dport
    elif packet.haslayer(ICMP):
        protocol = "ICMP"
        dst_port = 0
    else:
        protocol = "OTHER"
        dst_port = 0

    if dst_port in [80, 443, 22]:
        port_type = "common"
    elif dst_port == 53:
        port_type = "dns"
    elif dst_port == 0:
        port_type = "none"
    else:
        port_type = "random"

    return (reason, ip_type, protocol, port_type)

# === Choose action (Epsilon-greedy) ===
def choose_action(state):
    global EPSILON
    if state not in q_table:
        q_table[state] = {a: 0 for a in ACTIONS}
    if random.uniform(0, 1) < EPSILON:
        return random.choice(ACTIONS)
    return max(q_table[state], key=q_table[state].get)

# === Reward function ===
def get_reward(reason, action, ai_label):
    if reason in ["suspicious_tcp", "icmp_ping", "dns_query", "port_scan"] or ai_label == 1:
        return 1 if action == "block" else -1
    return -1 if action == "block" else 1

# === Q-Table update ===
def update_q_table(state, action, reward):
    old = q_table[state][action]
    q_table[state][action] = old + ALPHA * (reward - old)

# === Log ===
def log_decision(packet, state, action, reward):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()},{packet[IP].src},{packet[IP].dst},{state[0]},{state[1]},{state[2]},{state[3]},{action},{reward}\n")

# === Handle packet ===
def handle_packet(packet):
    global EPSILON

    if IP not in packet or packet[IP].src == "127.0.0.1":
        return

    df, reason, src, dst = extract_features(packet)
    if df.empty:
        return

    ai_label = model.predict(df)[0]
    state = get_state(packet, reason)
    action = choose_action(state)
    reward = get_reward(reason, action, ai_label)

    update_q_table(state, action, reward)
    log_decision(packet, state, action, reward)

    if action == "block":
        ban_ip(src)

    if EPSILON > MIN_EPSILON:
        EPSILON *= DECAY_RATE

    with open(Q_TABLE_FILE, "wb") as f:
        pickle.dump(q_table, f)

    print(f"[RL+AI] {action.upper()} | State: {state} | AI: {ai_label} | Reward: {reward} | Epsilon: {EPSILON:.4f}")

# === Start ===
print("[🤖] RL + AI Firewall is running... Press Ctrl+C to stop.")
try:
    sniff(prn=handle_packet, store=0)
except KeyboardInterrupt:
    with open(Q_TABLE_FILE, "wb") as f:
        pickle.dump(q_table, f)
    print("\n[✔️] Q-table saved. Exiting.")
