# -*- coding: utf-8 -*-
"""
Phase 3.2: Annotation Tasks — 只提问题不给答案，不输出 policy 建议。
"""
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Tuple

QUESTION_SPEECH = "用户在此处发生干预：请判断当时环境中最关键的风险源是什么？"
QUESTION_SAFETY = "安全等级发生变化：请判断是否属于误判或真实风险？"


def _should_annotate(summary: Dict[str, Any], tags: List[str]) -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    if "HAS_SPEECH_EVENT" in tags:
        out.append(("SPEECH", QUESTION_SPEECH))
    if "SAFETY_OSCILLATION" in tags:
        out.append(("SAFETY", QUESTION_SAFETY))
    trigger_type = (summary.get("trigger_type") or "").strip().upper()
    if "LOW_VC_PRESENT" in tags and trigger_type == "SAFETY_CHANGE":
        out.append(("SAFETY", QUESTION_SAFETY))
    if "HAS_CAUTION" in tags or "CONTROL_MODE_SWITCH" in tags or "NEGATIVE_PAL_TREND" in tags:
        out.append(("RISK", QUESTION_SAFETY))
    return out


def build_annotation_tasks(
    summaries: List[Dict[str, Any]],
    tags_by_episode: Dict[tuple, List[str]],
) -> List[Dict[str, Any]]:
    tasks: List[Dict[str, Any]] = []
    created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    for summary in summaries:
        sid = summary.get("session_id") or ""
        eid = summary.get("episode_id") or ""
        tags = tags_by_episode.get((sid, eid), [])
        for qtype, qtext in _should_annotate(summary, tags):
            task_id = f"{sid}_{eid}_{qtype}_{len(tasks)}"
            tasks.append(
                {
                    "task_id": task_id,
                    "version_tag": summary.get("version_tag") or "",
                    "session_id": sid,
                    "episode_id": eid,
                    "question": qtext,
                    "context": f"trigger_type={summary.get('trigger_type')} tags={tags}",
                    "created_at": created,
                }
            )
    return tasks


def write_annotation_tasks(tasks: List[Dict[str, Any]], out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for row in tasks:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

