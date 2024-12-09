from typing import Literal, TypedDict, NotRequired

AuthenticationType = Literal[
    'BasicAuth',
    'CustomAuth',
    'OAuth2',
    'ApiKey'
]

OAuth2GrantType = Literal[
    'CLIENT_CREDENTIALS',
    'AUTHORIZATION_CODE'
]

OAuth2ContentType = Literal[
    'URL_ENCODED'
    'APPLICATION_JSON'
]

OAuth2MethodType = Literal[
    'HTTP_POST'
    'HTTP_GET'
]

class AuthParameter(TypedDict):
    key: str
    required: bool
    label: str
    description: str
    sensitiveField: NotRequired[bool]
    connectorSuppliedValues: NotRequired[list[str]]

class OAuth2Defaults(TypedDict):
    tokenUrl: list[str]
    authUrl: list[str]
    oAuth2GrantTypesSupported: NotRequired[list[OAuth2GrantType]]
    oAuth2Scopes: NotRequired[list[str]]
    oAuth2CustomProperties: NotRequired[list[AuthParameter]]
    addBasicAuthHeader: bool
    oAuth2ContentType: OAuth2ContentType
    oAuth2MethodType: OAuth2MethodType

class CustomAuthConfig(TypedDict):
    authenticationType: str
    authParameters: list[AuthParameter]

class AuthenticationConfig(TypedDict):
    isBasicAuthSupported: NotRequired[bool]
    isApiKeyAuthSupported: NotRequired[bool]
    isOAuth2Supported: NotRequired[bool]
    isCustomAuthSupported: NotRequired[bool]
    oAuth2Defaults: NotRequired[OAuth2Defaults | None]
    customAuthConfig: NotRequired[list[CustomAuthConfig] | None]
