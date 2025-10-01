from diagrams import Diagram, Cluster, Edge

# AWS
from diagrams.aws.network import APIGateway, CloudFront
from diagrams.aws.compute import Lambda
from diagrams.aws.security import CertificateManager, SecretsManager
from diagrams.aws.management import Cloudwatch

# Digital Ocean
from diagrams.digitalocean.database import DbaasPrimary
from diagrams.digitalocean.network import Firewall

# Generic
from diagrams.onprem.client import Users
from diagrams.programming.language import Python
from diagrams.generic.network import VPN

# Edge styles
VPN_EDGE = Edge(color="gray40", style="dashed", label="IPsec")
READONLY_EDGE = Edge(color="gray40", style="dashed", label="read only")
PRIVATE_ROUTE_EDGE = Edge(color="gray40", style="dashed", label="private route")
SECRETS_EDGE = Edge(color="gray40", style="dashed", label="secrets")

# ---------------------------------------------------------
# Diagram 1. Platform view for cloud engineering
# ---------------------------------------------------------
with Diagram(
    "ACLED API Platform with VPCs and VPN",
    filename="out/acled_api_platform_vpc",
    outformat="png",
    show=False,
    direction="LR",
    graph_attr={"nodesep": "1.8", "ranksep": "1.6", "pad": "0.3", "splines": "spline"},
    node_attr={"fontsize": "11"},
    edge_attr={"fontsize": "10"},
):
    app = Users("Application service\nDigital Ocean Droplet")

    with Cluster("AWS"):
        cloudfront = CloudFront("Amazon CloudFront")
        apigw = APIGateway("Amazon API Gateway\nHTTP API")
        acm = CertificateManager("AWS Certificate Manager")
        secrets = SecretsManager("AWS Secrets Manager")

        with Cluster("AWS VPC"):
            lambda_fn = Lambda("AWS Lambda\nVPC attached")
            cw_logs = Cloudwatch("Amazon CloudWatch Logs")
            aws_vpn = VPN("AWS site to site VPN")

        acm >> cloudfront
        app >> cloudfront >> apigw >> lambda_fn
        lambda_fn >> cw_logs
        secrets >> SECRETS_EDGE >> lambda_fn

    with Cluster("Digital Ocean"):
        with Cluster("Digital Ocean VPC"):
            do_vpn = VPN("Digital Ocean VPN gateway")
            do_fw = Firewall("Digital Ocean Cloud Firewall")
            do_db = DbaasPrimary("Digital Ocean Managed MySQL\nprivate endpoint")
            do_vpn >> PRIVATE_ROUTE_EDGE >> do_fw >> do_db

    aws_vpn >> VPN_EDGE >> do_vpn
    lambda_fn >> READONLY_EDGE >> aws_vpn

# ---------------------------------------------------------
# Diagram 2. Backend request flow for application team
# ---------------------------------------------------------
with Diagram(
    "Request flow for backend developers",
    filename="out/request_flow_app_team",
    outformat="png",
    show=False,
    direction="LR",
    graph_attr={"nodesep": "2.0", "ranksep": "1.7", "pad": "0.4", "splines": "spline"},
    node_attr={"fontsize": "11"},
    edge_attr={"fontsize": "10"},
):
    app = Users("App on Digital Ocean Droplet")
    cf = CloudFront("Amazon CloudFront")
    api = APIGateway("Amazon API Gateway\nHTTP API")

    with Cluster("AWS Lambda function"):
        fn = Lambda("Handler")
        validator = Python("OpenAPI validator\nPydantic")

    logs = Cloudwatch("Amazon CloudWatch Logs")
    secrets = SecretsManager("AWS Secrets Manager")
    vpn = VPN("Site to site VPN")
    fw = Firewall("Digital Ocean Cloud Firewall")
    db = DbaasPrimary("Digital Ocean MySQL\nprivate endpoint")

    app >> Edge(label="1 request") >> cf
    cf >> Edge(label="2 forward") >> api
    api >> Edge(label="3 invoke") >> fn
    validator >> Edge(label="4 ok") >> fn
    secrets >> Edge(label="3a get secrets") >> fn
    fn >> Edge(label="8 write logs") >> logs
    fn >> Edge(label="3b validate") >> validator
    fn >> Edge(label="5 read only") >> vpn
    vpn >> Edge(label="6 private route") >> fw
    fw >> Edge(label="7 query") >> db
