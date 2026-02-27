# -*- coding: utf-8 -*-
"""
D1 候选生成：仅 weights.* 的受控采样（LHS / 随机），含基线 empty_patch。
Phase 2：固定对照组 baseline / aggressive / conservative + LHS（numpy 自实现），metadata 必带。
"""
import json
import os
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from simulation.d1.weights_schema import D1_WEIGHTS_BOUNDS, D1_WEIGHTS_DEFAULTS, D1_WEIGHTS_KEYS

# risk 相关关键权重（用于 aggressive/conservative）
RISK_WEIGHT_KEYS = [
    "weights.risk_density",
    "weights.redline_hit",
    "weights.occlusion_ratio",
    "weights.path_instability",
    "weights.motion_instability",
]


def _clamp(k: str, v: float) -> float:
    lo, hi = D1_WEIGHTS_BOUNDS[k]
    return round(max(lo, min(hi, v)), 4)


def generate_random_patch(seed: Optional[int] = None) -> Dict[str, float]:
    """在 D1_WEIGHTS_BOUNDS 内均匀采样，只生成 weights.* 键。"""
    rng = random.Random(seed)
    out: Dict[str, float] = {}
    for k in D1_WEIGHTS_KEYS:
        lo, hi = D1_WEIGHTS_BOUNDS[k]
        out[k] = round(rng.uniform(lo, hi), 4)
    return out


def _lhs_pure(n: int, d: int, rng: random.Random) -> List[List[float]]:
    """纯 Python LHS：n 样本，d 维，每维在 [0,1] 内分层且每层恰好一个点。"""
    u: List[List[float]] = [[0.0] * d for _ in range(n)]
    for j in range(d):
        perm = list(range(n))
        rng.shuffle(perm)
        for i in range(n):
            low = perm[i] / n
            high = (perm[i] + 1) / n
            u[i][j] = rng.uniform(low, high)
    return u


def generate_lhs_patches(n: int, seed: Optional[int] = None) -> List[Dict[str, float]]:
    """
    拉丁超立方采样 n 组 weights（每维分层）。纯 Python 实现，无额外依赖。
    """
    rng = random.Random(seed)
    d = len(D1_WEIGHTS_KEYS)
    u = _lhs_pure(n, d, rng)
    out: List[Dict[str, float]] = []
    for i in range(n):
        patch: Dict[str, float] = {}
        for j, k in enumerate(D1_WEIGHTS_KEYS):
            lo, hi = D1_WEIGHTS_BOUNDS[k]
            patch[k] = round(lo + (hi - lo) * u[i][j], 4)
        out.append(patch)
    return out


def _patch_with_metadata(
    payload: Dict[str, Any],
    d1_run_id: str,
    version_tag: str = "d1_v1",
    bucket: Optional[str] = None,
) -> Dict[str, Any]:
    """为 patch 加上 metadata（patch_kind, d1_run_id, version_tag；可选 bucket 供审计）。payload 内 metadata 会合并（如 phase3_convergent 的 sampler/bucket）。"""
    meta: Dict[str, Any] = {
        "patch_kind": "weights_only",
        "d1_run_id": d1_run_id,
        "version_tag": version_tag,
    }
    if bucket:
        meta["bucket"] = bucket
    payload_meta = (payload.get("metadata") or {})
    for k in ("bucket", "sampler", "converge_alpha", "converge_peak_decay", "converge_peak_hold_frames"):
        if k in payload_meta:
            meta[k] = payload_meta[k]
    return {"metadata": meta, **{k: v for k, v in payload.items() if k != "metadata"}}


def _aggressive_bounds() -> Dict[str, Tuple[float, float]]:
    """Aggressive 桶：风险相关权重的上界上浮 20%（cap 1.0），便于触到 Guarded 边界。"""
    out: Dict[str, Tuple[float, float]] = {}
    for k, (lo, hi) in D1_WEIGHTS_BOUNDS.items():
        if k in RISK_WEIGHT_KEYS:
            out[k] = (lo, min(1.0, round(hi * 1.2, 4)))
        else:
            out[k] = (lo, hi)
    return out


def generate_lhs_patches_aggressive(n: int, seed: Optional[int] = None) -> List[Dict[str, float]]:
    """LHS 采样，但使用 aggressive 上界（风险键上浮 20%，cap=1.0），用于扩大权重搜索边界。"""
    rng = random.Random(seed)
    d = len(D1_WEIGHTS_KEYS)
    u = _lhs_pure(n, d, rng)
    bounds = _aggressive_bounds()
    out: List[Dict[str, float]] = []
    for i in range(n):
        patch: Dict[str, float] = {}
        for j, k in enumerate(D1_WEIGHTS_KEYS):
            lo, hi = bounds[k]
            patch[k] = round(lo + (hi - lo) * u[i][j], 4)
        out.append(patch)
    return out


# Hyper 桶上界：RISK_WEIGHT_KEYS 允许略超 1.0，便于结构性变异；须过 conservative sustain gate
HYPER_CAP_DEFAULT = 1.4


def _hyper_bounds(cap: float = HYPER_CAP_DEFAULT) -> Dict[str, Tuple[float, float]]:
    """Hyper 桶：仅 RISK_WEIGHT_KEYS 上界允许 >1.0（默认 cap=1.4），便于越界育种。"""
    out: Dict[str, Tuple[float, float]] = {}
    for k, (lo, hi) in D1_WEIGHTS_BOUNDS.items():
        if k in RISK_WEIGHT_KEYS:
            out[k] = (lo, min(cap, round(hi * 1.5, 4)))
        else:
            out[k] = (lo, hi)
    return out


def generate_lhs_patches_hyper(n: int, seed: Optional[int] = None, cap: float = HYPER_CAP_DEFAULT) -> List[Dict[str, float]]:
    """LHS 采样，使用 hyper 上界（风险键 cap>1.0），用于“越界一小步”育种。"""
    rng = random.Random(seed)
    d = len(D1_WEIGHTS_KEYS)
    u = _lhs_pure(n, d, rng)
    bounds = _hyper_bounds(cap=cap)
    out: List[Dict[str, float]] = []
    for i in range(n):
        patch: Dict[str, float] = {}
        for j, k in enumerate(D1_WEIGHTS_KEYS):
            lo, hi = bounds[k]
            patch[k] = round(lo + (hi - lo) * u[i][j], 4)
        out.append(patch)
    return out


# stress_responsive 专属：smoothing 搜索范围（Phase 3 Step A+B）
RESPONSIVE_ALPHA_RANGE = (0.55, 0.70)
RESPONSIVE_PEAK_HOLD_RANGE = (3, 8)   # 整数帧，峰值记忆拉长以便 EMA 提前抬升
RESPONSIVE_PEAK_DECAY_RANGE = (0.88, 0.98)

# Phase3 convergent sampler 默认参数（PHASE3_CONVERGENT_SAMPLER_v1）
CONVERGE_DEFAULTS = {
    "exploit_ratio": 0.7,
    "alpha_mean": 0.635, "alpha_std": 0.02, "alpha_min": 0.60, "alpha_max": 0.68,
    "decay_mean": 0.895, "decay_std": 0.01, "decay_min": 0.88, "decay_max": 0.92,
    "explore_alpha_min": 0.58, "explore_alpha_max": 0.72,
    "explore_decay_min": 0.87, "explore_decay_max": 0.93,
    "peak_hold_fixed": 3,
}


def _truncated_normal(rng: random.Random, mu: float, sigma: float, lo: float, hi: float, max_tries: int = 100) -> float:
    """截断高斯采样：拒绝采样直到落在 [lo, hi] 内。"""
    for _ in range(max_tries):
        x = rng.gauss(mu, sigma)
        if lo <= x <= hi:
            return round(x, 4)
    return round(max(lo, min(hi, mu)), 4)


def generate_candidates(
    n: int,
    out_dir: str,
    method: str = "lhs",
    seed: Optional[int] = None,
    include_baseline: bool = True,
    d1_run_id: Optional[str] = None,
    version_tag: str = "d1_v1",
    include_responsive_alpha: bool = True,
    phase3_mode: str = "lhs",
    converge_exploit_ratio: float = 0.7,
    converge_alpha_mean: float = 0.635,
    converge_alpha_std: float = 0.02,
    converge_alpha_min: float = 0.60,
    converge_alpha_max: float = 0.68,
    converge_decay_mean: float = 0.895,
    converge_decay_std: float = 0.01,
    converge_decay_min: float = 0.88,
    converge_decay_max: float = 0.92,
    converge_explore_alpha_min: float = 0.58,
    converge_explore_alpha_max: float = 0.72,
    converge_explore_decay_min: float = 0.87,
    converge_explore_decay_max: float = 0.93,
    converge_peak_hold_fixed: int = 3,
) -> tuple:
    """
    生成 n 个候选 patch（JSON 文件）到 out_dir/candidates/*.json 并写 candidates.jsonl。
    固定对照组：baseline（empty）、aggressive、conservative；其余为 LHS。
    include_responsive_alpha=True 时，非 baseline 候选增加 stress_responsive 专属 smoothing：
    alpha ∈ [0.55, 0.70]，peak_hold_frames ∈ [3, 8]，peak_decay ∈ [0.88, 0.98]（仅 responsive 生效）。
    返回 (candidates_jsonl_path, list of patch_paths)。
    """
    os.makedirs(out_dir, exist_ok=True)
    candidates_dir = Path(out_dir) / "candidates"
    candidates_dir.mkdir(parents=True, exist_ok=True)
    out_path = Path(out_dir)
    rng = random.Random(seed)
    run_id = d1_run_id or "run"
    patch_paths: List[str] = []
    rows: List[Dict[str, Any]] = []
    converge_stats: List[Dict[str, Any]] = []  # 用于 sampling_plan.json

    use_convergent = (phase3_mode == "convergent" and include_responsive_alpha)

    def _add_responsive_smoothing(payload: Dict[str, Any], weight_bucket: Optional[str] = None) -> Dict[str, Any]:
        if not include_responsive_alpha:
            return payload
        if use_convergent:
            return _add_convergent_smoothing(payload, weight_bucket)
        out = dict(payload)
        lo_a, hi_a = RESPONSIVE_ALPHA_RANGE
        out["smoothing.alpha"] = round(rng.uniform(lo_a, hi_a), 4)
        lo_h, hi_h = RESPONSIVE_PEAK_HOLD_RANGE
        out["smoothing.peak_hold_frames"] = rng.randint(lo_h, hi_h)
        lo_d, hi_d = RESPONSIVE_PEAK_DECAY_RANGE
        out["smoothing.peak_decay"] = round(rng.uniform(lo_d, hi_d), 4)
        return out

    def _add_convergent_smoothing(payload: Dict[str, Any], weight_bucket: Optional[str] = None) -> Dict[str, Any]:
        out = dict(payload)
        out["smoothing.peak_hold_frames"] = converge_peak_hold_fixed
        if rng.random() < converge_exploit_ratio:
            bucket = "exploit"
            alpha = _truncated_normal(rng, converge_alpha_mean, converge_alpha_std, converge_alpha_min, converge_alpha_max)
            decay = _truncated_normal(rng, converge_decay_mean, converge_decay_std, converge_decay_min, converge_decay_max)
        else:
            bucket = "explore"
            alpha = round(rng.uniform(converge_explore_alpha_min, converge_explore_alpha_max), 4)
            decay = round(rng.uniform(converge_explore_decay_min, converge_explore_decay_max), 4)
        out["smoothing.alpha"] = alpha
        out["smoothing.peak_decay"] = decay
        converge_stats.append({"alpha": alpha, "peak_decay": decay, "bucket": bucket})
        meta = out.get("metadata") or {}
        meta["bucket"] = bucket
        meta["sampler"] = "phase3_convergent_v1"
        meta["converge_alpha"] = alpha
        meta["converge_peak_decay"] = decay
        meta["converge_peak_hold_frames"] = converge_peak_hold_fixed
        out["metadata"] = meta
        return out

    def write_patch(patch_id: str, data: Dict[str, Any]) -> None:
        fp = candidates_dir / f"{patch_id}.json"
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        patch_paths.append(str(fp.resolve()))
        rows.append({"patch_id": patch_id, "patch_path": str(fp.resolve())})

    # 1) baseline（empty，不搜 alpha）
    if include_baseline:
        baseline_data = _patch_with_metadata({}, run_id, version_tag)
        write_patch("baseline", baseline_data)

    # 2) aggressive：risk 相关权重 *2，clamp；可选 smoothing.alpha
    agg: Dict[str, Any] = {}
    for k in D1_WEIGHTS_KEYS:
        v = D1_WEIGHTS_DEFAULTS[k]
        if k in RISK_WEIGHT_KEYS:
            v = _clamp(k, v * 2.0)
        else:
            v = _clamp(k, v)
        agg[k] = v
    write_patch("aggressive", _patch_with_metadata(_add_responsive_smoothing(agg), run_id, version_tag))

    # 3) conservative：risk 相关 *0.7，clamp；可选 responsive smoothing（仅 responsive 合并时生效）
    cons: Dict[str, Any] = {}
    for k in D1_WEIGHTS_KEYS:
        v = D1_WEIGHTS_DEFAULTS[k]
        if k in RISK_WEIGHT_KEYS:
            v = _clamp(k, v * 0.7)
        else:
            v = _clamp(k, v)
        cons[k] = v
    write_patch("conservative", _patch_with_metadata(_add_responsive_smoothing(cons), run_id, version_tag))

    # 4) LHS 采样（n - 固定组数量）：60% standard，30% aggressive（cap=1.0），10% hyper（cap=1.3，越界育种）
    fixed_count = (1 if include_baseline else 0) + 2  # baseline + agg + cons
    num_sampled = max(0, n - fixed_count)
    if method == "lhs":
        num_standard = int(num_sampled * 0.6)
        num_aggressive = int(num_sampled * 0.3)
        num_hyper = num_sampled - num_standard - num_aggressive
        patches_std = generate_lhs_patches(num_standard, seed=seed)
        patches_agg = generate_lhs_patches_aggressive(num_aggressive, seed=(seed or 0) + 999)
        patches_hyper = generate_lhs_patches_hyper(num_hyper, seed=(seed or 0) + 1999, cap=HYPER_CAP_DEFAULT)
        patches = patches_std + patches_agg + patches_hyper
    else:
        patches = [generate_random_patch(seed=rng.randint(0, 2**31 - 1)) for _ in range(num_sampled)]

    num_standard = int(num_sampled * 0.6) if method == "lhs" and num_sampled else num_sampled
    num_aggressive = int(num_sampled * 0.3) if method == "lhs" and num_sampled else 0
    for i, p in enumerate(patches):
        pid = f"d1_candidate_{i:03d}"
        if method == "lhs":
            if i < num_standard:
                bucket = None
            elif i < num_standard + num_aggressive:
                bucket = "aggressive"
            else:
                bucket = "hyper"
        else:
            bucket = None
        p_with_smoothing = _add_responsive_smoothing(dict(p))
        write_patch(pid, _patch_with_metadata(p_with_smoothing, run_id, version_tag, bucket=bucket))

    candidates_jsonl = out_path / "candidates.jsonl"
    with open(candidates_jsonl, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    if use_convergent and converge_stats:
        alphas = [s["alpha"] for s in converge_stats]
        decays = [s["peak_decay"] for s in converge_stats]
        buckets = [s["bucket"] for s in converge_stats]
        sampling_plan = {
            "sampler": "phase3_convergent_v1",
            "exploit_ratio": converge_exploit_ratio,
            "peak_hold_fixed": converge_peak_hold_fixed,
            "params": {
                "alpha_mean": converge_alpha_mean, "alpha_std": converge_alpha_std,
                "alpha_min": converge_alpha_min, "alpha_max": converge_alpha_max,
                "decay_mean": converge_decay_mean, "decay_std": converge_decay_std,
                "decay_min": converge_decay_min, "decay_max": converge_decay_max,
                "explore_alpha_min": converge_explore_alpha_min, "explore_alpha_max": converge_explore_alpha_max,
                "explore_decay_min": converge_explore_decay_min, "explore_decay_max": converge_explore_decay_max,
            },
            "actual_stats": {
                "alpha_min": min(alphas), "alpha_max": max(alphas),
                "alpha_mean": round(sum(alphas) / len(alphas), 4),
                "alpha_std": round((sum((x - sum(alphas) / len(alphas)) ** 2 for x in alphas) / len(alphas)) ** 0.5, 4) if alphas else 0,
                "decay_min": min(decays), "decay_max": max(decays),
                "decay_mean": round(sum(decays) / len(decays), 4),
                "decay_std": round((sum((x - sum(decays) / len(decays)) ** 2 for x in decays) / len(decays)) ** 0.5, 4) if decays else 0,
                "bucket_exploit_count": buckets.count("exploit"),
                "bucket_explore_count": buckets.count("explore"),
            },
        }
        (out_path / "sampling_plan.json").write_text(
            json.dumps(sampling_plan, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    return str(candidates_jsonl.resolve()), patch_paths
