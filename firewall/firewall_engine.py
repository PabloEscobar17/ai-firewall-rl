from scapy.all import sniff, IP, TCP, UDP, ICMP
from datetime import datetime
import joblib
import pandas as pd
import ipaddress
import os

# === Paths ===
MODEL_PATH = "/root/Desktop/ai-firewall-testing/ai_model/firewall_model.pkl"
ENCODER_PATH = "/root/Desktop/ai-firewall-testing/ai_model/reason_encoder.pkl"
COLUMNS_PATH = "/root/Desktop/ai-firewall-testing/ai_model/model_columns.pkl"
LOG_FILE = "/root/Desktop/ai-firewall-testing/dataset/traffic_log.csv"

# === Load Model, Encoder, Columns ===
model = joblib.load(MODEL_PATH)
reason_encoder = joblib.load(ENCODER_PATH)
model_columns = joblib.load(COLUMNS_PATH)

# === Feature Extraction ===
def extract_features(packet, reason):
    return {
        "timestamp": str(datetime.now()),
        "src_ip": packet[IP].src,
        "dst_ip": packet[IP].dst,
        "reason": reason
    }

# === Preprocessing for Model ===
def preprocess_for_model(pkt_dict):
    try:
        src_ip = int(ipaddress.IPv4Address(pkt_dict["src_ip"]))
        dst_ip = int(ipaddress.IPv4Address(pkt_dict["dst_ip"]))
        reason_encoded = reason_encoder.transform([pkt_dict["reason"]])[0]
    except Exception as e:
        print(f"[!] Preprocessing failed: {e}")
        return pd.DataFrame()

    df = pd.DataFrame([{
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "reason": reason_encoded
    }])
    # Ensure column order matches training
    df = df[model_columns]
    return df

# === Logging & Action ===
def log_and_block(pkt_dict, decision):
    log_line = f'{pkt_dict["timestamp"]},{pkt_dict["src_ip"]},{pkt_dict["dst_ip"]},{pkt_dict["reason"]},{decision}'
    with open(LOG_FILE, "a") as f:
        f.write(log_line + "\n")
    print(f"[!] {decision.upper()}: {pkt_dict['src_ip']} → {pkt_dict['dst_ip']} | Reason: {pkt_dict['reason']}")

# === Main Classifier ===
def classify_packet(packet, reason):
    pkt_data = extract_features(packet, reason)
    df = preprocess_for_model(pkt_data)
    if df.empty:
        return

    prediction = model.predict(df)[0]
    label = "attack" if prediction == 1 else "normal"
    log_and_block(pkt_data, label)

# === Sniffer Callback ===
def packet_callback(packet):
    if IP not in packet or packet[IP].src == "127.0.0.1":
        return

    if TCP in packet:
        flags = packet.sprintf("%TCP.flags%")
        if flags in ["S", "SF", "SR", "SU", "SFP", "SFRPU"]:
            classify_packet(packet, f"Suspicious TCP flags: {flags}")
            return

    if ICMP in packet:
        classify_packet(packet, "ICMP packet (Ping) detected")
        return

    if UDP in packet and packet[UDP].dport == 53:
        classify_packet(packet, "DNS query detected")
        return

# === Start Sniffing ===
print("[+] AI-Powered Firewall Engine running... Press Ctrl+C to stop.")
sniff(prn=packet_callback, store=0)
