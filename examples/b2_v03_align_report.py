# examples/b2_v03_align_report.py
from __future__ import annotations
import json
import argparse
from typing import List, Dict, Any

from vision_pipeline.b2.v03.align_validator import parse_expected, find_match
from vision_pipeline.b2.v03.align_report import (
    classify_result,
    write_csv_report,
    write_markdown_report,
)
from vision_pipeline.b2.v03.narrative import build_narrative


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_jsonl(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--human", default="human_timeline.json")
    ap.add_argument("--b2", default="b2_v03_timeline.jsonl")
    ap.add_argument("--out", default="reports")
    args = ap.parse_args()

    human = load_json(args.human)
    b2_events = list(load_jsonl(args.b2))

    tolerance = {"L1": 6.0, "L2": 4.0, "L3": 2.5}

    rows: List[Dict[str, Any]] = []
    used = set()

    ok = late = miss = 0

    for h in human:
        t = h["t_video"]
        lvl = h.get("level", "L2")
        max_dt = tolerance.get(lvl, 4.0)
        expected = parse_expected(h.get("expected", ""))

        m = find_match(b2_events, t, expected, max_dt)
        if m is None:
            miss += 1
            rows.append({
                "human_t_str": h["t_str"],
                "label": h.get("label",""),
                "expected": h.get("expected",""),
                "b2_t_str": "",
                "decision": "",
                "dt": "",
                "result": "MISS",
                "evidence_ref": "",
                "narrative_M": "",
                "narrative_L": "",
            })
            continue

        idx = b2_events.index(m)
        used.add(idx)

        dt = m["_dt"]
        result = classify_result(dt, max_dt)
        if result == "OK":
            ok += 1
        else:
            late += 1

        # 加载 evidence 并生成 narrative
        evidence_ref = m.get("evidence_ref", "")
        narrative_m = ""
        narrative_l = ""

        if evidence_ref:
            try:
                evidence_pack = load_json(evidence_ref)
                narrative_m = build_narrative(evidence_pack, level="M")
                narrative_l = build_narrative(evidence_pack, level="L")
            except Exception:
                narrative_m = ""
                narrative_l = ""

        rows.append({
            "human_t_str": h["t_str"],
            "label": h.get("label",""),
            "expected": h.get("expected",""),
            "b2_t_str": m.get("t_str",""),
            "decision": m.get("decision",""),
            "dt": round(dt, 2),
            "result": result,
            "evidence_ref": evidence_ref,
            "narrative_M": narrative_m,
            "narrative_L": narrative_l,
        })

    # 误报（FP）
    fp = 0
    for i, e in enumerate(b2_events):
        if i in used:
            continue
        if e.get("decision") and e["decision"] != "NO_CHANGE":
            fp += 1
            rows.append({
                "human_t_str": "",
                "label": "",
                "expected": "",
                "b2_t_str": e.get("t_str",""),
                "decision": e.get("decision",""),
                "dt": "",
                "result": "FP",
                "evidence_ref": e.get("evidence_ref",""),
                "narrative_M": "",
                "narrative_L": "",
            })

    summary = {
        "OK": ok,
        "LATE": late,
        "MISS": miss,
        "FP": fp,
        "TOTAL_HUMAN_EVENTS": len(human),
    }

    csv_path = f"{args.out}/b2_v03_alignment.csv"
    md_path = f"{args.out}/b2_v03_alignment.md"

    write_csv_report(rows, csv_path)
    write_markdown_report(rows, summary, md_path)

    print(f"[Report] CSV → {csv_path}")
    print(f"[Report] MD  → {md_path}")
    print(f"[Summary] {summary}")


if __name__ == "__main__":
    main()

