# controller/database.py
import os
from pymongo import MongoClient
from datetime import datetime

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = 27017

# Connect to MongoDB
client = MongoClient(host=DB_HOST, port=DB_PORT)
db = client["noisy_neighbor_db"]
collection = db["metrics"]

def init_db():
    """Placeholder to keep main.py happy and confirm connection."""
    print(f"Connected to MongoDB at {DB_HOST}:{DB_PORT}")

def insert_metric(cpu, memory, latency, states):
    """Inserts a monitoring record into MongoDB."""
    record = {
        "timestamp": datetime.now(),
        "cpu": float(cpu),
        "memory": float(memory),
        "latency": float(latency),
        "states": states 
    }
    try:
        collection.insert_one(record)
    except Exception as e:
        print(f"Error inserting into MongoDB: {e}")

def get_recent_metrics(limit=30):
    """Fetches the most recent 'limit' records for the dashboard."""
    try:
        cursor = collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit)
        return list(cursor)
    except Exception as e:
        print(f"Error reading from MongoDB: {e}")
        return []