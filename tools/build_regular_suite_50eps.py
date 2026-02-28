#!/usr/bin/env python3
"""
B1 扩容：从现有 powerclips 构建 50-ep regular suite。
Regular 通道使用与 stress 相同的 episode 格式（manifest+records），仅 patch 不同。
合并 pulse(40) + sustain 中不在 pulse 的，取前 50 个。

用法:
  python3 tools/build_regular_suite_50eps.py
  # 输出: library_store/v1.1/golden_regular_v3_50eps/
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_SUITE = ROOT / "library_store" / "v1.1" / "golden_regular_v3_50eps"
PULSE = ROOT / "library_store" / "v1.1" / "golden_stress_v2_powerclips_pulse"
SUSTAIN = ROOT / "library_store" / "v1.1" / "golden_stress_v2_powerclips_sustain"
HARD50 = ROOT / "library_store" / "v1.1" / "golden_stress_v2_powerclips_hard50"


def _clips_from_manifest(p: Path) -> list:
    if not p.is_file():
        return []
    return json.loads(p.read_text()).get("clips") or []


def main() -> int:
    if not PULSE.is_dir():
        print("ERROR: pulse suite not found:", PULSE, file=sys.stderr)
        return 2

    clips: list = []
    seen: set = set()
    for suite_path, manifest_path in [
        (PULSE, PULSE / "suite_manifest.json"),
        (SUSTAIN, SUSTAIN / "suite_manifest.json") if SUSTAIN.is_dir() else (None, None),
        (HARD50, HARD50 / "suite_manifest.json") if HARD50.is_dir() else (None, None),
    ]:
        if suite_path is None or not manifest_path.is_file():
            continue
        for c in _clips_from_manifest(manifest_path):
            if c not in seen and (suite_path / c).is_dir():
                clips.append(c)
                seen.add(c)
                if len(clips) >= 50:
                    break
        if len(clips) >= 50:
            break
    clips = clips[:50]
    if len(clips) < 50:
        print("WARN: only %d clips available, using all" % len(clips), file=sys.stderr)

    sources = [PULSE]
    if SUSTAIN.is_dir():
        sources.append(SUSTAIN)
    if HARD50.is_dir():
        sources.append(HARD50)

    OUT_SUITE.mkdir(parents=True, exist_ok=True)
    for ep_id in clips:
        src = None
        for s in sources:
            if (s / ep_id).is_dir():
                src = s / ep_id
                break
        if not src or not src.is_dir():
            continue
        dst = OUT_SUITE / ep_id
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    manifest = {
        "suite_name": "golden_regular_v3_50eps",
        "total_clips": len(clips),
        "clips": clips,
        "rules": {"min_clip_len": 120, "max_clip_len": 900},
    }
    (OUT_SUITE / "suite_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("[B1] Built %s: %d episodes" % (OUT_SUITE, len(clips)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
