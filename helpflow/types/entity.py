from typing import Literal, NotRequired, TypedDict

Operator = Literal[
    # Column Filter Operator
    'PROJECTION',
    # Row Filter Operators
    'LESS_THAN',
    'GREATER_THAN',
    'BETWEEN',
    'LESS_THAN_OR_EQUAL_TO',
    'GREATER_THAN_OR_EQUAL_TO',
    'EQUAL_TO',
    'CONTAINS',
    'NOT_EQUAL_TO',
    # Operators with a Destination Field
    'ADDITION',
    'SUBTRACTION',
    'MULTIPLICATION',
    'DIVISION',
    # Masking related operators
    'MASK_ALL',
    'MASK_FIRST_N',
    'MASK_LAST_N',
    # Validation specific operators
    'VALIDATE_NON_NULL',
    'VALIDATE_NON_ZERO',
    'VALIDATE_NON_NEGATIVE',
    'VALIDATE_NUMERIC',
    # No op
    'NO_OP'
]

EntityCacheControlUnit = Literal[
    'NANOSECONDS',
    'MICROSECONDS',
    'MILLISECONDS',
    'SECONDS',
    'MINUTES',
    'HOURS',
    'DAYS'
]

FieldDataType = Literal[
    'String',
    'Integer',
    'Float',
    'Double',
    'Long',
    'Short',
    'BigInteger',
    'BigDecimal',
    'ByteArray',
    'Boolean',
    'Date',
    'DateTime',
    'Struct',
    'Map',
    'List'
]

WriteOperationType = Literal[
    'INSERT',
    'UPDATE',
    'UPSERT',
    'DELETE'
]

class EntityCacheControl(TypedDict):
    timeToLive: NotRequired[int]
    timeToLiveUnit: NotRequired[EntityCacheControlUnit]

class RangeConstraint(TypedDict):
    minRange: float
    maxRange: float

class FieldConstraints(TypedDict):
    allowedLengthRange: NotRequired[RangeConstraint]
    allowedValueRange: NotRequired[RangeConstraint]
    allowedValues: NotRequired[list[str]]
    allowedValuesRegexPattern: NotRequired[str]
    allowedDateFormat: NotRequired[str]

class WriteProperties(TypedDict):
    isCreatable: NotRequired[bool]
    isNullable: NotRequired[bool]
    isQueryable: NotRequired[bool]
    isUpsertable: NotRequired[bool]
    isDefaultedOnCreate: NotRequired[bool]
    supportedWriteOperations: NotRequired[list[WriteOperationType]]

class ReadProperties(TypedDict):
    isRetrievable: NotRequired[bool]
    isNullable: NotRequired[bool]
    isQueryable: NotRequired[bool]
    isTimestampFieldForIncrementalQueries: NotRequired[bool]

class FieldDefinition(TypedDict):
    fieldName: str
    dataType: FieldDataType
    label: NotRequired[str]
    description: NotRequired[str]
    isPrimaryKey: NotRequired[bool]
    defaultValue: NotRequired[str]
    isDeprecated: NotRequired[bool]
    constraints: NotRequired[FieldConstraints]
    readProperties: NotRequired[ReadProperties]
    writeProperties: NotRequired[WriteProperties]
    customProperties: NotRequired[dict[str, str]]
    filterOperators: NotRequired[list[Operator]] # TODO!! SOME FILTERS ARE DATA_TYPE-SPECIFIC
    dataTypeLabel: NotRequired[str]

class Entity(TypedDict):
    entityIdentifier: str
    hasNestedEntities: bool
    isWritable: bool
    label: NotRequired[str | None]
    description: NotRequired[str | None]

class EntityDefinition(TypedDict):
    entity: Entity
    fields: list[FieldDefinition]
    customProperties: NotRequired[dict[str, str] | None]
