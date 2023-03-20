from __future__ import annotations
from typing import Any, Dict, Iterator, List, Optional
import json

# From requirements.txt:
from custom_connector_sdk.lambda_handler.requests import QueryDataRequest


class RequestQueryHandler():
    def __init__(self, selected_field_names: List[str], filter_expression: Optional[str] = None):
        self.__selected_field_names = selected_field_names
        self.__filters: Optional[Dict[str, Any]] = None

        if filter_expression:
            self.__filters = self.parse_filter_expression(filter_expression)

    @property
    def selected_field_names(self) -> List[str]:
        return self.__selected_field_names

    @property
    def filters(self) -> Dict[str, Any]:
        return self.__filters or {}

    def connector_runtime_settings(self) -> Dict[str, Any]:
        pass

    def as_selected_fields_iter(self, records: Iterator[Dict[str, Any]]) -> Iterator[str]:
        return (json.dumps({k: v for k, v in record.items() if k in self.__selected_field_names})
                for record in records)

    @staticmethod
    def from_query_data_request(request: QueryDataRequest) -> 'RequestQueryHandler':
        return RequestQueryHandler(request.selected_field_names, request.filter_expression)

    @staticmethod
    def parse_filter_expression(exp: str) -> Dict[str, Any]:
        pass
