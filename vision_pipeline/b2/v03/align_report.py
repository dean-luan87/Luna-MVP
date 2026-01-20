# vision_pipeline/b2/v03/align_report.py
from __future__ import annotations
from typing import List, Dict, Any
import csv
import os


def classify_result(dt: float, max_dt: float) -> str:
    """
    对齐结果分类：
    - OK：快速命中
    - LATE：命中但延迟
    - MISS：未命中
    """
    if dt < 0:
        return "MISS"
    if dt <= max_dt * 0.5:
        return "OK"
    return "LATE"


def write_csv_report(
    rows: List[Dict[str, Any]],
    out_path: str,
) -> None:
    if not rows:
        return

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fieldnames = list(rows[0].keys())

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def write_markdown_report(
    rows: List[Dict[str, Any]],
    summary: Dict[str, Any],
    out_path: str,
) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        # 标题
        f.write("# B2 v0.3 Alignment Report\n\n")

        # 总览
        f.write("## Summary\n\n")
        for k, v in summary.items():
            f.write(f"- **{k}**: {v}\n")
        f.write("\n")

        # 表头
        f.write("## Details\n\n")
        f.write("| Human Time | Label | Expected | B2 Time | Decision | Δt(s) | Result | Narrative (M) |\n")
        f.write("|------------|-------|----------|---------|----------|-------|--------|---------------|\n")

        for r in rows:
            f.write(
                f"| {r['human_t_str']} "
                f"| {r.get('label','')} "
                f"| {r.get('expected','')} "
                f"| {r.get('b2_t_str','')} "
                f"| {r.get('decision','')} "
                f"| {r.get('dt','')} "
                f"| {r.get('result','')} "
                f"| {r.get('narrative_M','')} |\n"
            )

