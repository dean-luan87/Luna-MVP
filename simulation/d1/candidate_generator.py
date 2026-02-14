# -*- coding: utf-8 -*-
"""
D1 候选生成：仅 weights.* 的受控采样（LHS / 随机），含基线 empty_patch。
第一版：随机均匀采样；可选 LHS（需 scipy）。
"""
import json
import os
import random
from pathlib import Path
from typing import Any, Dict, List, Optional

from simulation.d1.weights_schema import D1_WEIGHTS_BOUNDS, D1_WEIGHTS_DEFAULTS, D1_WEIGHTS_KEYS


def generate_random_patch(seed: Optional[int] = None) -> Dict[str, float]:
    """在 D1_WEIGHTS_BOUNDS 内均匀采样，只生成 weights.* 键。"""
    rng = random.Random(seed)
    out: Dict[str, float] = {}
    for k in D1_WEIGHTS_KEYS:
        lo, hi = D1_WEIGHTS_BOUNDS[k]
        out[k] = round(rng.uniform(lo, hi), 4)
    return out


def generate_lhs_patches(n: int, seed: Optional[int] = None) -> List[Dict[str, float]]:
    """
    拉丁超立方采样 n 组 weights（每维分层）。
    无 scipy 时退化为随机采样。
    """
    try:
        from scipy.stats import qmc
        sampler = qmc.LatinHypercube(d=len(D1_WEIGHTS_KEYS), seed=seed)
        u = sampler.random(n=n)
        out: List[Dict[str, float]] = []
        for i in range(n):
            patch: Dict[str, float] = {}
            for j, k in enumerate(D1_WEIGHTS_KEYS):
                lo, hi = D1_WEIGHTS_BOUNDS[k]
                patch[k] = round(lo + (hi - lo) * float(u[i, j]), 4)
            out.append(patch)
        return out
    except ImportError:
        rng = random.Random(seed)
        return [generate_random_patch(seed=rng.randint(0, 2**31 - 1)) for _ in range(n)]


def generate_candidates(
    n: int,
    out_dir: str,
    method: str = "lhs",
    seed: Optional[int] = None,
    include_baseline: bool = True,
) -> tuple:
    """
    生成 n 个候选 patch（JSON 文件）并写 candidates.jsonl。
    include_baseline=True 时先写一条 baseline（empty patch）再写 n 个采样。
    返回 (candidates_jsonl_path, list of patch_paths)。
    """
    os.makedirs(out_dir, exist_ok=True)
    out_path = Path(out_dir)
    rng = random.Random(seed)
    patch_paths: List[str] = []
    rows: List[Dict[str, Any]] = []

    if include_baseline:
        # 命名为 empty_patch.json 使 sim_runner 识别为 baseline/empty_patch 并施加参考风险
        baseline_path = out_path / "empty_patch.json"
        with open(baseline_path, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)
        patch_paths.append(str(baseline_path.resolve()))
        rows.append({"patch_id": "baseline", "patch_path": str(baseline_path.resolve())})

    num_sampled = n - (1 if include_baseline else 0)
    if method == "lhs":
        patches = generate_lhs_patches(num_sampled, seed=seed)
    else:
        patches = [generate_random_patch(seed=rng.randint(0, 2**31 - 1)) for _ in range(num_sampled)]

    for i, p in enumerate(patches):
        pid = f"d1_candidate_{i:03d}"
        fp = out_path / f"{pid}.json"
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(p, f, indent=2)
        patch_paths.append(str(fp.resolve()))
        rows.append({"patch_id": pid, "patch_path": str(fp.resolve())})

    candidates_jsonl = out_path / "candidates.jsonl"
    with open(candidates_jsonl, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return str(candidates_jsonl.resolve()), patch_paths
