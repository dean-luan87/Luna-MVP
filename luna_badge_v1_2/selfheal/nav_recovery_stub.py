from core.logging import get_logger

log = get_logger("nav_recovery_stub")
"""
NavRecoveryStub
----------------
预留给 1.5.x 的"自愈系统 + 热修复"。

当前逻辑只做两件事：

  1）记录 NAV_STUCK 事件（方便后台与日志分析）

  2）打印将来可以调用的自愈动作（restart_nav_brain, reset_task_chain, replan_route）
"""

import json
import time
from pathlib import Path
from typing import Dict, Any

EVENT_LOG_PATH = Path("test_reports/nav_stuck_events.jsonl")


def _append_event(evt: Dict[str, Any]) -> None:
    EVENT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with EVENT_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(evt, ensure_ascii=False) + "\n")


def _plan_recovery_action(event: Dict[str, Any]) -> str:
    """
    简单根据 stuck_type 给出建议恢复策略（仅作为打印提示，不实际执行）。
    """
    stuck_type = event.get("stuck_type") or "no_progress"
    if stuck_type == "speed_zero":
        return "微调姿态 / 再尝试前进，若失败则重规划路径"
    if stuck_type == "loop_path":
        return "清空路径缓存 + 强制重规划（避免绕圈）"
    if stuck_type == "sensor_conflict":
        return "重启 depth/detector 模块，重新感知环境"
    return "重新评估导航状态 + 视情况执行重规划"


def handle_nav_stuck(event: Dict[str, Any]) -> None:
    """
    预留入口：当检测到 NAV_STUCK 时，可以调用这里。

    当前版本只落盘记录 + 打印未来可执行动作，不做真正的自愈。

    event 预期包含：

      - type: "error"
      - domain: "navigation.path"
      - code: "NAV_STUCK"
      - route_id, state, last_progress_value, idle_sec 等字段
    """
    ts = time.time()
    record = {
        "ts": ts,
        "code": event.get("code", "NAV_STUCK"),
        "route_id": event.get("route_id"),
        "state": event.get("state"),
        "last_progress_value": event.get("last_progress_value"),
        "idle_sec": event.get("idle_sec"),
        "stuck_type": event.get("stuck_type", "no_progress"),
        "raw": event,
    }
    _append_event(record)

    suggestion = _plan_recovery_action(record)

    # 这里只打印"将来可以做什么"，不真正执行
    print(
        "[NavRecoveryStub] NAV_STUCK detected. "
        f"route_id={record['route_id']} idle={record['idle_sec']}s "
        f"stuck_type={record['stuck_type']} -> suggested_action=({suggestion})"
    )


if __name__ == "__main__":
    demo_evt = {
        "type": "error",
        "domain": "navigation.path",
        "code": "NAV_STUCK",
        "route_id": "demo-route",
        "state": "WALKING",
        "last_progress_value": 12.3,
        "idle_sec": 20.5,
        "stuck_type": "no_progress",
    }
    handle_nav_stuck(demo_evt)
    log.info("demo nav_stuck event written to", EVENT_LOG_PATH")


















