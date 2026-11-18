"""Base adapter contract for connectivity protocols."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    protocol: str = ""

    @classmethod
    @abstractmethod
    def run_forever(cls) -> None:
        """Block forever, ingesting via connectivity.services.process_message."""
        raise NotImplementedError
