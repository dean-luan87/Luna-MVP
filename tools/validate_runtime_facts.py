#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate runtime facts in JSON logs.

Checks:
- speech_input == audio_input
- env_mode exists and has key fields
- system_facts consistency (frame_valid vs occlusion_state/perception_state)
"""

import argparse
import json
import os
from typing import Any, Dict, List, Tuple


def _load_log(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    if isinstance(payload, dict) and "data" in payload:
        return payload.get("data") or {}
    return payload if isinstance(payload, dict) else {}


def _collect_logs(log_dir: str, limit: int) -> List[str]:
    if not os.path.isdir(log_dir):
        return []
    files = [
        os.path.join(log_dir, name)
        for name in os.listdir(log_dir)
        if name.endswith(".json") and name.startswith("log_")
    ]
    files.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return files[:limit]


def _validate_entry(entry: Dict[str, Any], path: str) -> List[str]:
    issues: List[str] = []
    if entry.get("status") == "error":
        return issues

    audio_input = entry.get("audio_input", "")
    speech_input = entry.get("speech_input", audio_input)
    if audio_input != speech_input:
        issues.append("speech_input != audio_input")

    env_mode = entry.get("env_mode")
    if env_mode is None:
        issues.append("missing env_mode")
    else:
        for key in ("safety_level", "control_mode", "complexity_score"):
            if key not in env_mode:
                issues.append(f"env_mode missing {key}")

    facts = entry.get("system_facts")
    if isinstance(facts, dict):
        frame_valid = facts.get("frame_valid")
        perception = facts.get("perception_state")
        occlusion = facts.get("occlusion_state")
        if frame_valid is False:
            if perception != "DEGRADED":
                issues.append("frame_valid=false but perception_state!=DEGRADED")
            if occlusion != "UNKNOWN":
                issues.append("frame_valid=false but occlusion_state!=UNKNOWN")
        if frame_valid is True:
            if perception not in (None, "NORMAL"):
                issues.append("frame_valid=true but perception_state!=NORMAL")
            if occlusion in (None, "UNKNOWN"):
                issues.append("frame_valid=true but occlusion_state is UNKNOWN/None")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate runtime facts in JSON logs")
    parser.add_argument("--log-dir", default=os.path.join(os.getcwd(), "logs"), help="日志目录")
    parser.add_argument("--limit", type=int, default=20, help="检查最近N条日志")
    args = parser.parse_args()

    logs = _collect_logs(args.log_dir, args.limit)
    if not logs:
        print(f"未找到日志文件: {args.log_dir}")
        return 1

    total = 0
    failed: List[Tuple[str, List[str]]] = []

    for path in logs:
        entry = _load_log(path)
        total += 1
        issues = _validate_entry(entry, path)
        if issues:
            failed.append((path, issues))

    print(f"检查日志数: {total}")
    if not failed:
        print("✅ 通过：未发现一致性问题")
        return 0

    print(f"❌ 失败：{len(failed)} 条日志存在问题")
    for path, issues in failed:
        rel = os.path.relpath(path, os.getcwd())
        print(f"- {rel}: {', '.join(issues)}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
