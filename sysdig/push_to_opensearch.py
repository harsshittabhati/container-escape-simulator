
import requests
import json

OPENSEARCH_URL = "https://1<OPENSEARCH_IP_ADDRESS>:9200"
INDEX_NAME = "sysdig_alerts"
AUTH = ('<Your_Username>', '<Your_Password>')

def create_index():
    index_config = {
        "mappings": {
            "properties": {
                "timestamp": {"type": "date", "format": "HH:mm:ss.SSSSSSSSS"},
                "rule": {"type": "keyword"},
                "priority": {"type": "keyword"},
                "user": {"type": "keyword"},
                "process": {"type": "keyword"},
                "command": {"type": "keyword"},
                "output": {"type": "text"}
            }
        }
    }
    res = requests.put(f"{OPENSEARCH_URL}/{INDEX_NAME}", auth=AUTH, json=index_config, verify=False)
    print("Index creation response:", res.status_code, res.text)

def push_alert(alert):
    res = requests.post(f"{OPENSEARCH_URL}/{INDEX_NAME}/_doc", auth=AUTH, json=alert, verify=False)
    if res.status_code == 201:
        print(f"Alert sent: {alert['timestamp']}")
    else:
        print("Failed to send alert:", res.text)

def parse_sysdig_log(file_path):
    alerts = []
    with open(file_path, 'r') as f:
        for line in f:
            # Assuming the Sysdig alert log line format; parse accordingly
            # Example line (you need to adjust parsing):
            # 13:47:43.787418582 Container escape detected: mount by user root process mount
            parts = line.strip().split('|')
            if len(parts) < 2:
                continue
            timestamp = parts[0].strip()
            output = parts[1].strip()
            # Extract fields from output by your known pattern or regex
            alert = {
                "timestamp": timestamp,
                "rule": "sysdig_alert",
                "priority": "unknown",  # or extract priority if available
                "user": "unknown",
                "process": "unknown",
                "command": "unknown",
                "output": output
            }
            alerts.append(alert)
    return alerts

def main():
    create_index()
    alerts = parse_sysdig_log('/var/log/sysdig.log')  # Your actual Sysdig alerts log file path
    for alert in alerts:
        push_alert(alert)

if __name__ == "__main__":
    main()
