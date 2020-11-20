from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB
from diagrams.aws.network import Route53, CloudFront
from diagrams.onprem.database import PostgreSQL  # Would typically use RDS from aws.database
from diagrams.onprem.inmemory import Redis  # Would typically use ElastiCache from aws.database
from diagrams.aws.storage import S3
from diagrams.aws.database import Aurora

with Diagram(
        "Simple Programs API", direction='LR'
) as diag:  # It's LR by default, but you have a few options with the orientation
    dns = Route53("dns")
    load_balancer = ELB("Load Balancer")
    # database = PostgreSQL("Programs DB")
    cache = Redis("Cache")
    content = S3("Blob storage")
    content_cache = CloudFront("CloudFront")

    with Cluster("DB Cluster"):
        db_main = Aurora("main")
        db_main - [Aurora("backup"), Aurora("backup")]

    with Cluster("Programs API Cluster"):
        svc_group = [EC2("Server 1"), EC2("Server 2"), EC2("Server 3")]
    dns >> load_balancer >> svc_group
    svc_group >> cache >> db_main
    svc_group >> db_main
    svc_group >> content_cache >> content
diag
