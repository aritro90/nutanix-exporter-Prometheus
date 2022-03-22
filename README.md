# nutanix-exporter-Prometheus
This is a containerised exporter written in python to collect metrics for Cluster, Hosts, VMs and Storage Containers.

# Building the container

From the **build** directory, run:

 `docker build -t nutanix-prometheus-exporter .`

 # Running the container

 Available environment variables are listed in the `dockerfile` file in the **build** directory.

 Example of docker command line:

 `docker run -d --name nutanix-exporter-1 -p 8000:8000 -e PRISM=10.10.10.10 -e PRISM_USERNAME=admin -e PRISM_SECRET=mysecret nutanix-prometheus-exporter`

 You can then open your browser to [http://localhost:8000](http://localhost:8000) to verify metrics are being published correctly.
 
 To access the metrcis server from another machine over IP, allow the port on firewall in the metrics server VM 
 `firewall-cmd --zone=public --add-port=8000/tcp --permanent`
 
 `systemctl restart firewalld`

 You can use `docker logs nutanix-exporter-1` to troubleshoot issues in the container.
