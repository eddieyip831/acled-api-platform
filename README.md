# ACLED API Platform architecture

This repository renders the ACLED API system architecture as code using the `diagrams` Python library and Graphviz.

## Audience
* **Platform view** is for cloud engineering. It shows the main services, VPC and the site to site VPN.
* **Request flow** is for backend developers. It shows the exact call sequence through the compute and data path.

## Components
* Digital Ocean Droplet that runs the client application
* Digital Ocean VPC and Cloud Firewall
* Digital Ocean Managed MySQL with a private endpoint
* Digital Ocean VPN gateway for site to site connectivity
* Amazon CloudFront in front of Amazon API Gateway using the HTTP API type
* AWS Lambda inside an AWS VPC
* AWS Secrets Manager for credentials and configuration
* AWS Certificate Manager for public TLS certificates
* Amazon CloudWatch Logs for function logging
* AWS site to site VPN endpoint

## Backend request sequence
1. The application calls the public endpoint on Amazon CloudFront.
2. CloudFront forwards to Amazon API Gateway using the HTTP API type.
3. API Gateway invokes the AWS Lambda function in the VPC.
4. Lambda retrieves required secrets from AWS Secrets Manager.
5. Lambda performs read only queries by calling the database over the site to site VPN.
6. Traffic routes privately through the Digital Ocean Cloud Firewall.
7. Lambda queries Digital Ocean Managed MySQL on the private endpoint.
8. Lambda writes logs to Amazon CloudWatch Logs.

## Notes
* A NAT gateway is not shown. If the function needs general outbound internet access you can add NAT later. Secret retrieval does not require it.
* If you need mutual TLS for the client request, use a separate custom domain in API Gateway that enables mutual TLS. CloudFront remains in front for normal public traffic.
* Keep TLS in place on every hop.

## Render the diagrams
```bash
brew install graphviz
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install diagrams==0.24.4
mkdir -p out
python draw_architecture_vpc.py
open out
