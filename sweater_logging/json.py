import logging
import datetime

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record: logging.LogRecord, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # TODO use record.created instead
            now = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
        if record.name:
            log_record['logger'] = record.name
        if record.pathname:
            log_record['file'] = f'{record.pathname}:{record.lineno}'


def init_json_logging():
    return {
        'version': 1,
        'formatters': {
            'default': {
                '()': 'sweater_logging.json.CustomJsonFormatter',
            }
        },
        'handlers': {
            'default': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            }
        },
        'loggers': {
            'root': {
                'handlers': ['default'],
                'level': 'INFO',
            },
            'uvicorn': {
                'handlers': ['default'],
                'level': 'INFO',
            },
        }
    }
