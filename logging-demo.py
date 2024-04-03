import asyncio
import logging
import random
from contextvars import ContextVar

import sweater_logging
from sweater_logging import dynamic_logging_context

context_var: ContextVar[str | None] = ContextVar('context_var', default=None)


def random_number() -> int:
    return random.choice(range(1, 100))


async def async_method_grandchild():
    log = logging.getLogger('async_method_grandchild')
    log.info("Inside async_method_grandchild()")


async def async_method_child():
    log = logging.getLogger('async_method_child')
    log.info("Inside async_method_child()")
    await async_method_grandchild()


async def async_method_parent():
    log = logging.getLogger('async_method_parent')
    log.info("Inside async_method_parent()")
    log.debug("Setting dynamic logging context variables")
    context_var.set('context_value')
    await async_method_child()


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
    dynamic_logging_context.add_context_value('context_var', context_var)
    dynamic_logging_context.add_static_value('app', 'logging-demo')
    dynamic_logging_context.add_callable_value('random_number', random_number)
    asyncio.run(async_method_parent())
    logging.info("Done!")


if __name__ == "__main__":
    sweater_logging.init()
    main()
