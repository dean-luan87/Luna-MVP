from typing import Iterable, List, Optional

from common.change_demand import ChangeDemand


def collect_change_demands(tasks: Iterable, c_controller: Optional[object] = None) -> List[ChangeDemand]:
    """
    汇总 Task / C 的 ChangeDemand（只读、不消费、不触发）。
    """
    out: List[ChangeDemand] = []
    for t in tasks:
        if hasattr(t, "change_demands"):
            out.extend(t.change_demands())
    if c_controller and hasattr(c_controller, "change_demands"):
        out.extend(c_controller.change_demands())
    return out
