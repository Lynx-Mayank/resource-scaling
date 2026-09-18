from flask import Flask
import time

app = Flask(__name__)


@app.route("/")
def home():
    return "Dynamic Resource Scaling Demo"


@app.route("/work")
def work():
    # Simulate CPU-intensive work
    start = time.time()

    while time.time() - start < 0.5:
        _ = sum(i * i for i in range(10000))

    return "Work completed"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)