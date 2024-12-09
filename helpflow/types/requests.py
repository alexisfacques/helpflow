from typing import Literal, NotRequired, TypedDict

from .authentication import AuthenticationType
from .entity import EntityDefinition, WriteOperationType
from .configuration import ConnectorRuntimeSettings, ConnectorRuntimeSettingScope

##

##

AppFlowEventType = Literal[
    'DescribeConnectorConfigurationRequest',
    'DescribeEntityRequest',
    'ListEntitiesRequest',
    'QueryDataRequest',
    'RetrieveDataRequest',
    'ValidateConnectorRuntimeSettingsRequest',
    'ValidateCredentialsRequest',
    'WriteDataRequest'
]

##

##

class Credentials(TypedDict):
    secretArn: str
    authenticationType: AuthenticationType

class ConnectorContext(TypedDict):
    credentials: NotRequired[Credentials]
    apiVersion: str
    connectorRuntimeSettings: NotRequired[ConnectorRuntimeSettings]
    entityDefinition: NotRequired[EntityDefinition]

###

###

class AppFlowEvent(TypedDict):
    type: AppFlowEventType

class DescribeConnectorConfigurationRequest(TypedDict):
    type: Literal['DescribeConnectorConfigurationRequest']
    locale: str

class DescribeEntityRequest(TypedDict):
    type: Literal['DescribeEntityRequest']
    entityIdentifier: str
    connectorContext: ConnectorContext

class ListEntitiesRequest(TypedDict):
    type: Literal['ListEntitiesRequest']
    connectorContext: ConnectorContext
    entitiesPath: NotRequired[str | None]
    nextToken: NotRequired[str]
    maxResult: NotRequired[int]

class QueryDataRequest(TypedDict):
    type: Literal['QueryDataRequest']
    entityIdentifier: str
    connectorContext: ConnectorContext
    selectedFieldNames: list[str]
    filterExpression: NotRequired[str]
    nextToken: NotRequired[str]
    maxResult: NotRequired[int]

class RetrieveDataRequest(TypedDict):
    type: Literal['RetrieveDataRequest']
    entityIdentifier: str
    connectorContext: ConnectorContext
    selectedFieldNames: list[str]
    idFieldName: NotRequired[str]
    ids: NotRequired[list[str]]

class ValidateConnectorRuntimeSettingsRequest(TypedDict):
    type: Literal['ValidateConnectorRuntimeSettingsRequest']
    scope: ConnectorRuntimeSettingScope
    connectorRuntimeSettings: ConnectorRuntimeSettings

class ValidateCredentialsRequest(TypedDict):
    type: Literal['ValidateCredentialsRequest']
    credentials: Credentials
    connectorRuntimeSettings: NotRequired[ConnectorRuntimeSettings | None]

class WriteDataRequest(TypedDict):
    type: Literal['WriteDataRequest']
    entityIdentifier: str
    connectorContext: ConnectorContext
    operation: WriteOperationType
    idFieldNames: NotRequired[list[str]]
    records: NotRequired[list[str]]
    allOrNone: NotRequired[bool]
