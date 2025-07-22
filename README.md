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
├── rl_agent/
│   ├── rl_firewall.py
│   ├── train_from_logs.py
│   ├── visualize_q_table.py
│   └── attacker_agent.py
├── ai_model/
│   ├── train_classifier.py
│   ├── generate_encoders.py
│   └── firewall_model.pkl
├── attacks/
├── dashboard/
│   └── index.html
├── dataset/
│   └── rl_firewall_log.csv
├── main.py
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/PabloEscobar17/ai-firewall-rl.git
cd ai-firewall-rl
```

### 2. Install Dependencies

```bash
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt
```

Or manually:

```bash
pip3 install scapy pandas joblib seaborn matplotlib flask
```

---

### 3. Run the RL + AI Firewall

```bash
cd rl_agent
sudo python3 rl_firewall.py
```

> Starts packet sniffing, RL decision-making, and real-time logging.

---

### 4. Launch Attacks (For Testing)

```bash
sudo python3 main.py
```

Choose any of the following from CLI:
- SYN Flood  
- ICMP Flood  
- UDP Flood  
- HTTP GET Flood  
- Slowloris  
- DNS Amplification  
- Port Scan (auto-detected)  

---

## 📊 Live Dashboard

```bash
cd dashboard
python3 -m http.server 8080
```

View at: [http://localhost:8080](http://localhost:8080)

---


## 📈 Results

| Attack Type       | Detection | Block Accuracy |
|------------------|-----------|----------------|
| SYN Flood        | ✅        | 98%            |
| ICMP Flood       | ✅        | 96%            |
| UDP Flood        | ✅        | 95%            |
| DNS Amplification| ✅        | 94%            |
| Port Scan        | ✅        | Adaptive       |
| Slowloris        | ✅        | 93%            |

---

## 📄 License

MIT License. Free to use and extend with credit.

---

## 🔗 Authors

- [S Arjuna Sharma](mailto:arjunsharma7804@gmail.com) — [LinkedIn](https://www.linkedin.com/in/s-arjuna-sharma-83617033a/)  
- Shreyas MV






