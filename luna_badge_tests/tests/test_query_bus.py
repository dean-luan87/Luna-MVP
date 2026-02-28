import time
from core.task.query_bus import QueryBus, Query, QueryStatus


def test_query_bus_flow():
    spoken = []

    def speak(text):
        spoken.append(text)

    qb = QueryBus(speak)
    q = Query(
        id="q1",
        priority=1,
        created_ts=time.time(),
        text="结束任务吗？",
        timeout_seconds=1.0,
    )
    qb.push_query(q)
    qb.tick()
    assert spoken[-1] == "结束任务吗？"
    assert qb.has_active_query() is True

    qb.resolve_active({"answer": "yes"})
    assert qb.has_active_query() is False
    assert q.status == QueryStatus.RESOLVED
