# -*- coding: utf-8 -*-
"""
决策显示器输出：JSONL 持久化 + 开发态终端摘要。

独立于现有 trace，可共享 trace_anchor_id 便于对齐。
"""

from __future__ import annotations

import json
import os
from typing import Optional

from .schema import DecisionMonitorFrame


class DecisionMonitorLogger:
    """
    每帧写入一条 JSONL；可选打印简化责任链摘要到终端。
    """

    def __init__(
        self,
        jsonl_path: Optional[str] = None,
        emit_console_summary: bool = True,
        console_summary_interval: int = 1,
    ):
        self.jsonl_path = jsonl_path
        self.emit_console_summary = emit_console_summary
        self.console_summary_interval = max(1, int(console_summary_interval))
        self._write_count = 0

    def write(self, frame: DecisionMonitorFrame) -> None:
        self._write_count += 1
        if self.jsonl_path:
            self._append_jsonl(frame)
        if self.emit_console_summary and (self._write_count % self.console_summary_interval == 0):
            self._print_summary(frame)

    def _append_jsonl(self, frame: DecisionMonitorFrame) -> None:
        try:
            d = frame.to_dict()
            line = json.dumps(d, ensure_ascii=False, default=str) + "\n"
            if self.jsonl_path:
                os.makedirs(os.path.dirname(self.jsonl_path) or ".", exist_ok=True)
                with open(self.jsonl_path, "a", encoding="utf-8") as f:
                    f.write(line)
        except Exception:
            pass

    def _print_summary(self, frame: DecisionMonitorFrame) -> None:
        """开发态文本摘要：当前目标 → 状态 → 谁拍板 → 做了什么 → 预期后果；M0.5 主线接入一行观察。"""
        g = frame.goal
        i = frame.inputs
        s = frame.state
        d = frame.decision
        o = frame.outputs
        c = frame.consequence
        lines = [
            "--- DecisionMonitor ---",
            f"  目标: {g.goal_type or 'N/A'} | {g.goal_status or 'N/A'} | {g.goal_description or ''}",
            f"  输入: seq={i.frame_seq} ts={i.current_ts} sampled={i.sampled} active_b2={i.active_b2_impact}",
            f"  状态: safety={s.safety_level} risk={s.risk_score} weak_ev={s.weak_evidence_level}",
            f"  拍板: {d.decision_owner} | {d.decision_type} | {d.decision_reason}",
            f"  输出: mode={o.policy_intent_summary} fps={o.sampling_target_fps} run={o.modules_run} skip={o.modules_skipped}",
            f"  后果: {c.expected_gain or 'N/A'} | {c.expected_risk or 'N/A'}",
        ]
        mi = getattr(frame, "mainline_integration", None)
        if mi is not None:
            note = getattr(mi, "integration_observation_frame_note", None) or ""
            raw = getattr(mi, "integration_summary", None) or ""
            summary_preview = raw[:72] + ("..." if len(raw) > 72 else "")
            lines.append(f"  [MainlineM0.5] {note} | {summary_preview}")
        print("\n".join(lines))
