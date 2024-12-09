import json

import boto3
from cachetools import cached, TTLCache

@cached(cache=TTLCache(maxsize=1024, ttl=300))
def get_appflow_credentials(secret_arn: str) -> dict[str, str]:
    client = boto3.client('secretsmanager')

    response = client.get_secret_value(SecretId=secret_arn)
    return json.loads(response['SecretString'])
