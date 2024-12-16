import os
import csv
import re
from collections import Counter
import pandas as pd
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig

# Initialize TemplateMiner
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

# Directories
anomaly_dir = "anomalyLogs"
normal_dir = "normalLogs"

# Function to process log files and label events
def process_logs(directory, label):
    events = []
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
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
                            "File": file_name,
                            "Template ID": result.cluster_id,
                            "Label": label
                        })
                else:
                    match = log_pattern_with_quotes_db.match(line)
                    if match:
                        log_content = match.group("Content")
                        result = drain_parser.match(log_content)
                        if result:
                            events.append({
                                "File": file_name,
                                "Template ID": result.cluster_id,
                                "Label": label
                            })
                    else:
                        match = log_pattern.match(line)
                        if match:
                            log_content = match.group("Content")
                            result = drain_parser.match(log_content)
                            if result:
                                events.append({
                                    "File": file_name,
                                    "Template ID": result.cluster_id,
                                    "Label": label
                                })
    return events

# Process anomaly and normal logs
anomaly_events = process_logs(anomaly_dir, label=1)
normal_events = process_logs(normal_dir, label=0)

# Combine and count events
events = anomaly_events + normal_events
event_counts = Counter((event["File"], event["Template ID"]) for event in events)

# Create a matrix with files as rows and templates as columns
files = set(event["File"] for event in events)
templates = set(event["Template ID"] for event in events)

matrix = []
for file_name in files:
    print(f"Processing {file_name}")
    row = [file_name, 1 if file_name in [e["File"] for e in anomaly_events] else 0]  # Label based on anomaly or normal
    row.extend(event_counts.get((file_name, template), 0) for template in templates)
    matrix.append(row)

# Write matrix to CSV
header = ["File", "Label"] + [f"Template_{template}" for template in templates]
output_file = "event_matrix.csv"

with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(matrix)

print(f"Event matrix saved to {output_file}")

# Write templates to a CSV file
template_descriptions = [(cluster.cluster_id, cluster.get_template()) for cluster in drain_parser.drain.clusters]
templates_file = "templates.csv"

with open(templates_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Template ID", "Template Description"])
    writer.writerows(template_descriptions)

print(f"Templates saved to {templates_file}")
