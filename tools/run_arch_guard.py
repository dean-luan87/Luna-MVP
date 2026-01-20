#!/usr/bin/env python3
"""
Architecture Guard + DCS CI Runner

合并执行：
- Architecture Guard（文本/遗留/越权语义扫描）
- DCS（trace 硬规则判定）

一个入口，一个 report，一个退出码
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from typing import Dict, List, Tuple

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# ----------------------------
# Architecture Guard (text lint)
# ----------------------------

ARCH_GUARD_PATHS = [
    os.path.join(ROOT, ".cursor/guards/bc_authority_guard.md"),
    os.path.join(ROOT, "docs/architecture/BC_AUTHORITY_GUARD.md"),
]

# Very small, hard checks (expand later)
FORBIDDEN_PATTERNS = [
    # B must not "confirm risk" semantics (example keywords)
    r"\bconfirmed\b",
    r"\bconfirm(ed|s)? risk\b",
    r"必然(发生|出现)",
    r"已经(确认|确定)",
]

# B must not use WORLD_SHIFT legacy
FORBIDDEN_LEGACY = [
    r"\bWORLD_SHIFT\b",
    r"\bWorldChangeLevel\.WORLD\b",
]

@dataclass
class GuardResult:
    ok: bool
    errors: List[str]
    warnings: List[str]
    score: int  # 0-100
    grade: str  # GREEN/YELLOW/RED

def scan_repo_text(globs: List[str]) -> List[Tuple[str, str]]:
    files = []
    for g in globs:
        base = os.path.join(ROOT, g)
        if os.path.isfile(base):
            files.append(base)
    out = []
    for p in files:
        try:
            with open(p, "r", encoding="utf-8") as f:
                out.append((p, f.read()))
        except Exception:
            continue
    return out

def guard_architecture() -> GuardResult:
    errors: List[str] = []
    warnings: List[str] = []

    # Ensure guard docs exist
    for p in ARCH_GUARD_PATHS:
        if not os.path.exists(p):
            errors.append(f"[ARCH] missing guard doc: {p}")

    # Repo-wide quick scan for legacy / forbidden semantics
    # (Keep it small: only scan b2 folder + docs)
    scan_targets = []
    for root, _, filenames in os.walk(os.path.join(ROOT, "vision_pipeline")):
        for fn in filenames:
            if fn.endswith(".py") and ("/b2/" in root.replace("\\", "/")):
                scan_targets.append(os.path.join(root, fn))
    for root, _, filenames in os.walk(os.path.join(ROOT, "docs")):
        for fn in filenames:
            if fn.endswith(".md"):
                scan_targets.append(os.path.join(root, fn))

    for p in scan_targets:
        try:
            with open(p, "r", encoding="utf-8") as f:
                txt = f.read()
        except Exception:
            continue

        for pat in FORBIDDEN_LEGACY:
            if re.search(pat, txt):
                errors.append(f"[ARCH] legacy forbidden '{pat}' in {p}")

        # forbidden risk-confirm semantics: warning by default, can be upgraded to error later
        for pat in FORBIDDEN_PATTERNS:
            if re.search(pat, txt):
                warnings.append(f"[ARCH] suspicious wording '{pat}' in {p}")

    # Score/grade
    score = 100
    score -= min(60, 15 * len(errors))
    score -= min(30, 5 * len(warnings))
    score = max(0, score)

    grade = "GREEN"
    if score < 90 or warnings:
        grade = "YELLOW"
    if errors or score < 70:
        grade = "RED"

    ok = (len(errors) == 0)
    return GuardResult(ok=ok, errors=errors, warnings=warnings, score=score, grade=grade)

# ----------------------------
# DCS (Design Consistency Score) minimal hard rules
# ----------------------------

def dcs_check_trace(trace_path: str, seconds_limit: float = 30.0) -> GuardResult:
    """
    Minimal DCS runner:
    - Reads JSONL trace, checks hard invariants for the first N seconds window.
    - If trace not found: warning only (CI can require later).
    """
    errors: List[str] = []
    warnings: List[str] = []

    if not os.path.exists(trace_path):
        warnings.append(f"[DCS] trace not found: {trace_path} (skip)")
        return GuardResult(ok=True, errors=[], warnings=warnings, score=90, grade="YELLOW")

    first_t = None
    count = 0
    try:
        with open(trace_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                t = rec.get("time", {}).get("t_video_s")
                if t is None:
                    errors.append("[DCS] missing time.t_video_s")
                    continue
                if first_t is None:
                    first_t = float(t)
                if float(t) - first_t > seconds_limit:
                    break

                count += 1

                gate_mode = rec.get("gate", {}).get("mode")
                to_c_send = rec.get("to_c", {}).get("send")
                impact = rec.get("impact", {}).get("impact")
                advisory_only = rec.get("impact", {}).get("advisory_only")
                writeback = rec.get("writeback", {})

                # Hard rules
                if advisory_only is not True:
                    errors.append(f"[DCS] advisory_only must be True (t={t})")

                if gate_mode == "SUSPENDED" and to_c_send:
                    errors.append(f"[DCS] gate=SUSPENDED must not send to C (t={t})")

                if gate_mode == "READ_ONLY":
                    if any(writeback.get(k) for k in ["timeline", "health", "memory", "evidence_pack"]):
                        errors.append(f"[DCS] READ_ONLY must not writeback (t={t})")

                if impact == "NO_OP":
                    if to_c_send:
                        errors.append(f"[DCS] impact=NO_OP must not send to C (t={t})")
                    if writeback.get("timeline"):
                        errors.append(f"[DCS] impact=NO_OP must not write timeline (t={t})")

    except Exception as e:
        errors.append(f"[DCS] failed to parse trace: {e}")

    if count == 0:
        warnings.append("[DCS] trace empty or no valid lines")

    score = 100
    score -= min(70, 10 * len(errors))
    score -= min(20, 2 * len(warnings))
    score = max(0, score)

    grade = "GREEN"
    if warnings or score < 90:
        grade = "YELLOW"
    if errors or score < 70:
        grade = "RED"

    ok = (len(errors) == 0)
    return GuardResult(ok=ok, errors=errors, warnings=warnings, score=score, grade=grade)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trace", default=os.path.join(ROOT, "traces/b2_trace_v043.jsonl"))
    ap.add_argument("--seconds", type=float, default=30.0)
    ap.add_argument("--report", default=os.path.join(ROOT, "reports/arch_guard_report.json"))
    ap.add_argument("--use-dcs-eval", action="store_true", help="Use dcs_eval.py for DCS evaluation")
    args = ap.parse_args()

    arch = guard_architecture()
    
    # 如果使用 dcs_eval.py，先运行它
    if args.use_dcs_eval:
        import subprocess
        dcs_eval_script = os.path.join(ROOT, "tools", "dcs_eval.py")
        if os.path.exists(dcs_eval_script):
            print("Running dcs_eval.py...")
            result = subprocess.run([sys.executable, dcs_eval_script, args.trace], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f"⚠️ dcs_eval.py failed: {result.stderr}")
            else:
                print(result.stdout)
            
            # 读取生成的报告
            dcs_report_path = os.path.join(ROOT, "artifacts", "dcs_report.json")
            if os.path.exists(dcs_report_path):
                with open(dcs_report_path, "r", encoding="utf-8") as f:
                    dcs_report = json.load(f)
                red_count = dcs_report.get("red_count", 0)
                yellow_count = dcs_report.get("yellow_count", 0)
                green_count = dcs_report.get("green_count", 0)
                total = dcs_report.get("total", 0)
                
                dcs = GuardResult(
                    ok=(red_count == 0),
                    errors=[] if red_count == 0 else [f"DCS RED violations: {red_count}"],
                    warnings=[] if yellow_count == 0 else [f"DCS YELLOW violations: {yellow_count}"],
                    score=100 if red_count == 0 else (70 if yellow_count > 0 else 50),
                    grade="GREEN" if red_count == 0 else ("YELLOW" if yellow_count > 0 else "RED")
                )
            else:
                dcs = dcs_check_trace(args.trace, seconds_limit=args.seconds)
        else:
            print(f"⚠️ dcs_eval.py not found, falling back to built-in DCS check")
            dcs = dcs_check_trace(args.trace, seconds_limit=args.seconds)
    else:
        dcs = dcs_check_trace(args.trace, seconds_limit=args.seconds)

    final_ok = arch.ok and dcs.ok
    final_score = int(round((arch.score * 0.6) + (dcs.score * 0.4)))
    final_grade = "GREEN"
    if final_score < 90 or arch.grade == "YELLOW" or dcs.grade == "YELLOW":
        final_grade = "YELLOW"
    if (not final_ok) or final_score < 70 or arch.grade == "RED" or dcs.grade == "RED":
        final_grade = "RED"

    os.makedirs(os.path.dirname(args.report), exist_ok=True)
    out = {
        "final": {"ok": final_ok, "score": final_score, "grade": final_grade},
        "arch": arch.__dict__,
        "dcs": dcs.__dict__,
    }
    with open(args.report, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    # Console summary (CI readable)
    print("=== Architecture Guard ===")
    print(f"OK={arch.ok} SCORE={arch.score} GRADE={arch.grade}")
    for e in arch.errors:
        print("ERROR:", e)
    for w in arch.warnings[:20]:
        print("WARN:", w)

    print("=== DCS Trace Check ===")
    print(f"OK={dcs.ok} SCORE={dcs.score} GRADE={dcs.grade}")
    for e in dcs.errors:
        print("ERROR:", e)
    for w in dcs.warnings[:20]:
        print("WARN:", w)

    print("=== FINAL ===")
    print(f"OK={final_ok} SCORE={final_score} GRADE={final_grade}")
    print(f"Report: {args.report}")

    return 0 if final_ok else 2

if __name__ == "__main__":
    raise SystemExit(main())
