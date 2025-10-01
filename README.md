# ACLED API Platform — architecture diagrams as code

This repository renders the ACLED Trendfinder style API architecture using the `diagrams` Python library and Graphviz.  
The diagram shows an application service on DigitalOcean calling an AWS HTTP API on API Gateway that triggers a Lambda which reads from a DigitalOcean Managed MySQL database over TLS. Optional CloudFront, ACM and CloudWatch are included.

## Prerequisites
* macOS with Homebrew
* Python 3.9 or newer
* Graphviz

Install:
```bash
brew install graphviz
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
