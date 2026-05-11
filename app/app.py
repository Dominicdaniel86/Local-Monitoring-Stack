from flask import Flask, jsonify, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, Histogram, Gauge
import random
import time

app = Flask(__name__)

# === Custom prometheus metrics ===
REQUEST_COUNT = Counter(
    'flask_total_requests_count', # Metric name
    'Total number of requests received', # Metric description
    ['method', 'endpoint', 'http_status'] # Metric labels
)

RESPONSE_LATENCY = Histogram(
    'flask_response_latency_seconds',
    'Latency of HTTP responses in seconds',
    ['method', 'endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'flask_active_requests',
    'Number of active requests being processed'
)

# === Middleware: track every request ===

@app.before_request
def before_request():
    """Middleware to track request start time and increment active requests"""
    request.start_time = time.time() # Store for latency calculation
    ACTIVE_REQUESTS.inc() # Increment active requests

@app.after_request
def after_request(response):
    """Middleware to calculate latency, update metrics, and decrement active requests"""
    latency = time.time() - request.start_time # Calculate latency
    ACTIVE_REQUESTS.dec() # Decrement active requests
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        http_status=response.status_code
    ).inc() # Increment request count with labels
    RESPONSE_LATENCY.labels(
        method=request.method,
        endpoint=request.path
    ).observe(latency) # Observe latency for this request
    return response

# === Flask routes ===
@app.route('/')
def index():
    return jsonify({
        "message": "Hello from Flask with Prometheus metrics!",
        "possible_endpoints": ["/latency", "/error", "/metrics"]
    }), 200

@app.route('/latency')
def latency():
    """Simulates an endpoint with variable latency"""
    delay = random.uniform(0.1, 2.0) # Simulate latency between 100ms and 2s
    time.sleep(delay)
    return jsonify({
        "message": f"Response delayed by {delay:.2f} seconds",
        "delay": delay
    }), 200

@app.route('/error')
def error():
    """Returns 50% error to simulate a broken endpoint"""
    if random.random() < 0.5:
        return jsonify({"error": "Simulated error occurred!"}), 500
    return jsonify({"message": "Success!"}), 200

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
