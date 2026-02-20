# controller/main.py

import time
import random
import subprocess

from .monitor import get_container_stats, get_latency
from .model.predictor import detect_states

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

print("\n🚀 Correct Multi-Condition Detection System Started\n")

while True:
    try:
        r = random.random()

        # 70% NORMAL
        # 10% CPU
        # 10% MEMORY
        # 10% CPU + MEMORY

        if r < 0.70:
            pass

        elif r < 0.80:
            cpu_spike()

        elif r < 0.90:
            memory_spike()

        else:
            cpu_spike()
            memory_spike()

        # Wait briefly so stress actually starts
        time.sleep(1)

        total_cpu = 0
        total_memory = 0

        for container in ["cpu_stress", "memory_stress"]:
            cpu, memory = get_container_stats(container)
            total_cpu += cpu
            total_memory += memory

        latency = get_latency()

        print("--------------------------------------------------")
        print(f"CPU Usage     : {total_cpu:.2f}%")
        print(f"Memory Usage  : {total_memory:.2f}%")
        print(f"Latency       : {latency:.2f} ms")

        states = detect_states(total_cpu, total_memory, latency)

        print("Detected Issues:")
        for s in states:
            print(f" - {s}")

        time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopped manually.")
        break