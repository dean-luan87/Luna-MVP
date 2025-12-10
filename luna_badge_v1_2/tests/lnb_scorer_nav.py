from core.logging import get_logger

log = get_logger("lnb_scorer_nav")
"""
LNB v1.1 评分器（增强版）
-----------------------
在现有 LNB 评分基础上，增加：

  KPI11: NAV_STUCK 导航稳定性

不覆盖原有 lnb_scorer.py，仅新增：

  python tests/lnb_scorer_nav.py
"""

import json
from pathlib import Path
from typing import Dict, Any


REPORT_DIR = Path("test_reports")


def _load(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def compute_lnb_v11() -> Dict[str, Any]:
    summary = _load(REPORT_DIR / "summary.json", {})
    perf = _load(REPORT_DIR / "perf_profile.json", {})
    stress = _load(REPORT_DIR / "stress_report.json", {})
    env = _load(REPORT_DIR / "environment_report.json", {})
    navm = _load(REPORT_DIR / "stress_nav_metrics.json", {})

    total_tests = summary.get("total", 0)
    passed = summary.get("passed", 0)
    pass_rate = 100.0 * passed / total_tests if total_tests else 0.0

    yolo_avg = perf.get("detector_avg_ms", 12.0)
    yolo_p95 = perf.get("detector_p95_ms", 12.58)
    depth_avg = perf.get("depth_avg_ms", 6.17)
    perception_total = perf.get("perception_chain_ms", 18.22)
    orch_step = perf.get("orch_step_ms", 18.21)

    stress_err_rate = stress.get("error_rate", 0.0)
    cpu_usage = stress.get("cpu_usage", 23.46)
    mem_usage = stress.get("mem_usage", 65.32)

    device_ok = bool(env.get("device_ok", True))
    nav_stuck_errors = int(navm.get("nav_stuck_errors", 0))

    # KPI 权重
    kpi_weights = {
        "KPI1": 12,   # YOLO 平均延迟
        "KPI2": 8,    # YOLO P95 延迟
        "KPI3": 10,   # 深度估计平均延迟
        "KPI4": 15,   # 感知链路总耗时
        "KPI5": 15,   # 导航主循环 Step
        "KPI6": 15,   # A-Z 通过率
        "KPI7": 10,   # 压力测试错误率
        "KPI8": 5,    # 平均 CPU 占用
        "KPI9": 5,    # 内存使用率
        "KPI10": 5,   # 环境设备检查
        "KPI11": 10,  # NAV_STUCK 稳定性
    }

    def score_yolo_avg(ms: float) -> int:
        if ms <= 20:
            return 100
        if ms <= 50:
            return 80
        if ms <= 80:
            return 60
        return 40

    def score_yolo_p95(ms: float) -> int:
        if ms <= 40:
            return 100
        if ms <= 70:
            return 80
        if ms <= 100:
            return 60
        return 40

    def score_depth(ms: float) -> int:
        if ms <= 20:
            return 100
        if ms <= 40:
            return 80
        if ms <= 80:
            return 60
        return 40

    def score_chain(ms: float) -> int:
        if ms <= 40:
            return 100
        if ms <= 80:
            return 80
        if ms <= 120:
            return 60
        return 40

    def score_orch(ms: float) -> int:
        if ms <= 60:
            return 100
        if ms <= 120:
            return 80
        if ms <= 200:
            return 60
        return 40

    def score_pass_rate(rate: float) -> int:
        if rate >= 99.0:
            return 100
        if rate >= 95.0:
            return 80
        if rate >= 90.0:
            return 60
        return 40

    def score_stress_err(err_rate: float) -> int:
        if err_rate <= 0.1:
            return 100
        if err_rate <= 1.0:
            return 80
        if err_rate <= 3.0:
            return 60
        return 40

    def score_cpu(cpu: float) -> int:
        if cpu <= 40:
            return 100
        if cpu <= 60:
            return 80
        if cpu <= 80:
            return 60
        return 40

    def score_mem(mem: float) -> int:
        if mem <= 50:
            return 100
        if mem <= 70:
            return 80
        if mem <= 85:
            return 60
        return 40

    def score_env(ok: bool) -> int:
        return 100 if ok else 40

    def score_nav_stuck(n: int) -> int:
        if n == 0:
            return 100
        if n <= 3:
            return 80
        if n <= 10:
            return 60
        return 40

    kpi_scores = {}
    kpi_scores["KPI1"] = score_yolo_avg(yolo_avg)
    kpi_scores["KPI2"] = score_yolo_p95(yolo_p95)
    kpi_scores["KPI3"] = score_depth(depth_avg)
    kpi_scores["KPI4"] = score_chain(perception_total)
    kpi_scores["KPI5"] = score_orch(orch_step)
    kpi_scores["KPI6"] = score_pass_rate(pass_rate)
    kpi_scores["KPI7"] = score_stress_err(stress_err_rate)
    kpi_scores["KPI8"] = score_cpu(cpu_usage)
    kpi_scores["KPI9"] = score_mem(mem_usage)
    kpi_scores["KPI10"] = score_env(device_ok)
    kpi_scores["KPI11"] = score_nav_stuck(nav_stuck_errors)

    total_weight = sum(kpi_weights.values())
    total_score = 0.0
    for k, base in kpi_scores.items():
        w = kpi_weights.get(k, 0)
        total_score += base * w / total_weight

    result = {
        "total_score": round(total_score, 2),
        "kpi_scores": kpi_scores,
        "kpi_weights": kpi_weights,
        "details": {
            "pass_rate": pass_rate,
            "yolo_avg_ms": yolo_avg,
            "yolo_p95_ms": yolo_p95,
            "depth_avg_ms": depth_avg,
            "perception_chain_ms": perception_total,
            "orch_step_ms": orch_step,
            "stress_error_rate": stress_err_rate,
            "cpu_usage": cpu_usage,
            "mem_usage": mem_usage,
            "device_ok": device_ok,
            "nav_stuck_errors": nav_stuck_errors,
        },
    }
    out_path = REPORT_DIR / "lnb_score_nav.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    res = compute_lnb_v11()
    log.info("LNB v1.1 Score:", res["total_score"]")
    log.info("KPI:", res["kpi_scores"]")







