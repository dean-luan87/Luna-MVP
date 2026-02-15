#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2: D1 Tournament 一键跑通。
候选生成 → suite 回放 → Gate（含 guardian_discipline）→ 词典序排名 → 冠军证据包。
双通道时：Stress Gate（军工级）→ 冠军 personality_profile（证据链账本）+ run_manifest（可追溯）。
"""
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
import copy
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]


def _hash_dict(d: Dict[str, Any]) -> str:
    """稳定哈希，供 Determinism 校验（位级一致）。"""
    s = json.dumps(d, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def get_fingerprint_from_run(run_dir: Path, dual_channel: bool = True) -> Dict[str, Any]:
    """
    从已完成的 run 目录读取 rank_report，提取指纹：champion_id, rank_key, stress_summary_hash, regular_summary_hash。
    仅双通道时有效；无冠军时返回空指纹（可比较）。
    """
    run_dir = Path(run_dir)
    rp = run_dir / "rank_report.json"
    if not rp.is_file():
        return {
            "champion_id": None,
            "rank_key": (),
            "stress_summary_hash": "",
            "regular_summary_hash": "",
        }
    data = json.loads(rp.read_text(encoding="utf-8"))
    ranked = data.get("ranked") or []
    if not ranked or not dual_channel:
        return {
            "champion_id": data.get("champion_id"),
            "rank_key": (),
            "stress_summary_hash": "",
            "regular_summary_hash": "",
        }
    champ = ranked[0]
    champion_id = champ.get("patch_id") or data.get("champion_id")
    rank_key_list = champ.get("rank_key")
    rank_key = tuple(rank_key_list) if isinstance(rank_key_list, list) else ()
    stress_sc = champ.get("stress_scorecard") or {}
    regular_metrics = champ.get("regular_metrics") or {}
    stress_summary = {
        "guardian_discipline": stress_sc.get("guardian_discipline"),
        "high_risk_frames_count": stress_sc.get("high_risk_frames_count"),
        "early_gain_mean": stress_sc.get("early_gain_mean"),
        "exit_latency_p95": stress_sc.get("exit_latency_p95"),
        "hysteresis_efficiency": stress_sc.get("hysteresis_efficiency"),
    }
    regular_summary = {
        "guarded_tail_ratio_mean": regular_metrics.get("guarded_tail_ratio_mean"),
        "guarded_tail_ratio": regular_metrics.get("guarded_tail_ratio_mean"),
        "volatility_mean": regular_metrics.get("volatility_mean"),
    }
    return {
        "champion_id": champion_id,
        "rank_key": rank_key,
        "stress_summary_hash": _hash_dict(stress_summary),
        "regular_summary_hash": _hash_dict(regular_summary),
    }


def _run_d1_core(config: Dict[str, Any], run_dir: Path) -> Dict[str, Any]:
    """
    执行一次完整 D1 tournament：候选生成 → suite 回放 → 排名。
    写入 run_dir 下 rank_report.json；返回 report_data（含 ranked/eliminated/champion_id）。
    """
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    base_dir = config["base_dir"]
    version = config["version"]
    golden_suite_rel = config["golden_suite_rel"]
    stress_suite_rel = config["stress_suite_rel"]
    regular_suite_rel = config["regular_suite_rel"]
    dual_channel = config["dual_channel"]
    seed = config["seed"]
    n_candidates = config["n_candidates"]
    stress_base_patch = config.get("stress_base_patch") or {}
    regular_base_patch = config.get("regular_base_patch") or {}
    base_patch = config.get("base_patch") or {}
    mode = config.get("mode") or "replay"

    from simulation.d1.candidate_generator import generate_candidates
    from simulation.d1.lexicographic_ranker import rank_candidates, rank_candidates_dual_channel

    d1_run_id = run_dir.name
    candidates_jsonl, _ = generate_candidates(
        n=n_candidates,
        out_dir=str(run_dir),
        method="lhs",
        seed=seed,
        include_baseline=True,
        d1_run_id=d1_run_id,
        version_tag="d1_v1",
    )
    candidate_results: List[Dict[str, Any]] = []
    patch_schema_violations: List[Dict[str, Any]] = []
    with open(candidates_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            patch_id = row.get("patch_id", "")
            patch_path = row.get("patch_path", "")
            candidate_patch: Dict[str, Any] = {}
            if Path(patch_path).is_file():
                try:
                    candidate_patch = json.loads(Path(patch_path).read_text(encoding="utf-8"))
                except Exception:
                    candidate_patch = {}
            reason = _validate_candidate_patch(candidate_patch)
            if reason is not None:
                patch_schema_violations.append({"patch_id": patch_id, "reason": "L0: PATCH_SCHEMA_VIOLATION", "details": reason})
                continue
            candidate_dir = run_dir / patch_id
            candidate_dir.mkdir(parents=True, exist_ok=True)
            if dual_channel:
                effective_stress = _deep_merge(stress_base_patch, candidate_patch)
                effective_regular = _deep_merge(regular_base_patch, candidate_patch)
                eff_stress_path = candidate_dir / "effective_patch.stress.json"
                eff_regular_path = candidate_dir / "effective_patch.regular.json"
                eff_stress_path.write_text(json.dumps(effective_stress, ensure_ascii=False, indent=2), encoding="utf-8")
                eff_regular_path.write_text(json.dumps(effective_regular, ensure_ascii=False, indent=2), encoding="utf-8")
                report_stress = _run_suite(
                    patch_id, str(eff_stress_path), run_dir, base_dir, version, stress_suite_rel, mode,
                    sim_dir_suffix="_stress", report_dest_basename="suite_report.stress.json",
                )
                report_regular = _run_suite(
                    patch_id, str(eff_regular_path), run_dir, base_dir, version, regular_suite_rel, mode,
                    sim_dir_suffix="_regular", report_dest_basename="suite_report.regular.json",
                )
                candidate_results.append({
                    "patch_id": patch_id,
                    "patch_path": str(run_dir / patch_id / "patch.json") if (run_dir / patch_id / "patch.json").exists() else str(eff_stress_path),
                    "suite_report_path": report_stress or "",
                    "stress_suite_report_path": report_stress or "",
                    "regular_suite_report_path": report_regular or "",
                })
            else:
                effective = _deep_merge(base_patch, candidate_patch)
                effective_path = candidate_dir / "effective_patch.json"
                effective_path.write_text(json.dumps(effective, ensure_ascii=False, indent=2), encoding="utf-8")
                report_path = _run_suite(
                    patch_id, str(effective_path), run_dir, base_dir, version, golden_suite_rel, mode,
                )
                candidate_results.append({
                    "patch_id": patch_id,
                    "patch_path": str(run_dir / patch_id / "patch.json") if (run_dir / patch_id / "patch.json").exists() else str(effective_path),
                    "suite_report_path": report_path or "",
                })

    if dual_channel:
        report_data = rank_candidates_dual_channel(run_dir, candidate_results)
    else:
        report_data = rank_candidates(run_dir, candidate_results)
    if patch_schema_violations:
        report_data["eliminated"] = list(report_data.get("eliminated") or []) + patch_schema_violations
        run_dir.joinpath("rank_report.json").write_text(
            json.dumps(report_data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        md_path = run_dir / "rank_report.md"
        if md_path.is_file():
            lines = md_path.read_text(encoding="utf-8").splitlines()
            for e in patch_schema_violations:
                lines.append("- **%s**: %s" % (e.get("patch_id", ""), e.get("reason", "")))
            md_path.write_text("\n".join(lines), encoding="utf-8")
    return report_data


def run_d1_once(config: Dict[str, Any], run_dir: Path) -> Dict[str, Any]:
    """执行一次完整 D1 tournament，返回指纹。"""
    _run_d1_core(config, run_dir)
    return get_fingerprint_from_run(run_dir, dual_channel=config.get("dual_channel", False))


def run_with_determinism(config: Dict[str, Any], run_dir: Path, repeat: int = 3) -> Dict[str, Any]:
    """连续 repeat 次运行，指纹必须位级一致；否则返回 NON_DETERMINISTIC_EVOLUTION。"""
    runs: List[Dict[str, Any]] = []
    fp0 = get_fingerprint_from_run(run_dir, dual_channel=config.get("dual_channel", False))
    runs.append(fp0)
    for i in range(1, repeat):
        print("[D1] Determinism pass %s/%s" % (i + 1, repeat))
        sub_dir = run_dir / ("determinism_pass_%s" % (i + 1))
        fp = run_d1_once(deepcopy(config), sub_dir)
        runs.append(fp)
    first = runs[0]
    for idx, r in enumerate(runs[1:], start=2):
        if r != first:
            print("[D1] NON_DETERMINISTIC_EVOLUTION detected", file=sys.stderr)
            print("Run 1:", first, file=sys.stderr)
            print("Run %s:" % idx, r, file=sys.stderr)
            return {"status": "NON_DETERMINISTIC_EVOLUTION", "runs": runs}
    print("[D1] Determinism verified across all %s runs" % repeat)
    return {"status": "PASS", "runs": runs}


def write_failure_manifest(run_dir: Path, det_result: Dict[str, Any]) -> None:
    """Determinism 失败时写入证据链，标记本轮进化无效。"""
    run_dir = Path(run_dir)
    try:
        git_out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
            timeout=2,
        )
        git_commit = (git_out.stdout or "").strip() if git_out.returncode == 0 else ""
    except Exception:
        git_commit = ""
    manifest = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "determinism_status": det_result["status"],
        "determinism_runs": [
            {
                "champion_id": r.get("champion_id"),
                "rank_key": list(r.get("rank_key") or []),
                "stress_summary_hash": r.get("stress_summary_hash"),
                "regular_summary_hash": r.get("regular_summary_hash"),
            }
            for r in det_result.get("runs") or []
        ],
        "git_commit": git_commit,
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
    }
    (run_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )


sys.path.insert(0, str(ROOT))

# Candidate 只允许 weights.* 与 metadata 内白名单；禁止 smoothing.*（防 Goodhart）
ALLOWED_CANDIDATE_KEY_PREFIXES = ("weights.",)
ALLOWED_METADATA_KEYS = frozenset({"patch_id", "seed", "tag", "d1_run_id", "version_tag", "patch_kind"})


def _validate_candidate_patch(candidate: Dict[str, Any]) -> Optional[str]:
    """候选 patch 仅允许 weights.* 与 metadata 白名单；禁止 smoothing.*、risk_scale_factor（Presence-Only Contract）。"""
    if not isinstance(candidate, dict):
        return "not_dict"
    for k, v in candidate.items():
        if k == "metadata":
            if not isinstance(v, dict):
                return "metadata_not_dict"
            for mk in (v or {}).keys():
                if mk not in ALLOWED_METADATA_KEYS:
                    return "metadata_disallowed:%s" % mk
            continue
        if k == "risk_scale_factor" or k.startswith("smoothing."):
            return "disallowed_key:%s (physics in base only)" % k
        if not any(k.startswith(prefix) for prefix in ALLOWED_CANDIDATE_KEY_PREFIXES):
            return "disallowed_key:%s" % k
    return None


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """override 覆盖 base 同名字段；metadata 合并时仅保留 base 的物理水印 + override 的白名单键。军工级：深拷贝 base，避免后续任何嵌套修改污染入参。"""
    result = copy.deepcopy(base)
    for k, v in (override or {}).items():
        if k == "metadata":
            base_meta = result.get("metadata") or {}
            override_meta = v if isinstance(v, dict) else {}
            merged_meta = {**base_meta}
            for mk, mv in override_meta.items():
                if mk in ALLOWED_METADATA_KEYS:
                    merged_meta[mk] = mv
            result["metadata"] = merged_meta
            continue
        result[k] = v
    return result


def _effective_patch_smoothing_summary(patch: Dict[str, Any]) -> Dict[str, Any]:
    """从 effective_patch 摘出 smoothing.* 用于诊断。"""
    out = {}
    for k in ("smoothing.peak_hold_frames", "smoothing.peak_decay", "smoothing.alpha_high", "smoothing.alpha_switch_at"):
        if k in patch:
            out[k] = patch[k]
    return out


def _golden_suite_relative(golden_suite: str, base_dir: str = "library_store", version: str = "v1.1") -> str:
    """将 --golden-suite 转为相对 base_dir/version 的路径。"""
    p = golden_suite.strip().strip("/")
    if os.path.isabs(p) or p.startswith(base_dir):
        p = p.replace(base_dir, "").strip("/")
        if p.startswith(version + "/"):
            p = p[len(version) + 1:]
    return p


def _run_suite(
    patch_id: str,
    patch_path: str,
    run_dir: Path,
    base_dir: str,
    version: str,
    golden_suite_rel: str,
    mode: str,
    sim_dir_suffix: str = "",
    report_dest_basename: str = "suite_report.json",
) -> Optional[str]:
    """对单个 patch 跑 run_sim_suite，把 suite_report 归位到 run_dir/<patch_id>/<report_dest_basename>。返回 suite_report 路径。"""
    run_dir.mkdir(parents=True, exist_ok=True)
    candidate_dir = run_dir / patch_id
    candidate_dir.mkdir(parents=True, exist_ok=True)
    sim_out = run_dir / "sim_out"
    sim_dir = str(sim_out / "simulations" / (patch_id + sim_dir_suffix))
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "run_sim_suite.py"),
        "--base-dir", base_dir,
        "--version-tag", version,
        "--patch", patch_path,
        "--out-dir", str(sim_out),
        "--sim-dir", sim_dir,
        "--golden-suite", golden_suite_rel,
        "--mode", mode,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    match = re.search(r"suite_report:\s*(\S+)", proc.stdout or "")
    report_path = match.group(1).strip() if match else None
    if report_path and Path(report_path).is_file():
        if not report_dest_basename.endswith(".json"):
            report_dest_basename = report_dest_basename + ".json"
        dest_patch = candidate_dir / "patch.json"
        shutil.copy2(patch_path, dest_patch)
        report_data = json.loads(Path(report_path).read_text(encoding="utf-8"))
        episodes_dir = candidate_dir / ("episodes" + sim_dir_suffix) if sim_dir_suffix else candidate_dir / "episodes"
        episodes_dir.mkdir(parents=True, exist_ok=True)
        per = report_data.get("per_episode") or {}
        for eid, ep in per.items():
            sc_src = ep.get("scorecard_path")
            gate_src = ep.get("gate_result_path")
            if sc_src and Path(sc_src).is_file():
                sc_dest = episodes_dir / eid / "scorecard.json"
                sc_dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(sc_src, sc_dest)
                ep["scorecard_path"] = str(sc_dest)
            if gate_src and Path(gate_src).is_file():
                gate_dest = episodes_dir / eid / "gate_result.json"
                gate_dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(gate_src, gate_dest)
                ep["gate_result_path"] = str(gate_dest)
        dest_report = candidate_dir / report_dest_basename
        dest_report.write_text(json.dumps(report_data, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(dest_report)
    return None


def _top_informative_episodes(
    suite_report: Dict[str, Any],
    champion_id: str,
    run_dir: Path,
    top_k: int = 3,
) -> List[Tuple[str, str, Optional[str]]]:
    """
    选 top-k 最有信息 episode：优先 divergence_rate 高 / early_gain 大，或 guardian exit_latency p95 接近 6。
    返回 [(episode_id, scorecard_path, gate_result_path), ...]，路径为 run_dir 内或绝对路径。
    """
    per = suite_report.get("per_episode") or {}
    candidates: List[Tuple[float, str, str, Optional[str]]] = []
    for eid, ep in per.items():
        sc_path = ep.get("scorecard_path") or ""
        gate_path = ep.get("gate_result_path") or ""
        if not sc_path:
            continue
        # 信息量得分：divergence/early_gain 高、或 exit_latency_p95 接近 6
        try:
            sc = json.loads(Path(sc_path).read_text(encoding="utf-8"))
        except Exception:
            sc = {}
        early = (sc.get("early") or {}).get("early_gain_weighted") or sc.get("early_conservative_action_gain") or 0
        early = float(early)
        gd = sc.get("guardian_discipline") or {}
        exit_p95 = float(gd.get("exit_latency_p95") or 0)
        # 接近 6 的给高分
        info_score = early * 10
        if exit_p95 > 0:
            info_score += max(0, 10 - abs(6 - exit_p95))
        candidates.append((info_score, eid, sc_path, gate_path))
    candidates.sort(key=lambda x: -x[0])
    return [(eid, sc_path, gate_path) for _, eid, sc_path, gate_path in candidates[:top_k]]


def write_personality_profile(
    run_dir: Path,
    champion_id: str,
    stress_summary: Dict[str, Any],
    regular_summary: Dict[str, Any],
    effective_patch_path: str,
    suite_manifest: Dict[str, Any],
) -> None:
    """
    冠军证据链账本：生成 personality_profile.json 与 personality_profile.md。
    """
    run_dir = Path(run_dir)
    generated_at = datetime.now(timezone.utc).isoformat()
    profile = {
        "generated_at": generated_at,
        "champion_patch_id": champion_id,
        "effective_patch_path": effective_patch_path,
        "stress_channel": {
            "risk_scale_factor": 5.0,
            "guardian_discipline": stress_summary.get("guardian_discipline"),
            "high_risk_frames_count": stress_summary.get("high_risk_frames_count"),
            "early_gain_mean": stress_summary.get("early_gain_mean"),
            "exit_latency_p95": stress_summary.get("exit_latency_p95"),
            "hysteresis_efficiency": stress_summary.get("hysteresis_efficiency"),
        },
        "regular_channel": {
            "risk_scale_factor": 1.0,
            "guarded_tail_ratio": regular_summary.get("guarded_tail_ratio_mean") or regular_summary.get("guarded_tail_ratio"),
            "volatility_mean": regular_summary.get("volatility_mean"),
            "exit_latency_p95": regular_summary.get("exit_latency_p95"),
        },
        "suite_manifest": suite_manifest,
    }
    out_json = run_dir / "personality_profile.json"
    out_md = run_dir / "personality_profile.md"
    out_json.write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8")
    md = f"""
# Luna Champion Personality Profile

## Patch
- **Champion ID**: {champion_id}
- **Effective Patch**: {effective_patch_path}

---

## Stress Channel (risk_scale_factor = 5.0)
- High Risk Frames: {profile["stress_channel"].get("high_risk_frames_count")}
- Early Gain Mean: {profile["stress_channel"].get("early_gain_mean")}
- Exit Latency P95: {profile["stress_channel"].get("exit_latency_p95")}
- Hysteresis Efficiency: {profile["stress_channel"].get("hysteresis_efficiency")}

Guardian Discipline:
```json
{json.dumps(profile["stress_channel"].get("guardian_discipline") or {}, indent=2)}
```

---

## Regular Channel (risk_scale_factor = 1.0)
- Guarded Tail Ratio: {profile["regular_channel"].get("guarded_tail_ratio")}
- Volatility Mean: {profile["regular_channel"].get("volatility_mean")}
- Exit Latency P95: {profile["regular_channel"].get("exit_latency_p95")}

---

## Suite Manifest
```json
{json.dumps(suite_manifest, indent=2)}
```
"""
    out_md.write_text(md.strip(), encoding="utf-8")


def write_run_manifest(
    run_dir: Path,
    *,
    seed: int,
    stress_suite_hash: str = "",
    regular_suite_hash: str = "",
    base_patch_hash: str = "",
    git_commit: str = "",
    det_result: Optional[Dict[str, Any]] = None,
) -> None:
    """写入 run_manifest.json，便于冠军人格可追溯；含 determinism 时追加 determinism_status / determinism_runs。"""
    run_dir = Path(run_dir)
    manifest: Dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit,
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "seed": seed,
        "stress_suite_hash": stress_suite_hash,
        "regular_suite_hash": regular_suite_hash,
        "base_patch_hash": base_patch_hash,
    }
    if det_result is not None:
        manifest["determinism_status"] = det_result.get("status", "")
        manifest["determinism_runs"] = [
            {
                "champion_id": r.get("champion_id"),
                "rank_key": list(r.get("rank_key") or []),
                "stress_summary_hash": r.get("stress_summary_hash"),
                "regular_summary_hash": r.get("regular_summary_hash"),
            }
            for r in det_result.get("runs") or []
        ]
    (run_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="D1 Tournament Phase 2: candidates → suite → gate → lexicographic rank → champion bundle")
    p.add_argument("--golden-suite", default="", help="Golden suite path; use library_store/v1.1/golden_stress_v2_powerclips + base-patch for non-zero early_gain")
    p.add_argument("--base-dir", default="library_store")
    p.add_argument("--version-tag", default="v1.1")
    p.add_argument("--n-candidates", type=int, default=25, help="LHS sample size (fixed baseline/aggressive/conservative always included)")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--out-dir", default="outputs/d1_runs", help="Output root; timestamped subdir will be created unless --no-ts")
    p.add_argument("--no-ts", action="store_true", help="Do not add timestamp subdir; use out-dir as run_dir")
    p.add_argument("--write-debug-trace", action="store_true", help="For champion, write debug trace for top episodes")
    p.add_argument("--mode", choices=["replay", "recompute"], default="replay")
    p.add_argument("--base-patch", default="", help="Base physics patch (e.g. patches/physics/stress_v2_phys_v1.json); required with golden_stress_v2_powerclips for early_gain")
    p.add_argument("--dual-channel", action="store_true", help="Run Stress + Regular channels; rank by L0 Stress Gate then L1/L2/L3")
    p.add_argument("--stress-suite", default="", help="Stress channel suite (default=--golden-suite)")
    p.add_argument("--regular-suite", default="", help="Regular channel suite (default=--golden-suite)")
    p.add_argument("--stress-base-patch", default="patches/physics/stress_channel_phys_v1.json")
    p.add_argument("--regular-base-patch", default="patches/physics/regular_channel_phys_v1.json")
    p.add_argument("--determinism-check", type=int, default=1, help="Repeat N runs and require bit-identical champion; default 1 (no check)")
    args = p.parse_args()

    base_dir = args.base_dir.rstrip("/")
    version = args.version_tag
    golden_suite_arg = (args.golden_suite or "").strip()
    if not golden_suite_arg:
        golden_suite_rel = "golden_stress_v2"
    else:
        golden_suite_rel = _golden_suite_relative(golden_suite_arg, base_dir, version)

    suite_full = ROOT / base_dir / version / golden_suite_rel.replace("\\", "/").strip("/")
    if not suite_full.is_dir():
        print("[D1] ERROR: golden-suite dir not found:", suite_full, file=sys.stderr)
        if "powerclips" in golden_suite_arg:
            print("[D1] Build powerclips first: python3 tools/build_powerclips_golden.py --stress-dir library_store/v1.1/golden_stress_v2 --out-suite library_store/v1.1/golden_stress_v2_powerclips", file=sys.stderr)
            print("[D1] Or run with existing suite: --golden-suite library_store/v1.1/golden_stress_v2 (early_gain may stay 0)", file=sys.stderr)
        return 2

    dual_channel = getattr(args, "dual_channel", False)  # --dual-channel
    stress_suite_rel = _golden_suite_relative((args.stress_suite or args.golden_suite or "").strip() or "golden_stress_v2", base_dir, version) if dual_channel else golden_suite_rel
    regular_suite_rel = _golden_suite_relative((args.regular_suite or args.golden_suite or "").strip() or "golden_stress_v2", base_dir, version) if dual_channel else golden_suite_rel
    if dual_channel:
        for name, rel in [("stress", stress_suite_rel), ("regular", regular_suite_rel)]:
            full = ROOT / base_dir / version / rel.replace("\\", "/").strip("/")
            if not full.is_dir():
                print("[D1] ERROR: %s-suite dir not found: %s" % (name, full), file=sys.stderr)
                return 2

    out_root = Path(args.out_dir).resolve()
    if args.no_ts:
        run_dir = out_root
    else:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        run_dir = out_root / ts
    run_dir.mkdir(parents=True, exist_ok=True)

    base_patch: Dict[str, Any] = {}
    stress_base_patch: Dict[str, Any] = {}
    regular_base_patch: Dict[str, Any] = {}
    if dual_channel:
        for attr, key in [("stress_base_patch", "stress_base_patch"), ("regular_base_patch", "regular_base_patch")]:
            path = getattr(args, attr, "")
            if path:
                p = Path(path.strip())
                if not p.is_absolute():
                    p = ROOT / p
                if p.is_file():
                    if key == "stress_base_patch":
                        stress_base_patch = json.loads(p.read_text(encoding="utf-8"))
                        print("[D1] stress_base_patch loaded:", str(p), "keys:", list(stress_base_patch.keys()))
                    else:
                        regular_base_patch = json.loads(p.read_text(encoding="utf-8"))
                        print("[D1] regular_base_patch loaded:", str(p), "keys:", list(regular_base_patch.keys()))
                else:
                    print("[D1] WARN: %s file not found: %s" % (attr, p), file=sys.stderr)
        base_patch = stress_base_patch
    elif (args.base_patch or "").strip():
        base_path = Path(args.base_patch.strip())
        if not base_path.is_absolute():
            base_path = ROOT / base_path
        if base_path.is_file():
            base_patch = json.loads(base_path.read_text(encoding="utf-8"))
            print("[D1] base_patch loaded:", str(base_path), "keys:", list(base_patch.keys()))
        else:
            print("[D1] WARN: base-patch file not found:", base_path, file=sys.stderr)

    config: Dict[str, Any] = {
        "base_dir": base_dir,
        "version": version,
        "golden_suite_rel": golden_suite_rel,
        "stress_suite_rel": stress_suite_rel,
        "regular_suite_rel": regular_suite_rel,
        "dual_channel": dual_channel,
        "seed": args.seed,
        "n_candidates": args.n_candidates,
        "stress_base_patch": stress_base_patch,
        "regular_base_patch": regular_base_patch,
        "base_patch": base_patch,
        "mode": args.mode,
    }

    # 1) 生成候选
    from simulation.d1.candidate_generator import generate_candidates
    d1_run_id = run_dir.name
    candidates_jsonl, patch_paths = generate_candidates(
        n=args.n_candidates,
        out_dir=str(run_dir),
        method="lhs",
        seed=args.seed,
        include_baseline=True,
        d1_run_id=d1_run_id,
        version_tag="d1_v1",
    )
    print("[D1] candidates:", candidates_jsonl)

    # 2) 对每个候选：校验 allowlist → effective = merge(base, candidate) → 写 effective_patch.json → 跑 suite
    candidate_results: List[Dict[str, Any]] = []
    patch_schema_violations: List[Dict[str, Any]] = []
    with open(candidates_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            patch_id = row.get("patch_id", "")
            patch_path = row.get("patch_path", "")
            candidate_patch: Dict[str, Any] = {}
            if Path(patch_path).is_file():
                try:
                    candidate_patch = json.loads(Path(patch_path).read_text(encoding="utf-8"))
                except Exception:
                    candidate_patch = {}
            reason = _validate_candidate_patch(candidate_patch)
            if reason is not None:
                patch_schema_violations.append({"patch_id": patch_id, "reason": "L0: PATCH_SCHEMA_VIOLATION", "details": reason})
                print("[D1] PATCH_SCHEMA_VIOLATION", patch_id, reason, file=sys.stderr)
                continue
            candidate_dir = run_dir / patch_id
            candidate_dir.mkdir(parents=True, exist_ok=True)
            if dual_channel:
                effective_stress = _deep_merge(stress_base_patch, candidate_patch)
                effective_regular = _deep_merge(regular_base_patch, candidate_patch)
                eff_stress_path = candidate_dir / "effective_patch.stress.json"
                eff_regular_path = candidate_dir / "effective_patch.regular.json"
                eff_stress_path.write_text(json.dumps(effective_stress, ensure_ascii=False, indent=2), encoding="utf-8")
                eff_regular_path.write_text(json.dumps(effective_regular, ensure_ascii=False, indent=2), encoding="utf-8")
                report_stress = _run_suite(
                    patch_id, str(eff_stress_path), run_dir, base_dir, version, stress_suite_rel, args.mode,
                    sim_dir_suffix="_stress", report_dest_basename="suite_report.stress.json",
                )
                report_regular = _run_suite(
                    patch_id, str(eff_regular_path), run_dir, base_dir, version, regular_suite_rel, args.mode,
                    sim_dir_suffix="_regular", report_dest_basename="suite_report.regular.json",
                )
                candidate_results.append({
                    "patch_id": patch_id,
                    "patch_path": str(run_dir / patch_id / "patch.json") if (run_dir / patch_id / "patch.json").exists() else str(eff_stress_path),
                    "suite_report_path": report_stress or "",
                    "stress_suite_report_path": report_stress or "",
                    "regular_suite_report_path": report_regular or "",
                })
                if not report_stress:
                    print("[D1] WARN: no stress suite_report for %s" % patch_id, file=sys.stderr)
                if not report_regular:
                    print("[D1] WARN: no regular suite_report for %s" % patch_id, file=sys.stderr)
            else:
                effective = _deep_merge(base_patch, candidate_patch)
                effective_path = candidate_dir / "effective_patch.json"
                effective_path.write_text(json.dumps(effective, ensure_ascii=False, indent=2), encoding="utf-8")
                report_path = _run_suite(
                    patch_id, str(effective_path), run_dir, base_dir, version, golden_suite_rel, args.mode,
                )
                candidate_results.append({
                    "patch_id": patch_id,
                    "patch_path": str(run_dir / patch_id / "patch.json") if (run_dir / patch_id / "patch.json").exists() else str(effective_path),
                    "suite_report_path": report_path or "",
                })
                if not report_path:
                    print(f"[D1] WARN: no suite_report for {patch_id}", file=sys.stderr)

    # 3) 词典序排名
    from simulation.d1.lexicographic_ranker import rank_candidates, rank_candidates_dual_channel
    if dual_channel:
        report_data = rank_candidates_dual_channel(run_dir, candidate_results)
    else:
        report_data = rank_candidates(run_dir, candidate_results)
    if patch_schema_violations:
        report_data["eliminated"] = list(report_data.get("eliminated") or []) + patch_schema_violations
        run_dir.joinpath("rank_report.json").write_text(
            json.dumps(report_data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        md_path = run_dir / "rank_report.md"
        if md_path.is_file():
            lines = md_path.read_text(encoding="utf-8").splitlines()
            for e in patch_schema_violations:
                lines.append("- **%s**: %s" % (e.get("patch_id", ""), e.get("reason", "")))
            md_path.write_text("\n".join(lines), encoding="utf-8")
    champion_id = report_data.get("champion_id")
    print("[D1] Champion:", champion_id)
    print("[D1] rank_report:", str(run_dir / "rank_report.json"))
    print("[D1] rank_report_md:", str(run_dir / "rank_report.md"))
    ranked = report_data.get("ranked") or []
    det_result: Optional[Dict[str, Any]] = None
    if dual_channel and report_data.get("channels"):
        ch_stress = report_data["channels"].get("stress") or {}
        print("[D1] stress: high_risk_frames_total=%s patch_count=%s" % (ch_stress.get("high_risk_frames_total"), ch_stress.get("patch_count")))
        if ranked:
            rm = ranked[0].get("regular_metrics") or {}
            print("[D1] regular (champion): guarded_ratio_delta_mean=%s volatility_mean=%s" % (rm.get("guarded_ratio_delta_mean"), rm.get("volatility_mean")))
        # Determinism Enforcement：同一输入连续 N 次冠军必须位级一致
        if getattr(args, "determinism_check", 1) > 1:
            det_result = run_with_determinism(config, run_dir, repeat=args.determinism_check)
            if det_result["status"] != "PASS":
                write_failure_manifest(run_dir, det_result)
                print("[D1] NON_DETERMINISTIC_EVOLUTION: 本轮进化无效，未产出冠军人格档案", file=sys.stderr)
                return 1
        # 军工级可追溯：run_manifest.json
        try:
            git_out = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
                timeout=2,
            )
            git_commit = (git_out.stdout or "").strip() if git_out.returncode == 0 else ""
        except Exception:
            git_commit = ""
        stress_suite_hash = ""
        regular_suite_hash = ""
        base_patch_hash = ""
        if champion_id:
            stress_report_path = run_dir / champion_id / "suite_report.stress.json"
            regular_report_path = run_dir / champion_id / "suite_report.regular.json"
            for p, name in [(stress_report_path, "stress"), (regular_report_path, "regular")]:
                if p.is_file():
                    data = json.loads(p.read_text(encoding="utf-8"))
                    ep_ids = sorted((data.get("per_episode") or {}).keys())
                    h = hashlib.sha256(json.dumps(ep_ids).encode()).hexdigest()[:16]
                    if name == "stress":
                        stress_suite_hash = h
                    else:
                        regular_suite_hash = h
            base_path = getattr(args, "stress_base_patch", "") or ""
            if base_path and Path(base_path).is_file():
                base_path = str(ROOT / base_path) if not Path(base_path).is_absolute() else base_path
                base_patch_hash = hashlib.sha256(Path(base_path).read_bytes()).hexdigest()[:16]
        write_run_manifest(
            run_dir,
            seed=args.seed,
            stress_suite_hash=stress_suite_hash,
            regular_suite_hash=regular_suite_hash,
            base_patch_hash=base_patch_hash,
            git_commit=git_commit,
            det_result=det_result if getattr(args, "determinism_check", 1) > 1 else None,
        )
        # 冠军 personality_profile（证据链账本，仅 determinism PASS 或未校验时写入）
        if champion_id and ranked:
            champ = ranked[0]
            stress_sc = champ.get("stress_scorecard") or {}
            stress_metrics = champ.get("stress_metrics") or {}
            regular_metrics = champ.get("regular_metrics") or {}
            stress_summary = {
                "guardian_discipline": stress_sc.get("guardian_discipline"),
                "high_risk_frames_count": stress_sc.get("high_risk_frames_count"),
                "early_gain_mean": stress_sc.get("early_gain_mean") or stress_metrics.get("early_gain_weighted_mean"),
                "exit_latency_p95": stress_sc.get("exit_latency_p95"),
                "hysteresis_efficiency": stress_sc.get("hysteresis_efficiency"),
            }
            regular_summary = {
                "guarded_tail_ratio_mean": regular_metrics.get("guarded_tail_ratio_mean"),
                "guarded_tail_ratio": regular_metrics.get("guarded_tail_ratio_mean"),
                "volatility_mean": regular_metrics.get("volatility_mean"),
                "exit_latency_p95": None,
            }
            eff_path = run_dir / champion_id / "effective_patch.stress.json"
            effective_patch_path = str(eff_path) if eff_path.is_file() else str(run_dir / champion_id / "effective_patch.stress.json")
            suite_manifest: Dict[str, Any] = {"seed": args.seed, "episode_ids": []}
            if (run_dir / champion_id / "suite_report.stress.json").is_file():
                sr = json.loads((run_dir / champion_id / "suite_report.stress.json").read_text(encoding="utf-8"))
                suite_manifest["episode_ids"] = sorted((sr.get("per_episode") or {}).keys())
                suite_manifest["suite_id"] = sr.get("suite_id")
            try:
                git_out = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=str(ROOT), timeout=2)
                suite_manifest["git_commit"] = (git_out.stdout or "").strip() if git_out.returncode == 0 else ""
            except Exception:
                suite_manifest["git_commit"] = ""
            write_personality_profile(
                run_dir,
                champion_id,
                stress_summary,
                regular_summary,
                effective_patch_path,
                suite_manifest,
            )
            print("[D1] personality_profile:", str(run_dir / "personality_profile.json"), str(run_dir / "personality_profile.md"))
    # 早期增益诊断（防全 0 真空）
    if ranked:
        agg = ranked[0].get("aggregated") or {}
        print("[D1] early_gain_mean:", agg.get("early_gain_weighted_mean"))
    if champion_id:
        suite_report_path = run_dir / champion_id / ("suite_report.stress.json" if dual_channel else "suite_report.json")
        if suite_report_path.is_file():
            per = (json.loads(suite_report_path.read_text(encoding="utf-8")) or {}).get("per_episode") or {}
            for eid in sorted(per.keys())[:1]:
                sc_path = (per.get(eid) or {}).get("scorecard_path")
                if sc_path and Path(sc_path).is_file():
                    sc = json.loads(Path(sc_path).read_text(encoding="utf-8"))
                    early = sc.get("early") or {}
                    n_hr = early.get("high_risk_seq_count", 0)
                    risk_max = early.get("risk_used_for_decision_max")
                    th = early.get("threshold_safe_to_caution")
                    b_hr = early.get("baseline_first_guarded_in_high_risk")
                    c_hr = early.get("candidate_first_guarded_in_high_risk")
                    print("[D1] early_gain_diagnostics (sample ep): high_risk_frames_count=%s risk_used_max=%s threshold_safe_to_caution=%s first_guarded_baseline=%s first_guarded_candidate=%s" % (n_hr, risk_max, th, b_hr, c_hr))
                    rj = run_dir / "rank_report.json"
                    diag = {
                        "high_risk_frames_count": n_hr,
                        "risk_used_for_decision_max": risk_max,
                        "threshold_safe_to_caution": th,
                        "first_guarded_baseline": b_hr,
                        "first_guarded_candidate": c_hr,
                        "early_gain_mean": (ranked[0].get("aggregated") or {}).get("early_gain_weighted_mean") if ranked else None,
                    }
                    eff_path = run_dir / champion_id / ("effective_patch.stress.json" if dual_channel else "effective_patch.json")
                    if eff_path.is_file():
                        eff = json.loads(eff_path.read_text(encoding="utf-8"))
                        smooth = _effective_patch_smoothing_summary(eff)
                        diag["effective_patch_smoothing"] = smooth
                        print("[D1] effective_patch_smoothing:", smooth)
                    if rj.is_file():
                        data = json.loads(rj.read_text(encoding="utf-8"))
                        data["early_gain_diagnostics"] = diag
                        rj.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                    break

    # 4) 冠军证据包
    champion_bundle_dir = run_dir / "champion_bundle"
    champion_bundle_dir.mkdir(parents=True, exist_ok=True)
    if champion_id:
        champion_patch_src = run_dir / champion_id / "patch.json"
        if champion_patch_src.is_file():
            shutil.copy2(champion_patch_src, champion_bundle_dir / "champion_patch.json")
        suite_report_path = run_dir / champion_id / ("suite_report.stress.json" if dual_channel else "suite_report.json")
        if suite_report_path.is_file():
            suite_report = json.loads(suite_report_path.read_text(encoding="utf-8"))
            for eid, sc_path, gate_path in _top_informative_episodes(suite_report, champion_id, run_dir, top_k=3):
                name = Path(sc_path).name.replace(".json", "")
                if Path(sc_path).is_file():
                    shutil.copy2(sc_path, champion_bundle_dir / f"ep_{eid}_scorecard.json")
                if gate_path and Path(gate_path).is_file():
                    shutil.copy2(gate_path, champion_bundle_dir / f"ep_{eid}_gate_result.json")

    print("[D1] champion_bundle:", champion_bundle_dir)
    print("[D1] 查看冠军与解释: cat", str(run_dir / "rank_report.md"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
