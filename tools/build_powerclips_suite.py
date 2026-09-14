#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PowerClips 燃料工厂：从 sweep 产出的 replay_output.jsonl 筛选高压片段，生成可复现、可审计的 clip suite。
核心物理口径由 POWERCLIP_RULES 锁定；clip_id / suite_hash 均确定性，参与后续 suite_hash 与 D1 回溯。
"""
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

OBS_V1 = "OBS_V1"

# 物理口径：必须写入 manifest 并参与 suite_hash，不得漂移
POWERCLIP_RULES = {
    "risk_max_min": 0.60,
    "min_high_risk_frames": 30,
    "pre_padding_frames": 60,
    "post_padding_frames": 60,
    "min_clip_len": 120,
    "max_clip_len": 900,
}


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    """逐行加载 JSONL，失败行跳过。"""
    out: List[Dict[str, Any]] = []
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8").strip().splitlines():
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def write_jsonl(path: Path, records: List[Dict[str, Any]]) -> None:
    """写入 JSONL，每行一个 JSON。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, obj: Any) -> None:
    """写入 JSON，sort_keys=True 保证可复现。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def collect_replay_files(sweep_dir: Path) -> List[Path]:
    """收集所有 replay_output.jsonl，顺序固定（deterministic）。"""
    files = sorted(sweep_dir.glob("**/replay_output.jsonl"))
    return [f for f in files if f.is_file()]


def generate_deterministic_id(replay_path: Path, clip_start: int, clip_end: int) -> str:
    """clip_id 不依赖时间戳，仅依赖路径与区间。"""
    raw = f"{replay_path.resolve()}_{clip_start}_{clip_end}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def extract_patch_hash(replay_path: Path) -> str:
    """从 replay 所在或父级目录寻找 patch 文件并哈希；找不到则空串。"""
    for d in [replay_path.parent, replay_path.parent.parent]:
        for name in ("patch.json", "effective_patch.json", "effective_patch.stress.json"):
            p = d / name
            if p.is_file():
                return hashlib.sha256(p.read_bytes()).hexdigest()[:16]
    return ""


def _source_episode_ids(source_golden_dir: Path) -> List[str]:
    """源 suite 下所有含 records.jsonl 的子目录名，按长度降序（便于最长前缀匹配）。"""
    if not source_golden_dir.is_dir():
        return []
    ids = [
        d.name for d in sorted(source_golden_dir.iterdir())
        if d.is_dir() and (d / "records.jsonl").is_file()
    ]
    return sorted(ids, key=len, reverse=True)


def _episode_id_from_replay_path(replay_path: Path, source_episode_ids: List[str]) -> Optional[str]:
    """
    从 replay 路径推断源 episode_id。
    sim 输出目录名为 {episode_id}_{patch_id}，例如 stress_v2_a3_trace_tr4950_5069_effective_patch.stress。
    """
    dir_name = replay_path.parent.name
    for ep_id in source_episode_ids:
        if dir_name == ep_id or dir_name.startswith(ep_id + "_"):
            return ep_id
    return None


def _load_source_obs_v1_slice(
    source_golden_dir: Path,
    episode_id: str,
    clip_start: int,
    clip_end: int,
) -> Optional[List[Dict[str, Any]]]:
    """
    从源 episode 的 records.jsonl 中只取 OBS_V1 行，再按帧下标 [clip_start:clip_end] 切片。
    recompute 时 run_episode 只消费 OBS_V1，且与 replay 行一一对应。
    """
    records_path = source_golden_dir / episode_id / "records.jsonl"
    if not records_path.is_file():
        return None
    records = load_jsonl(records_path)
    obs_v1 = [r for r in records if (r.get("record_type") or "").strip() == OBS_V1]
    if clip_end > len(obs_v1):
        return None
    return obs_v1[clip_start:clip_end]


def _risk_value(rec: Dict[str, Any]) -> Optional[float]:
    """从单条 record 取风险值：优先 risk_used_for_decision，否则 decision.a3_debug.ema / complexity_score。"""
    v = rec.get("risk_used_for_decision")
    if v is not None:
        try:
            return float(v)
        except (TypeError, ValueError):
            pass
    dec = rec.get("decision") or {}
    if isinstance(dec, dict):
        debug = dec.get("a3_debug") or {}
        if isinstance(debug, dict):
            for key in ("ema", "raw_effective", "complexity_score"):
                v = debug.get(key)
                if v is not None:
                    try:
                        return float(v)
                    except (TypeError, ValueError):
                        pass
    v = rec.get("complexity_score")
    if v is not None:
        try:
            return float(v)
        except (TypeError, ValueError):
            pass
    return None


def _run_lengths(values: List[float], thr: float) -> List[int]:
    """连续 value >= thr 的每段长度。"""
    lengths: List[int] = []
    n = 0
    for v in values:
        if v >= thr:
            n += 1
        else:
            if n:
                lengths.append(n)
            n = 0
    if n:
        lengths.append(n)
    return lengths


def replay_stats(replay_path: Path) -> Optional[Tuple[float, int]]:
    """仅统计 risk_max 与 high_risk_frames，不裁剪；用于诊断。风险值优先 risk_used_for_decision，否则 fallback 到 decision.a3_debug.ema 等。"""
    records = load_jsonl(replay_path)
    if not records:
        return None
    risk_values = []
    for r in records:
        v = _risk_value(r)
        if v is not None:
            risk_values.append(v)
    if not risk_values:
        return None
    risk_max = max(risk_values)
    high_risk_count = sum(1 for r in records if r.get("high_risk") is True)
    if high_risk_count == 0 and risk_values:
        threshold = 0.38
        high_risk_count = sum(1 for r in records if (_risk_value(r) or 0) >= threshold)
    return risk_max, high_risk_count


def process_single_replay(
    replay_path: Path,
    rules: Optional[Dict[str, Any]] = None,
    source_golden_dir: Optional[Path] = None,
    source_episode_ids: Optional[List[str]] = None,
) -> Optional[Dict[str, Any]]:
    """
    单条 replay 筛选与裁剪：risk_max >= risk_max_min、high_risk_frames >= min_high_risk_frames，
    裁剪连续高压段 ± padding，满足 min/max_clip_len。
    若提供 source_golden_dir，则 records.jsonl 写源 episode 的 OBS_V1 切片（供 recompute 消费）；
    否则写 replay 行切片（仅适合 replay 模式，recompute 会得到 0 帧）。
    rules 未传时使用 POWERCLIP_RULES；返回 manifest dict 供 suite 汇总；不通过则返回 None。
    """
    r = rules or POWERCLIP_RULES
    records = load_jsonl(replay_path)
    if not records:
        return None

    risk_values = []
    for rec in records:
        v = _risk_value(rec)
        if v is not None:
            risk_values.append(v)
    if not risk_values:
        return None
    risk_max = max(risk_values)

    if risk_max < r["risk_max_min"]:
        return None

    threshold_fallback = 0.38
    high_risk_indices = [
        i for i, rec in enumerate(records)
        if rec.get("high_risk") is True or (_risk_value(rec) or 0) >= threshold_fallback
    ]
    if len(high_risk_indices) < r["min_high_risk_frames"]:
        return None

    # 可选：要求存在一段连续 N 帧 risk >= thr（打状态机连续门槛）
    min_consecutive = r.get("min_consecutive_over")
    if min_consecutive:
        thr, frames = min_consecutive
        risk_vals_replay = [(_risk_value(rec) or 0) for rec in records]
        run_lens = _run_lengths(risk_vals_replay, thr)
        if not run_lens or max(run_lens) < frames:
            return None

    start = min(high_risk_indices)
    end = max(high_risk_indices)
    clip_start = max(0, start - r["pre_padding_frames"])
    clip_end = min(len(records), end + r["post_padding_frames"])
    clip_len = clip_end - clip_start

    if clip_len < r["min_clip_len"]:
        return None

    if clip_len > r["max_clip_len"]:
        clip_end = clip_start + r["max_clip_len"]
    clip_len = clip_end - clip_start

    # 接口对齐 D1 recompute：写 OBS_V1 切片而非 replay 行，否则 run_episode 的 obs_v1 为空，high_risk 全 0
    source_episode_id: Optional[str] = None
    if source_golden_dir and source_episode_ids is not None:
        episode_id = _episode_id_from_replay_path(replay_path, source_episode_ids)
        if not episode_id:
            return None
        clip_records = _load_source_obs_v1_slice(source_golden_dir, episode_id, clip_start, clip_end)
        if not clip_records:
            return None
        source_episode_id = episode_id
    else:
        clip_records = records[clip_start:clip_end]

    clip_id = generate_deterministic_id(replay_path, clip_start, clip_end)
    out = {
        "clip_id": clip_id,
        "source_replay": str(replay_path.resolve()),
        "risk_max": risk_max,
        "high_risk_frames": len(high_risk_indices),
        "clip_start": clip_start,
        "clip_end": clip_end,
        "clip_len": clip_len,
        "rules": dict(r),
        "source_patch_hash": extract_patch_hash(replay_path),
        "_clip_records": clip_records,
    }
    if source_episode_id is not None:
        out["source_episode_id"] = source_episode_id
    return out


def write_suite_manifest(out_suite: Path, clips: List[Dict[str, Any]], suite_name: str, rules: Optional[Dict[str, Any]] = None) -> None:
    """写入 suite_manifest.json：suite_name, total_clips, avg_risk_max, rules, clips=sorted(clip_ids)。"""
    r = rules or POWERCLIP_RULES
    if not clips:
        manifest = {
            "suite_name": suite_name,
            "total_clips": 0,
            "avg_risk_max": 0.0,
            "rules": r,
            "clips": [],
        }
    else:
        clip_ids = sorted(c["clip_id"] for c in clips)
        avg_risk_max = sum(c["risk_max"] for c in clips) / len(clips)
        manifest = {
            "suite_name": suite_name,
            "total_clips": len(clips),
            "avg_risk_max": round(avg_risk_max, 4),
            "rules": r,
            "clips": clip_ids,
        }
    write_json(out_suite / "suite_manifest.json", manifest)


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(
        description="PowerClips 燃料工厂：从 sweep 的 replay_output.jsonl 筛选高压片段，输出确定性 clip suite"
    )
    p.add_argument("--sweep-output-dir", required=True, help="Sweep 产出目录（含 **/replay_output.jsonl）")
    p.add_argument("--out-suite-dir", required=True, help="输出 suite 目录，如 library_store/v1.1/golden_stress_v2_powerclips")
    p.add_argument("--source-golden-suite-dir", default="", help="源 episode 的 golden 目录（如 library_store/v1.1/golden_stress_v2）。必填时从源 records 取 OBS_V1 切片写入 clip，供 D1 recompute 使用；不填则写 replay 行切片（recompute 会 0 帧）")
    p.add_argument("--suite-name", default="golden_stress_v2_powerclips", help="Suite 名称，写入 suite_manifest")
    p.add_argument("--max-clips", type=int, default=30, help="最多保留 clip 数（第一版建议 10–30，便于人工 inspect）")
    p.add_argument("--diagnose", action="store_true", help="仅输出每文件 risk_max / high_risk_frames，不写 suite，用于判断门槛是否过严")
    p.add_argument("--risk-max-min", type=float, default=None, help="覆盖 risk_max_min（默认 0.60）；诊断后若无一通过可试 0.38")
    p.add_argument("--min-high-risk-frames", type=int, default=None, help="覆盖 min_high_risk_frames（默认 30）；可试 10")
    p.add_argument("--clip-pre", type=int, default=None, help="裁剪窗口前向 padding 帧数（覆盖 pre_padding_frames，默认 60）")
    p.add_argument("--clip-post", type=int, default=None, help="裁剪窗口后向 padding 帧数（覆盖 post_padding_frames，默认 60）")
    p.add_argument("--min-consecutive-over", default="0.6:30", help="主产线默认 0.6:30（连续高压）；空串或 --pulse 表示 pulse 素材。格式 thr:frames，如 0.6:60")
    args = p.parse_args()

    sweep_dir = Path(args.sweep_output_dir)
    if not sweep_dir.is_dir():
        sweep_dir = ROOT / args.sweep_output_dir.strip()
    if not sweep_dir.is_dir():
        print("ERROR: sweep_output_dir not found:", args.sweep_output_dir, file=sys.stderr)
        return 2

    out_suite = Path(args.out_suite_dir)
    if not out_suite.is_absolute():
        out_suite = ROOT / args.out_suite_dir.strip()
    ensure_dir(out_suite)

    all_candidates = collect_replay_files(sweep_dir)
    print("[powerclips] found", len(all_candidates), "replay_output.jsonl under", sweep_dir)

    if args.diagnose:
        risk_max_min = POWERCLIP_RULES["risk_max_min"]
        min_hr = POWERCLIP_RULES["min_high_risk_frames"]
        stats_ok = []
        no_risk = 0
        for replay_path in all_candidates:
            s = replay_stats(replay_path)
            if s is None:
                no_risk += 1
                continue
            rm, hr = s
            pass_risk = rm >= risk_max_min
            pass_hr = hr >= min_hr
            stats_ok.append((replay_path, rm, hr, pass_risk and pass_hr))
        for replay_path, rm, hr, ok in sorted(stats_ok, key=lambda x: (-x[1], -x[2]))[:20]:
            print("[diagnose]", replay_path.name, "risk_max=%.4f" % rm, "high_risk_frames=%d" % hr, "PASS" if ok else "FAIL")
        n_pass = sum(1 for _, _, _, ok in stats_ok if ok)
        n_risk_ok = sum(1 for _, rm, _, _ in stats_ok if rm >= risk_max_min)
        n_hr_ok = sum(1 for _, _, hr, _ in stats_ok if hr >= min_hr)
        print("[diagnose] total with risk data:", len(stats_ok), "| no risk (any key):", no_risk)
        print("[diagnose] risk_max >= %.2f:" % risk_max_min, n_risk_ok, "| high_risk_frames >= %d:" % min_hr, n_hr_ok, "| PASS both:", n_pass)
        if no_risk == len(all_candidates) and all_candidates:
            first_path = all_candidates[0]
            recs = load_jsonl(first_path)
            if recs:
                first_rec = recs[0]
                print("[diagnose] 所有 replay 均无风险字段。首条 record 的键（供核对格式）:", sorted(first_rec.keys()))
                dec = first_rec.get("decision")
                if isinstance(dec, dict):
                    print("[diagnose] 首条 record.decision 的键:", sorted(dec.keys()))
            else:
                print("[diagnose] 首文件无有效行")
            print("[diagnose] PowerClips 需 replay 含 risk_used_for_decision 或 decision.a3_debug.ema；来源应为 sim_runner mode=recompute 或含 a3_debug 的 trace。")
        elif n_pass == 0 and len(stats_ok) > 0:
            print("[diagnose] 建议：可尝试 --risk-max-min 0.38 或 --min-high-risk-frames 10 放宽门槛后重跑")
        return 0

    effective_rules = dict(POWERCLIP_RULES)
    if args.risk_max_min is not None:
        effective_rules["risk_max_min"] = args.risk_max_min
        print("[powerclips] override risk_max_min =", args.risk_max_min)
    if args.min_high_risk_frames is not None:
        effective_rules["min_high_risk_frames"] = args.min_high_risk_frames
        print("[powerclips] override min_high_risk_frames =", args.min_high_risk_frames)
    if args.clip_pre is not None:
        effective_rules["pre_padding_frames"] = args.clip_pre
        print("[powerclips] override pre_padding_frames =", args.clip_pre)
    if args.clip_post is not None:
        effective_rules["post_padding_frames"] = args.clip_post
        print("[powerclips] override post_padding_frames =", args.clip_post)
    if (args.min_consecutive_over or "").strip():
        part = args.min_consecutive_over.strip().split(":")
        if len(part) == 2:
            try:
                thr = float(part[0])
                frames = int(part[1])
                effective_rules["min_consecutive_over"] = (thr, frames)
                print("[powerclips] min_consecutive_over: risk>=%s for >=%d consecutive frames" % (thr, frames))
            except (ValueError, TypeError):
                print("WARN: invalid --min-consecutive-over, ignored:", args.min_consecutive_over, file=sys.stderr)
        else:
            print("WARN: --min-consecutive-over format thr:frames (e.g. 0.6:60), ignored:", args.min_consecutive_over, file=sys.stderr)

    source_golden_dir: Optional[Path] = None
    source_episode_ids: Optional[List[str]] = None
    if (args.source_golden_suite_dir or "").strip():
        source_golden_dir = Path(args.source_golden_suite_dir.strip())
        if not source_golden_dir.is_absolute():
            source_golden_dir = ROOT / source_golden_dir
        if source_golden_dir.is_dir():
            source_episode_ids = _source_episode_ids(source_golden_dir)
            print("[powerclips] source-golden-suite-dir:", source_golden_dir, "episodes:", len(source_episode_ids))
        else:
            print("WARN: source-golden-suite-dir not found, clips will use replay rows (recompute will get 0 frames):", source_golden_dir, file=sys.stderr)
            source_golden_dir = None
            source_episode_ids = None

    clips: List[Dict[str, Any]] = []
    for replay_path in all_candidates:
        result = process_single_replay(
            replay_path,
            rules=effective_rules,
            source_golden_dir=source_golden_dir,
            source_episode_ids=source_episode_ids,
        )
        if result:
            clip_id = result["clip_id"]
            clip_dir = out_suite / clip_id
            ensure_dir(clip_dir)
            write_jsonl(clip_dir / "records.jsonl", result.pop("_clip_records"))
            manifest = {k: v for k, v in result.items() if not k.startswith("_")}
            # 保留 source_episode_id 等供审计
            write_json(clip_dir / "manifest.json", manifest)
            clips.append(manifest)
            print("[powerclips]", clip_id, "risk_max=%.4f" % result["risk_max"], "high_risk=%d" % result["high_risk_frames"], "len=%d" % result["clip_len"])
            if len(clips) >= args.max_clips:
                print("[powerclips] reached --max-clips", args.max_clips)
                break

    write_suite_manifest(out_suite, clips, args.suite_name, rules=effective_rules)
    print("[powerclips] wrote", len(clips), "clips to", out_suite)
    print("[powerclips] suite_manifest.json:", out_suite / "suite_manifest.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
