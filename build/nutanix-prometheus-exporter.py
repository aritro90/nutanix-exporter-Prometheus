import os,requests,json,time
from prometheus_client import start_http_server, Gauge, Enum, Info
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR   

def process_request(url, method, user, password, headers, payload=None, secure=False):
    """
    Processes a web request and handles result appropriately with retries.
    Returns the content of the web request if successfull.
    """
    if payload is not None:
        payload = json.dumps(payload)

    #configuring web request behavior
    timeout=10
    retries = 5
    sleep_between_retries = 5

    while retries > 0:
        try:

            if method == 'GET':
                #print("secure is {}".format(secure))
                response = requests.get(
                    url,
                    headers=headers,
                    auth=(user, password),
                    verify=secure,
                    timeout=timeout
                )
            elif method == 'POST':
                response = requests.post(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password),
                    verify=secure,
                    timeout=timeout
                )
            elif method == 'PUT':
                response = requests.put(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password),
                    verify=secure,
                    timeout=timeout
                )
            elif method == 'PATCH':
                response = requests.patch(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password),
                    verify=secure,
                    timeout=timeout
                )
            elif method == 'DELETE':
                response = requests.delete(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password),
                    verify=secure,
                    timeout=timeout
                )

        except requests.exceptions.HTTPError as error_code:
            print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] Http Error! Status code: {response.status_code}{bcolors.RESET}")
            print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] reason: {response.reason}{bcolors.RESET}")
            print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] text: {response.text}{bcolors.RESET}")
            print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] elapsed: {response.elapsed}{bcolors.RESET}")
            print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] headers: {response.headers}{bcolors.RESET}")
            if payload is not None:
                print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] payload: {payload}{bcolors.RESET}")
            print(json.dumps(
                json.loads(response.content),
                indent=4
            ))
            exit(response.status_code)
        except requests.exceptions.ConnectionError as error_code:
            if retries == 1:
                print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] {type(error_code).__name__} {str(error_code)} {bcolors.RESET}")
                exit(1)
            else:
                print(f"{bcolors.WARNING}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [WARNING] {type(error_code).__name__} {str(error_code)} {bcolors.RESET}")
                time.sleep(sleep_between_retries)
                retries -= 1
                print(f"{bcolors.WARNING}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [WARNING] Retries left: {retries}{bcolors.RESET}")
                continue
        except requests.exceptions.Timeout as error_code:
            if retries == 1:
                print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] {type(error_code).__name__} {str(error_code)} {bcolors.RESET}")
                exit(1)
            else:
                print(f"{bcolors.WARNING}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [WARNING] {type(error_code).__name__} {str(error_code)} {bcolors.RESET}")
                time.sleep(sleep_between_retries)
                retries -= 1
                print(f"{bcolors.WARNING}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [WARNING] Retries left: {retries}{bcolors.RESET}")
                continue
        except requests.exceptions.RequestException as error_code:
            print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] {response.status_code} {bcolors.RESET}")
            exit(response.status_code)
        break

    if response.ok:
        return response
    if response.status_code == 401:
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] {response.status_code} {response.reason} {bcolors.RESET}")
        exit(response.status_code)
    elif response.status_code == 500:
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] {response.status_code} {response.reason} {response.text} {bcolors.RESET}")
        exit(response.status_code)
    else:
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d_%H:%M:%S')} [ERROR] Request failed! Status code: {response.status_code}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d_%H:%M:%S')} [ERROR] reason: {response.reason}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d_%H:%M:%S')} [ERROR] text: {response.text}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d_%H:%M:%S')} [ERROR] raise_for_status: {response.raise_for_status()}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d_%H:%M:%S')} [ERROR] elapsed: {response.elapsed}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d_%H:%M:%S')} [ERROR] headers: {response.headers}{bcolors.RESET}")
        if payload is not None:
            print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d_%H:%M:%S')} [ERROR] payload: {payload}{bcolors.RESET}")
        print(json.dumps(
            json.loads(response.content),
            indent=4
        ))
        exit(response.status_code)

def prism_get_cluster(api_server,username,secret,secure=False):
    """Retrieves data from the Prism Element v2 REST API endpoint /clusters.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        
    Returns:
        Cluster uuid as cluster_uuid. Cluster details as cluster_details
    """
    
    #region prepare the api call
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    api_server_port = int(os.getenv("APP_PORT", "9440"))
    api_server_endpoint = "/PrismGateway/services/rest/v2.0/clusters/"
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "GET"
    #endregion

    print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Making a {method} API call to {url} with secure set to {secure}{bcolors.RESET}")
    resp = process_request(url,method,username,secret,headers,secure=secure)

    # deal with the result/response
    if resp.ok:
        json_resp = json.loads(resp.content)
        cluster_uuid = json_resp['entities'][0]['uuid']
        cluster_details = json_resp['entities'][0]
        return cluster_uuid, cluster_details
    else:
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] Request failed! Status code: {resp.status_code}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] reason: {resp.reason}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] text: {resp.text}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] raise_for_status: {resp.raise_for_status()}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] elapsed: {resp.elapsed}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] headers: {resp.headers}{bcolors.RESET}")
        if payload is not None:
            print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] payload: {payload}{bcolors.RESET}")
        print(json.dumps(
            json.loads(response.content),
            indent=4
        ))
        raise

def prism_get_vm(api_server,username,secret,secure=False):
    """Retrieves data from the Prism Element v1 REST API endpoint /vms .

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        
    Returns:
        List of VMs and their details as vm_details
    """
    
    #region prepare the api call
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    api_server_port = int(os.getenv("APP_PORT", "9440"))
    api_server_endpoint = f"/PrismGateway/services/rest/v1/vms"
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "GET"
    #endregion
    
    print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Making a {method} API call to {url} with secure set to {secure}{bcolors.RESET}")
    resp = process_request(url,method,username,secret,headers,secure=secure)

    # deal with the result/response
    if resp.ok:
        json_resp = json.loads(resp.content)
        vm_details = json_resp['entities']
        return vm_details
    else:
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] Request failed! Status code: {resp.status_code}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] reason: {resp.reason}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] text: {resp.text}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] raise_for_status: {resp.raise_for_status()}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] elapsed: {resp.elapsed}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] headers: {resp.headers}{bcolors.RESET}")
        if payload is not None:
            print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] payload: {payload}{bcolors.RESET}")
        print(json.dumps(
            json.loads(response.content),
            indent=4
        ))
        raise

def prism_get_host(api_server,username,secret,secure=False):
    """Retrieves data from the Prism Element v2 REST API endpoint /hosts .

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        
    Returns:
        List of hosts and their details as host_details
    """
    
    #region prepare the api call
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    api_server_port = int(os.getenv("APP_PORT", "9440"))
    api_server_endpoint = f"/PrismGateway/services/rest/v2.0/hosts"
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "GET"
    #endregion
    
    print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Making a {method} API call to {url} with secure set to {secure}{bcolors.RESET}")
    resp = process_request(url,method,username,secret,headers,secure=secure)

    # deal with the result/response
    if resp.ok:
        json_resp = json.loads(resp.content)
        host_details = json_resp['entities']
        return host_details
    else:
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] Request failed! Status code: {resp.status_code}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] reason: {resp.reason}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] text: {resp.text}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] raise_for_status: {resp.raise_for_status()}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] elapsed: {resp.elapsed}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] headers: {resp.headers}{bcolors.RESET}")
        if payload is not None:
            print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] payload: {payload}{bcolors.RESET}")
        print(json.dumps(
            json.loads(response.content),
            indent=4
        ))
        raise

def prism_get_storage_containers(api_server,username,secret,secure=False):
    """Retrieves data from the Prism Element v2 REST API endpoint /storage_containers.

    Args:
        api_server: The IP or FQDN of Prism.
        username: The Prism user name.
        secret: The Prism user name password.
        
    Returns:
        Storage containers details as storage_containers_details
    """
    
    #region prepare the api call
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    api_server_port = int(os.getenv("APP_PORT", "9440"))
    api_server_endpoint = f"/PrismGateway/services/rest/v2.0/storage_containers/"
    url = "https://{}:{}{}".format(
        api_server,
        api_server_port,
        api_server_endpoint
    )
    method = "GET"
    #endregion
    
    print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Making a {method} API call to {url} with secure set to {secure}{bcolors.RESET}")
    resp = process_request(url,method,username,secret,headers,secure=secure)

    # deal with the result/response
    if resp.ok:
        json_resp = json.loads(resp.content)
        storage_containers_details = json_resp['entities']
        return storage_containers_details
    else:
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] Request failed! Status code: {resp.status_code}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] reason: {resp.reason}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] text: {resp.text}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] raise_for_status: {resp.raise_for_status()}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] elapsed: {resp.elapsed}{bcolors.RESET}")
        print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] headers: {resp.headers}{bcolors.RESET}")
        if payload is not None:
            print(f"{bcolors.FAIL}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [ERROR] payload: {payload}{bcolors.RESET}")
        print(json.dumps(
            json.loads(response.content),
            indent=4
        ))
        raise

class NutanixMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """
    def __init__(self, app_port=9440, polling_interval_seconds=5, prism='127.0.0.1', user='admin', pwd='Nutanix/4u', prism_secure=False, vm_metrics=True, host_metrics=True, cluster_metrics=True, storage_containers_metrics=True):
        self.app_port = app_port
        self.polling_interval_seconds = polling_interval_seconds
        self.prism = prism
        self.user = user
        self.pwd = pwd
        self.prism_secure = prism_secure
        self.vm_metrics = vm_metrics
        self.host_metrics = host_metrics
        self.cluster_metrics = cluster_metrics
        self.storage_containers_metrics = storage_containers_metrics
        
        if self.cluster_metrics:
            print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d_%H:%M:%S')} [INFO] Initializing metrics for clusters...{bcolors.RESET}")
            
            cluster_uuid, cluster_details = prism_get_cluster(api_server=prism,username=user,secret=pwd,secure=self.prism_secure)
            
            for key,value in cluster_details['stats'].items():
                #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                key_string = f"NutanixClusters_stats_{key}"
                key_string = key_string.replace(".","_")
                key_string = key_string.replace("-","_")
                setattr(self, key_string, Gauge(key_string, key_string, ['cluster']))
            for key,value in cluster_details['usage_stats'].items():
                #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                key_string = f"NutanixClusters_usage_stats_{key}"
                key_string = key_string.replace(".","_")
                key_string = key_string.replace("-","_")
                setattr(self, key_string, Gauge(key_string, key_string, ['cluster']))
            
            #self.lts = Enum("is_lts", "AOS Long Term Support", ['cluster'], states=['True', 'False'])
            setattr(self, 'NutanixClusters_info', Info('is_lts', 'Long Term Support AOS true/false', ['cluster']))

        if self.vm_metrics:
            print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d_%H:%M:%S')} [INFO] Initializing metrics for virtual machines...{bcolors.RESET}")
            vm_details = prism_get_vm(api_server=prism,username=user,secret=pwd,secure=self.prism_secure)

            # we need to loop through all VMs to define attributes, as some attributes are only returned if they are set.  This avoids
            # a keyError on fetch
            for entity in vm_details:
                for key,value in entity['stats'].items():
                    #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                    key_string = f"NutanixVms_stats_{key}"
                    key_string = key_string.replace(".","_")
                    key_string = key_string.replace("-","_")
                    if not hasattr(self, key_string):
                        setattr(self, key_string, Gauge(key_string, key_string.strip(), ['vm']))
                for key,value in entity['usageStats'].items():
                    #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                    key_string = f"NutanixVms_usage_stats_{key}"
                    key_string = key_string.replace(".","_")
                    key_string = key_string.replace("-","_")
                    if not hasattr(self, key_string):
                        setattr(self, key_string, Gauge(key_string, key_string, ['vm']))

        if self.host_metrics:
            print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d_%H:%M:%S')} [INFO] Initializing metrics for Hosts...{bcolors.RESET}")
            host_details = prism_get_host(api_server=prism,username=user,secret=pwd,secure=self.prism_secure)
            for key,value in host_details[0]['stats'].items():
                #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                key_string = f"NutanixHosts_stats_{key}"
                key_string = key_string.replace(".","_")
                key_string = key_string.replace("-","_")
                setattr(self, key_string, Gauge(key_string, key_string, ['host']))
            for key,value in host_details[0]['usage_stats'].items():
                #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                key_string = f"NutanixHosts_usage_stats_{key}"
                key_string = key_string.replace(".","_")
                key_string = key_string.replace("-","_")
                setattr(self, key_string, Gauge(key_string, key_string, ['host']))

        if self.storage_containers_metrics:
            print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d_%H:%M:%S')} [INFO] Initializing metrics for storage containers...{bcolors.RESET}")
            storage_containers_details = prism_get_storage_containers(api_server=prism,username=user,secret=pwd,secure=self.prism_secure)
            for key,value in storage_containers_details[0]['stats'].items():
                #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                key_string = f"NutanixStorageContainers_stats_{key}"
                key_string = key_string.replace(".","_")
                key_string = key_string.replace("-","_")
                setattr(self, key_string, Gauge(key_string, key_string, ['storage_container']))
            for key,value in storage_containers_details[0]['usage_stats'].items():
                #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                key_string = f"NutanixStorageContainers_usage_stats_{key}"
                key_string = key_string.replace(".","_")
                key_string = key_string.replace("-","_")
                setattr(self, key_string, Gauge(key_string, key_string, ['storage_container']))
            
    def run_metrics_loop(self):
        """Metrics fetching loop"""
        print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Starting metrics loop {bcolors.RESET}")
        while True:
            self.fetch()
            print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Waiting for {self.polling_interval_seconds} seconds...{bcolors.RESET}")
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics with
        new values.
        """
        
        if self.cluster_metrics:
            print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Collecting clusters metrics{bcolors.RESET}")
            cluster_uuid, cluster_details = prism_get_cluster(api_server=self.prism,username=self.user,secret=self.pwd,secure=self.prism_secure)
        
            for key, value in cluster_details['stats'].items():
                #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                key_string = f"NutanixClusters_stats_{key}"
                key_string = key_string.replace(".","_")
                key_string = key_string.replace("-","_")
                self.__dict__[key_string].labels(cluster=cluster_details['name']).set(value)
            for key, value in cluster_details['usage_stats'].items():
                #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                key_string = f"NutanixClusters_usage_stats_{key}"
                key_string = key_string.replace(".","_")
                key_string = key_string.replace("-","_")
                self.__dict__[key_string].labels(cluster=cluster_details['name']).set(value)
            
            #self.lts.labels(cluster=cluster_details['name']).state(str(cluster_details['is_lts']))
            self.NutanixClusters_info.labels(cluster=cluster_details['name']).info({'is_lts': str(cluster_details['is_lts'])})
        
        if self.vm_metrics:
            vm_details = prism_get_vm(api_server=self.prism,username=self.user,secret=self.pwd,secure=self.prism_secure)
            print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Collecting vm metrics for {bcolors.RESET}")
            for entity in vm_details:
                print(entity)
                print("\n")
                for key, value in entity['stats'].items():
                    #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                    key_string = f"NutanixVms_stats_{key}"
                    key_string = key_string.replace(".","_")
                    key_string = key_string.replace("-","_")
                    self.__dict__[key_string].labels(vm=entity['vmName']).set(value)
                for key, value in entity['usageStats'].items():
                    #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                    key_string = f"NutanixVms_usage_stats_{key}"
                    key_string = key_string.replace(".","_")
                    key_string = key_string.replace("-","_")
                    self.__dict__[key_string].labels(vm=entity['vmName']).set(value)
                    
        if self.host_metrics:
            host_details = prism_get_host(api_server=self.prism,username=self.user,secret=self.pwd,secure=self.prism_secure)
            print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Collecting Host metrics for {bcolors.RESET}")
            for entity in host_details:
                for key, value in entity['stats'].items():
                    #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                    key_string = f"NutanixHosts_stats_{key}"
                    key_string = key_string.replace(".","_")
                    key_string = key_string.replace("-","_")
                    self.__dict__[key_string].labels(host=entity['name']).set(value)
                for key, value in entity['usage_stats'].items():
                    #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                    key_string = f"NutanixHosts_usage_stats_{key}"
                    key_string = key_string.replace(".","_")
                    key_string = key_string.replace("-","_")
                    self.__dict__[key_string].labels(host=entity['name']).set(value)
                    

        if self.storage_containers_metrics:
            print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Collecting storage containers metrics{bcolors.RESET}")
            storage_containers_details = prism_get_storage_containers(api_server=self.prism,username=self.user,secret=self.pwd,secure=self.prism_secure)
            for container in storage_containers_details:
                for key, value in container['stats'].items():
                    #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                    key_string = f"NutanixStorageContainers_stats_{key}"
                    key_string = key_string.replace(".","_")
                    key_string = key_string.replace("-","_")
                    self.__dict__[key_string].labels(storage_container=container['name']).set(value)
                for key, value in container['usage_stats'].items():
                    #making sure we are compliant with the data model (https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)
                    key_string = f"NutanixStorageContainers_usage_stats_{key}"
                    key_string = key_string.replace(".","_")
                    key_string = key_string.replace("-","_")
                    self.__dict__[key_string].labels(storage_container=container['name']).set(value)

def main():
    """Main entry point"""

    print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Getting environment variables...{bcolors.RESET}")
    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "30"))
    app_port = int(os.getenv("APP_PORT", "9440"))
    exporter_port = int(os.getenv("EXPORTER_PORT", "8000"))

    print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Initializing metrics class...{bcolors.RESET}")
    nutanix_metrics = NutanixMetrics(
        app_port=app_port,
        polling_interval_seconds=polling_interval_seconds,
        prism=os.getenv('PRISM'),
        user = os.getenv('PRISM_USERNAME'),
        pwd = os.getenv('PRISM_SECRET'),
        prism_secure=bool(os.getenv("PRISM_SECURE", False)),
        vm_metrics=bool(os.getenv('VM_METRICS', True)),
        host_metrics=bool(os.getenv('HOST_METRICS', True)),
        cluster_metrics=bool(os.getenv('CLUSTER_METRICS', True)),
        storage_containers_metrics=bool(os.getenv('STORAGE_CONTAINERS_METRICS', True))
    )
    
    print(f"{bcolors.OK}{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} [INFO] Starting http server on port {exporter_port}{bcolors.RESET}")
    start_http_server(exporter_port)
    nutanix_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()
