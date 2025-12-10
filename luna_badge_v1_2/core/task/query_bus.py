from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, List, Optional
import time
from infra.logging_manager import get_logger

logger = get_logger("query_bus")


class QueryStatus(Enum):
    PENDING = "pending"
    WAITING_USER = "waiting_user"
    RESOLVED = "resolved"
    TIMEOUT = "timeout"


@dataclass
class Query:
    id: str
    priority: int
    created_ts: float
    text: str
    timeout_seconds: float
    status: QueryStatus = QueryStatus.PENDING
    on_resolved: Optional[Callable[[Dict], None]] = None
    on_timeout: Optional[Callable[[], None]] = None


class QueryBus:
    def __init__(self, tts_say: Callable[[str], None]) -> None:
        self._tts_say = tts_say
        self._queries: List[Query] = []
        self._active_query_id: Optional[str] = None

    def push_query(self, query: Query) -> None:
        self._queries.append(query)
        self._queries.sort(key=lambda q: q.priority, reverse=True)
        logger.debug(f"[QUERY] push id={query.id}, priority={query.priority}")

    def _get_active_query(self) -> Optional[Query]:
        if self._active_query_id is None:
            return None
        for q in self._queries:
            if q.id == self._active_query_id:
                return q
        return None

    def has_active_query(self) -> bool:
        return self._get_active_query() is not None

    def tick(self) -> None:
        now = time.time()
        active = self._get_active_query()

        if active is None:
            for q in self._queries:
                if q.status == QueryStatus.PENDING:
                    self._active_query_id = q.id
                    q.status = QueryStatus.WAITING_USER
                    self._tts_say(q.text)
                    logger.info(f"[QUERY] ask id={q.id}, text={q.text}")
                    break
            return

        if active.status == QueryStatus.WAITING_USER:
            if now - active.created_ts > active.timeout_seconds:
                active.status = QueryStatus.TIMEOUT
                logger.warning(f"[QUERY] timeout id={active.id}")
                if active.on_timeout:
                    active.on_timeout()
                self._active_query_id = None

    def resolve_active(self, result: Dict) -> None:
        active = self._get_active_query()
        if not active:
            return
        active.status = QueryStatus.RESOLVED
        logger.info(f"[QUERY] resolved id={active.id}, result={result}")
        if active.on_resolved:
            active.on_resolved(result)
        self._active_query_id = None
