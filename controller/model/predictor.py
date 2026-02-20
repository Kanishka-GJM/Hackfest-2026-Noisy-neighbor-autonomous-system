# controller/model/predictor.py

def detect_states(cpu, memory, latency):
    """
    Multi-condition detection.
    Each resource is evaluated independently.
    Allows natural combinations.
    """

    cpu_flag = cpu > 120          # CPU spike threshold
    memory_flag = memory > 40     # Memory pressure threshold
    latency_flag = latency > 200  # Latency anomaly threshold

    states = []

    if cpu_flag:
        states.append("CPU_CONTENTION")

    if memory_flag:
        states.append("MEMORY_PRESSURE")

    if latency_flag:
        states.append("LATENCY_ANOMALY")

    if not states:
        states.append("NORMAL")

    return states