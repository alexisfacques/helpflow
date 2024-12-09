from typing import Callable

from .lambda_context import LambdaContext

from .requests import (
    ConnectorRuntimeSettings,
    DescribeConnectorConfigurationRequest,
    DescribeEntityRequest,
    ListEntitiesRequest,
    QueryDataRequest,
    RetrieveDataRequest,
    ValidateConnectorRuntimeSettingsRequest,
    WriteDataRequest
)
from .responses import (
    DescribeConnectorConfigurationResponse,
    DescribeEntityResponse,
    ListEntitiesResponse,
    QueryDataResponse,
    RetrieveDataResponse,
    ValidateConnectorRuntimeSettingsResponse,
    WriteDataResponse
)

CredentialsSecretValue = dict[str, str]

DescribeConnectorConfigurationHandler = Callable[[DescribeConnectorConfigurationRequest, LambdaContext], DescribeConnectorConfigurationResponse]
DescribeEntityHandler = Callable[[DescribeEntityRequest, LambdaContext], DescribeEntityResponse]
ListEntitiesHandler = Callable[[ListEntitiesRequest, LambdaContext], ListEntitiesResponse]
QueryDataHandler = Callable[[QueryDataRequest, LambdaContext], QueryDataResponse]
RetrieveDataHandler = Callable[[RetrieveDataRequest, LambdaContext], RetrieveDataResponse]
ValidateConnectorRuntimeSettingsHandler = Callable[[ValidateConnectorRuntimeSettingsRequest, LambdaContext], ValidateConnectorRuntimeSettingsResponse]

ValidateCredentialsHandler = Callable[
    [CredentialsSecretValue, ConnectorRuntimeSettings | None, LambdaContext],
    bool
]

WriteDataHandler = Callable[[WriteDataRequest, LambdaContext], WriteDataResponse]