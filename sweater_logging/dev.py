import logging

from rich.logging import RichHandler


def init_dev_logging():
    logging_format = "%(message)s"
    logging.basicConfig(
        level="DEBUG", format=logging_format, datefmt="[%I:%M:%S %p]", handlers=[
            RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)
        ]
    )
