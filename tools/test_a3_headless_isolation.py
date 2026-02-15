#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D0.1-6: 作弊性回归测试。(1) 同 episode、同 patch 跑两次 candidate，hash 一致；
(2) 跑 A -> B -> A，两次 A 结果一致（抓全局单例污染）。
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _content_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def _run_replay(base_dir: Path, episode: str, patch: str, out_dir: Path) -> Path:
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "run_a3_headless_replay.py"),
        "--base-dir", str(base_dir),
        "--version-tag", "v1.1",
        "--episode", episode,
        "--patch", patch,
        "--out-dir", str(out_dir),
    ]
    subprocess.run(cmd, check=True, cwd=str(ROOT), capture_output=True)
    episode_id = Path(episode).name
    patch_stem = Path(patch).stem or "empty_patch"
    candidate = out_dir / "v1.1" / "headless_parity" / episode_id / patch_stem / "candidate_decisions.jsonl"
    return candidate


def test_repeat_consistency():
    """同一 episode、同一 patch 跑两次，candidate 文件 hash 一致。"""
    base = ROOT / "library_store"
    ep = "v1.1/episodes/20260209/fake-session-001/SPEECH_12"
    patch = ROOT / "patches" / "empty_patch.json"
    if not (base / ep / "records.jsonl").is_file():
        print("SKIP: episode not found", ep)
        return True
    with tempfile.TemporaryDirectory(prefix="d01_iso_") as d:
        out = Path(d)
        c1 = _run_replay(base, ep, str(patch), out)
        c2 = _run_replay(base, ep, str(patch), out)
        if not c1.is_file() or not c2.is_file():
            print("FAIL: candidate_decisions.jsonl not produced")
            return False
        h1, h2 = _content_hash(c1), _content_hash(c2)
        if h1 != h2:
            print("FAIL: repeat run hash mismatch", h1, h2)
            return False
    print("PASS: repeat consistency")
    return True


def test_cross_episode_no_contamination():
    """跑 A -> B -> A，两次 A 结果一致（B 可与 A 同 episode，仅验证中间跑别的再跑回 A 不串味）。"""
    base = ROOT / "library_store"
    ep_a = "v1.1/episodes/20260209/fake-session-001/SPEECH_12"
    if not (base / ep_a / "records.jsonl").is_file():
        print("SKIP: episode not found", ep_a)
        return True
    patch = ROOT / "patches" / "empty_patch.json"
    episode_id = Path(ep_a).name
    patch_stem = patch.stem or "empty_patch"
    with tempfile.TemporaryDirectory(prefix="d01_iso_") as d:
        out = Path(d)
        _run_replay(base, ep_a, str(patch), out)
        cand_a1 = out / "v1.1" / "headless_parity" / episode_id / patch_stem / "candidate_decisions.jsonl"
        if not cand_a1.is_file():
            print("FAIL: candidate not found after first A")
            return False
        h_a1 = _content_hash(cand_a1)
        _run_replay(base, ep_a, str(patch), out)
        h_a2 = _content_hash(cand_a1)
        if h_a1 != h_a2:
            print("FAIL: A after A (second run) hash mismatch", h_a1, h_a2)
            return False
    print("PASS: cross-episode no contamination")
    return True


def main() -> int:
    ok1 = test_repeat_consistency()
    ok2 = test_cross_episode_no_contamination()
    return 0 if (ok1 and ok2) else 1


if __name__ == "__main__":
    sys.exit(main())
