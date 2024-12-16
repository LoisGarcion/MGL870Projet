import csv
import json
import re
import sys
import time
from collections import Counter
import pandas as pd
import requests
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.preprocessing import StandardScaler
import logging

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1310721596452896879/tilIJNiZnbYHRnnT6PqE5FBmLYAee4Mi0piu5EKkRHenhjN-3Vq53GXstsBbt17c4OYc"
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def send_discord_alert(message):
    """Send an alert message to a Discord webhook."""
    payload = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code == 204:  # 204 No Content means success
        logging.info("Alert sent to Discord!")
    else:
        logging.info(f"Failed to send alert to Discord. Status code: {response.status_code}")
        logging.info(f"Response: {response.text}")

# Load the data
df = pd.read_csv("event_matrix.csv")

# Split the data into 60% training, 20% validation, and 20% testing
train_size = int(0.60 * len(df))
val_size = int(0.20 * len(df))

# Adjusted Splits for Time-Series Data
train_df = df.iloc[:train_size]
val_df = df.iloc[train_size:train_size + val_size]
test_df = df.iloc[train_size + val_size:]

# Separate features and labels
X_train = train_df.drop(columns=['File', 'Label'])  # Features
y_train = train_df['Label'].astype(int)  # Labels

X_val = val_df.drop(columns=['File', 'Label'])
y_val = val_df['Label'].astype(int)

X_test = test_df.drop(columns=['File', 'Label'])
y_test = test_df['Label'].astype(int)

# Feature names for later use
feature_names = X_train.columns

# Scale the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)
X_test = scaler.transform(X_test)

# Train Random Forest
rf_model = RandomForestClassifier(class_weight='balanced', random_state=42)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict_proba(X_test)[:, 1]

# Evaluate model
def evaluate_model(y_true, y_pred, model_name, threshold):
    pred = (y_pred >= threshold).astype(int)
    accuracy = accuracy_score(y_true, pred)
    precision = precision_score(y_true, pred)
    recall = recall_score(y_true, pred)
    auc = roc_auc_score(y_true, y_pred)

    logging.info(f"Performance of {model_name}:")
    logging.info(f"Accuracy: {accuracy:.4f}")
    logging.info(f"Precision: {precision:.4f}")
    logging.info(f"Recall: {recall:.4f}")
    logging.info(f"AUC: {auc:.4f}")
    logging.info('-' * 30)

evaluate_model(y_test, rf_pred, f"Random Forest", threshold=0.5)

# LIVE DETECTION PART
LOKI_URL = "http://loki:3100/loki/api/v1/query_range"
QUERY = '{exporter="OTLP"}'

def fetch_logs():
    # Calculate the time range for the last 1 minute
    current_time_ns = int(time.time() * 1e9)  # Current time in nanoseconds
    ten_minutes_ago_ns = current_time_ns - int(10 * 60 * 1e9)  # 10 minutes ago in nanoseconds

    # Update the query to include the time range
    params = {
        'query': QUERY,
        'start': ten_minutes_ago_ns,
        'end': current_time_ns,
        'limit': 3000
    }

    response = requests.get(LOKI_URL, params=params)
    logging.info(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        logs = response.json()
        with open('logs.json', 'w') as f:
            json.dump(logs, f, indent=4)
        return True
    else:
        logging.info(f"Error fetching logs: {response.text}")
        return False

def extract_body_to_csv(input_file, output_file):
    with open(input_file, "r") as infile:
        data = json.load(infile)

    # Navigate to the "values" field in the JSON
    results = data.get("data", {}).get("result", [])

    # Extract the "body" field from each log entry
    bodies = []
    for result in results:
        for value in result.get("values", []):
            log_entry = json.loads(value[1])  # Parse the JSON string in the second element
            body = log_entry.get("body")
            if body:
                bodies.append([body])

    # Write the extracted "body" values to a CSV file
    with open(output_file+".csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(bodies)

config = TemplateMinerConfig()
config.profiling_enabled = True
drain_parser = TemplateMiner(config=config)

# Log pattern for parsing log content
log_pattern = re.compile(
    r'(?P<Content>.*)'
)
log_pattern_no_quotes_db = re.compile(
    r'^(?P<Date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+ gmt) '  # Matches timestamp
    r'\[\d+\] (?:notice|log|error|warning|info|debug):\s+'  # Matches log level
    r'(?P<Content>.+)$'  # Matches the log message content
)

log_pattern_with_quotes_db = re.compile(
    r'^"(?P<Date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+ gmt) '  # Matches timestamp inside quotes
    r'\[\d+\] (?:notice|log|error|warning|info|debug):\s+'  # Matches log level
    r'(?P<Content>.+)"$'  # Matches log message content and ensures it ends with a quote
)

# Function to process log files and label events
def process_logs(filepath):
    events = []
    with open("templates.csv", "r", encoding="utf-8") as f:
        templates = f.readlines()
        for template in templates:
            drain_parser.add_log_message(template)
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        logs = f.readlines()
        for line in logs:
            line = line.strip().lower()
            match = log_pattern_no_quotes_db.match(line)
            if match:
                log_content = match.group("Content")
                result = drain_parser.add_log_message(log_content)
            else:
                match = log_pattern_with_quotes_db.match(line)
                if match:
                    log_content = match.group("Content")
                    result = drain_parser.add_log_message(log_content)
                else:
                    match = log_pattern.match(line)
                    if match:
                        log_content = match.group("Content")
                        result = drain_parser.add_log_message(log_content)

        for line in logs:
            line = line.strip().lower()
            match = log_pattern_no_quotes_db.match(line)
            if match:
                log_content = match.group("Content")
                result = drain_parser.match(log_content)
                if result:
                    events.append({
                        "Template ID": result.cluster_id,
                    })
            else:
                match = log_pattern_with_quotes_db.match(line)
                if match:
                    log_content = match.group("Content")
                    result = drain_parser.match(log_content)
                    if result:
                        events.append({
                            "Template ID": result.cluster_id,
                        })
                else:
                    match = log_pattern.match(line)
                    if match:
                        log_content = match.group("Content")
                        result = drain_parser.match(log_content)
                        if result:
                            events.append({
                                "Template ID": result.cluster_id,
                            })
    return events


while True:
    success = fetch_logs()
    if success:
        extract_body_to_csv('logs.json', 'live_logs')
        events = process_logs("live_logs.csv")

        # Define the full range of template IDs
        template_ids = list(range(1, 108))

        # Count occurrences of each Template ID from processed logs
        template_counts = Counter(event["Template ID"] for event in events)

        # Ensure all template IDs are represented
        counts = [template_counts.get(template_id, 0) for template_id in template_ids]

        # Write to a CSV file
        with open("template_counts.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(counts)  # Second row: Counts

        logging.info("Updated template_counts.csv")

        # Load the template counts CSV and set column names to match X_train
        df = pd.read_csv("template_counts.csv", header=None)

        # Assign feature names based on X_train columns
        df.columns = feature_names  # Ensure the feature names match those used in training

        # Extract the feature values (drop any irrelevant columns)
        X_live = df[feature_names].values  # Ensure we're using the correct features

        # Make predictions with the trained model
        prediction = rf_model.predict_proba(X_live)[:, 1]
        logging.info(f"Prediction: {prediction}")
        if prediction >= 0.3:
            logging.info("Anomaly Detected!")
            send_discord_alert("Anomaly Detected!")
        else:
            logging.info("No Anomaly Detected")

    time.sleep(20)  # Fetch logs every minute
