# controller/monitor.py

import subprocess
import requests
import time

CRITICAL_URL = "http://localhost:5000"

def get_container_stats(container_name):
    try:
        result = subprocess.check_output(
            ["docker", "stats", "--no-stream", "--format",
             "{{.CPUPerc}},{{.MemPerc}}", container_name]
        )
        output = result.decode("utf-8").strip().split(",")
        cpu = float(output[0].replace("%", ""))
        memory = float(output[1].replace("%", ""))
        return cpu, memory
    except:
        return 0.0, 0.0

def get_latency():
    try:
        start = time.time()
        requests.get(CRITICAL_URL)
        return (time.time() - start) * 1000
    except:
        return None