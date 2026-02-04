import argparse
import glob
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

from analyze_a3_trace import compute_jitter, maybe_diagnose


def mean_std(vals):
    if not vals:
        return 0.0, 0.0
    mean = sum(vals) / len(vals)
    var = sum((x - mean) ** 2 for x in vals) / len(vals)
    return mean, math.sqrt(var)


def percentile(sorted_vals, pct):
    if not sorted_vals:
        return 0.0
    idx = int(round((pct / 100.0) * (len(sorted_vals) - 1)))
    idx = max(0, min(len(sorted_vals) - 1, idx))
    return float(sorted_vals[idx])


def load_rows(paths):
    rows = []
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rows.append(json.loads(line))
    rows.sort(key=lambda r: r.get("ts", 0))
    return rows


def split_windows(rows, window_sec):
    if not rows:
        return []
    start_ts = rows[0].get("ts", 0)
    windows = defaultdict(list)
    for r in rows:
        ts = r.get("ts", start_ts)
        idx = int((ts - start_ts) // window_sec)
        windows[idx].append(r)
    return [windows[k] for k in sorted(windows.keys())]


def switches_per_min(window_rows):
    control_seq = [r.get("a3", {}).get("control_mode") for r in window_rows]
    switches = sum(
        1 for i in range(1, len(control_seq))
        if control_seq[i] != control_seq[i - 1]
    )
    duration_sec = window_rows[-1]["ts"] - window_rows[0]["ts"]
    return switches / max(duration_sec / 60.0, 1e-6)


def guarded_p50(window_rows):
    jitter = compute_jitter(window_rows)
    guarded_dwell = jitter["dwell"].get("GUARDED", [])
    if not guarded_dwell:
        return 0.0
    return percentile(sorted(guarded_dwell), 50)


def vc_band_ratio(window_rows, low, high):
    vals = []
    modes = []
    for r in window_rows:
        view = r.get("view", {})
        vc = view.get("view_confidence")
        if vc is None:
            continue
        vals.append(vc)
        modes.append(r.get("a3", {}).get("control_mode"))
    if not vals:
        return 0.0, {}
    in_band = [(v, m) for v, m in zip(vals, modes) if low <= v <= high]
    ratio = len(in_band) / len(vals) if vals else 0.0
    mode_counter = Counter(m for _, m in in_band)
    total = sum(mode_counter.values()) or 1
    mode_ratio = {k: v / total for k, v in mode_counter.items()}
    return ratio, mode_ratio


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="trace jsonl paths (supports glob)")
    parser.add_argument("--window-sec", type=int, default=300, help="window size in seconds")
    parser.add_argument("--vc-band", default="0.35,0.45", help="vc band low,high")
    args = parser.parse_args()

    expanded = []
    for p in args.paths:
        matches = glob.glob(p)
        expanded.extend(matches if matches else [p])

    rows = load_rows(expanded)
    if not rows:
        print("Trace 为空或无法读取")
        return

    low_str, high_str = args.vc_band.split(",")
    low, high = float(low_str), float(high_str)

    windows = split_windows(rows, args.window_sec)
    total_windows = len(windows)

    diagnosis_hits = 0
    diagnosis_conf = []
    root_causes = []
    vc_band_ratios = []
    vc_band_mode_ratios = Counter()
    switches_per_min_vals = []
    guarded_p50_vals = []

    for w in windows:
        jitter = compute_jitter(w)
        diag = maybe_diagnose(jitter)
        if diag:
            diagnosis_hits += 1
            diagnosis_conf.append(diag["diagnosis"]["confidence"])
            root_causes.append(diag["diagnosis"]["root_cause"])

        ratio, mode_ratio = vc_band_ratio(w, low, high)
        vc_band_ratios.append(ratio)
        for k, v in mode_ratio.items():
            vc_band_mode_ratios[k] += v

        switches_per_min_vals.append(switches_per_min(w))
        guarded_p50_vals.append(guarded_p50(w))

    occurrence_ratio = diagnosis_hits / max(total_windows, 1)
    conf_mean, conf_std = mean_std(diagnosis_conf)
    root_cause_mode = Counter(root_causes).most_common(1)[0][0] if root_causes else "NONE"

    vc_band_ratio_mean = sum(vc_band_ratios) / max(len(vc_band_ratios), 1)
    switches_per_min_vals_sorted = sorted(switches_per_min_vals)
    guarded_p50_vals_sorted = sorted(guarded_p50_vals)

    switches_per_min_p95 = percentile(switches_per_min_vals_sorted, 95)
    guarded_p95 = percentile(guarded_p50_vals_sorted, 95)

    vc_band_mode_ratio = {}
    if vc_band_mode_ratios:
        total = sum(vc_band_mode_ratios.values()) or 1
        vc_band_mode_ratio = {k: v / total for k, v in vc_band_mode_ratios.items()}

    readiness = "READY" if occurrence_ratio >= 0.6 and root_cause_mode == "VC_THRESHOLD_OSCILLATION" else "NOT_READY"

    summary = {
        "windows": total_windows,
        "window_sec": args.window_sec,
        "diagnosis_occurrence_ratio": occurrence_ratio,
        "root_cause_mode": root_cause_mode,
        "confidence_mean": conf_mean,
        "confidence_std": conf_std,
        "vc_band_ratio_mean": vc_band_ratio_mean,
        "vc_band_mode_ratio": vc_band_mode_ratio,
        "switches_per_min_p95": switches_per_min_p95,
        "guarded_p95_sec": guarded_p95,
        "recommendation": {
            "action": "ADD_HYSTERESIS",
            "readiness": readiness,
            "apply_now": False,
        },
    }

    print("\n=== A3 Long-term Health ===")
    print(f"windows: {total_windows} ({args.window_sec // 60}-min)")
    print(f"diagnosis_occurrence_ratio: {occurrence_ratio:.2f}")
    print(f"root_cause_mode: {root_cause_mode}")
    print(f"confidence_mean/std: {conf_mean:.2f} / {conf_std:.2f}")
    print(f"vc_band_ratio_mean: {vc_band_ratio_mean:.2f}")
    print(f"switches_per_min p95: {switches_per_min_p95:.2f}")
    print(f"guarded_p95_sec: {guarded_p95:.2f}")
    print("recommendation:")
    print(f"  action: {summary['recommendation']['action']}")
    print(f"  readiness: {summary['recommendation']['readiness']}")

    out_path = Path("logs/a3_longterm_health.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\nJSON written to {out_path}")


if __name__ == "__main__":
    main()
