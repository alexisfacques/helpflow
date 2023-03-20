"""TODO:"""
import logging

# From local modules:
from custom_connector_sdk.lambda_handler.lambda_handler import BaseLambdaConnectorHandler

from .configuration_handler import ConfigurationHandler
from .helpflow_resolver import HelpFlowResolver

LOGGER = logging.getLogger()


def lambda_handler(event, context):
    """
    :param event:
    :param context:
    """
    LOGGER.info(event)
    helpflow_resolver: HelpFlowResolver = HelpFlowResolver()
    configuration_handler: ConfigurationHandler = ConfigurationHandler()
    return BaseLambdaConnectorHandler(helpflow_resolver, helpflow_resolver, configuration_handler).lambda_handler(event, context)
