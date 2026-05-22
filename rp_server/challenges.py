"""In-memory challenge cache."""

from __future__ import annotations

import secrets
import threading
from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass(frozen=True)
class ChallengeRecord:
    challenge: str
    metadata: dict[str, str] = field(default_factory=dict)


class ChallengeCache:
    def __init__(self) -> None:
        self._challenges: Dict[Tuple[str, str], ChallengeRecord] = {}
        self._lock = threading.Lock()

    def issue(
        self,
        scope: str,
        key: str,
        size: int = 32,
        metadata: dict[str, str] | None = None,
    ) -> str:
        challenge = secrets.token_urlsafe(size)
        with self._lock:
            self._challenges[(scope, key)] = ChallengeRecord(
                challenge=challenge,
                metadata=metadata or {},
            )
        return challenge

    def pop(self, scope: str, key: str) -> str | None:
        record = self.pop_record(scope, key)
        return record.challenge if record else None

    def pop_record(self, scope: str, key: str) -> ChallengeRecord | None:
        with self._lock:
            return self._challenges.pop((scope, key), None)
