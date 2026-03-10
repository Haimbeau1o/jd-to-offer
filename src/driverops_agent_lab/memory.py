from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field


@dataclass
class DriverLongTermMemory:
    preferred_peak_windows: list[str] = field(default_factory=list)
    preferred_campaigns: list[str] = field(default_factory=list)
    recent_recommended_zones: list[str] = field(default_factory=list)


class ConversationMemoryStore:
    def __init__(self, max_items: int = 6, max_long_term_items: int = 4) -> None:
        self._recent_queries: dict[str, deque[str]] = defaultdict(lambda: deque(maxlen=max_items))
        self._long_term_memory: dict[str, DriverLongTermMemory] = defaultdict(DriverLongTermMemory)
        self._max_long_term_items = max_long_term_items

    def add_query(self, driver_id: str, query: str) -> None:
        self._recent_queries[driver_id].append(query)

    def get_recent_queries(self, driver_id: str) -> list[str]:
        return list(self._recent_queries[driver_id])

    def remember_peak_windows(self, driver_id: str, windows: list[str]) -> None:
        memory = self._long_term_memory[driver_id]
        self._remember_values(memory.preferred_peak_windows, windows)

    def remember_campaigns(self, driver_id: str, campaigns: list[str]) -> None:
        memory = self._long_term_memory[driver_id]
        self._remember_values(memory.preferred_campaigns, campaigns)

    def remember_recommended_zone(self, driver_id: str, zone: str) -> None:
        if not zone:
            return
        memory = self._long_term_memory[driver_id]
        self._remember_values(memory.recent_recommended_zones, [zone])

    def get_long_term_memory(self, driver_id: str) -> DriverLongTermMemory:
        memory = self._long_term_memory[driver_id]
        return DriverLongTermMemory(
            preferred_peak_windows=list(memory.preferred_peak_windows),
            preferred_campaigns=list(memory.preferred_campaigns),
            recent_recommended_zones=list(memory.recent_recommended_zones),
        )

    def build_memory_snapshot(self, driver_id: str) -> list[str]:
        snapshot: list[str] = []
        recent_queries = self.get_recent_queries(driver_id)
        long_term_memory = self.get_long_term_memory(driver_id)

        if recent_queries:
            snapshot.append(f"recent_queries={' | '.join(recent_queries[-3:])}")
        if long_term_memory.preferred_peak_windows:
            snapshot.append(f"preferred_peak_windows={','.join(long_term_memory.preferred_peak_windows)}")
        if long_term_memory.preferred_campaigns:
            snapshot.append(f"preferred_campaigns={','.join(long_term_memory.preferred_campaigns)}")
        if long_term_memory.recent_recommended_zones:
            snapshot.append(f"recent_recommended_zones={','.join(long_term_memory.recent_recommended_zones)}")
        return snapshot

    def _remember_values(self, target: list[str], values: list[str]) -> None:
        for value in values:
            if not value:
                continue
            if value in target:
                target.remove(value)
            target.append(value)
            if len(target) > self._max_long_term_items:
                del target[0]
