"""
memory_interface.py

This defines the CONTRACT between the Conversation System (Member 1)
and the Memory Storage / Retrieval System (Member 2/3).

Share this file with your teammates early. Whoever builds the real
memory module should implement a class matching MemoryStoreInterface.
Until that's ready, MockMemoryStore lets you build and test your
whole pipeline on your own.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


@dataclass
class MemoryItem:
    content: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    importance: float = 0.5   # 0-1, set by the memory evolution module
    memory_id: str = ""


class MemoryStoreInterface(ABC):
    """Abstract contract every memory backend must satisfy."""

    @abstractmethod
    def retrieve_relevant(self, user_id: str, query: str, top_k: int = 5) -> List[MemoryItem]:
        """Return up to top_k memories most relevant to `query` for this user."""
        raise NotImplementedError

    @abstractmethod
    def store_interaction(self, user_id: str, user_message: str, ai_response: str) -> None:
        """Persist a new turn so the memory system can learn/evolve from it."""
        raise NotImplementedError


class MockMemoryStore(MemoryStoreInterface):
    """
    Temporary stand-in for Member 2/3's real module.
    Returns a couple of fake memories so you can build and test
    the full pipeline before the real thing exists.
    """

    def __init__(self):
        self._log = []

    def retrieve_relevant(self, user_id: str, query: str, top_k: int = 5) -> List[MemoryItem]:
        return [
            MemoryItem(content=f"User previously asked about: '{query[:40]}'", importance=0.6),
            MemoryItem(content="User prefers short, direct answers", importance=0.4),
        ][:top_k]

    def store_interaction(self, user_id: str, user_message: str, ai_response: str) -> None:
        self._log.append({"user_id": user_id, "user_message": user_message, "ai_response": ai_response})
