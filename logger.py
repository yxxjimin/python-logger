import json
import logging
import sys
from copy import copy
from typing import Literal, Self
    

class Logger(logging.Logger):
    _fmt = '%(asctime)s - %(levelprefix)8s - [%(name)s]: %(message)s (%(filename)s:%(lineno)d)'
    _datefmt = '%Y-%m-%d %H:%M:%S %Z'

    def __init__(self, name):
        super().__init__(name)

    @classmethod
    def get_logger(
        cls,
        name: str,
        logging_level: int = logging.DEBUG,
        filename: str | None = None,
    ) -> Self:
        logger = cls(name)
        logger.setLevel(logging_level)
        logger.addHandler(cls._get_stream_handler())

        if filename:
            logger.add_file_handler(filename)

        return logger

    def add_file_handler(
        self,
        filename: str
    ) -> Self:
        self.addHandler(self._get_file_handler(filename))
        return self
    
    def add_json_handler(
        self,
        filename: str
    ) -> Self:
        hdlr = self._get_file_handler(filename)
        hdlr.setFormatter(_JSONFormatter())
        self.addHandler(hdlr)
        return self

    @classmethod
    def _get_stream_handler(cls) -> logging.StreamHandler:
        hdlr = logging.StreamHandler(stream=sys.stdout)
        hdlr.setFormatter(cls._get_color_formatter(use_colors=True))
        return hdlr
    
    @classmethod
    def _get_file_handler(cls, filename: str) -> logging.FileHandler:
        hdlr = logging.FileHandler(filename)
        hdlr.setFormatter(cls._get_color_formatter(use_colors=False))
        return hdlr

    @classmethod
    def _get_color_formatter(cls, use_colors: bool) -> logging.Formatter:
        return _ColorFormatter(cls._fmt, cls._datefmt, use_colors=use_colors)

    @classmethod
    def _get_json_formatter(cls) -> logging.Formatter:
        return _JSONFormatter()


class _ColorFormatter(logging.Formatter):
    _level_name_colors = {
        logging.DEBUG: lambda level_name: f"\033[36m{level_name}\033[0m",
        logging.INFO: lambda level_name: f"\033[32m{level_name}\033[0m",
        logging.WARNING: lambda level_name: f"\033[33m{level_name}\033[0m",
        logging.ERROR: lambda level_name: f"\033[31m{level_name}\033[0m",
        logging.CRITICAL: lambda level_name: f"\033[91m{level_name}\033[0m",
    }

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: Literal['%', '{', '$'] = '%',
        use_colors: bool | None = None,
    ):
        if isinstance(use_colors, bool):
            self.use_colors = use_colors
        else:
            self.use_colors = sys.stdout.isatty()
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def _color_level_name(self, level_name: str, level_no: int) -> str:
        def default(level_name: str) -> str:
            return str(level_name)

        func = self._level_name_colors.get(level_no, default)
        return func(level_name)

    def formatMessage(self, record: logging.LogRecord) -> str:
        recordcopy = copy(record)
        levelname = recordcopy.levelname
        seperator = ' ' * (8 - len(recordcopy.levelname))
        if self.use_colors:
            levelname = self._color_level_name(levelname, recordcopy.levelno)
        recordcopy.__dict__['levelprefix'] = levelname + seperator
        return super().formatMessage(recordcopy)


class _JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({
            'asctime': record.asctime,
            'levelname': record.levelname,
            'levelno': record.levelno,
            'name': record.name,
            'message': record.message,
            'filename': record.filename,
            'lineno': record.lineno,
        }, indent=2)
