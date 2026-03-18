# 🔊 Proactive Noisy Neighbour — Autonomous Mitigation System

> An intelligent, self-healing system that **detects and autonomously mitigates noisy neighbour interference** in containerised environments using real-time monitoring, ML-based state detection, and Docker-level actuation.

---

## 📌 Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Running the Dashboard](#running-the-dashboard)
- [Detected States](#detected-states)
- [Mitigation Actions](#mitigation-actions)
- [Retraining the Model](#retraining-the-model)
- [Tech Stack](#tech-stack)

---

## Overview

The **Noisy Neighbour Problem** occurs in shared containerised environments where one container monopolises CPU, memory, or network resources — degrading the performance of co-located services.

This system takes a **proactive, closed-loop approach**:

1. **Monitors** Docker container resource usage and service latency in real time.
2. **Detects** abnormal states using a trained ML model and rule-based thresholds.
3. **Decides** the best mitigation action based on the detected state.
4. **Acts** by applying Docker resource constraints to throttle the offending containers.
5. **Persists** all metrics into MongoDB for historical analysis and dashboard visualisation.

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                        MAPE-K Control Loop                      │
│                                                                 │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐  │
│   │ MONITOR  │───▶│  DETECT  │───▶│  DECIDE  │───▶│   ACT   │  │
│   │          │    │          │    │          │    │         │  │
│   │ CPU/Mem/ │    │ ML Model │    │ Decision │    │ Docker  │  │
│   │ Latency  │    │ + Rules  │    │ Engine   │    │ Update  │  │
│   └──────────┘    └──────────┘    └──────────┘    └─────────┘  │
│         │                                               │       │
│         └─────────────── MongoDB ─────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

Every **3 seconds**, the controller:
- Randomly injects chaos (CPU spike, memory spike, or both) via the stress containers
- Reads resource stats for `cpu_stress` and `memory_stress` containers
- Measures HTTP latency of the `critical_service`
- Classifies the system state
- Applies Docker constraints to neutralise the offending container

---

## Architecture

### Docker Services

| Container         | Role                                                        |
|-------------------|-------------------------------------------------------------|
| `cpu_stress`      | Noisy neighbour — simulates CPU-intensive workloads         |
| `memory_stress`   | Noisy neighbour — simulates memory-heavy workloads          |
| `critical_service`| Victim service — a Flask app that must stay responsive      |
| `mongodb`         | Stores all monitoring metrics for the dashboard             |

### Controller Components (run locally)

| Module               | Responsibility                                              |
|----------------------|-------------------------------------------------------------|
| `main.py`            | Orchestrates the full MAPE-K loop                           |
| `monitor.py`         | Reads CPU/memory stats and measures service latency         |
| `model/predictor.py` | State detection logic (rule-based thresholds)               |
| `model/train_model.py`| Trains and serialises the ML model (Logistic Regression)  |
| `decision_engine.py` | Maps detected states to mitigation actions                  |
| `actuator.py`        | Applies Docker resource updates (`docker update`)           |
| `database.py`        | MongoDB read/write abstraction                              |
| `dashboard.py`       | Flask web server for the live monitoring dashboard          |

---

## Project Structure

```
Proactive_noisy_neighbour/
│
├── app/                          # Critical (victim) service
│   ├── app.py                    # Flask API — simulates a latency-sensitive service
│   └── Dockerfile                # Containerises the critical service
│
├── controller/                   # Autonomous controller (runs on host)
│   ├── main.py                   # Main loop — chaos injection + MAPE-K cycle
│   ├── monitor.py                # Reads Docker stats and HTTP latency
│   ├── decision_engine.py        # Decides actions based on detected state
│   ├── actuator.py               # Applies Docker constraints
│   ├── database.py               # MongoDB interface
│   ├── dashboard.py              # Live dashboard (Flask + Chart.js)
│   ├── templates/
│   │   └── index.html            # Dashboard UI
│   └── model/
│       ├── predictor.py          # State detection (multi-condition thresholds)
│       ├── train_model.py        # ML model training script
│       └── model.pkl             # Pre-trained Logistic Regression model
│
├── Docker-compose.yml            # Defines all Docker services
├── requirements.txt              # Python dependencies for the controller
└── README.md
```

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (running)
- Python 3.10+
- pip

Install Python dependencies:

```bash
pip install -r requirements.txt
pip install pymongo flask
```

> **Note:** `pymongo` and `flask` are required by the controller but are not currently listed in `requirements.txt`. Add them if needed.

---

## Getting Started

### 1. Start the Docker Environment

```bash
docker-compose up -d
```

This launches:
- Two stress containers (`cpu_stress`, `memory_stress`)
- The critical Flask service on **port 5000**
- MongoDB on **port 27017**

Verify containers are running:

```bash
docker ps
```

### 2. Run the Autonomous Controller

From the `controller/` directory:

```bash
cd controller
python main.py
```

The controller will begin its monitoring loop. You'll see output like:

```
🚀 Correct Multi-Condition Detection System Started (MongoDB Version)

Connected to MongoDB at localhost:27017
--------------------------------------------------
CPU Usage     : 145.23%
Memory Usage  : 62.10%
Latency       : 87.45 ms
Detected Issues:
 - CPU_CONTENTION
 - MEMORY_PRESSURE
   >>> ACTION: cpu_throttle -> 0.5
   >>> ACTION: memory_limit -> 256m
CPU updated for cpu_stress
Memory updated for memory_stress
```

Press `Ctrl+C` to stop.

---

## Running the Dashboard

The live dashboard visualises metrics stored in MongoDB using Chart.js.

From the `controller/` directory:

```bash
cd controller
python dashboard.py
```

Open your browser at **[http://localhost:8050](http://localhost:8050)**

The dashboard shows:
- Real-time **CPU usage** chart
- Real-time **Memory usage** chart
- Real-time **Latency** chart
- Current **detected system state**

The charts auto-refresh every few seconds from the `/api/data` endpoint.

---

## Detected States

The predictor evaluates each resource independently and can detect multiple simultaneous issues:

| State                    | Trigger Condition                               |
|--------------------------|-------------------------------------------------|
| `NORMAL`                 | All metrics within safe thresholds              |
| `CPU_CONTENTION`         | Combined CPU usage > **120%**                   |
| `MEMORY_PRESSURE`        | Combined memory usage > **40%**                 |
| `LATENCY_ANOMALY`        | HTTP latency > **200 ms**                       |

Multiple states can be active simultaneously (e.g., `CPU_CONTENTION` + `MEMORY_PRESSURE`).

---

## Mitigation Actions

The decision engine maps each detected state to a Docker mitigation action:

| State                       | Action                                           |
|-----------------------------|--------------------------------------------------|
| `CPU_CONTENTION`            | Throttle `cpu_stress` to **0.5 CPUs**            |
| `MEMORY_PRESSURE`           | Limit `memory_stress` to **256 MB RAM**          |
| `LATENCY_ANOMALY`           | Boost `critical_service` CPU shares to **2048**  |
| `MULTI_RESOURCE_CONTENTION` | Apply all three actions simultaneously           |

Actions are applied using `docker update` — no container restart required.

---

## Retraining the Model

To retrain the Logistic Regression model with updated sample data:

```bash
cd controller
python model/train_model.py
```

This will output a fresh `model.pkl` to `controller/model/model.pkl`.

> The training dataset covers five classes: Normal, CPU spike, Memory pressure, CPU+Memory, and All-resource contention.

---

## Tech Stack

| Layer        | Technology                                  |
|--------------|---------------------------------------------|
| Containers   | Docker, Docker Compose                      |
| Chaos Engine | `polinux/stress` Docker image               |
| Controller   | Python 3.10                                 |
| ML Model     | scikit-learn (Logistic Regression), joblib  |
| Database     | MongoDB (via `pymongo`)                     |
| Dashboard    | Flask + Chart.js                            |
| Victim App   | Flask (Dockerised)                          |

---

## Authors

Built for **Hackfest 2026** — Noisy Neighbour Autonomous Mitigation System.
