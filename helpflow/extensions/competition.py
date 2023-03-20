"""Foo."""
from typing import Any, Dict

# From requirements.txt:
from custom_connector_sdk.connector.context import Entity, EntityDefinition
from custom_connector_sdk.connector.fields import FieldConstraints, FieldDataType, FieldDefinition, \
                                                  RangeConstraint, ReadOperationProperty
from helpflow import HelpFlowResolver
from helpflow.helpflow_resolver import PageTuple
from helpflow.handlers import RequestContinuationHandler, RequestQueryHandler
from requests import Session

from ..skillcorner_utils import get_offset


@HelpFlowResolver.entity(definition=EntityDefinition(
    entity=Entity(
        entity_identifier='/competitions/',
        label='Competitions',
        has_nested_entities=True,
        is_writable=False
    ),
    fields=[
        # API response parameters.
        FieldDefinition(
            field_name='id',
            data_type=FieldDataType.Integer,
            label='Competition ID',
            is_primary_key=True,
            is_deprecated=False,
            read_properties=ReadOperationProperty(
                is_retrievable=True,
                is_nullable=False,
                is_queryable=False,
                is_timestamp_field_for_incremental_queries=False
            )
        ),
        FieldDefinition(
            field_name='area',
            data_type=FieldDataType.String,
            label='Area',
            is_primary_key=False,
            is_deprecated=False,
            constraints=FieldConstraints(
                allowed_length_range=RangeConstraint(
                    min_range=1,
                    max_range=10
                )
            ),
            read_properties=ReadOperationProperty(
                is_retrievable=True,
                is_nullable=False,
                is_queryable=False,
                is_timestamp_field_for_incremental_queries=False
            )
        ),
        FieldDefinition(
            field_name='name',
            data_type=FieldDataType.String,
            label='Competition name',
            is_primary_key=False,
            is_deprecated=False,
            constraints=FieldConstraints(
                allowed_length_range=RangeConstraint(
                    min_range=1,
                    max_range=50
                )
            ),
            read_properties=ReadOperationProperty(
                is_retrievable=True,
                is_nullable=False,
                is_queryable=False,
                is_timestamp_field_for_incremental_queries=False
            )
        )
    ]
))
def get_competitions(http: Session, continuation: RequestContinuationHandler, params: RequestParametersHandler) \
        -> PageTuple:
    qs: Dict[str, str] = {'limit': str(continuation.max_results)}

    if continuation.state is not None and 'offset' in continuation.state:
        qs['offset'] = continuation.state['offset']

    res = http.get('https://skillcorner.com/api/competitions/', params=qs)
    res.raise_for_status()

    payload: Dict[str, Any] = res.json()

    continuation.state = ({'offset': get_offset(payload['next'])} if 'next' in payload
                          and payload['next'] is not None else {})

    return (continuation, params.as_selected_fields_iter(payload.get('results', [])))
