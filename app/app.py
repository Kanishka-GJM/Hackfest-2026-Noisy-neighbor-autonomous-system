from flask import Flask
import time
import random

app = Flask(__name__)

@app.route("/")
def home():
    delay = random.uniform(0.05, 0.3)
    time.sleep(delay)
    return {"message": "Critical Service Running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)