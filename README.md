# Local Monitoring Stack

A small observability stack: A Python-Flask app instrumented with Prometheus metrics, scraped by Prometheus, and visualized in Grafana. All services run as their own container locally using Docker.

## How to Set Up This Project

✅ **Requirements -** Before starting, make sure you have installed:

- Docker
- Docker-Compose

### Step 1 - Clone/Download the Project

`git clone https://github.com/Dominicdaniel86/Local-Monitoring-Stack`  
`cd Local-Monitoring-Stack`

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
| cadvisor | <http://localhost:8080>   |

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

1. Log in

    - URL: <http://localhost:3000>
    - Username: `admin`
    - Password: `admin`

2. Add Prometheus as a data source

    2.1 Go to Connections -> Data Sources -> Add data source
    2.2 Choose Prometheus
    2.3 Set URL to <http://prometheus:9090> (use container name, not localhost)
    2.4 Click Save & Test

3. Import the Grafana dashboard

    3.1 Got to Dashboards -> New -> Import
    3.2 Copy-paste the content of `/grafana/test-dashboard.json` into the JSON field
    3.3 Click on Load and give the Dashboard a name

### Step 7 - AWS Deployment

1. Connect to your EC2 instance via SSH
2. Execute the following commands to install git:

    ```bash
    sudo dnf update -y || sudo yum update -y
    sudo dnf install -y git git || sudo yum install -y git
    ```

3. Clone the repository (like in step 1)
4. Execute the bash setup script:

    ```bash
    cd Local-Monitoring-Stack/scripts
    chmod +x setup-ec2.sh
    ./setup-ec2.sh
    ```

5. Follow steps 2 to 6 on the EC2 instance

> [!Info] Note that you might need to assign an IPV-4 address to your EC2 instance in order to open the Prometheus/Grafana interfaces, as localhost is not going to work here.
