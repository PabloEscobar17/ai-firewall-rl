import pandas as pd
import pickle
import os

# === Paths ===
LOG_PATH = "/root/Desktop/ai-firewall-testing/dataset/rl_firewall_log.csv"
Q_TABLE_PATH = "/root/Desktop/ai-firewall-testing/rl_agent/q_table.pkl"

# === Hyperparameters ===
ALPHA = 0.1

# === Load Q-table or initialize ===
if os.path.exists(Q_TABLE_PATH):
    with open(Q_TABLE_PATH, "rb") as f:
        q_table = pickle.load(f)
else:
    q_table = {}

# === Load Logs ===
df = pd.read_csv(LOG_PATH, names=[
    "timestamp", "src", "dst", "reason", "ip_type", "protocol", "port_type", "action", "reward"
])

# === Train Q-table ===
for _, row in df.iterrows():
    state = (row["reason"], row["ip_type"], row["protocol"], row["port_type"])
    action = row["action"]
    reward = row["reward"]

    if pd.isna(action) or pd.isna(reward):
        continue  # Skip bad rows

    if state not in q_table:
        q_table[state] = {"allow": 0, "block": 0}

    current_q = q_table[state][action]
    updated_q = current_q + ALPHA * (reward - current_q)
    q_table[state][action] = updated_q

# === Save Trained Q-table ===
with open(Q_TABLE_PATH, "wb") as f:
    pickle.dump(q_table, f)

print("✅ Q-table trained from historical logs and saved.")
