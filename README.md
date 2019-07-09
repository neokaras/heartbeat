# Heartbeat Service

## Summary
Heartbeat Service monitors liveliness of nodes/devices based on the set TTL.
Node registers and reconfirms it's liveliness via /heartbeat endpoint. Node is considered DOWN if does not reconfirm it's liveliness with TTL window.
Node status report can viewed via /report endpoint

## Architecture
Heartbeat Service is Python Tornado app with two endpoints /heartbeat and /report
Filesystem is used as database of record (file with node/device is touched when /heartbeat endpoint is hit)
Redis is used for TTL management (a record is set with TTL when /heartbeat endpoint is hit)
Node/device is considered DOWN when it exists in the filesystem but is not present in Redis
/hearbeat endpoint contacted by nodes/devices to register liveliness, takes one parameter device={device_name}
/report endpoint displays the status (UP/DOWN) of all nodes/devices that were seen.

## GCP Provisioning
* terraform to provisiong GCP resources (compute and firewall) and kick off ansible run
* ansible builds GCP compute instance - install Docker, docker-compose, app code and Dockerfile
* docker-compose builds Docker images and starts the app containers

### Prerequisites
installed on a machine that runs provisioning
* terraform
* ansible
* GCP api-key.json
* passwordless ssh key pair (GCP Porject or instance level)

### Setup and Run
1. git clone https://github.com/neokaras/heartbeat.git
2. cd terraform/
3. update variables.tf with your own zone, region, project, api-key and ssh-key or overide on the command line
4. terraform init
5. terraform apply

### Testing
1. after terraform run, heartbeat-endpoints.txt contains the urls for /heartbeat and /report
2. get the url for /heartbeat endpoint form terraform/heartbeat-endpoints.txt
3. run the test python3 test/heartbeat-runner.py --url={url_for_heartbeat_endpoint}
4. view results at /report endpoint
