#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smoke：对比 envelope 与 flat 两种 JSONL 经 analyze_unified_env_min_wiring_v1 后的关键统计是否一致，
防止 _load_rows 双格式兼容被改坏。

仅标准库；在 Luna-Core 根目录执行：

  python3 tools/smoke_compare_unified_env_min_wiring_v1.py \\
    --envelope-jsonl logs/unified_env_min_wiring_snapshot_v1.jsonl \\
    --flat-jsonl logs/window_real_unified_env_min_wiring_round02.jsonl
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent

KEY_FIELDS = (
    "row_count",
    "fill_applied_count",
    "effective_fill_count",
    "ineffective_fill_count",
)


def _run_analyzer(*, input_jsonl: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "analyze_unified_env_min_wiring_v1.py"),
        "--input-jsonl",
        str(input_jsonl.resolve()),
        "--output-dir",
        str(out_dir.resolve()),
    ]
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    if r.returncode != 0:
        msg = (r.stderr or r.stdout or "").strip() or f"exit {r.returncode}"
        raise RuntimeError(f"analyzer failed: {msg}")

    js = list(out_dir.glob("analyze_unified_env_min_wiring_v1_*.json"))
    if not js:
        raise RuntimeError(f"no analyze_unified_env_min_wiring_v1_*.json under {out_dir}\n{r.stdout}")
    return max(js, key=lambda p: p.stat().st_mtime)


def _load_payload(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _first_effective_id(payload: Dict[str, Any]) -> Optional[str]:
    samples = payload.get("samples")
    if not isinstance(samples, dict):
        return None
    eff = samples.get("effective")
    if not isinstance(eff, list) or not eff:
        return None
    first = eff[0]
    if not isinstance(first, dict):
        return None
    v = first.get("id")
    return str(v) if v is not None else None


def _compare(
    a: Dict[str, Any], b: Dict[str, Any]
) -> Tuple[bool, List[str]]:
    diffs: List[str] = []
    for k in KEY_FIELDS:
        va, vb = a.get(k), b.get(k)
        if va != vb:
            diffs.append(f"{k}: envelope={va!r} flat={vb!r}")
    id_a, id_b = _first_effective_id(a), _first_effective_id(b)
    if id_a != id_b:
        diffs.append(f"first_effective_sample.id: envelope={id_a!r} flat={id_b!r}")
    return (len(diffs) == 0, diffs)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Smoke: envelope vs flat min wiring analyzer parity"
    )
    ap.add_argument("--envelope-jsonl", required=True, type=Path)
    ap.add_argument("--flat-jsonl", required=True, type=Path)
    args = ap.parse_args()

    env_in = args.envelope_jsonl
    flat_in = args.flat_jsonl
    if not env_in.is_file():
        print(f"ERROR: missing envelope file: {env_in.resolve()}", file=sys.stderr)
        return 2
    if not flat_in.is_file():
        print(f"ERROR: missing flat file: {flat_in.resolve()}", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="smoke_min_wiring_env_") as d_env:
        with tempfile.TemporaryDirectory(prefix="smoke_min_wiring_flat_") as d_flat:
            p_env = Path(d_env)
            p_flat = Path(d_flat)
            try:
                j_env = _run_analyzer(input_jsonl=env_in, out_dir=p_env)
                j_flat = _run_analyzer(input_jsonl=flat_in, out_dir=p_flat)
            except RuntimeError as e:
                print(f"ERROR: {e}", file=sys.stderr)
                return 1

            payload_env = _load_payload(j_env)
            payload_flat = _load_payload(j_flat)
            ok, diffs = _compare(payload_env, payload_flat)

            print(f"envelope analyzer JSON: {j_env}")
            print(f"flat analyzer JSON:     {j_flat}")
            for k in KEY_FIELDS:
                print(f"  {k}: {payload_env.get(k)} / {payload_flat.get(k)}")
            print(
                f"  first_effective_id: {_first_effective_id(payload_env)!r} / "
                f"{_first_effective_id(payload_flat)!r}"
            )

            if ok:
                print("OK: envelope and flat results match")
                return 0
            print("MISMATCH:", file=sys.stderr)
            for line in diffs:
                print(line, file=sys.stderr)
            return 1


if __name__ == "__main__":
    raise SystemExit(main())
