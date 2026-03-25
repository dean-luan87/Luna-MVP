# -*- coding: utf-8 -*-
"""
Benchmark Triage Board M0（场景问题分诊板）

定位（写死）：
- 分诊层，不是评测层：把 benchmark 结果转成研发优先级
- 只消费统一 benchmark 输出（ScenarioBenchmarkResult + summary）
- 输出：case/module/issue 三类排序 + next focus + triage_summary
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


def _i(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:
        return default


QUALITY_SCORE = {"poor": 50, "acceptable": 20, "good": 0, "unknown": 0}
ISSUE_SCORE = {
    # M0: type weight should dominate frequency
    "blocked_without_resolution": 120,
    "feedback_not_effective": 90,
    "high_dead_branch_ratio": 50,
}


def _priority_level(score: int) -> str:
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


@dataclass
class BenchmarkTriageCaseItem:
    case_id: str
    case_type: Optional[str]
    quality_grade: Optional[str]
    issue_type: Optional[str]
    optimization_hint_type: Optional[str]
    optimization_hint_module: Optional[str]
    priority_score: int
    priority_level: str
    triage_reason: str


@dataclass
class BenchmarkTriageModuleItem:
    module_name: str
    related_case_count: int
    poor_case_count: int
    issue_types: List[str] = field(default_factory=list)
    priority_score: int = 0
    priority_level: str = "low"
    triage_reason: Optional[str] = None


@dataclass
class BenchmarkTriageIssueItem:
    issue_type: str
    case_count: int
    poor_case_count: int
    related_modules: List[str] = field(default_factory=list)
    priority_score: int = 0
    priority_level: str = "low"
    triage_reason: Optional[str] = None


@dataclass
class BenchmarkTriageBoardResult:
    ranked_cases: List[BenchmarkTriageCaseItem] = field(default_factory=list)
    ranked_modules: List[BenchmarkTriageModuleItem] = field(default_factory=list)
    ranked_issues: List[BenchmarkTriageIssueItem] = field(default_factory=list)
    next_focus_case_ids: List[str] = field(default_factory=list)
    next_focus_modules: List[str] = field(default_factory=list)
    next_focus_issue_types: List[str] = field(default_factory=list)
    triage_summary: Optional[str] = None


def _case_score(r: Dict[str, Any]) -> Tuple[int, str]:
    q = _s(r.get("quality_grade")) or "unknown"
    issue = _s(r.get("issue_type"))
    hint_mod = _s(r.get("optimization_hint_module"))
    blocked = bool(r.get("blocked") is True)

    score = 0
    reasons: List[str] = []

    score += QUALITY_SCORE.get(q, 0)
    if q in ("poor", "acceptable"):
        reasons.append(f"quality={q}(+{QUALITY_SCORE.get(q,0)})")

    if issue:
        add = ISSUE_SCORE.get(issue, 0)
        if add:
            score += add
            reasons.append(f"issue={issue}(+{add})")
        else:
            reasons.append(f"issue={issue}(+0)")

    if blocked and issue == "blocked_without_resolution":
        # extra nudge for blocked cases
        score += 10
        reasons.append("blocked(+10)")

    if hint_mod:
        score += 10
        reasons.append("actionable_hint(+10)")

    return score, "; ".join(reasons) if reasons else "no strong signals"


def build_triage_board(results: List[Dict[str, Any]]) -> BenchmarkTriageBoardResult:
    # 1) cases
    case_items: List[BenchmarkTriageCaseItem] = []
    for r in results:
        if not isinstance(r, dict) or not r.get("case_id"):
            continue
        score, reason = _case_score(r)
        lvl = _priority_level(score)
        case_items.append(
            BenchmarkTriageCaseItem(
                case_id=str(r.get("case_id")),
                case_type=_s(r.get("case_type")),
                quality_grade=_s(r.get("quality_grade")),
                issue_type=_s(r.get("issue_type")),
                optimization_hint_type=_s(r.get("optimization_hint_type")),
                optimization_hint_module=_s(r.get("optimization_hint_module")),
                priority_score=int(score),
                priority_level=lvl,
                triage_reason=reason,
            )
        )
    case_items.sort(key=lambda x: x.priority_score, reverse=True)

    # 2) modules aggregation
    mod_stats: Dict[str, Dict[str, Any]] = {}
    for c in case_items:
        m = c.optimization_hint_module
        if not m:
            continue
        st = mod_stats.setdefault(m, {"related": 0, "poor": 0, "issues": set(), "score": 0})
        st["related"] += 1
        if c.quality_grade == "poor":
            st["poor"] += 1
            st["score"] += 20
        st["score"] += 10  # each related case
        if c.issue_type:
            st["issues"].add(c.issue_type)
            if c.issue_type == "blocked_without_resolution":
                st["score"] += 25
            elif c.issue_type == "feedback_not_effective":
                st["score"] += 20
    module_items: List[BenchmarkTriageModuleItem] = []
    for m, st in mod_stats.items():
        score = int(st["score"])
        lvl = _priority_level(score)
        module_items.append(
            BenchmarkTriageModuleItem(
                module_name=m,
                related_case_count=int(st["related"]),
                poor_case_count=int(st["poor"]),
                issue_types=sorted(list(st["issues"])),
                priority_score=score,
                priority_level=lvl,
                triage_reason=f"related={st['related']} poor={st['poor']} issues={sorted(list(st['issues']))}",
            )
        )
    module_items.sort(key=lambda x: x.priority_score, reverse=True)

    # 3) issue aggregation
    issue_stats: Dict[str, Dict[str, Any]] = {}
    for c in case_items:
        it = c.issue_type
        if not it:
            continue
        st = issue_stats.setdefault(it, {"cases": 0, "poor": 0, "mods": set(), "score": 0})
        st["cases"] += 1
        if c.quality_grade == "poor":
            st["poor"] += 1
            st["score"] += 25
        st["score"] += 10
        if c.optimization_hint_module:
            st["mods"].add(c.optimization_hint_module)
        # type weights
        st["score"] += ISSUE_SCORE.get(it, 0)
    issue_items: List[BenchmarkTriageIssueItem] = []
    for it, st in issue_stats.items():
        score = int(st["score"])
        lvl = _priority_level(score)
        issue_items.append(
            BenchmarkTriageIssueItem(
                issue_type=it,
                case_count=int(st["cases"]),
                poor_case_count=int(st["poor"]),
                related_modules=sorted(list(st["mods"])),
                priority_score=score,
                priority_level=lvl,
                triage_reason=f"cases={st['cases']} poor={st['poor']} mods={sorted(list(st['mods']))}",
            )
        )
    issue_items.sort(key=lambda x: x.priority_score, reverse=True)

    next_cases = [c.case_id for c in case_items[:3]]
    next_modules = [m.module_name for m in module_items[:3]]
    next_issues = [i.issue_type for i in issue_items[:3]]

    # triage summary
    worst = next_cases[:2]
    top_mod = next_modules[:2]
    top_issue = next_issues[:2]
    summary = (
        f"最差场景：{', '.join(worst) or '—'}；"
        f"优先模块：{', '.join(top_mod) or '—'}；"
        f"突出 issue：{', '.join(top_issue) or '—'}。"
    )

    return BenchmarkTriageBoardResult(
        ranked_cases=case_items,
        ranked_modules=module_items,
        ranked_issues=issue_items,
        next_focus_case_ids=next_cases,
        next_focus_modules=next_modules,
        next_focus_issue_types=next_issues,
        triage_summary=summary,
    )


def load_results_from_input(path: str) -> List[Dict[str, Any]]:
    p = Path(path)
    d = json.loads(p.read_text(encoding="utf-8"))
    res = d.get("results") if isinstance(d, dict) else None
    if not isinstance(res, list):
        return []
    return [x for x in res if isinstance(x, dict)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=str)
    ap.add_argument("--out", default=None, type=str)
    args = ap.parse_args()

    results = load_results_from_input(args.input)
    board = build_triage_board(results)
    payload = asdict(board)

    if args.out:
        Path(args.out).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print("wrote:", args.out)
    else:
        # concise stdout summary
        print(json.dumps({"next_focus_case_ids": board.next_focus_case_ids, "next_focus_modules": board.next_focus_modules, "next_focus_issue_types": board.next_focus_issue_types, "triage_summary": board.triage_summary}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

