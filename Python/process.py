import csv
import json
import re
from collections import Counter

import pandas as pd
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig

# Initialize TemplateMiner with configuration
config = TemplateMinerConfig()
config.load("drain3.ini")
config.profiling_enabled = True
drain_parser = TemplateMiner(config=config)

# Function to extract and write content
def process_log_file(input_file, output_file):
    with open(input_file, "r") as infile:
        log_content = infile.read()
    # Extract the parts enclosed in "||"
    matches = re.findall(r'"timeUnixNano":"(.*?)".*?"body":\{"stringValue":"(.*?)"}', log_content)

    # Write the isolated parts to the output file
    with open(output_file, "w") as outfile:
        for time, body in matches:
            outfile.write(f"TimeUnixNano: {time}, Body: {body}\n")

# Process the log file
process_log_file("../Collector/otel-collector.log","./formatted_log.log")

log_pattern = re.compile(
    r'timeunixnano: (?P<Timestamp>\d+),\s*'  # Match timeunixnano (lowercase) with digits
    r'body:*(?P<Content>.*)'  # Match body wrapped in || and capture the content inside
)

# Step 1: Parse logs and generate templates
templates = {}
parsed_events = []


with open("./formatted_log.log", "r", encoding='utf-8') as f:
    logs = f.readlines()
for i,line in enumerate(logs):
    line = line.lower()
    match = log_pattern.match(line)
    if match :
        log_content = match.group("Content")
        drain_parser.add_log_message(log_content)
    else :
        print(f"No match for line {i}: {line}")

for i,line in enumerate(logs):
    line = line.lower()
    match = log_pattern.match(line)
    if match :
        log_content = match.group("Content")
        result = drain_parser.match(log_content)
        if result :
            print(f"Matched line {i} with template {result.cluster_id}")
            template_id = result.cluster_id
            template_description = result.get_template()
            parsed_events.append({
                "Timestamp": match.group("Timestamp"),
                "Template ID": template_id,
            })
            if template_id not in templates:
                templates[template_id] = template_description
        else :
            print(f"No template found for line {i}: {line}")
    else :
        print(f"No match for line {i}: {line}")

print(f"Found {len(templates)} templates and {len(parsed_events)} parsed events")

parsed_df = pd.DataFrame(parsed_events)
parsed_df.to_csv("parsedlogs.csv", index=False)

template_df = pd.DataFrame(templates.items(), columns=["Template ID", "Template Description"])
template_df.to_csv("templates.csv", index=False)

with open('parsedlogs.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header
    events = [(int(row[0]) // 1_000_000, int(row[1])) for row in csv_reader]  # [(timestamp, event_id), ...]

# Load the JSON file
with open('blocks.json', 'r') as json_file:
    blocks = json.load(json_file)

# Sort events and blocks by timestamp
events.sort(key=lambda x: x[0])
blocks.sort(key=lambda x: x['timestamp'])

# Count events for each block
output_rows = []
event_ids = {event_id for _, event_id in events}  # Unique event IDs for header
for i, block in enumerate(blocks):
    start_time = block['timestamp']
    end_time = blocks[i + 1]['timestamp'] if i + 1 < len(blocks) else float('inf')

    # Count events within the range
    counts = Counter(event_id for timestamp, event_id in events if start_time <= timestamp < end_time)

    # Create a row with the block's timestamp, anomaly, and counts
    row = [block['timestamp'], block['anomaly']]
    row.extend(counts.get(event_id, 0) for event_id in sorted(event_ids))
    output_rows.append(row)

# Write to a new CSV file
header = ['Timestamp', 'Label'] + sorted(event_ids)
with open('output.csv', 'w', newline='') as output_file:
    csv_writer = csv.writer(output_file)
    csv_writer.writerow(header)
    csv_writer.writerows(output_rows)

print("Output CSV created: output.csv")