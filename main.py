import yaml
import requests
import time
import sys # move to imports, was out of place before
from urllib.parse import urlparse # import for better URL parsing
from collections import defaultdict

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET') # adding defaults
    headers = endpoint.get('headers', {})
    body = endpoint.get('body', None)

    try:
        response = requests.request(method, url, headers=headers, json=body, timeout=0.5) # need to add 500ms timeout as per instructions
        if 200 <= response.status_code < 300:
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException:
        return "DOWN"

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        start_time = time.time()
        
        for endpoint in config:
            parsed_url = urlparse(endpoint["url"])
            domain = parsed_url.hostname # ignore port number 
        
            result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            availability = round(100 * stats["up"] / stats["total"])
            print(f"{domain} has {availability}% availability percentage")

        print("---")
        spent_time = time.time() - start_time
        sleep_time = 15 - spent_time
        if sleep_time > 0:
            time.sleep(sleep_time) # change how long we sleep based on how long the checks took

# Entry point of the program
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
