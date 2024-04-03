import logging
import os

from .context import dynamic_logging_context
from .dev import init_dev_logging
from .json import init_json_logging


old_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    for key, value in dynamic_logging_context.get_logging_context().items():
        setattr(record, key, value)
    return record


def is_logging_production(env_name: str) -> bool:
    if env_name.lower() == 'production' or env_name.lower() == 'prod' or env_name.lower() == 'staging':
        return True
    return False


def init(json_logs=None):
    production = False
    if 'ENV' in os.environ.keys():
        production = is_logging_production(os.environ['ENV'])
    if 'ENVIRONMENT' in os.environ.keys():
        production = is_logging_production(os.environ['ENVIRONMENT'])
    if 'JSON_LOGGING' in os.environ.keys():
        production = True
    if json_logs is not None:
        production = json_logs
    if production:
        init_json_logging()
    else:
        init_dev_logging()
    logging.setLogRecordFactory(record_factory)
