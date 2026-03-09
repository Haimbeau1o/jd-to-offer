from __future__ import annotations

from collections import defaultdict, deque


class ConversationMemoryStore:
    def __init__(self, max_items: int = 6) -> None:
        self._recent_queries: dict[str, deque[str]] = defaultdict(lambda: deque(maxlen=max_items))

    def add_query(self, driver_id: str, query: str) -> None:
        self._recent_queries[driver_id].append(query)

    def get_recent_queries(self, driver_id: str) -> list[str]:
        return list(self._recent_queries[driver_id])
