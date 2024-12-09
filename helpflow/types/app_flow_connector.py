from typing import cast
from collections.abc import Iterator

from .requests import (
    AppFlowEvent,
    DescribeConnectorConfigurationRequest,
    DescribeEntityRequest,
    ListEntitiesRequest,
    QueryDataRequest,
    RetrieveDataRequest,
    ValidateConnectorRuntimeSettingsRequest,
    ValidateCredentialsRequest,
    WriteDataRequest
)

from .authentication import (
    AuthenticationType,
    AuthenticationConfig,
    CustomAuthConfig,
    OAuth2Defaults
)

from .responses import (
    AppFlowResponse,
    DescribeConnectorConfigurationResponse,
    DescribeEntityResponse,
    ListEntitiesResponse,
    QueryDataResponse,
    RetrieveDataResponse,
    ValidateConnectorRuntimeSettingsResponse,
    ValidateCredentialsResponse,
    WriteDataResponse
)

from .handlers import (
    ValidateCredentialsHandler,
)

from .app_flow_entity import AppFlowEntity

from .utilities import get_appflow_credentials

from .configuration import ConnectorMode
from .lambda_context import LambdaContext


class AppFlowConnector:
    __registered_entities: dict[str, AppFlowEntity] = {}

    __custom_authorizers: dict[str, tuple[ValidateCredentialsHandler, CustomAuthConfig]] = {}
    __authorizers: dict[
        AuthenticationType,
        tuple[ValidateCredentialsHandler, OAuth2Defaults | None]
    ] = {}

    def __init__(self) -> None:
        pass

    @staticmethod
    def HandleApiKeyAuthorization():
        def wrapper(fn: ValidateCredentialsHandler):
            AppFlowConnector.__authorizers['ApiKey'] = (fn, None)
            return fn
        return wrapper
    
    @staticmethod
    def HandleBasicAuthorization():
        def wrapper(fn: ValidateCredentialsHandler):
            AppFlowConnector.__authorizers['BasicAuth'] = (fn, None)
            return fn
        return wrapper

    @staticmethod
    def HandleCustomAuthorization(config: CustomAuthConfig):
        def wrapper(fn: ValidateCredentialsHandler):
            # TODO: Throw error if authorizer already declared?
            AppFlowConnector.__custom_authorizers[config['authenticationType']] = (fn, config)
            return fn
        return wrapper

    @staticmethod
    def HandleOAuth2Authorization(config: OAuth2Defaults):
        def wrapper(fn: ValidateCredentialsHandler):
            AppFlowConnector.__authorizers['OAuth2'] = (fn, config)
            return fn
        return wrapper
    
    @staticmethod
    def RegisterEntity(entity: AppFlowEntity):
        AppFlowConnector.__registered_entities[entity.id] = entity
        return entity

    @property
    def authentication_config(self) -> AuthenticationConfig:
        """
        """
        return {
            'isBasicAuthSupported': 'BasicAuth' in self.__authorizers,
            'isApiKeyAuthSupported': 'ApiKey' in self.__authorizers,
            'isOAuth2Supported': 'OAuth2' in self.__authorizers,
            'isCustomAuthSupported': len(self.__custom_authorizers) > 0,
            'oAuth2Defaults': (
                cast(OAuth2Defaults, self.__authorizers['OAuth2'][1])
                if 'OAuth2' in self.__authorizers
                else None
            ),
            'customAuthConfig': (
                [auth[1] for auth in self.__custom_authorizers.values()]
                if len(self.__custom_authorizers) > 0
                else None
            )
        }
    
    @property
    def entities(self) -> Iterator[AppFlowEntity]:
        # TODO: Handle non registered entities.
        return iter(self.__registered_entities.values())

    @property
    def modes(self) -> list[ConnectorMode]:
        return ['SOURCE'] # TODO
    
    @property
    def supported_api_versions(self) -> list[str]:
        return ['ALL']

    def get_entity(self, id: str) -> AppFlowEntity:
        return self.__registered_entities[id]

    def __describe_connector_configuration(
            self,
            req: DescribeConnectorConfigurationRequest,
            context: LambdaContext
        ) -> DescribeConnectorConfigurationResponse:
        """
        """
        return {
            'isSuccess': True,
            'connectorOwner': 'FOO',
            'connectorName': 'Connector Name',
            'connectorVersion': 'Connector Version',
            'connectorModes': self.modes,
            'supportedApiVersions': self.supported_api_versions,
            'authenticationConfig': self.authentication_config,
            'operatorsSupported': list(),
            'triggerFrequenciesSupported': list(),
            'supportedWriteOperations': list(),
            'supportedTriggerTypes': list()
        }

    def __describe_entity(
            self,
            req: DescribeEntityRequest, 
            context: LambdaContext
        ) -> DescribeEntityResponse:
        """
        """
        # TODO: Handle Caching
        entity: AppFlowEntity = self.get_entity(req['entityIdentifier'])
        return {
            'isSuccess': True,
            'entityDefinition': entity.entity_definition
        }

    def __list_entities(
            self,
            req: ListEntitiesRequest,
            context: LambdaContext
        ) -> ListEntitiesResponse:
        """
        """
        # Handle max items and continuation.
        return {
            'isSuccess': True,
            'entities': list(e.entity for e in self.entities)
        }

    def __query_data(
            self,
            req: QueryDataRequest,
            context: LambdaContext
        ) -> QueryDataResponse:
        """
        """
        return {'isSuccess': True}

    def __retrieve_data(
            self,
            req: RetrieveDataRequest,
            context: LambdaContext
        ) -> RetrieveDataResponse:
        """
        """
        return {'isSuccess': True}

    def __validate_connector_runtime_settings(
            self,
            req: ValidateConnectorRuntimeSettingsRequest,
            context: LambdaContext
        ) -> ValidateConnectorRuntimeSettingsResponse:
        """
        """
        return {'isSuccess': True}

    def __validate_credentials(
            self,
            req: ValidateCredentialsRequest,
            context: LambdaContext
        ) -> ValidateCredentialsResponse:
        """
        """
        # TODO: Check how is handled CustomAuth.
        if req['credentials']['authenticationType'] not in self.__authorizers:
            raise Exception() # TODO
        
        handler: ValidateCredentialsHandler = self.__authorizers[
            req['credentials']['authenticationType']
        ][0]
        
        return {'isSuccess': handler(
            get_appflow_credentials(req['credentials']['secretArn']),
            req['connectorRuntimeSettings'] if 'connectorRuntimeSettings' in req else None,
            context
        )}

    def __write_data(
            self,
            req: WriteDataRequest,
            context: LambdaContext
        ) -> WriteDataResponse:
        """
        """
        return {'isSuccess': True}

    def __call__(self, event: AppFlowEvent, context: LambdaContext) -> AppFlowResponse:
        if event['type'] == 'DescribeConnectorConfigurationRequest':
            return self.__describe_connector_configuration(cast(DescribeConnectorConfigurationRequest, event), context)
        
        elif event['type'] == 'DescribeEntityRequest':
            return self.__describe_entity(cast(DescribeEntityRequest, event), context)
        
        elif event['type'] == 'ListEntitiesRequest':
            return self.__list_entities(cast(ListEntitiesRequest, event), context)
        
        elif event['type'] == 'QueryDataRequest':
            return self.__query_data(cast(QueryDataRequest, event), context)

        elif event['type'] == 'RetrieveDataRequest':
            return self.__retrieve_data(cast(RetrieveDataRequest, event), context)
        
        elif event['type'] == 'ValidateConnectorRuntimeSettingsRequest':
            return self.__validate_connector_runtime_settings(cast(ValidateConnectorRuntimeSettingsRequest, event), context)
        
        elif event['type'] == 'ValidateCredentialsRequest':
            return self.__validate_credentials(cast(ValidateCredentialsRequest, event), context)
        
        elif event['type'] == 'WriteDataRequest':
            return self.__write_data(cast(WriteDataRequest, event), context)
        
        else:
            return {'isSuccess': False,
                    'errorDetails': {'errorCode': 'ClientError',
                                     'errorMessage': 'Unsupported AWS AppFlow event type'}}

