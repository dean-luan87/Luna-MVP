from core.logging import get_logger

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
log = get_logger("perf_dashboard")
"""
自动可视化 Dashboard 生成器
生成 HTML Dashboard，整合 YOLO 模型对比、链路压测等结果
"""

import os
import json
from datetime import datetime
from pathlib import Path


DASHBOARD_PATH = os.path.join("perf_logs", "perf_dashboard.html")


def load_json(path):
    """加载 JSON 文件"""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def main():
    os.makedirs("perf_logs", exist_ok=True)
    
    log.info("\n=== 生成性能 Dashboard ===\n")
    
    # 加载数据
    yolo_bench = load_json(os.path.join("perf_logs", "yolo_model_benchmark.json"))
    stress_result = load_json(os.path.join("perf_logs", "stress_realtime_result.json"))
    realtime_bench = load_json(os.path.join("test_reports", "benchmark_realtime_report.json"))
    
    # 准备 Chart.js 数据
    yolo_labels = []
    yolo_avg = []
    yolo_p95 = []
    
    if yolo_bench and "models" in yolo_bench:
        for m in yolo_bench["models"]:
            yolo_labels.append(m["model"])
            yolo_avg.append(m.get("avg", 0))
            yolo_p95.append(m.get("p95", 0))
    
    stress_labels = []
    stress_latencies = []
    if stress_result and "latencies" in stress_result:
        # 只取前100个点，避免图表过于密集
        latencies = stress_result["latencies"][:100]
        for idx, v in enumerate(latencies):
            stress_labels.append(idx)
            stress_latencies.append(v)
    
    # 全链路 Benchmark 数据
    pipeline_labels = []
    pipeline_values = []
    if realtime_bench and "segment_totals" in realtime_bench:
        for segment, value in realtime_bench["segment_totals"].items():
            pipeline_labels.append(segment)
            pipeline_values.append(value)
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Luna Badge 性能 Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif;
      background: linear-gradient(135deg, #0b1120 0%, #1e293b 100%);
      color: #e5e7eb;
      margin: 0;
      padding: 20px;
      min-height: 100vh;
    }}
    .container {{
      max-width: 1400px;
      margin: 0 auto;
    }}
    h1 {{
      color: #f9fafb;
      margin-bottom: 10px;
      font-size: 2rem;
    }}
    .header {{
      margin-bottom: 30px;
    }}
    .tag {{
      display: inline-block;
      background: #1e293b;
      color: #f9fafb;
      border-radius: 999px;
      padding: 6px 12px;
      margin-right: 8px;
      margin-bottom: 8px;
      font-size: 12px;
      border: 1px solid #334155;
    }}
    .card {{
      background: #111827;
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 20px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.4);
      border: 1px solid #1e293b;
    }}
    .card h2 {{
      color: #f9fafb;
      margin-bottom: 16px;
      font-size: 1.25rem;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
      gap: 20px;
    }}
    canvas {{
      background: #020617;
      border-radius: 8px;
      padding: 12px;
      max-height: 400px;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
      margin-top: 16px;
    }}
    .stat-item {{
      background: #1e293b;
      padding: 12px;
      border-radius: 8px;
      border-left: 3px solid #3b82f6;
    }}
    .stat-label {{
      font-size: 12px;
      color: #9ca3af;
      margin-bottom: 4px;
    }}
    .stat-value {{
      font-size: 20px;
      color: #f9fafb;
      font-weight: 600;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🚀 Luna Badge 性能 Dashboard</h1>
      <div class="tag">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
      <div class="tag">数据目录: perf_logs/</div>
      <div class="tag">版本: 1.3.0</div>
    </div>

    <div class="grid">
      <div class="card">
        <h2>YOLO 模型对比 (avg / p95)</h2>
        <canvas id="yoloChart"></canvas>
        <div class="stats" id="yoloStats"></div>
      </div>

      <div class="card">
        <h2>链路压测延迟曲线</h2>
        <canvas id="stressChart"></canvas>
        <div class="stats" id="stressStats"></div>
      </div>
    </div>

    <div class="card">
      <h2>全链路各段耗时分布</h2>
      <canvas id="pipelineChart"></canvas>
    </div>
  </div>

  <script>
    // 数据
    const yoloLabels = {json.dumps(yolo_labels, ensure_ascii=False)};
    const yoloAvg = {json.dumps(yolo_avg)};
    const yoloP95 = {json.dumps(yolo_p95)};

    const stressLabels = {json.dumps(stress_labels)};
    const stressLatencies = {json.dumps(stress_latencies)};

    const pipelineLabels = {json.dumps(pipeline_labels, ensure_ascii=False)};
    const pipelineValues = {json.dumps(pipeline_values)};

    // Chart.js 配置
    const chartOptions = {{
      responsive: true,
      maintainAspectRatio: true,
      plugins: {{
        legend: {{ 
          labels: {{ color: '#e5e7eb' }},
          position: 'top'
        }},
        tooltip: {{
          backgroundColor: 'rgba(0,0,0,0.8)',
          titleColor: '#f9fafb',
          bodyColor: '#e5e7eb',
          borderColor: '#3b82f6',
          borderWidth: 1
        }}
      }},
      scales: {{
        x: {{
          ticks: {{ color: '#9ca3af' }},
          grid: {{ color: 'rgba(55,65,81,0.3)' }}
        }},
        y: {{
          ticks: {{ color: '#9ca3af' }},
          grid: {{ color: 'rgba(55,65,81,0.3)' }},
          beginAtZero: true
        }}
      }}
    }};

    // YOLO Chart
    if (yoloLabels.length > 0) {{
      const ctxYolo = document.getElementById('yoloChart').getContext('2d');
      new Chart(ctxYolo, {{
        type: 'bar',
        data: {{
          labels: yoloLabels,
          datasets: [
            {{
              label: 'avg 延迟 (ms)',
              data: yoloAvg,
              backgroundColor: 'rgba(59, 130, 246, 0.6)',
              borderColor: 'rgba(59, 130, 246, 1)',
              borderWidth: 2
            }},
            {{
              label: 'p95 延迟 (ms)',
              data: yoloP95,
              backgroundColor: 'rgba(16, 185, 129, 0.6)',
              borderColor: 'rgba(16, 185, 129, 1)',
              borderWidth: 2
            }}
          ]
        }},
        options: chartOptions
      }});

      // 显示统计信息
      const yoloStats = document.getElementById('yoloStats');
      yoloLabels.forEach((label, idx) => {{
        const stat = document.createElement('div');
        stat.className = 'stat-item';
        stat.innerHTML = `
          <div class="stat-label">${{label}}</div>
          <div class="stat-value">${{yoloAvg[idx].toFixed(2)}}ms</div>
        `;
        yoloStats.appendChild(stat);
      }});
    }} else {{
      document.getElementById('yoloChart').parentElement.innerHTML = '<p style="color: #9ca3af;">暂无 YOLO 模型对比数据</p>';
    }}

    // Stress Chart
    if (stressLabels.length > 0) {{
      const ctxStress = document.getElementById('stressChart').getContext('2d');
      new Chart(ctxStress, {{
        type: 'line',
        data: {{
          labels: stressLabels,
          datasets: [
            {{
              label: '链路延迟 (ms)',
              data: stressLatencies,
              fill: false,
              tension: 0.15,
              borderColor: 'rgba(236, 72, 153, 1)',
              backgroundColor: 'rgba(236, 72, 153, 0.1)',
              borderWidth: 2,
              pointRadius: 0
            }}
          ]
        }},
        options: chartOptions
      }});

      // 显示统计信息
      const stressStats = document.getElementById('stressStats');
      const avg = stressLatencies.reduce((a, b) => a + b, 0) / stressLatencies.length;
      const max = Math.max(...stressLatencies);
      const min = Math.min(...stressLatencies);
      
      const stats = [
        {{label: '平均延迟', value: avg.toFixed(2) + 'ms'}},
        {{label: '最大延迟', value: max.toFixed(2) + 'ms'}},
        {{label: '最小延迟', value: min.toFixed(2) + 'ms'}},
        {{label: '样本数', value: stressLatencies.length}}
      ];
      
      stats.forEach(stat => {{
        const statEl = document.createElement('div');
        statEl.className = 'stat-item';
        statEl.innerHTML = `
          <div class="stat-label">${{stat.label}}</div>
          <div class="stat-value">${{stat.value}}</div>
        `;
        stressStats.appendChild(statEl);
      }});
    }} else {{
      document.getElementById('stressChart').parentElement.innerHTML = '<p style="color: #9ca3af;">暂无压测数据</p>';
    }}

    // Pipeline Chart
    if (pipelineLabels.length > 0) {{
      const ctxPipeline = document.getElementById('pipelineChart').getContext('2d');
      new Chart(ctxPipeline, {{
        type: 'doughnut',
        data: {{
          labels: pipelineLabels,
          datasets: [
            {{
              data: pipelineValues,
              backgroundColor: [
                'rgba(59, 130, 246, 0.8)',
                'rgba(16, 185, 129, 0.8)',
                'rgba(236, 72, 153, 0.8)',
                'rgba(251, 191, 36, 0.8)',
                'rgba(139, 92, 246, 0.8)',
                'rgba(239, 68, 68, 0.8)',
                'rgba(34, 197, 94, 0.8)'
              ],
              borderColor: '#1e293b',
              borderWidth: 2
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: true,
          plugins: {{
            legend: {{ 
              labels: {{ color: '#e5e7eb' }},
              position: 'right'
            }},
            tooltip: {{
              backgroundColor: 'rgba(0,0,0,0.8)',
              titleColor: '#f9fafb',
              bodyColor: '#e5e7eb',
              borderColor: '#3b82f6',
              borderWidth: 1
            }}
          }}
        }}
      }});
    }} else {{
      document.getElementById('pipelineChart').parentElement.innerHTML = '<p style="color: #9ca3af;">暂无全链路数据</p>';
    }}
  </script>
</body>
</html>
"""

    with open(DASHBOARD_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    
    log.info(f"✅ Dashboard 已生成: {DASHBOARD_PATH}")
    log.info("   用浏览器打开即可查看图表。")
    log.info(f"   文件路径: {os.path.abspath(DASHBOARD_PATH)}")


if __name__ == "__main__":
    main()


















