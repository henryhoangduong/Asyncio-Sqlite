import asyncio
import logging
import sqlite3
from collections.abc import AsyncIterator, Generator, Iterable
from functools import partial
from pathlib import Path
from queue import Empty, Queue, SimpleQueue
from typing import Any, Callable, Optional, Literal
from warnings import warn


from .context import contextmanager
from .cursor import Cursor

__all__ = ["connect", "Connection", "Cursor"]

LOG = logging.getLogger("aiosqlite")


IsolationLevel = Optional[Literal["DEFERRED", "IMMEDIATE", "EXCLUSIVE"]]


def set_result(fut: asyncio.Future, result: Any) -> None:
    """Set the result of a future if it hasn't been set already."""
    if not fut.done():
        fut.set_result(result)
