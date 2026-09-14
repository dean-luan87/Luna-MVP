#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实视频 → baseline/candidate replay → exit_latency 审计。
流程：跑视频得 trace → 转 episode(records) → recompute 得 baseline + candidate replay → 审计。
用于验证：分叉是否稳定触发、是否长尾粘滞、是否 baseline_no_entry 爆发。
不依赖 library_store，out 目录下自含 episode + 两份 bundle + audit report。
"""
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

TRACE_PATH = ROOT / "logs" / "a3_trace.jsonl"


def _trace_to_episode_dir(
    trace_path: Path,
    episode_dir: Path,
    max_records: Optional[int],
    last_records: Optional[int] = None,
) -> str:
    """把 a3_trace.jsonl 中有 seq+obs 的行转为 OBS_V1 records，写入 episode_dir。
    若 last_records 指定则只保留最后 N 条（用于「后 2 分钟」等片段）；否则用 max_records 限制条数（从头取）。"""
    episode_dir.mkdir(parents=True, exist_ok=True)
    records = []
    with open(trace_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if "obs" not in row or row.get("seq") is None:
                continue
            records.append({
                "record_type": "OBS_V1",
                "ts": row.get("ts", len(records)),
                "seq": row.get("seq", len(records)),
                "sampled": row.get("sampled", False),
                "obs": row.get("obs", {}),
            })
            if last_records is None and max_records is not None and len(records) >= max_records:
                break
    if last_records is not None and len(records) > last_records:
        records = records[-last_records:]
    with open(episode_dir / "records.jsonl", "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    meta = {
        "episode_id": episode_dir.name,
        "record_count": len(records),
        "source_trace": str(trace_path),
    }
    with open(episode_dir / "meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    # episode_rel_path 相对 ROOT，供 run_episode(base_dir=ROOT, episode_rel_path=...)
    try:
        return str(episode_dir.relative_to(ROOT))
    except ValueError:
        return str(episode_dir)


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="Video → trace → episode → baseline/candidate replay → exit audit")
    p.add_argument("--video", required=True, help="视频路径")
    p.add_argument("--config", required=True, help="Guardian B patch JSON 路径（candidate 用）")
    p.add_argument("--out", default=None, help="输出目录，默认 outputs/video_replay_<video_stem>")
    p.add_argument("--max-frames", type=int, default=None, help="最多处理帧数（默认不限制）。600 ≈ 20s@30fps")
    p.add_argument("--last-records", type=int, default=None, help="只取 trace 最后 N 条做 episode（如 3600=后2分钟@30fps），与 --max-frames 二选一")
    p.add_argument("--frame-step", type=int, default=1)
    args = p.parse_args()

    video_path = Path(args.video)
    if not video_path.is_file():
        print("ERROR: 视频不存在:", video_path, file=sys.stderr)
        return 2
    config_path = Path(args.config)
    if not config_path.is_file():
        print("ERROR: config 不存在:", config_path, file=sys.stderr)
        return 2

    out_dir = Path(args.out) if args.out else ROOT / "outputs" / f"video_replay_{video_path.stem}"
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    episode_dir = out_dir / "episode"
    # 清空旧 trace，跑视频
    if TRACE_PATH.exists():
        TRACE_PATH.unlink()
    TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
    print("Step 1: 跑视频生成 trace ...")
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "run_video_a3_trace.py"),
        "--video", str(video_path.resolve()),
        "--frame-step", str(args.frame_step),
    ]
    # 取后 N 条时需先跑全片，耗时会很长
    if args.last_records is not None:
        timeout_sec = 2400  # 6m42s 全片约需 15～25 分钟，给 40 分钟
        print("(使用 --last-records 会先跑全片，约 15～25 分钟，请耐心等待)")
    elif args.max_frames is not None:
        cmd.extend(["--max-frames", str(args.max_frames)])
        timeout_sec = 900
    else:
        timeout_sec = 900
    rc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=timeout_sec)
    if rc.returncode != 0:
        print("ERROR: run_video_a3_trace 失败:", rc.stderr[:800], file=sys.stderr)
        return 2
    if not TRACE_PATH.is_file():
        print("ERROR: trace 未生成:", TRACE_PATH, file=sys.stderr)
        return 2

    print("Step 2: trace → episode (records.jsonl) ...")
    episode_rel = _trace_to_episode_dir(
        TRACE_PATH, episode_dir,
        max_records=args.max_frames if args.last_records is None else None,
        last_records=args.last_records,
    )
    records_path = episode_dir / "records.jsonl"
    if not records_path.is_file() or os.path.getsize(records_path) == 0:
        print("ERROR: episode 无有效 records", file=sys.stderr)
        return 2

    print("Step 3: recompute baseline + candidate ...")
    from simulation.sim_runner import run_episode

    sim_out = str(out_dir)
    baseline_bundle = run_episode(
        str(ROOT), "v1.1", episode_rel, "", sim_out,
        bundle_episode_id="video_replay", mode="recompute",
    )
    candidate_bundle = run_episode(
        str(ROOT), "v1.1", episode_rel, str(config_path.resolve()), sim_out,
        bundle_episode_id="video_replay", baseline_bundle_path=baseline_bundle, mode="recompute",
    )
    baseline_replay = Path(baseline_bundle) / "replay_output.jsonl"
    candidate_replay = Path(candidate_bundle) / "replay_output.jsonl"
    if not baseline_replay.is_file() or not candidate_replay.is_file():
        print("ERROR: replay 未生成", file=sys.stderr)
        return 2

    print("Step 4: exit_latency 审计 ...")
    from tools.audit_exit_latency import run_audit

    audit_path = Path(candidate_bundle) / "exit_audit_report.json"
    report = run_audit(
        str(baseline_replay.resolve()),
        str(candidate_replay.resolve()),
        out_path=str(audit_path.resolve()),
        top_k=10,
    )
    s = report["summary"]
    print("--- Audit Summary ---")
    print("exit_latency_p50:", s["exit_latency_p50"])
    print("exit_latency_p95:", s["exit_latency_p95"])
    print("exit_latency_max:", s["exit_latency_max"])
    print("hysteresis_efficiency:", s["hysteresis_efficiency"])
    print("baseline_no_entry_count:", s["baseline_no_entry_count"])
    print("guarded_tail_ratio:", s.get("guarded_tail_ratio"))
    print("max_dwell_frames:", s.get("max_dwell_frames"))
    print("Written:", audit_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
