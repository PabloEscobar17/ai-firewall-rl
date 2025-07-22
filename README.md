# AI-Driven Adaptive Firewall 🚀

A hybrid firewall combining Reinforcement Learning and AI-based real-time classification to block network threats dynamically.

## 🔒 Features
- Detects and blocks SYN Floods, UDP Floods, DNS Amplification, ICMP Pings, Port Scans
- Adaptive decision-making using RL (Q-Learning)
- AI classifier trained on historical logs
- Live Q-table training
- Real-time dashboard for monitoring

## 📁 Project Structure
- `rl_agent/` → Q-learning firewall
- `ai_model/` → Trained ML model and encoders
- `attacks/` → Simulated attack scripts
- `dataset/` → Packet logs and training data
- `dashboard/` → Flask-based log visualizer
- `attacker_agent.py` → Simulated attacker script

## 📦 Setup
```bash
pip install -r requirements.txt
sudo python3 rl_agent/rl_firewall.py

🧠 Authors

S Arjuna Sharma
Shreyas MV


Then commit & push:

```bash
git add README.md
git commit -m "📝 Added README"
git push

