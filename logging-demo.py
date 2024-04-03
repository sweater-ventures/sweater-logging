import logging

import sweater_logging


def example_error():
    log = logging.getLogger('example_error')
    log.debug("Inside example_error()")
    local = 'variable'
    number = 42
    something = {'foo': 'bar'}
    raise ValueError("This is a test error")


def main():
    log = logging.getLogger('main')
    log.info("Hello, logging!")
    try:
        example_error()
    except ValueError as e:
        log.error("Caught an error", exc_info=e)
    log.info("This log message has extra info attached", extra={
        'example': 'string',
        'example-number': 42,
        'something': {'foo': 'bar'}
    })


if __name__ == "__main__":
    sweater_logging.init()
    main()
