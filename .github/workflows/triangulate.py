import json, time
from datetime import datetime

sample_trace = {
    "timestamp": datetime.utcnow().isoformat(),
    "mac": "00:1A:2B:3C:4D:5E",
    "ssid": "GNEKOW-COWENS-NODE",
    "vendor": "Ubiquiti Networks"
}

with open("logs/trace_" + str(int(time.time())) + ".json", "w") as f:
    json.dump(sample_trace, f, indent=2)
