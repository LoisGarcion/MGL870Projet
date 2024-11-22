import re
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
        print(f"log_content: {log_content}")
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
