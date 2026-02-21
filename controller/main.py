# controller/main.py

import time
import random
import subprocess

from monitor import get_container_stats, get_latency
from model.predictor import detect_states
from decision_engine import decide_actions
from actuator import update_cpu, update_memory, update_priority
from database import init_db, insert_metric

CHECK_INTERVAL = 3
SPIKE_DURATION = 12

def cpu_spike():
    subprocess.Popen(
        ["docker", "exec", "cpu_stress",
         "stress", "--cpu", "4", "--timeout", str(SPIKE_DURATION)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def memory_spike():
    subprocess.Popen(
        ["docker", "exec", "memory_stress",
         "stress", "--vm", "1",
         "--vm-bytes", "600M",
         "--timeout", str(SPIKE_DURATION)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

print("\n🚀 Correct Multi-Condition Detection System Started (MongoDB Version)\n")

# Initialize DB connection
init_db()

while True:
    try:
        r = random.random()

        # Random Chaos Generation
        if r < 0.70:
            pass # Normal
        elif r < 0.80:
            cpu_spike()
        elif r < 0.90:
            memory_spike()
        else:
            cpu_spike()
            memory_spike()

        # Wait briefly so stress actually starts
        time.sleep(1)

        # 1. MONITOR
        total_cpu = 0
        total_memory = 0

        for container in ["cpu_stress", "memory_stress"]:
            cpu, memory = get_container_stats(container)
            total_cpu += cpu
            total_memory += memory

        latency = get_latency()
        if latency is None: latency = 0 # Handle timeout

        print("--------------------------------------------------")
        print(f"CPU Usage     : {total_cpu:.2f}%")
        print(f"Memory Usage  : {total_memory:.2f}%")
        print(f"Latency       : {latency:.2f} ms")

        # 2. DETECT
        states = detect_states(total_cpu, total_memory, latency)

        print("Detected Issues:")
        for s in states:
            print(f" - {s}")

        # 3. RECORD (Save to MongoDB)
        insert_metric(total_cpu, total_memory, latency, states)

        # 4. MITIGATE (Actuator)
        for s in states:
            actions = decide_actions(s)
            for action_type, value in actions:
                print(f"   >>> ACTION: {action_type} -> {value}")
                if action_type == "cpu_throttle":
                    update_cpu("cpu_stress", value)
                elif action_type == "memory_limit":
                    update_memory("memory_stress", value)
                elif action_type == "boost_priority":
                    update_priority("critical_service", value)

        time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopped manually.")
        break