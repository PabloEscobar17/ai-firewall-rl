import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
import os

# === Paths ===
LOG_PATH = "/root/Desktop/ai-firewall-testing/dataset/rl_firewall_log.csv"
ENCODER_PATH = "/root/Desktop/ai-firewall-testing/ai_model/encoders.pkl"

# === Read CSV safely, skipping corrupted lines ===
df = pd.read_csv(
    LOG_PATH,
    header=None,
    names=[
        "timestamp", "src_ip", "dst_ip", "reason",
        "ip_type", "protocol", "port_type", "action", "reward"
    ],
    on_bad_lines='skip'
)

# === Fit LabelEncoders ===
encoders = {}
for col in ["src_ip", "dst_ip", "reason"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    encoders[col] = le

# === Save encoders ===
os.makedirs(os.path.dirname(ENCODER_PATH), exist_ok=True)
joblib.dump(encoders, ENCODER_PATH)
print(f"[✅] Encoders saved to: {ENCODER_PATH}")
