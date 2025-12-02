"""
生成增强版 dashboard_nav.html：

  - 在原有指标基础上增加 NAV_STUCK 显示

  - 不修改现有 dashboard.html
"""

import json
from pathlib import Path


REPORT_DIR = Path("test_reports")


def _load(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def gen_dashboard_nav():
    summary = _load(REPORT_DIR / "summary.json", {})
    lnb = _load(REPORT_DIR / "lnb_score_nav.json", {})
    navm = _load(REPORT_DIR / "stress_nav_metrics.json", {})

    total = summary.get("total", 0)
    passed = summary.get("passed", 0)
    pass_rate = 100.0 * passed / total if total else 0.0

    total_score = lnb.get("total_score", 0.0)
    nav_stuck_errors = int(navm.get("nav_stuck_errors", 0))

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>Luna Badge v1.3.x Dashboard (NAV+)</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #020617; color: #e5e7eb; }}
    .container {{ max-width: 1080px; margin: 32px auto; padding: 16px; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }}
    .card {{ background: #020617; border-radius: 12px; padding: 16px; border: 1px solid #1f2937; box-shadow: 0 10px 40px rgba(15,23,42,0.8); }}
    .card h2 {{ font-size: 16px; margin-bottom: 8px; color: #93c5fd; }}
    .metric {{ font-size: 14px; margin-top: 4px; }}
    .metric span.label {{ color: #9ca3af; margin-right: 4px; }}
    .badge-ok {{ color: #22c55e; }}
    .badge-warn {{ color: #eab308; }}
    .badge-bad {{ color: #f97316; }}
    .title {{ font-size: 22px; margin-bottom: 4px; }}
    .subtitle {{ font-size: 13px; color: #9ca3af; margin-bottom: 16px; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="title">Luna Badge v1.3.x - 视角导航监控总览（NAV+ 扩展）</div>
    <div class="subtitle">包含 NAV_STUCK 导航卡死监控的增强版仪表盘</div>

    <div class="grid">
      <div class="card">
        <h2>测试总览</h2>
        <div class="metric"><span class="label">总模块数:</span>{total}</div>
        <div class="metric"><span class="label">通过模块:</span>{passed}</div>
        <div class="metric"><span class="label">通过率:</span>{pass_rate:.1f}%</div>
      </div>

      <div class="card">
        <h2>LNB v1.1 评分</h2>
        <div class="metric"><span class="label">总分:</span>{total_score:.2f}</div>
      </div>

      <div class="card">
        <h2>NAV_STUCK 稳定性</h2>
        <div class="metric">
          <span class="label">导航卡死事件数:</span>
          <span class="{{ 'badge-ok' if nav_stuck_errors == 0 else ('badge-warn' if nav_stuck_errors <= 3 else 'badge-bad') }}">
            {nav_stuck_errors}
          </span>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

    out_path = REPORT_DIR / "dashboard_nav.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path


if __name__ == "__main__":
    p = gen_dashboard_nav()
    print("dashboard_nav generated at", p)



