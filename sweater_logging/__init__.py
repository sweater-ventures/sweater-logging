
import os
from .dev import init_dev_logging
from .json import init_json_logging


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
