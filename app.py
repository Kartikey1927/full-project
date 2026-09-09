from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os

app = Flask(__name__)

REQUEST_COUNT = Counter('app_requests_total', 'Total HTTP Request Count')
APP_VERSION = "v1.1.0"

@app.route('/')
def hello():
    REQUEST_COUNT.inc()
    return jsonify({
        "message": "Microservice is live with Prometheus metrics!",
        "version": APP_VERSION,
        "environment": os.getenv("ENVIRONMENT", "development")
    })

@app.route('/healthz')
def health_check():
    return jsonify({"status": "UP"}), 200

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
