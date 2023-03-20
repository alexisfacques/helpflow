"""A handler object class for AppFlow entity definitions and resolver strategy, per entity."""
import json
import logging
from typing import Any, Callable, Dict, Iterator, Optional, Tuple, TypedDict, cast
from urllib3 import Retry

# From requirements.txt:
import boto3
from cachetools import cached, TTLCache
from requests.adapters import HTTPAdapter
from requests import Session

from custom_connector_sdk.connector.context import EntityDefinition

from custom_connector_sdk.lambda_handler.handlers import MetadataHandler, RecordHandler
from custom_connector_sdk.lambda_handler.requests import DescribeEntityRequest, ListEntitiesRequest, \
                                                         QueryDataRequest, RetrieveDataRequest, WriteDataRequest
from custom_connector_sdk.lambda_handler.responses import DescribeEntityResponse, ListEntitiesResponse, \
                                                          QueryDataResponse, RetrieveDataResponse, WriteDataResponse, \
                                                          ErrorCode, ErrorDetails

# From local modules:
from .handlers import RequestContinuationHandler, RequestQueryHandler

# Type annotations:
PageTuple = Tuple[RequestContinuationHandler, Iterator[Dict[str, Any]]]


LOGGER = logging.getLogger()


class AppFlowCredentials(TypedDict):
    apiKey: str
    authenticationType: str
    apiSecretKey: str


@cached(cache=TTLCache(maxsize=1024, ttl=300))
def get_appflow_credentials(**kwargs) -> AppFlowCredentials:
    client = boto3.client('secretsmanager')

    response = client.get_secret_value(**kwargs)
    return cast(AppFlowCredentials, json.loads(response['SecretString']))


def get_session(secret_arn: str) -> Session:
    HTTP_ADAPTER: HTTPAdapter = HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1))

    credentials: AppFlowCredentials = get_appflow_credentials(SecretId=secret_arn)
    http: Session = Session()

    http.mount('https://', HTTP_ADAPTER)
    http.mount('http://', HTTP_ADAPTER)

    if credentials['authenticationType'] == 'APIKEY':
        http.params[credentials['apiKey']] = credentials['apiSecretKey']
        return http
    else:
        raise ValueError('Unsupported authenticationType \'%s\'.' % credentials['authenticationType'])


class HelpFlowResolver(MetadataHandler, RecordHandler):
    __resolvers: Dict[str, Tuple[EntityDefinition, Callable[[Session, RequestContinuationHandler,
                                                             RequestQueryHandler], PageTuple]]] = {}

    def list_entities(self, request: ListEntitiesRequest) -> ListEntitiesResponse:
        return ListEntitiesResponse(
            is_success=True,
            entities=[entity_definition.entity for entity_definition, _ in self.__resolvers.values()]
        )

    def describe_entity(self, request: DescribeEntityRequest) -> DescribeEntityResponse:
        return DescribeEntityResponse(
            is_success=True,
            entity_definition=self.__resolvers[request.entity_identifier][0]
        )

    def query_data(self, request: QueryDataRequest) -> QueryDataResponse:
        try:
            session: Session = get_session(request.connector_context.credentials.secret_arn)
            continuation: RequestContinuationHandler = RequestContinuationHandler.from_query_data_request(request)
            parameters: RequestQueryHandler = RequestQueryHandler.from_query_data_request(request)

            continuation, records = self.__resolvers[request.entity_identifier][1](session, continuation, parameters)
            next_token: Optional[str] = continuation.next_token if continuation is not None else None

            ret = QueryDataResponse(is_success=True, records=list(records), next_token=next_token)
            LOGGER.info(ret)
            return ret

        except Exception as err:
            error_details = ErrorDetails(error_code=ErrorCode.ServerError, error_message=str(err))
            return QueryDataResponse(is_success=False, records=[], error_details=error_details)

    def retrieve_data(self, request: RetrieveDataRequest) -> RetrieveDataResponse:
        return RetrieveDataResponse(is_success=True, records=[])  # TODO

    def write_data(self, request: WriteDataRequest) -> WriteDataResponse:
        return WriteDataResponse(is_success=False)  # Write mode is not supported by this connector.

    @staticmethod
    def entity(definition: EntityDefinition):
        def wrapper(handler: Callable[[Session, RequestContinuationHandler, RequestQueryHandler], PageTuple]):
            HelpFlowResolver.__resolvers[definition.entity.entity_identifier] = (definition, handler)

        return wrapper
