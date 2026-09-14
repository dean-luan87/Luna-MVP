# -*- coding: utf-8 -*-
"""
最小 smoke：生成 1 帧 DecisionMonitor JSONL，并验证 action_hint_whitebox_trace 字段存在。

约束：
- 不跑视频、不跑长 trace
- 输出写入 logs/ 下独立文件
- 终端输出仅摘要
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.append(str(_ROOT))

from decision_monitor.builder import DecisionMonitorBuilder  # noqa: E402
from decision_monitor.logger import DecisionMonitorLogger  # noqa: E402


def _write_and_verify(jsonl_path: str) -> None:
    p = Path(jsonl_path)
    if not p.exists():
        raise RuntimeError(f"JSONL 未生成: {jsonl_path}")
    first = p.read_text(encoding="utf-8").splitlines()[0]
    d = json.loads(first)

    frame_has = "action_hint_whitebox_trace" in d
    runtime_summary = (
        (d.get("mainline_integration") or {}).get("integration_summary")
        if isinstance(d.get("mainline_integration"), dict)
        else None
    )
    runtime_summary_ok = bool((runtime_summary or "").strip())

    # 摘要输出（禁止刷屏）
    print(
        json.dumps(
            {
                "jsonl_path": str(p),
                "has_action_hint_whitebox_trace": frame_has,
                "integration_summary_present": runtime_summary_ok,
                "integration_summary_preview": (runtime_summary or "")[:80],
            },
            ensure_ascii=False,
        )
    )

    if not frame_has:
        raise AssertionError("frame 中缺少 action_hint_whitebox_trace")
    if not runtime_summary_ok:
        raise AssertionError("mainline_integration.integration_summary 为空（runtime_ctx 摘要不可审计）")


def main() -> None:
    root = _ROOT
    logs_dir = root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    stamp = time.strftime("%Y%m%d_%H%M%S")
    jsonl_path = str(logs_dir / f"smoke_action_hint_whitebox_trace_{stamp}.jsonl")

    # 用 env 模拟最小用户反馈（容器流 + opened_container）
    os.environ["CONFIRMATION_INPUT_TYPE"] = "opened_container"
    os.environ["CONFIRMATION_INPUT_RAW_TEXT"] = "打开了"

    # 最小 ctx：只注入能让 search/sidecar/hint 链路稳定产出白盒的字段
    ctx = {
        "trace_anchor_id": f"smoke_{stamp}",
        "input_source_type": "smoke",
        "input_source_path": str(root / "find_test.jpg"),  # 不要求存在，仅做审计字段
        "focus_object_label": "药瓶",
        # 给一组简单 vision 候选，触发 object_search_hint evidence（容器/遮挡分支之一）
        "visual_audit_objects": [
            {"label": "cup", "bbox": [0.10, 0.10, 0.60, 0.70]},
            {"label": "bottle", "bbox": [0.25, 0.25, 0.45, 0.60]},
        ],
        "visual_audit_texts": [],
        "visual_audit_description": "smoke: bottle overlaps cup (container/occlusion hint)",
        "input_image_width": 640,
        "input_image_height": 480,
        # 避免人工校准阻塞
        "skip_human_check": True,
        # 主流程字段允许缺省，占位即可
        "sampled": True,
        "route": "smoke",
    }

    builder = DecisionMonitorBuilder(trace_anchor_id_prefix="smoke")
    frame = builder.build(ctx)

    logger = DecisionMonitorLogger(jsonl_path=jsonl_path, emit_console_summary=False)
    logger.write(frame)

    _write_and_verify(jsonl_path)


if __name__ == "__main__":
    main()

