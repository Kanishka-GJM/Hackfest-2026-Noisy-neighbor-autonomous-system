# controller/actuator.py

import subprocess

def update_cpu(container, cpu_value):
    subprocess.call(
        ["docker", "update", f"--cpus={cpu_value}", container],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print(f"CPU updated for {container}")

def update_memory(container, memory_limit):
    subprocess.call(
        ["docker", "update",
         f"--memory={memory_limit}",
         f"--memory-swap={memory_limit}",
         container],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print(f"Memory updated for {container}")

def update_priority(container, shares):
    subprocess.call(
        ["docker", "update", f"--cpu-shares={shares}", container],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print(f"Priority boosted for {container}")