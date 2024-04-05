import logging
import os
from logging.config import dictConfig

from .context import dynamic_logging_context
from .dev import init_dev_logging
from .json import init_json_logging


old_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    for key, value in dynamic_logging_context.get_logging_context().items():
        if value is not None:
            setattr(record, key, value)
    return record


def is_logging_production(env_name: str) -> bool:
    if env_name.lower() == 'production' or env_name.lower() == 'prod' or env_name.lower() == 'staging':
        return True
    return False


logging_config: dict = {}
is_local: bool = True


def uvicorn_init(json_logs: bool = None):
    global logging_config
    global is_local
    production = False
    if 'ENV' in os.environ.keys():
        production = is_logging_production(os.environ['ENV'])
    if 'ENVIRONMENT' in os.environ.keys():
        production = is_logging_production(os.environ['ENVIRONMENT'])

    if 'JSON_LOGGING' in os.environ.keys():
        production = True
    if json_logs is not None:
        production = json_logs
    is_local = not production
    if production:
        logging_config = init_json_logging()
    else:
        logging_config = init_dev_logging()
    logging.setLogRecordFactory(record_factory)


def init(json_logs: bool = None):
    uvicorn_init(json_logs=json_logs)
    dictConfig(logging_config)
