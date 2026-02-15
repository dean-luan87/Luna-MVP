# -*- coding: utf-8 -*-
"""
D1 候选生成：仅 weights.* 的受控采样（LHS / 随机），含基线 empty_patch。
Phase 2：固定对照组 baseline / aggressive / conservative + LHS（numpy 自实现），metadata 必带。
"""
import json
import os
import random
from pathlib import Path
from typing import Any, Dict, List, Optional

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
) -> Dict[str, Any]:
    """为 patch 加上 metadata（patch_kind, d1_run_id, version_tag）。"""
    return {
        "metadata": {
            "patch_kind": "weights_only",
            "d1_run_id": d1_run_id,
            "version_tag": version_tag,
        },
        **{k: v for k, v in payload.items() if k != "metadata"},
    }


def generate_candidates(
    n: int,
    out_dir: str,
    method: str = "lhs",
    seed: Optional[int] = None,
    include_baseline: bool = True,
    d1_run_id: Optional[str] = None,
    version_tag: str = "d1_v1",
) -> tuple:
    """
    生成 n 个候选 patch（JSON 文件）到 out_dir/candidates/*.json 并写 candidates.jsonl。
    固定对照组：baseline（empty）、aggressive（risk 权重*2 并 clamp）、conservative（*0.7 并 clamp）；
    其余为 LHS 采样（n - 3）。每个 patch 带 metadata（patch_kind, d1_run_id, version_tag）。
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

    def write_patch(patch_id: str, data: Dict[str, Any]) -> None:
        fp = candidates_dir / f"{patch_id}.json"
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        patch_paths.append(str(fp.resolve()))
        rows.append({"patch_id": patch_id, "patch_path": str(fp.resolve())})

    # 1) baseline（empty）
    if include_baseline:
        baseline_data = _patch_with_metadata({}, run_id, version_tag)
        write_patch("baseline", baseline_data)

    # 2) aggressive：risk 相关权重 *2，clamp
    agg: Dict[str, float] = {}
    for k in D1_WEIGHTS_KEYS:
        v = D1_WEIGHTS_DEFAULTS[k]
        if k in RISK_WEIGHT_KEYS:
            v = _clamp(k, v * 2.0)
        else:
            v = _clamp(k, v)
        agg[k] = v
    write_patch("aggressive", _patch_with_metadata(agg, run_id, version_tag))

    # 3) conservative：risk 相关 *0.7，clamp
    cons: Dict[str, float] = {}
    for k in D1_WEIGHTS_KEYS:
        v = D1_WEIGHTS_DEFAULTS[k]
        if k in RISK_WEIGHT_KEYS:
            v = _clamp(k, v * 0.7)
        else:
            v = _clamp(k, v)
        cons[k] = v
    write_patch("conservative", _patch_with_metadata(cons, run_id, version_tag))

    # 4) LHS 采样（n - 固定组数量）
    fixed_count = (1 if include_baseline else 0) + 2  # baseline + agg + cons
    num_sampled = max(0, n - fixed_count)
    if method == "lhs":
        patches = generate_lhs_patches(num_sampled, seed=seed)
    else:
        patches = [generate_random_patch(seed=rng.randint(0, 2**31 - 1)) for _ in range(num_sampled)]

    for i, p in enumerate(patches):
        pid = f"d1_candidate_{i:03d}"
        write_patch(pid, _patch_with_metadata(p, run_id, version_tag))

    candidates_jsonl = out_path / "candidates.jsonl"
    with open(candidates_jsonl, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return str(candidates_jsonl.resolve()), patch_paths
