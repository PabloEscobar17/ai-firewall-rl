import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import ipaddress

# Load data
df = pd.read_csv("/root/Desktop/ai-firewall-testing/dataset/dataset.csv")

# Drop timestamp
df = df.drop(columns=["timestamp"])

# Convert IPs to integers (better than label encoding)
df["src_ip"] = df["src_ip"].apply(lambda x: int(ipaddress.IPv4Address(x)))
df["dst_ip"] = df["dst_ip"].apply(lambda x: int(ipaddress.IPv4Address(x)))

# Encode 'reason' and save the encoder
reason_encoder = LabelEncoder()
df["reason"] = reason_encoder.fit_transform(df["reason"])
joblib.dump(reason_encoder, "/root/Desktop/ai-firewall-testing/ai_model/reason_encoder.pkl")

# Encode label column
df["label"] = df["label"].apply(lambda x: 1 if x == "attack" else 0)

# Prepare features and target
X = df[["src_ip", "dst_ip", "reason"]]
y = df["label"]

# Save column order for real-time inference
joblib.dump(X.columns.tolist(), "/root/Desktop/ai-firewall-testing/ai_model/model_columns.pkl")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save model
model_path = "/root/Desktop/ai-firewall-testing/ai_model/firewall_model.pkl"
joblib.dump(clf, model_path)
print(f"Model saved to: {model_path}")

