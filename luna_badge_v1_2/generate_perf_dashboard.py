from core.logging import get_logger

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
log = get_logger("generate_perf_dashboard")
"""
从 perf_logs 中最新的一组采样文件生成可视化 Dashboard：

- 折线：total_ms / det_ms / nav_ms
- 折线：FPS
- 条形：det/nav/overhead 平均耗时
"""

import os
import csv
import json
from pathlib import Path
import html

PERF_DIR = Path("perf_logs")


def _latest_pair():
    """找到最新的一组 *_samples.csv + *_report.json"""
    csv_files = sorted(PERF_DIR.glob("*_samples.csv"))
    if not csv_files:
        raise RuntimeError("perf_logs 下没有 *_samples.csv 文件，可先跑 demo_realtime_navigation.py 采样")
    csv_path = csv_files[-1]
    base = csv_path.stem.replace("_samples", "")
    json_path = PERF_DIR / f"{base}_report.json"
    if not json_path.exists():
        raise RuntimeError(f"未找到对应报告文件: {json_path}")
    return csv_path, json_path, base


def main():
    os.makedirs(PERF_DIR, exist_ok=True)
    csv_path, json_path, base = _latest_pair()

    log.info(f"[INFO] 读取采样文件: {csv_path.name}")
    log.info(f"[INFO] 读取报告文件: {json_path.name}")

    # 读取 samples
    frames = []
    det_ms = []
    nav_ms = []
    total_ms = []
    fps = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            frames.append(int(row["frame"]))
            det_ms.append(float(row["det_ms"]))
            nav_ms.append(float(row["nav_ms"]))
            total_ms.append(float(row["total_ms"]))
            fps.append(float(row["fps"]))

    # 读取报告
    with open(json_path, "r", encoding="utf-8") as f:
        report = json.load(f)

    overhead_ms = [t - d - n for t, d, n in zip(total_ms, det_ms, nav_ms)]
    avg_det = report.get("avg_det", 0.0)
    avg_nav = report.get("avg_nav", 0.0)
    avg_total = report.get("avg_total", 0.0)
    avg_overhead = max(avg_total - avg_det - avg_nav, 0.0)

    html_path = PERF_DIR / f"{base}_dashboard.html"

    # 直接内嵌数据，使用 Chart.js CDN
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>Luna Badge 性能 Dashboard - {html.escape(base)}</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #111; color: #eee; padding: 16px; }}
    h1, h2 {{ margin-bottom: 8px; }}
    .card {{ background: #1b1b1b; border-radius: 12px; padding: 16px; margin-bottom: 16px; box-shadow: 0 0 8px rgba(0,0,0,0.4); }}
    canvas {{ max-width: 100%; }}
    .stats-grid {{ display: flex; flex-wrap: wrap; gap: 16px; }}
    .stat-item {{ flex: 1 1 180px; background: #222; border-radius: 8px; padding: 12px; }}
    .label {{ font-size: 12px; color: #aaa; }}
    .value {{ font-size: 20px; font-weight: 600; }}
  </style>
</head>
<body>
  <h1>Luna Badge 性能 Dashboard</h1>
  <div class="card">
    <div class="stats-grid">
      <div class="stat-item">
        <div class="label">模式</div>
        <div class="value">{html.escape(str(report.get("mode", "")))}</div>
      </div>
      <div class="stat-item">
        <div class="label">标签</div>
        <div class="value">{html.escape(str(report.get("tag", "")))}</div>
      </div>
      <div class="stat-item">
        <div class="label">样本数</div>
        <div class="value">{report.get("count", 0)}</div>
      </div>
      <div class="stat-item">
        <div class="label">平均总延迟(ms)</div>
        <div class="value">{report.get("avg_total", 0.0):.1f}</div>
      </div>
      <div class="stat-item">
        <div class="label">P95(ms)</div>
        <div class="value">{report.get("p95", 0.0):.1f}</div>
      </div>
      <div class="stat-item">
        <div class="label">P99(ms)</div>
        <div class="value">{report.get("p99", 0.0):.1f}</div>
      </div>
    </div>
  </div>

  <div class="card">
    <h2>全链路延迟（ms）</h2>
    <canvas id="latencyChart"></canvas>
  </div>

  <div class="card">
    <h2>FPS 曲线</h2>
    <canvas id="fpsChart"></canvas>
  </div>

  <div class="card">
    <h2>平均耗时拆分</h2>
    <canvas id="avgChart"></canvas>
  </div>

  <script>
    const frames = {frames};
    const detMs = {det_ms};
    const navMs = {nav_ms};
    const totalMs = {total_ms};
    const fpsArr = {fps};
    const overheadMs = {overhead_ms};
    const avgDet = {avg_det:.3f};
    const avgNav = {avg_nav:.3f};
    const avgOverhead = {avg_overhead:.3f};
    const avgTotal = {avg_total:.3f};

    // 延迟曲线
    const ctxLatency = document.getElementById('latencyChart').getContext('2d');
    new Chart(ctxLatency, {{
      type: 'line',
      data: {{
        labels: frames,
        datasets: [
          {{
            label: 'total_ms',
            data: totalMs,
            borderWidth: 1,
            borderColor: 'rgb(255, 99, 132)',
          }},
          {{
            label: 'det_ms',
            data: detMs,
            borderWidth: 1,
            borderColor: 'rgb(54, 162, 235)',
          }},
          {{
            label: 'nav_ms',
            data: navMs,
            borderWidth: 1,
            borderColor: 'rgb(75, 192, 192)',
          }}
        ]
      }},
      options: {{
        responsive: true,
        plugins: {{
          legend: {{ labels: {{ color: '#eee' }} }},
        }},
        scales: {{
          x: {{ title: {{ display: true, text: 'frame', color: '#aaa' }}, ticks: {{ color: '#aaa' }}, grid: {{ color: '#333' }} }},
          y: {{ title: {{ display: true, text: 'ms', color: '#aaa' }}, ticks: {{ color: '#aaa' }}, grid: {{ color: '#333' }} }}
        }}
      }}
    }});

    // FPS 曲线
    const ctxFps = document.getElementById('fpsChart').getContext('2d');
    new Chart(ctxFps, {{
      type: 'line',
      data: {{
        labels: frames,
        datasets: [
          {{
            label: 'fps',
            data: fpsArr,
            borderWidth: 1,
            borderColor: 'rgb(255, 206, 86)',
          }}
        ]
      }},
      options: {{
        responsive: true,
        plugins: {{
          legend: {{ labels: {{ color: '#eee' }} }},
        }},
        scales: {{
          x: {{ title: {{ display: true, text: 'frame', color: '#aaa' }}, ticks: {{ color: '#aaa' }}, grid: {{ color: '#333' }} }},
          y: {{ title: {{ display: true, text: 'fps', color: '#aaa' }}, ticks: {{ color: '#aaa' }}, grid: {{ color: '#333' }} }}
        }}
      }}
    }});

    // 平均耗时
    const ctxAvg = document.getElementById('avgChart').getContext('2d');
    new Chart(ctxAvg, {{
      type: 'bar',
      data: {{
        labels: ['det_ms', 'nav_ms', 'overhead', 'total_ms'],
        datasets: [
          {{
            label: 'avg ms',
            data: [avgDet, avgNav, avgOverhead, avgTotal],
            backgroundColor: [
              'rgba(54, 162, 235, 0.8)',
              'rgba(75, 192, 192, 0.8)',
              'rgba(153, 102, 255, 0.8)',
              'rgba(255, 99, 132, 0.8)'
            ]
          }}
        ]
      }},
      options: {{
        responsive: true,
        plugins: {{
          legend: {{ labels: {{ color: '#eee' }} }},
        }},
        scales: {{
          y: {{
            beginAtZero: true,
            title: {{ display: true, text: 'ms', color: '#aaa' }},
            ticks: {{ color: '#aaa' }},
            grid: {{ color: '#333' }}
          }},
          x: {{
            ticks: {{ color: '#aaa' }},
            grid: {{ color: '#333' }}
          }}
        }}
      }}
    }});
  </script>
</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    log.info(f"[INFO] Dashboard 生成完成：{html_path}")
    log.info(f"[INFO] 在浏览器中打开：open {html_path}")


if __name__ == "__main__":
    main()






