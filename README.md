<img src="./docs/assets/pocket.png" alt="Pocket Logo" width="100" height="100"> 

# Pocket

## Overview
**Pocket** is a tool designed to run network HTTP and Ping tests, collect metrics using Prometheus, and visualize them with Grafana in a easily customizable way. This project uses docker compose to build out each component as separate services that work together to provide a complete localized monitoring solution.

Pocket is meant to be an easily customizable monitoring stack that can be deployed anywhere docker is supported. Tests can be tailored to specific environments and testing instances can be added and removed without the need to rebuild any container images.

## Services

### pocket_worker
- **Description**: 
  - The `pocket_worker` service is responsible for executing the actual network tests.
  - The tests are defined in the `pocket-conf.yaml` file.
  - It exposes Prometheus metrics at the `/metrics` endpoint, which can be accessed on port `:8000`.

### pocket_prometheus
- **Description**:
  - The `pocket_prometheus` service runs a Prometheus server that automatically connects to and scrapes the metrics from the `pocket_worker`.
  - The Prometheus web interface can be accessed on port `:9090`.

### pocket_grafana
- **Description**:
  - The `pocket_grafana` service handles visualizing the metrics through a pre-built Grafana dashboard.
  - Grafana is accessible on port `:3000`.
  - By default, **anonymous** access is enabled. For admin access, the default Grafana `admin:admin` credentials will work, and update via environment variables as needed.
  - **Environment Variables** - Set in .env file. 
    - `GF_AUTH_ANONYMOUS_ENABLED` - Handles anonymous login. This may be desired if running locally.
    - `GF_DASHBOARDS_DEFAULT_HOME_DASHBOARD_PATH` - Sets the path to the default dashboard. The dashboard JSON file is set in the `grafana/provisioning/dashboards` directory and can be customized easily if changes are desired.
    - `GF_USERS_HOME_PAGE` - Sets the default home page to the `Network Metrics` dashboard so users are brought directly to this dashboard once grafana is accessed.
## Getting Started

1. **Clone the Repository**:
   ```bash
   git clone https://your-repo-url.git
   cd your-app

2. **Customize the pocket-conf.yaml tests**
    ```
    global_wait_time: 2 # wait time between running tests

    http_timeout: 2 # HTTP timeout in seconds
  
    # List of hosts/paths for GET requests
    http_get_requests: 
      - https://wikipedia.org
      - https://example.com

    ping_timeout: 1 # Ping timeout in seconds

    # List of hosts for ping tests
    ping_check:
      - 1.1.1.1
      - 8.8.8.8
    ```
3. **Build the pocket_tester image before deploying**
    ```
    docker-compose build
    ```
4. **Deploy the app**
    ```
    docker-compose up -d
    ```
5. **Access the Grafana dashboard**

    In your preferred browser, access the app on port `3000`. If running locally, this would be `https://localhost:3000`. 

### Authors
- Bailey Young - Contributor

