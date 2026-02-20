# controller/decision_engine.py

def decide_actions(state):

    actions = []

    if state == "CPU_CONTENTION":
        actions.append(("cpu_throttle", 0.5))

    elif state == "MEMORY_PRESSURE":
        actions.append(("memory_limit", "256m"))

    elif state == "LATENCY_ANOMALY":
        actions.append(("boost_priority", 2048))

    elif state == "MULTI_RESOURCE_CONTENTION":
        actions.append(("cpu_throttle", 0.5))
        actions.append(("memory_limit", "256m"))
        actions.append(("boost_priority", 2048))

    return actions