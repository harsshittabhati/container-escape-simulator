import re
import json

# Path to Sysdig escape log (converted to plain text earlier)
log_path = "escape_logs.txt"
output_json = "escape_alerts.json"

# Keywords to watch for
escape_keywords = ["mount", "/bin/bash", "/usr/bin/bash", "sh", "/bin/sh"]

alerts = []

with open(log_path, "r") as f:
    for line in f:
        for keyword in escape_keywords:
            if f" {keyword}" in line:
                alert = {
                    "timestamp": line.split()[0],
                    "user": re.search(r"uid=\d+\((.*?)\)", line),
                    "process": re.search(r"\scomm=(\S+)", line),
                    "command": keyword,
                    "severity": "high" if keyword in ["mount"] else "medium"
                }
                alert["user"] = alert["user"].group(1) if alert["user"] else "<NA>"
                alert["process"] = alert["process"].group(1) if alert["process"] else "<NA>"
                alerts.append(alert)

# Save to JSON
with open(output_json, "w") as outfile:
    json.dump(alerts, outfile, indent=4)

print(f"✅ Total container escape alerts found: {len(alerts)}")
for a in alerts:
    print(f"[!] {a['timestamp']} | User: {a['user']} | Process: {a['process']} | Command: {a['command']} | Severity: {a['severity']}")

