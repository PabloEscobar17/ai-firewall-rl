import pandas as pd
import os

log_file = "/root/Desktop/ai-firewall-testing/dataset/traffic_log.csv"
output_file = "/root/Desktop/ai-firewall-testing/dataset/dataset.csv"

if not os.path.exists(log_file):
    print("Log file not found!")
    exit()

# Load the CSV file properly
df = pd.read_csv(log_file)

# Add label column based on reason
def label_row(reason):
    if any(keyword in reason for keyword in ["Blacklisted", "Suspicious", "ICMP", "DNS"]):
        return "attack"
    else:
        return "normal"

df["label"] = df["reason"].apply(label_row)

# Save to dataset
df.to_csv(output_file, index=False)
print(f"[+] Dataset saved to {output_file}")

