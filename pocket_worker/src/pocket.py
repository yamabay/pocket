from prometheus_client import start_http_server, Counter, Summary, Gauge
import requests
import time
import yaml
from nornir import InitNornir
from nornir.core.task import Task, Result
import logging
from pythonping import ping


def render_configs(conf_file):
    try:
        with open(conf_file, "r") as file:
            config = yaml.safe_load(file)
        return config

    except Exception as e:
        print(f"Error opening config file: {e}")
        return None


def create_metrics():

    return {
    "http_get_rtt": Gauge("http_get_rtt", "RTT for basic HTTP GET requests", ["url"]),
    "http_get_summary": Summary("http_get", "Summary of HTTP GET requests", ["url"]),
    "ping_reachable": Gauge("ping_reachable", "Basic ping reachability to host", ["host"]),
    "ping_rtt": Gauge("ping_rtt", "RTT for basic ping reachability check", ["host"]),
    }


def make_request(task: Task, config, logger, metrics: dict) -> None:

    for url in config["http_get_requests"]:
        logger.info(f"HTTP request :: GET :: {url}")
        try:
            response = requests.get(url, timeout=config["http_timeout"])
            metrics["http_get_rtt"].labels(url=url).set(response.elapsed.total_seconds())
            metrics["http_get_summary"].labels(url=url).observe(response.elapsed.total_seconds())
        except Exception as e:
            logger.info(f"HTTP request :: Error :: {e}")
            metrics["http_get_rtt"].labels(url=url).set(-1)
            metrics["http_get_summary"].labels(url=url).observe(-1)
    return None


def ping_hosts(task: Task, config, logger, metrics: dict) -> None:

    for host in config["ping_check"]:
        try:
            logger.info(f"Ping check :: {host}")
            result = ping(host, timeout=config["ping_timeout"], count=2)
            logger.info(f"{result.packet_loss}")
            if result.packet_loss == 1.0:
                metrics["ping_reachable"].labels(host=host).set(0)
                logger.info(f"Ping packet loss detected :: {host}")
                metrics["ping_rtt"].labels(host=host).set(-1)
            else:
                metrics["ping_reachable"].labels(host=host).set(1)
                metrics["ping_rtt"].labels(host=host).set(result.rtt_min_ms)
        except Exception as e:
            logger.info(f"Ping check :: ERROR :: {host} :: {e}")
    return None


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )

    logger = logging.getLogger(__name__)

    # Start up the server to expose the metrics
    start_http_server(8000)

    metrics = create_metrics()
    config = render_configs("pocket-conf.yaml")

    nr = InitNornir(
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": "inventory/hosts.yaml",
            }
        }
    )

    count = 1

    while True:

        logger.info(f"Running tests :: Count {count}")

        nr.run(
            task=make_request,
            config=config,
            logger=logger,
            metrics=metrics,
        )

        nr.run(
            task=ping_hosts,
            config=config,
            logger=logger,
            metrics=metrics,
        )
            
        time.sleep(config["global_wait_time"])
        count += 1