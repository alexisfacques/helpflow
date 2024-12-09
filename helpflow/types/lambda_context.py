from typing import Any, TypedDict

class Identity(TypedDict):
    cognito_identity_id: str
    cognito_identity_pool_id: str

class Client(TypedDict):
    installation_id: str
    app_title: str
    app_version_name: str
    app_version_code: str
    app_package_name: str

class ClientContext(TypedDict):
    client: Client
    custom: dict[str, Any]
    env: dict[str, Any]

class LambdaContext:
    function_name: str
    function_version: str
    invoked_function_arn: str
    memory_limit_in_mb: str
    aws_request_id: str
    log_group_name: str
    log_stream_name: str
    identity: Identity
    client_context: ClientContext

    @staticmethod
    def get_remaining_time_in_millis() -> int:
        return 0