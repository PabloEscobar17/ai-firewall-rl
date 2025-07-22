import pickle
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

Q_TABLE_PATH = "/root/Desktop/ai-firewall-testing/rl_agent/q_table.pkl"

with open(Q_TABLE_PATH, "rb") as f:
    q_table = pickle.load(f)

# Safely convert Q-table to DataFrame
rows = []
for state, actions in q_table.items():
    if len(state) != 4:
        continue  # skip old-format entries
    try:
        rows.append({
            "reason": state[0],
            "ip_type": state[1],
            "protocol": state[2],
            "port_type": state[3],
            "q_allow": actions.get("allow", 0),
            "q_block": actions.get("block", 0)
        })
    except Exception as e:
        print(f"Skipping bad state: {state} due to error: {e}")

df = pd.DataFrame(rows)

# Compute preference: higher = more likely to block
df["preference"] = df["q_block"] - df["q_allow"]

# Create a pivot table by reason and ip_type
pivot = df.pivot_table(index="reason", columns="ip_type", values="preference", aggfunc="mean")

# Plot
plt.figure(figsize=(8, 6))
sns.heatmap(pivot, annot=True, cmap="coolwarm", center=0)
plt.title("🔥 RL Agent's Block vs Allow Preference")
plt.ylabel("Traffic Reason")
plt.xlabel("Source IP Type")
plt.tight_layout()
plt.show()

