import json, os, hashlib
from datetime import datetime

# Load arrest timeline (mock example)
arrest_events = [
    {"name": "John Doe", "timestamp": "2025-09-03T19:24:00Z", "location": "Golden Valley"},
    {"name": "Jane Smith", "timestamp": "2025-09-02T18:00:00Z", "location": "Kingman"}
]

# Load latest trace file
trace_files = sorted([f for f in os.listdir("logs") if f.startswith("trace_")], reverse=True)
latest = trace_files[0]
with open(f"logs/{latest}", "r") as f:
    trace = json.load(f)

# Correlate by timestamp proximity (±5 seconds)
trace_time = datetime.fromisoformat(trace["timestamp"].replace("Z", "+00:00"))
correlated = []
for event in arrest_events:
    event_time = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
    delta = abs((trace_time - event_time).total_seconds())
    if delta <= 5:
        correlated.append(event)

# Prepare output
os.makedirs("correlations", exist_ok=True)
output = {
    "trace_file": latest,
    "trace": trace,
    "correlated_events": correlated,
    "timestamp": datetime.utcnow().isoformat()
}

# Hash for integrity
hash = hashlib.sha256(json.dumps(output).encode()).hexdigest()
output["hash"] = hash

# Save result
filename = f"correlations/correlation_{int(datetime.utcnow().timestamp())}.json"
with open(filename, "w") as f:
    json.dump(output, f, indent=2)

print(f"Correlation written to {filename}")
