from flask import Flask, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

# Prometheus Metrics (SLI Tracking)
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status_code'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Latency', ['endpoint'])

@app.route('/')
def home():
    start_time = time.time()
    
    # Simulate slight random processing latency
    latency = random.uniform(0.01, 0.05)
    time.sleep(latency)
    
    REQUEST_COUNT.labels(method='GET', endpoint='/', status_code='200').inc()
    REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start_time)
    
    return "Microservice Running Cleanly!", 200

@app.route('/health')
def health():
    return {"status": "UP"}, 200

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)