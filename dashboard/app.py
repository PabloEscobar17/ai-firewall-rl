import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    LOG_PATH = "/root/Desktop/ai-firewall-testing/dataset/rl_firewall_log.csv"
    try:
        df = pd.read_csv(LOG_PATH, names=[
            "timestamp", "src", "dst", "reason", "ip_type", "protocol", "port_type", "action", "reward"]
        )
        last_50 = df.tail(50).to_dict(orient="records")
    except Exception as e:
        last_50 = []
        print(f"[!] Log file error: {e}")

    return render_template("index.html", logs=last_50)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)

