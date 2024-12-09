from .app_flow_connector import AppFlowConnector
from .app_flow_entity import AppFlowEntity
from .handlers import CredentialsSecretValue, ConnectorRuntimeSettings
from .requests import AppFlowEvent
from .lambda_context import LambdaContext


teams: AppFlowEntity = AppFlowEntity(
    id='teams',
    fields=(
        {
            'fieldName': 'Team_ID',
            'dataType': 'Integer',
            'isPrimaryKey': True,
            'isDeprecated': False,
            'readProperties': {
                'isRetrievable': True,
                'isNullable': False,
                'isQueryable': False,
                'isTimestampFieldForIncrementalQueries': False
            }
        },
        {
            'fieldName': 'Name',
            'dataType': 'String',
            'isPrimaryKey': False,
            'isDeprecated': False,
            'readProperties': {
                'isRetrievable': True,
                'isNullable': False,
                'isQueryable': False,
                'isTimestampFieldForIncrementalQueries': False
            }
        }
    )
)

sessions: AppFlowEntity = AppFlowEntity(
    id='sessions',
    fields=(
        {
            'fieldName': 'teamID',
            'dataType': 'Integer',
            'isPrimaryKey': False,
            'isDeprecated': False,
            'readProperties': {
                'isRetrievable': False,
                'isNullable': False,
                'isQueryable': True,
                'isTimestampFieldForIncrementalQueries': False
            }
        },
        {
            'fieldName': 'minDate',
            'dataType': 'Integer',
            'isPrimaryKey': False,
            'isDeprecated': False,
            'readProperties': {
                'isRetrievable': False,
                'isNullable': False,
                'isQueryable': True,
                'isTimestampFieldForIncrementalQueries': True
            }
        },
        {
            'fieldName': 'Session_ID',
            'dataType': 'Integer',
            'isPrimaryKey': True,
            'isDeprecated': False,
            'readProperties': {
                'isRetrievable': True,
                'isNullable': False,
                'isQueryable': False,
                'isTimestampFieldForIncrementalQueries': False
            }
        },
        {
            'fieldName': 'Team_ID',
            'dataType': 'Integer',
            'isPrimaryKey': False,
            'isDeprecated': False,
            'readProperties': {
                'isRetrievable': True,
                'isNullable': False,
                'isQueryable': False,
                'isTimestampFieldForIncrementalQueries': False
            }
        },
        {
            'fieldName': 'Training',
            'dataType': 'Boolean',
            'isPrimaryKey': False,
            'isDeprecated': False,
            'readProperties': {
                'isRetrievable': True,
                'isNullable': False,
                'isQueryable': False,
                'isTimestampFieldForIncrementalQueries': False
            }
        },
        {
            'fieldName': 'Session',
            'dataType': 'String',
            'isPrimaryKey': False,
            'isDeprecated': False,
            'readProperties': {
                'isRetrievable': True,
                'isNullable': False,
                'isQueryable': False,
                'isTimestampFieldForIncrementalQueries': False
            }
        },
        {
            'fieldName': 'Drill',
            'dataType': 'String',
            'isPrimaryKey': False,
            'isDeprecated': False,
            'readProperties': {
                'isRetrievable': True,
                'isNullable': False,
                'isQueryable': False,
                'isTimestampFieldForIncrementalQueries': False
            }
        },
        {
            'fieldName': 'Note',
            'dataType': 'Integer',
            'isPrimaryKey': False,
            'isDeprecated': False,
            'readProperties': {
                'isRetrievable': True,
                'isNullable': True,
                'isQueryable': False,
                'isTimestampFieldForIncrementalQueries': False
            }
        },
        {
            'fieldName': 'Date',
            'dataType': 'Integer',
            'isPrimaryKey': False,
            'isDeprecated': False,
            'readProperties': {
                'isRetrievable': True,
                'isNullable': False,
                'isQueryable': False,
                'isTimestampFieldForIncrementalQueries': False
            }
        }
    )
)

@teams.Query()
def get_teams():
    return

AppFlowConnector.RegisterEntity(teams)

AppFlowConnector.HandleBasicAuthorization()
def validate_basic_authorization(
    credentials: CredentialsSecretValue,
    config: ConnectorRuntimeSettings | None,
    context: LambdaContext
) -> bool:
    return True


def lambda_handler(event: AppFlowEvent, context: LambdaContext):
    """
    """
    connector = AppFlowConnector()

    return connector(event, context)