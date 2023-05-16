import requests, yaml, time

def check_availability_percentage(up_http_responses, total_http_requests):
    return 0 if total_http_requests == 0 else round((up_http_responses / total_http_requests) * 100)

def check_health_of_http_endpoint(http_endpoint):
    url = http_endpoint['url']
    headers = http_endpoint.get('headers', {})
    method = http_endpoint.get('method', 'GET')
    body = http_endpoint.get('body', None)

    start = time.time()
    response = requests.request(method, url, headers=headers, json=body)
    end = time.time()

    # latency in milliseconds
    latency = (end - start) * 1000

    if response.status_code >= 200 and response.status_code < 300 and latency < 500:
        return response.status_code, latency, 'UP' 
    else:
        return response.status_code, latency, 'DOWN'

if __name__ == '__main__':
    url_domains = {}

    http_endpoints_file_path = input("Enter the path to the YAML HTTP Endpoints file: ")
    with open(http_endpoints_file_path, 'r') as file:
        http_endpoints = yaml.safe_load(file)
    
    try:
        while True:
            for http_endpoint in http_endpoints:
                url_domain = http_endpoint['url'].split('//')[-1].split('/')[0]
                if url_domain not in url_domains:
                    url_domains[url_domain] = {
                        'up_http_responses': 0,
                        'total_http_requests': 0
                    }
                
                status_code, latency, http_outcome = check_health_of_http_endpoint(http_endpoint)
                if http_outcome == 'UP':
                    url_domains[url_domain]['up_http_responses'] += 1
                url_domains[url_domain]['total_http_requests'] += 1
            
            #     print(f"Endpoint with name {http_endpoint['name']} has HTTP response code {status_code} and response latency {latency} ms => {http_outcome}")
            
            # print("Test cycle ends. The program logs to the console:")
            
            for url_domain, count in url_domains.items():
                availability_percentage = check_availability_percentage(count['up_http_responses'], count['total_http_requests'])
                print(f"{url_domain} has {availability_percentage}% availability percentage")
            
            time.sleep(15)
    
    except KeyboardInterrupt:
        print("User manually exited the program.")