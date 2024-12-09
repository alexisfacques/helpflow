from typing import Literal, NotRequired, TypedDict


from .authentication import AuthenticationConfig
from .configuration import (
    ConnectorMode,
    ConnectorRuntimeSetting,
    ConnectorTriggerType,
    ConnectorTriggerFrequency
)
from .entity import Operator, Entity, EntityCacheControl, EntityDefinition, WriteOperationType


ErrorCode = Literal[
    # Invalid arguments provided as input/HttpStatus 400/413 from application/Bad Request exception from Application.
    # For example QueryURI too large, write request payload too large etc.
    'InvalidArgument'
    # Credentials were rejected by the underlying application/HttpStatus 401 from Application.
    'InvalidCredentials',
    # Resource access denied by the underlying application/HttpStatus 403 from Application.
    'AccessDenied',
    # The request to the underlying application timed out/HttpStatus 408 from Application/
    # HttpClient timeout while sending request.
    'RequestTimeout',
    # Request got rejected by the underlying application due to rate limit violation/HttpStatus 429 from Application.
    'RateLimitExceeded',
    # Application is not available to serve the requests at the moment/HttpStatus 503 from Application.
    'ServiceUnavailable',
    # Specifies error is due to client or HttpStatus 4XX from Application.
    # Use specific error codes if present.
    'ClientError',
    # Specifies error is due to Application or HttpStatus 5XX from Application.
    # Use specific error codes if present.
    'ServerError',
    # Unknown Error from the Application. Use this ErrorCode only when you are not able to use the
    # other specific error codes.
    'UnknownError',
    # Specifies that the connector encountered failure, for some records, while writing to the application.
    'PartialWriteFailure',
    # Specifies that the connector is unable to find resource like AWS SecretManagerARN etc.
    'ResourceNotFoundError'
]

class ErrorDetails(TypedDict):
    errorCode: ErrorCode
    errorMessage: str
    retryAfterSeconds: NotRequired[int]

class AppFlowResponse(TypedDict):
    isSuccess: bool
    errorDetails: NotRequired[ErrorDetails]

class DescribeConnectorConfigurationResponse(AppFlowResponse):
    connectorOwner: str
    connectorName: str
    connectorVersion: str
    connectorModes: list[ConnectorMode]
    supportedApiVersions: list[str]
    operatorsSupported: list[Operator]
    triggerFrequenciesSupported: list[ConnectorTriggerFrequency]
    supportedWriteOperations: list[WriteOperationType]
    supportedTriggerTypes: list[ConnectorTriggerType]
    authenticationConfig: AuthenticationConfig
    connectorRuntimeSetting: NotRequired[list[ConnectorRuntimeSetting]]
    logoUrl: NotRequired[str]

class DescribeEntityResponse(AppFlowResponse):
    entityDefinition: EntityDefinition
    cacheControl: NotRequired[EntityCacheControl]

class ListEntitiesResponse(AppFlowResponse):
    entities: list[Entity]
    nextToken: NotRequired[str | None]
    cacheControl: NotRequired[EntityCacheControl]

class QueryDataResponse(AppFlowResponse):
    nextToken: NotRequired[str]
    records: NotRequired[list[str]]

class RetrieveDataResponse(AppFlowResponse):
    records: NotRequired[list[str]]

class ValidateConnectorRuntimeSettingsResponse(AppFlowResponse):
    errorsByInputField: NotRequired[dict[str, str]]

class ValidateCredentialsResponse(AppFlowResponse):
    pass

class WriteRecordResult(AppFlowResponse):
    recordId: str

class WriteDataResponse(AppFlowResponse):
    writeRecordResults: NotRequired[list[WriteRecordResult]]

