import argparse
import csv
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

# 确保项目根在 path 中（用于 intervention 等模块）
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

# F) ENGAGED 跨段稳定性体检 v0
try:
    from intervention.long_term_stability import compute_long_term_diagnosis
except ImportError:
    compute_long_term_diagnosis = None

# J) 仲裁 × 类型节律联动体检 v0
try:
    from intervention.arbitration_diagnosis import compute_arbitration_diagnosis
except ImportError:
    compute_arbitration_diagnosis = None


def pearson(xs, ys):
    if len(xs) < 2:
        return 0.0
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    deny = math.sqrt(sum((y - my) ** 2 for y in ys))
    return num / (denx * deny) if denx and deny else 0.0


def mean_std(vals):
    if not vals:
        return 0.0, 0.0
    mean = sum(vals) / len(vals)
    var = sum((x - mean) ** 2 for x in vals) / len(vals)
    return mean, math.sqrt(var)


def _sanitize_label(k):
    """matplotlib 的 category 轴要求 str/bytes，None 会报错"""
    return k if isinstance(k, (str, bytes)) else (str(k) if k is not None else "N/A")


def write_png(out_png, control_counter, quality_counter, vc_vals, motion_vals):
    try:
        import matplotlib.pyplot as plt  # noqa: F401
    except Exception:
        return False

    control_labels = [_sanitize_label(k) for k in control_counter.keys()]
    control_vals = [control_counter[k] for k in control_counter.keys()]
    quality_labels = [_sanitize_label(k) for k in quality_counter.keys()]
    quality_vals = [quality_counter[k] for k in quality_counter.keys()]

    vc_mean, vc_std = mean_std(vc_vals)
    motion_mean, motion_std = mean_std(motion_vals)

    plt.figure(figsize=(10, 6))
    plt.subplot(2, 2, 1)
    plt.bar(control_labels, control_vals)
    plt.title("Control Mode Count")
    plt.subplot(2, 2, 2)
    plt.bar(quality_labels, quality_vals)
    plt.title("Frame Quality Count")
    plt.subplot(2, 2, 3)
    plt.bar(["view_confidence", "motion_instability"], [vc_mean, motion_mean])
    plt.title("Means")
    plt.subplot(2, 2, 4)
    plt.bar(["view_confidence", "motion_instability"], [vc_std, motion_std])
    plt.title("Std Dev")
    plt.tight_layout()
    plt.savefig(out_png)
    return True


def _percentile(sorted_vals, pct):
    if not sorted_vals:
        return 0.0
    idx = int(round((pct / 100.0) * (len(sorted_vals) - 1)))
    return float(sorted_vals[max(0, min(len(sorted_vals) - 1, idx))])


def _norm_view(r):
    """兼容 trace：有 view 用 view，否则用 obs 映射为 view。缺失统一为 NONE/0 便于报表。"""
    view = r.get("view")
    if view is not None:
        return view
    obs = r.get("obs") or {}
    q = obs.get("frame_quality")
    return {
        "frame_quality": q if q is not None else "NONE",
        "view_confidence": obs.get("vc") if obs.get("vc") is not None else 0.0,
        "motion_instability": obs.get("motion") if obs.get("motion") is not None else 0.0,
    }


def _norm_a3(r):
    """兼容 trace：有 a3 用 a3，否则用 decision + obs 映射。缺失统一为 NONE/0 便于报表。"""
    a3 = r.get("a3")
    if a3 is not None:
        return a3
    dec = r.get("decision") or {}
    obs = r.get("obs") or {}
    ctrl = dec.get("control_mode") or obs.get("control_mode")
    return {
        "control_mode": ctrl if ctrl is not None else "NONE",
        "complexity_raw": dec.get("complexity_raw") if dec.get("complexity_raw") is not None else obs.get("complexity"),
        "complexity_effective": dec.get("complexity_effective") if dec.get("complexity_effective") is not None else obs.get("complexity"),
        "inputs": {
            "path_instability": obs.get("path"),
            "roi_count": obs.get("roi"),
            "branch_load": obs.get("branch"),
        },
    }


def compute_jitter(rows):
    control_seq = []
    control_ts = []
    control_counter = Counter()
    vc_by_control = defaultdict(list)
    motion_by_control = defaultdict(list)
    quality_by_control = defaultdict(list)

    for r in rows:
        view = _norm_view(r) or {}
        a3 = _norm_a3(r) or {}
        ts = r.get("ts")
        control = a3.get("control_mode")
        quality = view.get("frame_quality")
        vc = view.get("view_confidence")
        motion = view.get("motion_instability")

        control_seq.append(control)
        control_ts.append(ts)
        control_counter[control] += 1
        quality_by_control[control].append(quality)
        if vc is not None:
            vc_by_control[control].append(vc)
        if motion is not None:
            motion_by_control[control].append(motion)

    transitions = Counter()
    for i in range(1, len(control_seq)):
        prev = control_seq[i - 1]
        curr = control_seq[i]
        if prev != curr:
            transitions[(prev, curr)] += 1

    dwell = defaultdict(list)
    if control_seq and control_ts:
        start_idx = 0
        for i in range(1, len(control_seq)):
            if control_seq[i] != control_seq[start_idx]:
                dur = control_ts[i - 1] - control_ts[start_idx]
                dwell[control_seq[start_idx]].append(dur)
                start_idx = i
        dur = control_ts[-1] - control_ts[start_idx]
        dwell[control_seq[start_idx]].append(dur)

    return {
        "control_counter": control_counter,
        "transitions": transitions,
        "dwell": dwell,
        "vc_by_control": vc_by_control,
        "motion_by_control": motion_by_control,
        "quality_by_control": quality_by_control,
    }


def maybe_diagnose(jitter_metrics):
    guarded_vc_mean, _ = mean_std(jitter_metrics["vc_by_control"].get("GUARDED", []))
    assisted_vc_mean, _ = mean_std(jitter_metrics["vc_by_control"].get("ASSISTED", []))

    g_to_a = jitter_metrics["transitions"].get(("GUARDED", "ASSISTED"), 0)
    a_to_g = jitter_metrics["transitions"].get(("ASSISTED", "GUARDED"), 0)
    switch_symmetry = abs(g_to_a - a_to_g) <= 1

    guarded_dwell = jitter_metrics["dwell"].get("GUARDED", [])
    guarded_p50 = _percentile(sorted(guarded_dwell), 50) if guarded_dwell else 0.0

    cond_vc_gap = abs(guarded_vc_mean - assisted_vc_mean) > 0.1
    cond_symmetry = switch_symmetry
    cond_short_dwell = guarded_p50 < 2.0
    hits = sum([cond_vc_gap, cond_symmetry, cond_short_dwell])

    if hits < 2:
        return None

    return {
        "diagnosis": {
            "root_cause": "VC_THRESHOLD_OSCILLATION",
            "confidence": 0.92,
            "evidence": {
                "guarded_vc_mean": guarded_vc_mean,
                "assisted_vc_mean": assisted_vc_mean,
                "switch_symmetry": switch_symmetry,
                "guarded_p50_sec": guarded_p50,
            },
            "recommendation": {
                "action": "ADD_HYSTERESIS",
                "enter_guarded_lt": 0.38,
                "exit_guarded_gt": 0.45,
                "urgency": "LOW",
                "apply_now": False,
            },
        }
    }


ACTIVE_CONTROL_MODES = {"ASSISTED", "GUARDED"}


def _compute_core_metrics(rows):
    """对给定 rows 做一遍聚合，返回 dict（用于 ALL 或 ACTIVE 口径）。"""
    control_counter = Counter()
    quality_counter = Counter()
    vc_vals = []
    motion_vals = []
    raw_vals = []
    eff_vals = []
    path_vals = []
    roi_vals = []
    branch_vals = []
    pal_vals = []
    path_motion_pairs = []
    path_roi_pairs = []
    branch_motion_pairs = []
    branch_path_pairs = []
    pal_path_pairs = []
    for r in rows:
        view = _norm_view(r) or {}
        a3 = _norm_a3(r) or {}
        control = a3.get("control_mode")
        quality = view.get("frame_quality")
        control_counter[control] += 1
        quality_counter[quality] += 1
        vc = view.get("view_confidence")
        motion = view.get("motion_instability")
        raw = a3.get("complexity_raw")
        eff = a3.get("complexity_effective")
        inputs = a3.get("inputs", {})
        path_in = inputs.get("path_instability")
        roi_in = inputs.get("roi_count")
        branch_in = inputs.get("branch_load")
        if vc is not None:
            vc_vals.append(vc)
        if motion is not None:
            motion_vals.append(motion)
        if raw is not None:
            raw_vals.append(raw)
        if eff is not None:
            eff_vals.append(eff)
        if path_in is not None:
            path_vals.append(path_in)
            if motion is not None:
                path_motion_pairs.append((path_in, motion))
            if roi_in is not None:
                path_roi_pairs.append((path_in, roi_in))
        if roi_in is not None:
            roi_vals.append(roi_in)
        if branch_in is not None:
            branch_vals.append(branch_in)
            if motion is not None:
                branch_motion_pairs.append((branch_in, motion))
            if path_in is not None:
                branch_path_pairs.append((branch_in, path_in))
        pal = r.get("pal", {}).get("horizon_difficulty")
        if pal is not None and path_in is not None:
            pal_vals.append(pal)
            pal_path_pairs.append((pal, path_in))
    total = len(rows)
    control_seq = [_norm_a3(r).get("control_mode") for r in rows]
    switches = sum(1 for i in range(1, len(control_seq)) if control_seq[i] != control_seq[i - 1])
    duration_sec = (rows[-1]["ts"] - rows[0]["ts"]) if len(rows) >= 2 else 0.0
    switches_per_min = switches / max(duration_sec / 60.0, 1e-6)
    corr_motion_raw = pearson(motion_vals, raw_vals)
    corr_vc_eff = pearson(vc_vals, eff_vals)
    path_for_corr_motion = [p for p, m in path_motion_pairs]
    motion_for_corr = [m for p, m in path_motion_pairs]
    path_for_corr_roi = [p for p, r in path_roi_pairs]
    roi_for_corr = [r for p, r in path_roi_pairs]
    corr_path_motion = pearson(path_for_corr_motion, motion_for_corr) if path_motion_pairs else 0.0
    corr_path_roi = pearson(path_for_corr_roi, roi_for_corr) if path_roi_pairs else 0.0
    branch_for_corr_motion = [b for b, m in branch_motion_pairs]
    motion_for_corr_b = [m for b, m in branch_motion_pairs]
    branch_for_corr_path = [b for b, p in branch_path_pairs]
    path_for_corr_b = [p for b, p in branch_path_pairs]
    corr_branch_motion = pearson(branch_for_corr_motion, motion_for_corr_b) if branch_motion_pairs else 0.0
    corr_branch_path = pearson(branch_for_corr_path, path_for_corr_b) if branch_path_pairs else 0.0
    vc_mean, vc_std = mean_std(vc_vals)
    motion_mean, motion_std = mean_std(motion_vals)
    path_p50 = _percentile(sorted(path_vals), 50) if path_vals else 0.0
    path_p95 = _percentile(sorted(path_vals), 95) if path_vals else 0.0
    branch_p50 = _percentile(sorted(branch_vals), 50) if branch_vals else 0.0
    branch_p95 = _percentile(sorted(branch_vals), 95) if branch_vals else 0.0
    branch_gt0_ratio = sum(1 for b in branch_vals if b > 0) / len(branch_vals) if branch_vals else 0.0
    return {
        "total": total,
        "control_counter": control_counter,
        "quality_counter": quality_counter,
        "vc_vals": vc_vals,
        "motion_vals": motion_vals,
        "raw_vals": raw_vals,
        "eff_vals": eff_vals,
        "path_vals": path_vals,
        "roi_vals": roi_vals,
        "branch_vals": branch_vals,
        "pal_vals": pal_vals,
        "path_motion_pairs": path_motion_pairs,
        "path_roi_pairs": path_roi_pairs,
        "branch_motion_pairs": branch_motion_pairs,
        "branch_path_pairs": branch_path_pairs,
        "pal_path_pairs": pal_path_pairs,
        "switches_per_min": switches_per_min,
        "corr_motion_raw": corr_motion_raw,
        "corr_vc_eff": corr_vc_eff,
        "corr_path_motion": corr_path_motion,
        "corr_path_roi": corr_path_roi,
        "corr_branch_motion": corr_branch_motion,
        "corr_branch_path": corr_branch_path,
        "vc_mean": vc_mean,
        "vc_std": vc_std,
        "motion_mean": motion_mean,
        "motion_std": motion_std,
        "path_p50": path_p50,
        "path_p95": path_p95,
        "branch_p50": branch_p50,
        "branch_p95": branch_p95,
        "branch_gt0_ratio": branch_gt0_ratio,
    }


def _print_core_block(label, m):
    """打印一段 ALL 或 ACTIVE 的核心指标。"""
    total = m["total"]
    if total == 0:
        print(f"\n--- {label} ---\n  (0 frames)")
        return
    print(f"\n--- {label} ---")
    print("Total frames:", total)
    print("Control mode ratio:")
    for k, v in m["control_counter"].items():
        print(f"  {k}: {v/total:.2%}")
    print("Frame quality ratio:")
    for k, v in m["quality_counter"].items():
        print(f"  {k}: {v/total:.2%}")
    print("Stability:")
    print(f"  control switches / min: {m['switches_per_min']:.2f}")
    print(f"  view_confidence mean/std: {m['vc_mean']:.3f} / {m['vc_std']:.3f}")
    print(f"  motion_instability mean/std: {m['motion_mean']:.3f} / {m['motion_std']:.3f}")
    print("Path v0 (path_instability):")
    if m["path_vals"]:
        print(f"  p50: {m['path_p50']:.3f}, p95: {m['path_p95']:.3f}")
        print(f"  corr(path, motion): {m['corr_path_motion']:.3f}")
        print(f"  corr(path, roi): {m['corr_path_roi']:.3f}")
    else:
        print("  (no path data)")
    print("Branch v0 (branch_load):")
    if m["branch_vals"]:
        print(f"  p50: {m['branch_p50']:.3f}, p95: {m['branch_p95']:.3f}")
        print(f"  corr(branch, motion): {m['corr_branch_motion']:.3f}")
        print(f"  corr(branch, path): {m['corr_branch_path']:.3f}")
        print(f"  branch>0 占比: {m['branch_gt0_ratio']:.2%}")
    else:
        print("  (no branch data)")
    print("Correlations:")
    print(f"  corr(motion_instability, complexity_raw): {m['corr_motion_raw']:.3f}")
    print(f"  corr(view_confidence, complexity_effective): {m['corr_vc_eff']:.3f}")


def main(path, jitter=False, longterm=False, active_only=False):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))

    if not rows:
        print("Trace 为空或无法读取")
        return

    active_rows = [r for r in rows if _norm_a3(r).get("control_mode") in ACTIVE_CONTROL_MODES]
    n_active = len(active_rows)
    n_all = len(rows)
    active_frame_ratio = n_active / n_all if n_all else 0.0

    if active_only:
        print("active_frame_ratio (ACTIVE/ALL):", f"{n_active}/{n_all} = {active_frame_ratio:.2%}")
        if not active_rows:
            print("ACTIVE: 0 frames (control_mode not in ASSISTED/GUARDED)")
            return
        m = _compute_core_metrics(active_rows)
        _print_core_block("ACTIVE", m)
        return

    # 默认：ALL + ACTIVE 双口径
    m_all = _compute_core_metrics(rows)
    _print_core_block("ALL", m_all)
    print("\nactive_frame_ratio (ACTIVE/ALL):", f"{n_active}/{n_all} = {active_frame_ratio:.2%}")
    if active_rows:
        m_active = _compute_core_metrics(active_rows)
        _print_core_block("ACTIVE", m_active)

    # 以下沿用 ALL 口径的变量名，供后续 PAL/ENGAGED/CSV/PNG 使用
    total = m_all["total"]
    control_counter = m_all["control_counter"]
    quality_counter = m_all["quality_counter"]
    vc_vals = m_all["vc_vals"]
    motion_vals = m_all["motion_vals"]
    raw_vals = m_all["raw_vals"]
    eff_vals = m_all["eff_vals"]
    path_vals = m_all["path_vals"]
    roi_vals = m_all["roi_vals"]
    branch_vals = m_all["branch_vals"]
    pal_vals = m_all["pal_vals"]
    path_motion_pairs = m_all["path_motion_pairs"]
    path_roi_pairs = m_all["path_roi_pairs"]
    branch_motion_pairs = m_all["branch_motion_pairs"]
    branch_path_pairs = m_all["branch_path_pairs"]
    pal_path_pairs = m_all["pal_path_pairs"]
    switches_per_min = m_all["switches_per_min"]
    corr_motion_raw = m_all["corr_motion_raw"]
    corr_vc_eff = m_all["corr_vc_eff"]
    corr_path_motion = m_all["corr_path_motion"]
    corr_path_roi = m_all["corr_path_roi"]
    corr_branch_motion = m_all["corr_branch_motion"]
    corr_branch_path = m_all["corr_branch_path"]
    vc_mean = m_all["vc_mean"]
    vc_std = m_all["vc_std"]
    motion_mean = m_all["motion_mean"]
    motion_std = m_all["motion_std"]
    path_p50 = m_all["path_p50"]
    path_p95 = m_all["path_p95"]
    branch_p50 = m_all["branch_p50"]
    branch_p95 = m_all["branch_p95"]
    branch_gt0_ratio = m_all["branch_gt0_ratio"]
    control_seq = [_norm_a3(r).get("control_mode") for r in rows]
    switches = sum(1 for i in range(1, len(control_seq)) if control_seq[i] != control_seq[i - 1])

    # PAL v0（只读前瞻）
    if pal_vals:
        pal_p50 = _percentile(sorted(pal_vals), 50)
        pal_p95 = _percentile(sorted(pal_vals), 95)
        pal_mean, pal_std = mean_std(pal_vals)
        pal_pairs = [(r.get("pal", {}).get("horizon_difficulty"), eff) for r in rows if r.get("pal", {}).get("horizon_difficulty") is not None and (eff := _norm_a3(r).get("complexity_effective")) is not None]
        pal_for_corr = [p for p, e in pal_pairs]
        eff_for_corr = [e for p, e in pal_pairs]
        corr_pal_eff = pearson(pal_for_corr, eff_for_corr) if pal_pairs else 0.0
        pal_for_path = [p for p, path in pal_path_pairs]
        path_for_pal = [path for p, path in pal_path_pairs]
        corr_pal_path = pearson(pal_for_path, path_for_pal) if pal_path_pairs else 0.0
        # 平滑性：PAL 标准差应 <= complexity 标准差（更平滑）
        eff_std = math.sqrt(sum((x - sum(eff_vals)/len(eff_vals))**2 for x in eff_vals)/len(eff_vals)) if eff_vals else 0.0
        print("\nPAL v0 (horizon_difficulty):")
        print(f"  p50: {pal_p50:.3f}, p95: {pal_p95:.3f}")
        print(f"  mean/std: {pal_mean:.3f} / {pal_std:.3f}")
        print(f"  corr(pal, complexity_effective): {corr_pal_eff:.3f}")
        print(f"  corr(pal, path): {corr_pal_path:.3f}")
        print(f"  平滑性: pal_std={pal_std:.3f} vs eff_std={eff_std:.3f} (PAL应更平滑)")

    # ACTIVE × PAL 节律 v0
    rhythm_rows = [r for r in rows if "rhythm" in r]
    if rhythm_rows:
        rhythm_counter = Counter()
        for r in rhythm_rows:
            s = r.get("rhythm", {}).get("state")
            if s:
                rhythm_counter[s] += 1
        total_rhythm = len(rhythm_rows)
        print("\n节律 v0 (rhythm.state):")
        for k, v in rhythm_counter.items():
            print(f"  {k}: {v}/{total_rhythm} ({v/total_rhythm:.1%})")

    # ENGAGED 介入强度 v0
    LEVEL_MAP = {"L0": 0, "L1": 1, "L2": 2, "L3": 3}
    engagement_rows = [r for r in rows if "engagement" in r]
    if engagement_rows:
        eng_counter = Counter()
        engaged_only = []
        guarded_l3 = 0
        l3_vc_low = 0
        level_seq = []
        for r in engagement_rows:
            lev = r.get("engagement", {}).get("level", "L0")
            eng_counter[lev] += 1
            level_seq.append(lev)
            if r.get("rhythm", {}).get("state") == "ENGAGED":
                engaged_only.append(lev)
            if _norm_a3(r).get("control_mode") == "GUARDED" and lev == "L3":
                guarded_l3 += 1
            if lev == "L3" and _norm_view(r).get("view_confidence", 1.0) < 0.75:
                l3_vc_low += 1
        total_eng = len(engagement_rows)
        print("\n介入强度 v0 (engagement.level):")
        for k in ["L0", "L1", "L2", "L3"]:
            v = eng_counter.get(k, 0)
            if v > 0:
                print(f"  {k}: {v}/{total_eng} ({v/total_eng:.1%})")
        # A) ENGAGED×level 只读观测
        if engaged_only:
            eng_in_engaged = Counter(engaged_only)
            print("  ENGAGED×level 分布:", dict(eng_in_engaged))
            # 平均驻留时长、切换率
            engaged_rows = [r for r in engagement_rows if r.get("rhythm", {}).get("state") == "ENGAGED"]
            if engaged_rows and len(engaged_rows) >= 2:
                level_seq_eng = [r.get("engagement", {}).get("level", "L0") for r in engaged_rows]
                ts_eng = [r.get("ts") for r in engaged_rows if r.get("ts") is not None]
                switches_eng = sum(1 for i in range(1, len(level_seq_eng)) if level_seq_eng[i] != level_seq_eng[i - 1])
                dur_eng = ts_eng[-1] - ts_eng[0] if ts_eng else 0
                switches_per_min_eng = switches_eng / max(dur_eng / 60.0, 1e-6)
                dwells = []
                start_i = 0
                for i in range(1, len(level_seq_eng)):
                    if level_seq_eng[i] != level_seq_eng[start_i] and i > start_i and ts_eng:
                        dwells.append(ts_eng[i - 1] - ts_eng[start_i])
                        start_i = i
                if ts_eng and start_i < len(ts_eng):
                    dwells.append(ts_eng[-1] - ts_eng[start_i])
                avg_dwell = sum(dwells) / len(dwells) if dwells else 0
                print("  平均驻留时长(s):", round(avg_dwell, 2))
                print("  level 切换率(switches/min):", round(switches_per_min_eng, 2))
                # rhythm 切换率（level 应不放大）
                rhythm_seq = [r.get("rhythm", {}).get("state") for r in rows if r.get("rhythm")]
                rhythm_switches = sum(1 for i in range(1, len(rhythm_seq)) if rhythm_seq[i] != rhythm_seq[i - 1])
                dur_total = rows[-1].get("ts", 0) - rows[0].get("ts", 1) if len(rows) >= 2 else 1
                rhythm_sw_per_min = rhythm_switches / max(dur_total / 60.0, 1e-6)
                print("  rhythm 切换率(switches/min):", round(rhythm_sw_per_min, 2), "(level 应 ≤ rhythm)")
            # corr(level_numeric, pal), corr(level_numeric, complexity_effective)
            levels_num = [LEVEL_MAP.get(r.get("engagement", {}).get("level", "L0"), 0) for r in engaged_rows]
            pal_eng = [r.get("pal", {}).get("horizon_difficulty") for r in engaged_rows]
            eff_eng = [_norm_a3(r).get("complexity_effective") for r in engaged_rows]
            pairs_pal = [(l, p) for l, p in zip(levels_num, pal_eng) if p is not None]
            pairs_eff = [(l, e) for l, e in zip(levels_num, eff_eng) if e is not None]
            corr_lev_pal = pearson([x[0] for x in pairs_pal], [x[1] for x in pairs_pal]) if len(pairs_pal) >= 2 else 0
            corr_lev_eff = pearson([x[0] for x in pairs_eff], [x[1] for x in pairs_eff]) if len(pairs_eff) >= 2 else 0
            print("  corr(level, pal):", round(corr_lev_pal, 3))
            print("  corr(level, complexity_effective):", round(corr_lev_eff, 3))
        if guarded_l3 > 0:
            print(f"  ⚠ L3 & GUARDED 违规: {guarded_l3} (应为 0)")
        if l3_vc_low > 0:
            print(f"  ⚠ L3 & vc<0.75 违规: {l3_vc_low} (应为 0)")
        # level 抖动：1s 内来回（A→B→A 连续 3 样本）
        jitter_count = 0
        for i in range(len(level_seq) - 2):
            if level_seq[i] == level_seq[i + 2] and level_seq[i] != level_seq[i + 1]:
                jitter_count += 1
        print("  level 抖动（1s 内来回）:", jitter_count, "次")

    # J) ENGAGED 事实信号 (engaged_signal) — signal-only，解释交给 N 层
    engaged_signal_rows = [r for r in rows if "engaged_signal" in r]
    engaged_expect_speak = [r for r in rows if r.get("rhythm", {}).get("state") == "ENGAGED" and r.get("engagement", {}).get("level") in ("L1", "L2", "L3")]
    print("\nENGAGED 事实信号 (engaged_signal):")
    if engaged_signal_rows:
        block_counter = Counter()
        for r in engaged_signal_rows:
            sig = r.get("engaged_signal", {})
            if sig.get("blocked") and sig.get("block_stage"):
                block_counter[sig["block_stage"]] += 1
        total_sig = len(engaged_signal_rows)
        total_expect = len(engaged_expect_speak)
        block_rate = total_sig / total_expect if total_expect else 0
        print("  ENGAGED 未执行/阻断:", f"{total_sig}/{total_expect}" if total_expect else "N/A", f"({block_rate:.1%})" if total_expect else "")
        print("  block_stage 分布:", dict(block_counter))
    else:
        print("  无 engaged_signal 记录（本段未进入 ENGAGED，或 ENGAGED 时均已执行）")
        if engaged_expect_speak:
            print("  ENGAGED 帧数:", len(engaged_expect_speak))

    # 兼容旧 trace：engaged_failure（已由 engaged_signal 替代）
    engaged_failure_rows = [r for r in rows if "engaged_failure" in r]
    if engaged_failure_rows:
        print("\nENGAGED 失败回退 (engaged_failure，旧格式):")
        fail_counter = Counter(r.get("engaged_failure", {}).get("reason", "FAIL_UNKNOWN") for r in engaged_failure_rows)
        print("  失败原因分布:", dict(fail_counter))

    # C) PAL lookahead_m 分布（ENGAGED 内 8/12/18）
    pal_lookahead_rows = [r for r in rows if r.get("pal", {}).get("lookahead_m") is not None]
    if pal_lookahead_rows:
        lookahead_vals = [r["pal"]["lookahead_m"] for r in pal_lookahead_rows]
        lookahead_counter = Counter(lookahead_vals)
        print("\nPAL lookahead_m (C 调制):")
        print("  分布:", dict(lookahead_counter))

    # K) 多模态输入冲突 v0
    multimodal_rows = [r for r in rows if "multimodal_conflict" in r]
    if multimodal_rows:
        src_counter = Counter()
        for r in multimodal_rows:
            mc = r.get("multimodal_conflict", {})
            sel = mc.get("selected_source")
            if sel:
                src_counter[sel] += 1
        print("\nK) 多模态输入冲突 v0 (multimodal_conflict):")
        print(f"  冲突事件数: {len(multimodal_rows)}")
        print(f"  selected_source 分布: {dict(src_counter)}")
        if multimodal_rows:
            last_mc = multimodal_rows[-1].get("multimodal_conflict", {})
            print(f"  最近: sources={last_mc.get('sources')}, selected={last_mc.get('selected_source')}, reason={last_mc.get('reason')}")

    # L) 影子运行模式 v0
    shadow_rows = [r for r in rows if "shadow_decision" in r]
    if shadow_rows:
        would_speak_count = sum(1 for r in shadow_rows if r.get("shadow_decision", {}).get("would_speak"))
        print("\nL) 影子运行模式 v0 (shadow_decision):")
        print(f"  shadow 事件数: {len(shadow_rows)}")
        print(f"  would_speak 次数: {would_speak_count}")
        if shadow_rows:
            last_shadow = shadow_rows[-1].get("shadow_decision", {})
            print(f"  最近: would_speak={last_shadow.get('would_speak')}, task_id={last_shadow.get('task_id')}, type={last_shadow.get('type')}")

    # G) 多任务介入仲裁 v0
    arbitration_rows = [r for r in rows if "arbitration" in r]
    if arbitration_rows:
        winner_count = sum(1 for r in arbitration_rows if r.get("arbitration", {}).get("winner"))
        deferred_count = sum(len(r.get("arbitration", {}).get("deferred", [])) for r in arbitration_rows)
        print("\nG) 多任务介入仲裁 v0 (arbitration):")
        print(f"  仲裁事件数: {len(arbitration_rows)}")
        print(f"  winner 次数: {winner_count}")
        print(f"  deferred 总次数: {deferred_count}")
        if arbitration_rows:
            last_arb = arbitration_rows[-1].get("arbitration", {})
            print(f"  最近: winner={last_arb.get('winner')}, deferred={last_arb.get('deferred')}")
            if last_arb.get("fairness"):
                print(f"  fairness: {last_arb.get('fairness')}")
        # K/L 层：与 arbitration 同条 trace 的 k、l 字段
        with_k = sum(1 for r in arbitration_rows if r.get("k"))
        with_l = sum(1 for r in arbitration_rows if r.get("l"))
        print(f"  K/L 层: 含 k 的条数={with_k}, 含 l 的条数={with_l}")
        if arbitration_rows and (with_k or with_l):
            sample = next((r for r in arbitration_rows if r.get("k") or r.get("l")), None)
            if sample:
                print(f"  最近一条 K/L: k={sample.get('k')}, l={sample.get('l')}")

    # J) 仲裁 × 类型节律联动体检 v0（只读，不反馈到实时系统）
    if longterm and compute_arbitration_diagnosis:
        arb_diag = compute_arbitration_diagnosis(rows)
        print("\nJ) 仲裁 × 类型节律联动体检 (arbitration_diagnosis):")
        print(json.dumps(arb_diag, ensure_ascii=False, indent=2))

    # F) ENGAGED 跨段稳定性体检 v0（只读，不反馈到实时系统）
    if longterm and compute_long_term_diagnosis:
        diagnosis = compute_long_term_diagnosis(rows)
        print("\nF) ENGAGED 跨段稳定性体检 (long_term_diagnosis):")
        print(json.dumps(diagnosis, ensure_ascii=False, indent=2))

    # 主线 A：介入资格门禁（v0）
    intervention_rows = [r for r in rows if "intervention" in r]
    if intervention_rows:
        task_state_counter = Counter()
        reason_counter = Counter()
        eligible_count = 0
        active_rows = []
        for r in intervention_rows:
            inv = r["intervention"]
            ts = inv.get("task_state", "NONE")
            reason = inv.get("reason", "UNKNOWN")
            task_state_counter[ts] += 1
            reason_counter[reason] += 1
            if inv.get("eligible", False):
                eligible_count += 1
            if ts == "ACTIVE":
                active_rows.append(r)
        total_inv = len(intervention_rows)
        print("\n主线 A (Intervention Eligibility v0):")
        print(f"  task_state 分布: {dict(task_state_counter)}")
        print(f"  reason 分布: {dict(reason_counter)}")
        print(f"  eligible 占比: {eligible_count}/{total_inv} = {eligible_count/total_inv:.1%}")
        if active_rows:
            active_eligible = sum(1 for r in active_rows if r["intervention"].get("eligible", False))
            print(f"  ACTIVE 下 eligible 占比: {active_eligible}/{len(active_rows)} = {active_eligible/len(active_rows):.1%}")

    jitter_metrics = None
    if jitter:
        jitter_metrics = compute_jitter(rows)
        print("\nJitter detail:")
        for mode, cnt in jitter_metrics["control_counter"].items():
            vc_mean, vc_std = mean_std(jitter_metrics["vc_by_control"].get(mode, []))
            motion_mean, motion_std = mean_std(jitter_metrics["motion_by_control"].get(mode, []))
            print(f"  {mode}: count={cnt}, vc_mean/std={vc_mean:.3f}/{vc_std:.3f}, motion_mean/std={motion_mean:.3f}/{motion_std:.3f}")

        print("\nTransitions:")
        for (prev, curr), cnt in jitter_metrics["transitions"].items():
            print(f"  {prev} -> {curr}: {cnt}")

        print("\nDwell (sec):")
        for mode, vals in jitter_metrics["dwell"].items():
            sorted_vals = sorted(vals)
            print(f"  {mode}: mean={sum(vals)/len(vals):.3f}, p50={_percentile(sorted_vals, 50):.3f}, count={len(vals)}")

        diagnosis = maybe_diagnose(jitter_metrics)
        if diagnosis:
            print("\nDiagnosis:")
            print(json.dumps(diagnosis, ensure_ascii=False, indent=2))

    out_csv = "logs/a3_metrics.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        for k, v in control_counter.items():
            w.writerow([f"control_ratio_{k}", v / total])
        for k, v in quality_counter.items():
            w.writerow([f"quality_ratio_{k}", v / total])
        w.writerow(["control_switches_per_min", switches_per_min])
        w.writerow(["vc_mean", vc_mean])
        w.writerow(["vc_std", vc_std])
        w.writerow(["motion_mean", motion_mean])
        w.writerow(["motion_std", motion_std])
        w.writerow(["corr_motion_raw", corr_motion_raw])
        w.writerow(["corr_vc_effective", corr_vc_eff])
        if branch_vals:
            w.writerow(["branch_p50", branch_p50])
            w.writerow(["branch_p95", branch_p95])
            w.writerow(["corr_branch_motion", corr_branch_motion])
            w.writerow(["corr_branch_path", corr_branch_path])
            w.writerow(["branch_gt0_ratio", branch_gt0_ratio])
        if pal_vals:
            w.writerow(["pal_p50", pal_p50])
            w.writerow(["pal_p95", pal_p95])
            w.writerow(["pal_mean", pal_mean])
            w.writerow(["pal_std", pal_std])
            w.writerow(["corr_pal_eff", corr_pal_eff])
            w.writerow(["corr_pal_path", corr_pal_path])
        if jitter_metrics:
            for (prev, curr), cnt in jitter_metrics["transitions"].items():
                w.writerow([f"transition_{prev}_to_{curr}", cnt])
            for mode, vals in jitter_metrics["dwell"].items():
                if vals:
                    sorted_vals = sorted(vals)
                    w.writerow([f"dwell_mean_{mode}", sum(vals) / len(vals)])
                    w.writerow([f"dwell_p50_{mode}", _percentile(sorted_vals, 50)])
            for mode, vals in jitter_metrics["vc_by_control"].items():
                vc_mean_mode, vc_std_mode = mean_std(vals)
                w.writerow([f"vc_mean_{mode}", vc_mean_mode])
                w.writerow([f"vc_std_{mode}", vc_std_mode])
            for mode, vals in jitter_metrics["motion_by_control"].items():
                motion_mean_mode, motion_std_mode = mean_std(vals)
                w.writerow([f"motion_mean_{mode}", motion_mean_mode])
                w.writerow([f"motion_std_{mode}", motion_std_mode])

    print(f"\nCSV written to {out_csv}")

    out_png = "logs/a3_metrics.png"
    if write_png(out_png, control_counter, quality_counter, vc_vals, motion_vals):
        print(f"PNG written to {out_png}")
    else:
        print("PNG skipped (matplotlib 未安装)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("trace", help="a3_trace.jsonl path")
    parser.add_argument("--jitter", action="store_true", help="输出抖动细分统计")
    parser.add_argument("--longterm", action="store_true", help="F) ENGAGED 跨段稳定性体检")
    parser.add_argument("--active-only", action="store_true", help="仅输出 ACTIVE 口径（control_mode in ASSISTED/GUARDED）")
    args = parser.parse_args()
    main(args.trace, jitter=args.jitter, longterm=args.longterm, active_only=args.active_only)
