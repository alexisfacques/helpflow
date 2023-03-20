"""TODO:"""
from importlib import import_module
import logging
import os

# From local modules:
from custom_connector_sdk.lambda_handler.lambda_handler import BaseLambdaConnectorHandler

from .configuration_resolver import ConfigurationResolver
from .helpflow_resolver import HelpFlowResolver


LOGGER = logging.getLogger()


def lambda_handler(event, context):
    EXTENSIONS_DIR: str = os.environ.get('EXTENSIONS_DIR', 'extensions')
    import_module(f'{EXTENSIONS_DIR}', __name__)

    helpflow: HelpFlowResolver = HelpFlowResolver()
    configuration: ConfigurationResolver = ConfigurationResolver()
    return BaseLambdaConnectorHandler(helpflow, helpflow, configuration).lambda_handler(event, context)
