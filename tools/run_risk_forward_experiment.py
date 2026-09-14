#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风险前移验证实验：不改 SimRunner，用已有 baseline replay 构造“轻微前移”候选，
验证 early_gain / volatility / gate 的关系。哲学验证：更保守是否真的更好？
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulation.logic.gate import is_gate_passed
from simulation.logic.scorer import score


def load_replay(bundle_dir: str) -> list:
    path = os.path.join(bundle_dir.rstrip("/"), "replay_output.jsonl")
    if not os.path.isfile(path):
        return []
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def write_replay(bundle_dir: str, records: list) -> None:
    os.makedirs(bundle_dir, exist_ok=True)
    path = os.path.join(bundle_dir, "replay_output.jsonl")
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def make_slight_forward_candidate(baseline_records: list) -> list:
    """
    轻微前移：仅第 0 帧改为 GUARDED，其余与 baseline 一致。
    模拟“略早进入 GUARDED”的 patch 效果。
    """
    out = []
    for i, r in enumerate(baseline_records):
        rec = json.loads(json.dumps(r))
        dec = rec.get("decision") or {}
        if i == 0:
            dec["control_mode"] = "GUARDED"
            dec["decision_source"] = "synthetic_slight_forward"
        rec["decision"] = dec
        out.append(rec)
    return out


def make_full_guarded_candidate(baseline_records: list) -> list:
    """
    全程保守：全部帧 GUARDED，无切换。
    验证：early_gain 高且 volatility=0 时 Gate 应 PASS。
    """
    out = []
    for r in baseline_records:
        rec = json.loads(json.dumps(r))
        dec = rec.get("decision") or {}
        dec["control_mode"] = "GUARDED"
        dec["decision_source"] = "synthetic_full_guarded"
        rec["decision"] = dec
        out.append(rec)
    return out


def main():
    import argparse
    p = argparse.ArgumentParser(description="Risk forward experiment: synthetic candidate vs baseline")
    p.add_argument("--baseline-bundle", default=None, help="Path to baseline replay bundle (default: outputs/v1.1/simulations/SPEECH_12_baseline)")
    p.add_argument("--out-dir", default=os.path.join(ROOT, "outputs", "v1.1", "simulations"), help="Simulations dir")
    args = p.parse_args()
    baseline_bundle = args.baseline_bundle or os.path.join(args.out_dir, "SPEECH_12_baseline")
    if not os.path.isdir(baseline_bundle):
        print("ERROR: baseline bundle not found:", baseline_bundle, file=sys.stderr)
        return 1
    baseline_records = load_replay(baseline_bundle)
    if not baseline_records:
        print("ERROR: no replay in baseline", file=sys.stderr)
        return 1
    out_dir = args.out_dir.rstrip("/")
    results = []
    for name, maker in [
        ("B_slight_forward", make_slight_forward_candidate),
        ("C_full_guarded", make_full_guarded_candidate),
    ]:
        candidate_bundle = os.path.join(out_dir, f"SPEECH_12_{name}")
        candidate_records = maker(baseline_records)
        write_replay(candidate_bundle, candidate_records)
        scorecard = score(baseline_path=baseline_bundle, candidate_path=candidate_bundle)
        scorecard_path = os.path.join(candidate_bundle, "scorecard.json")
        os.makedirs(candidate_bundle, exist_ok=True)
        with open(scorecard_path, "w", encoding="utf-8") as f:
            json.dump(scorecard, f, ensure_ascii=False, indent=2)
        passed, reasons = is_gate_passed(scorecard)
        results.append((name, scorecard, passed, reasons))
        eff = scorecard.get("efficiency") or {}
        print("\n---", name, "---")
        print("early_conservative_action_gain:", scorecard.get("early_conservative_action_gain"))
        print("danger_delta:", scorecard.get("danger_delta"))
        print("volatility_index:", scorecard.get("volatility_index"))
        print("regression_count:", scorecard.get("regression_count"))
        print("GUARDED_RATIO_DELTA:", eff.get("guarded_ratio_delta"))
        print("LOOKAHEAD_DROP_RATIO:", eff.get("lookahead_drop_ratio"))
        print("GATE:", "PASS" if passed else "FAIL", reasons)
    print("\n=== 哲学验证小结 ===")
    for name, sc, passed, reasons in results:
        eg = sc.get("early_conservative_action_gain", 0)
        vol = sc.get("volatility_index", 0)
        print(f"  {name}: early_gain={eg}, volatility={vol}, GATE={'PASS' if passed else 'FAIL'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
