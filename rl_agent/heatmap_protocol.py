import pickle
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

Q_TABLE_PATH = "/root/Desktop/ai-firewall-testing/rl_agent/q_table.pkl"

with open(Q_TABLE_PATH, "rb") as f:
    q_table = pickle.load(f)

# Convert Q-table to DataFrame
rows = []
for state, actions in q_table.items():
    if len(state) == 4:
        rows.append({
            "reason": state[0],
            "ip_type": state[1],
            "protocol": state[2],
            "port_type": state[3],
            "q_allow": actions["allow"],
            "q_block": actions["block"]
        })

df = pd.DataFrame(rows)
df["preference"] = df["q_block"] - df["q_allow"]

# Pivot on reason vs protocol
pivot = df.pivot_table(index="reason", columns="protocol", values="preference", aggfunc="mean")
sns.heatmap(pivot, annot=True, cmap="coolwarm", center=0)
plt.title("🔥 RL Agent Preference (Reason vs Protocol)")
plt.ylabel("Traffic Reason")
plt.xlabel("Protocol")
plt.tight_layout()
plt.show()
