import logging
from datetime import datetime
from logging import LogRecord
from pathlib import Path
from typing import Optional

from rich.logging import RichHandler
from rich.scope import render_scope
from rich.traceback import Traceback

default_items = [
    "args",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "message",
    "module",
    "msecs",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "taskName",
    "thread",
    "threadName",
    "color_message",
]


def get_non_default_items(record: LogRecord) -> dict:
    return {k: v for k, v in record.__dict__.items() if k not in default_items}


class CustomRichHandler(RichHandler):
    def __init__(self, *args, **kwargs):
        if "class" in kwargs.keys():
            del kwargs["class"]
        super().__init__(*args, **kwargs)

    def render(
        self,
        *,
        record: LogRecord,
        traceback: Optional[Traceback],
        message_renderable: "ConsoleRenderable",
    ) -> "ConsoleRenderable":
        """Render log for display.

        Args:
            record (LogRecord): logging Record.
            traceback (Optional[Traceback]): Traceback instance or None for no Traceback.
            message_renderable (ConsoleRenderable): Renderable (typically Text) containing log message contents.

        Returns:
            ConsoleRenderable: Renderable to display log.
        """
        path = Path(record.pathname).name
        level = self.get_level_text(record)
        time_format = None if self.formatter is None else self.formatter.datefmt
        log_time = datetime.fromtimestamp(record.created)
        renderables = [message_renderable]
        if traceback:
            renderables.append(traceback)
        extras = get_non_default_items(record)
        if extras:
            renderables.append(render_scope(extras))

        log_renderable = self._log_render(
            self.console,
            renderables,
            log_time=log_time,
            time_format=time_format,
            level=level,
            path=path,
            line_no=record.lineno,
            link_path=record.pathname if self.enable_link_path else None,
        )
        return log_renderable


def init_dev_logging() -> dict:
    return {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(message)s",
                "datefmt": "[%I:%M:%S %p]",
            },
        },
        "handlers": {
            "console": {
                "class": "sweater_logging.dev.CustomRichHandler",  # for litestar
                "()": "sweater_logging.dev.CustomRichHandler",
                "rich_tracebacks": True,
                "tracebacks_show_locals": True,
                "formatter": "default",
            }
        },
        "loggers": {
            "root": {
                "handlers": ["console"],
                "level": "DEBUG",
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["console"],
                "level": "CRITICAL",
            },
        },
        "disable_existing_loggers": False,
    }
