from __future__ import annotations
from base64 import urlsafe_b64encode, urlsafe_b64decode
import json

from typing import Any, Dict, Optional, Union

# From requirements.txt:
from custom_connector_sdk.lambda_handler.requests import QueryDataRequest


class RequestContinuationHandler():
    def __init__(self, max_results: Union[int, str], next_token: Optional[str] = None):
        self.__max_results: int = int(max_results)
        self.state: Optional[Dict[str, Any]] = None

        if next_token is not None:
            self.state = self.decode_token(next_token)

    @property
    def max_results(self) -> int:
        return self.__max_results

    @property
    def next_token(self) -> Optional[str]:
        if self.state:
            return self.encode_token(self.state)

        return None

    @staticmethod
    def from_query_data_request(request: QueryDataRequest) -> 'RequestContinuationHandler':
        return RequestContinuationHandler(request.max_results, request.next_token)

    @staticmethod
    def decode_token(next_token: str) -> Optional[Dict[str, Any]]:
        ret = json.loads(urlsafe_b64decode(next_token))
        if isinstance(ret, dict):
            return ret

        raise ValueError('Invalid token value.')

    @staticmethod
    def encode_token(state: Dict[str, Any]) -> str:
        return urlsafe_b64encode(json.dumps(state).encode('utf-8')).decode('utf-8')
