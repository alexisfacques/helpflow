"""
In this module, we define the AppFlow Connector configuration panel. This includes:
- The capability of the connector:
  - supported modes,
  - supported Auth types,
  - scheduling frequencies,
  – runtime settings of different scopes (source mode, destination mode, both and connector profile) etc..

This information is fetched during connector registration process and stored in AppFlow connector registry.
Using this information Amazon AppFlow UI renders the connector and navigate the user accordingly.
"""
import os
from typing import Tuple

# From requirements.txt:
from custom_connector_sdk.connector.auth import AuthenticationConfig
from custom_connector_sdk.connector.configuration import ConnectorModes
from custom_connector_sdk.connector.context import ConnectorContext
from custom_connector_sdk.connector.settings import ConnectorRuntimeSetting, \
                                                    ConnectorRuntimeSettingDataType, \
                                                    ConnectorRuntimeSettingScope

from custom_connector_sdk.lambda_handler.handlers import ConfigurationHandler
from custom_connector_sdk.lambda_handler.requests import ValidateConnectorRuntimeSettingsRequest, \
                                                         ValidateCredentialsRequest, \
                                                         DescribeConnectorConfigurationRequest
from custom_connector_sdk.lambda_handler.responses import DescribeConnectorConfigurationResponse, \
                                                          ValidateConnectorRuntimeSettingsResponse, \
                                                          ValidateCredentialsResponse

API_VERSION: str = os.environ['API_VERSION']

CONNECTOR_OWNER: str = os.environ['CONNECTOR_OWNER']
CONNECTOR_NAME: str = os.environ['CONNECTOR_NAME']
CONNECTOR_VERSION: str = os.environ['CONNECTOR_VERSION']


class ConfigurationResolver(ConfigurationHandler):
    """Skillcorner Configuration Handler."""
    def validate_connector_runtime_settings(self, request: ValidateConnectorRuntimeSettingsRequest) \
            -> ValidateConnectorRuntimeSettingsResponse:
        """
        :param request:

        :return:
        """
        # TODO: Implement Runtime connector settings validation.
        # if errors:
        #     return ValidateConnectorRuntimeSettingsResponse(is_success=False, error_details=errors)
        return ValidateConnectorRuntimeSettingsResponse(is_success=True)

    def validate_credentials(self, request: ValidateCredentialsRequest) -> ValidateCredentialsResponse:
        """
        :param request:

        :return:
        """
        connector_context = ConnectorContext(api_version=API_VERSION, credentials=request.credentials,
                                             connector_runtime_settings=request.connector_runtime_settings)

        # TODO: Do request to check user credentials.
        # if error_details:
        #     return ValidateCredentialsResponse(is_success=False,
        #                                        error_details=error_details)
        return ValidateCredentialsResponse(is_success=True)

    def describe_connector_configuration(self, request: DescribeConnectorConfigurationRequest) \
            -> DescribeConnectorConfigurationResponse:
        """
        :param request:

        :return:
        """
        connector_runtime_setting: Tuple[ConnectorRuntimeSetting, ...] = ()

        authentication_config: AuthenticationConfig = AuthenticationConfig(is_basic_auth_supported=True,
                                                                           is_api_key_auth_supported=True)

        return DescribeConnectorConfigurationResponse(authentication_config=authentication_config,
                                                      connector_modes=[ConnectorModes.SOURCE],
                                                      connector_name=CONNECTOR_NAME,
                                                      connector_owner=CONNECTOR_OWNER,
                                                      connector_runtime_setting=connector_runtime_setting,
                                                      connector_version=CONNECTOR_VERSION,
                                                      is_success=True,
                                                      supported_api_versions=[API_VERSION])
