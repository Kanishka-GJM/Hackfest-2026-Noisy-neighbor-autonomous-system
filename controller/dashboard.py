# controller/dashboard.py
from flask import Flask, jsonify, render_template
from database import get_recent_metrics

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data")
def data():
    # Get data from MongoDB
    raw_data = get_recent_metrics(limit=50)
    
    # Reverse the list so the graph draws from left (old) to right (new)
    raw_data.reverse()
    
    # Prepare lists for Chart.js
    timestamps = []
    cpu_data = []
    memory_data = []
    latency_data = []
    states_data = []

    for entry in raw_data:
        # Format time as HH:MM:SS
        time_str = entry["timestamp"].strftime("%H:%M:%S")
        
        timestamps.append(time_str)
        cpu_data.append(entry["cpu"])
        memory_data.append(entry["memory"])
        latency_data.append(entry["latency"])
        
        # Join the states list into a string (e.g., "CPU_CONTENTION")
        states_str = ", ".join(entry["states"]) if entry["states"] else "NORMAL"
        states_data.append(states_str)

    return jsonify({
        "timestamps": timestamps,
        "cpu": cpu_data,
        "memory": memory_data,
        "latency": latency_data,
        "states": states_data
    })

if __name__ == "__main__":
    # Runs on port 8050 to avoid conflict with your critical service (5000)
    app.run(host="0.0.0.0", port=8050, debug=True)