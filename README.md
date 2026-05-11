# Local Monitoring Stack

A small observability stack: A Python-Flask app instrumented with Prometheus metrics, scraped by Prometheus, and visualized in Grafana. All services run as their own container locally using Docker.

## How to Set Up This Project

✅ **Requirements -** Before starting, make sure you have installed:

- Docker
- Docker-Compose

### Step 1 - Clone/Download the Project

`git clone ...`
`cd ...`

### Step 2 - Start the containers

`docker compose up --build`

Optionally use the *detach* option to free up the console:

`docker compose up --build -d`

### Step 3 - Verify services are running

| Service | URL |
| ------- | --- |
| Flask App | <http://localhost:5000>  |
| Prometheus | <http://localhost:9090> |
| Grafana | <http://localhost:3000>    |

## Step 4 - Generate Some Traffic

Open a Bash Shell (or similar tools) to call the Apps endpoints. This produces metrics that Prometheus grabs:

```bash
# Normal request
curl http://localhost:5000/

# Slow endpoint (0.5 - 2s latency)
curl http://localhost:5000/latency

# Broken endpoint
curl http://localhost:5000/error

# Raw Prometheus metrics
curl http://localhost:5000/metrics

```

### Step 5 - Verify that Prometheus is Scraping

1. Open <http://localhost:9090/targets>
2. Verify that you can see `flask-app` with state **UP**
3. Query for the custom metrics in the explore tab:

    - `flask_request_count_total` - total requests by endpoint
    - `rate(flask_request_count_total[1m])` - requests per second
    - `flask_request_latency_seconds_bucket` - latency histogram

### Step 6 - Open Grafana
