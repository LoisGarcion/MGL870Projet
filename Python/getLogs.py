import requests
import json
import re
import time

from pandas.io.common import file_exists

LOKI_URL = "http://localhost:54667/loki/api/v1/query_range"
QUERY = '{exporter="OTLP"}'

def fetch_logs():
    # Calculate the time range for the last 1 minute
    current_time_ns = int(time.time() * 1e9)  # Current time in nanoseconds
    one_minute_ago_ns = current_time_ns - int(6000 * 1e9)  # One minute ago in nanoseconds

    # Update the query to include the time range
    params = {
        'query': QUERY,
        'start': one_minute_ago_ns,
        'end': current_time_ns
    }

    response = requests.get(LOKI_URL, params=params)
    print(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        logs = response.json()
        with open('logs.json', 'w') as f:
            json.dump(logs, f, indent=4)
    else:
        print(f"Error fetching logs: {response.text}")

import json
import csv

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
    if IS_ANOMALY == 0:
        output_file = output_file = "./normalLogs/"+output_file
    else:
        output_file = output_file = "./anomalyLogs/"+output_file
    cpt = 0
    while file_exists(output_file+str(cpt)+".csv"):
        cpt+= 1
    with open(output_file+str(cpt)+".csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(bodies)

IS_ANOMALY = 1

# Example usage
fetch_logs()
extract_body_to_csv("logs.json", "bodies")
