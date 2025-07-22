# 🔥 AI-Driven Adaptive Firewall Using Reinforcement Learning and Real-Time Threat Classification

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This project presents a smart, self-learning firewall that dynamically evolves by combining **Reinforcement Learning (RL)** and a **real-time AI classifier** to detect and defend against multiple real-world network attacks.

Developed by **S Arjuna Sharma** and **Shreyas MV**

---

## 🚀 Key Features

- ✅ Detects and defends against 8+ common network attacks
- ✅ Combines Reinforcement Learning (Q-Learning) with a lightweight AI classifier
- ✅ Real-time packet sniffing and dynamic defense
- ✅ Live web dashboard showing latest packet decisions
- ✅ Adaptive learning using reward feedback and log training
- ✅ AI predicts threats using features like source, destination, protocol, etc.
- ✅ Detects stealthy behaviors like **Port Scanning**, **DNS Amplification**, and more

---

## 📁 Project Structure

```bash
ai-firewall-rl/
│
├── rl_agent/                  # RL Firewall logic
│   ├── rl_firewall.py         # Final combined RL+AI firewall
│   ├── train_from_logs.py     # Train Q-table using historical logs
│   ├── visualize_q_table.py   # Visual heatmap of Q-table states
│   └── attacker_agent.py      # Random attack launcher using subprocess
│
├── ai_model/                  # AI threat classifier
│   ├── train_classifier.py    # Train model from logs
│   ├── generate_encoders.py   # Label encode categorical features
│   └── firewall_model.pkl     # Trained AI model
│
├── attacks/                   # All attack scripts (SYN, ICMP, Slowloris, etc.)
│
├── dashboard/                 
│   └── index.html             # Live log viewer (Jinja2 rendered)
│
├── dataset/
│   └── rl_firewall_log.csv    # Logged decisions + features + rewards
│
├── main.py                    # CLI launcher for all attacks
└── README.md


## ⚙️ Setup Instructions

-1. Clone the repo
-git clone https://github.com/PabloEscobar17/ai-firewall-rl.git
-cd ai-firewall-rl

-2. Install Dependencies
-Ensure you're on Kali Linux or a Debian-based distro.
-sudo apt update
-sudo apt install python3-pip
-pip3 install -r requirements.txt

-Required Python packages:
-pip3 install scapy pandas joblib seaborn matplotlib flask

-3. Run the RL + AI Firewall
-cd rl_agent
-sudo python3 rl_firewall.py

-4. Launch Attacks for Testing (in a second terminal)
-sudo python3 main.py / sudo python3 attacker_agent.py





