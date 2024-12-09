from typing import Literal, TypedDict

ConnectorMode = Literal[
    'SOURCE',
    'DESTINATION'
]

ConnectorRuntimeSettings = dict[str, str]

ConnectorRuntimeSettingDataType = Literal[
    'String',
    'Date',
    'DateTime',
    'Long',
    'Integer',
    'Boolean'
]   

ConnectorRuntimeSettingScope = Literal[
    # Settings to be populated during connector profile creation.
    'CONNECTOR_PROFILE',
    # Setting to be populated during a flow creation if the connector is chosen as a source connector.
    'SOURCE',
    # Setting to be populated during a flow creation if the connector is chosen as a destination connector.
    'DESTINATION',
    # Setting to be populated during a flow creation if the connector is chosen either as a source or a destination
    # connector.
    'SOURCE_AND_DESTINATION'
]

ConnectorTriggerType = Literal[
    'SCHEDULED',
    'ONDEMAND'
]

ConnectorTriggerFrequency = Literal[
    'BYMINUTE',
    'HOURLY',
    'DAILY',
    'WEEKLY',
    'MONTHLY',
    'ONCE',
]

class ConnectorRuntimeSetting(TypedDict):
    key: str
    dataType: ConnectorRuntimeSettingDataType
    required: bool
    label: str
    description: str
    scope: ConnectorRuntimeSettingScope
    connectorSuppliedValueOptions: list[str]