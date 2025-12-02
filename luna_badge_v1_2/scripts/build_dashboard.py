#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard 生成脚本

功能：
- 读取 CSV 数据
- 生成交互式 HTML Dashboard
- 使用 ECharts 可视化
"""

import json
import csv
import sys
from pathlib import Path

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Luna Badge Perf Dashboard - {run_id}</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<style>
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    margin: 20px;
    background: #f5f5f5;
}}
h2 {{
    color: #333;
    margin-bottom: 20px;
}}
.chart-container {{
    background: white;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}}
.chart {{
    width: 100%;
    height: 400px;
}}
.stats {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-bottom: 20px;
}}
.stat-card {{
    background: white;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}}
.stat-label {{
    font-size: 12px;
    color: #666;
    margin-bottom: 5px;
}}
.stat-value {{
    font-size: 24px;
    font-weight: bold;
    color: #333;
}}
</style>
</head>
<body>
<h2>🌙 Luna Badge 性能 Dashboard - {run_id}</h2>

<div class="stats">
    <div class="stat-card">
        <div class="stat-label">总帧数</div>
        <div class="stat-value">{total_frames}</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">平均延迟</div>
        <div class="stat-value">{avg_latency:.1f}ms</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">P95 延迟</div>
        <div class="stat-value">{p95_latency:.1f}ms</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">P99 延迟</div>
        <div class="stat-value">{p99_latency:.1f}ms</div>
    </div>
</div>

<div class="chart-container">
    <h3>端到端延迟分布</h3>
    <div id="latency" class="chart"></div>
</div>

<div class="chart-container">
    <h3>各阶段平均耗时</h3>
    <div id="segments" class="chart"></div>
</div>

<div class="chart-container">
    <h3>延迟趋势（最近 100 帧）</h3>
    <div id="trend" class="chart"></div>
</div>

<script>
const data = {data_json};

// 计算统计数据
const latencies = data.map(d => d.end_to_end_ms || 0);
const avg = latencies.reduce((a, b) => a + b, 0) / latencies.length;
const sorted = [...latencies].sort((a, b) => a - b);
const p95 = sorted[Math.floor(sorted.length * 0.95)];
const p99 = sorted[Math.floor(sorted.length * 0.99)];

// 延迟分布图
const chart1 = echarts.init(document.getElementById('latency'));
chart1.setOption({{
    title: {{text: '端到端延迟分布', left: 'center'}},
    tooltip: {{trigger: 'axis'}},
    xAxis: {{
        type: 'category',
        data: data.map((d, i) => i + 1),
        name: '帧序号'
    }},
    yAxis: {{
        type: 'value',
        name: '延迟 (ms)'
    }},
    series: [{{
        type: 'line',
        data: latencies,
        smooth: true,
        lineStyle: {{color: '#667eea'}},
        areaStyle: {{color: 'rgba(102, 126, 234, 0.1)'}}
    }}]
}});

// 分段耗时图
const segments = {{
    capture: data.reduce((s, d) => s + (d.client_capture_ms || 0), 0) / data.length,
    encode: data.reduce((s, d) => s + (d.client_encode_ms || 0), 0) / data.length,
    upload: data.reduce((s, d) => s + (d.net_upload_ms || 0), 0) / data.length,
    infer: data.reduce((s, d) => s + (d.server_infer_ms || 0), 0) / data.length,
    download: data.reduce((s, d) => s + (d.net_download_ms || 0), 0) / data.length,
}};

const chart2 = echarts.init(document.getElementById('segments'));
chart2.setOption({{
    title: {{text: '各阶段平均耗时', left: 'center'}},
    tooltip: {{trigger: 'axis', axisPointer: {{type: 'shadow'}}}},
    xAxis: {{
        type: 'category',
        data: ['capture', 'encode', 'upload', 'infer', 'download']
    }},
    yAxis: {{
        type: 'value',
        name: '耗时 (ms)'
    }},
    series: [{{
        type: 'bar',
        data: [segments.capture, segments.encode, segments.upload, segments.infer, segments.download],
        itemStyle: {{
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {{offset: 0, color: '#667eea'}},
                {{offset: 1, color: '#764ba2'}}
            ])
        }}
    }}]
}});

// 趋势图（最近 100 帧）
const recentData = data.slice(-100);
const chart3 = echarts.init(document.getElementById('trend'));
chart3.setOption({{
    title: {{text: '延迟趋势（最近 100 帧）', left: 'center'}},
    tooltip: {{trigger: 'axis'}},
    xAxis: {{
        type: 'category',
        data: recentData.map((d, i) => i + 1),
        name: '帧序号'
    }},
    yAxis: {{
        type: 'value',
        name: '延迟 (ms)'
    }},
    series: [{{
        type: 'line',
        data: recentData.map(d => d.end_to_end_ms || 0),
        smooth: true,
        lineStyle: {{color: '#22c55e'}},
        markLine: {{
            data: [
                {{type: 'average', name: '平均值'}},
                {{yAxis: 250, name: '目标线'}}
            ]
        }}
    }}]
}});
</script>
</body>
</html>
"""


def build(path_jsonl: Path):
    """构建 Dashboard"""
    csv_path = path_jsonl.with_suffix(".csv")
    
    if not csv_path.exists():
        print(f"[ERROR] CSV 文件不存在: {csv_path}")
        print(f"[INFO] 请先运行: python3 scripts/analyze_perf.py {path_jsonl}")
        return
    
    # 读取 CSV
    data = []
    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 转换数值字段
            for key, value in row.items():
                if key != "frame_id" and key != "seq":
                    try:
                        row[key] = float(value) if value else 0.0
                    except ValueError:
                        row[key] = 0.0
            data.append(row)
    
    if not data:
        print(f"[ERROR] CSV 文件为空")
        return
    
    # 计算统计值
    latencies = [d.get("end_to_end_ms", 0) for d in data]
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    sorted_lat = sorted(latencies)
    p95_latency = sorted_lat[int(len(sorted_lat) * 0.95)] if sorted_lat else 0
    p99_latency = sorted_lat[int(len(sorted_lat) * 0.99)] if sorted_lat else 0
    
    # 生成 HTML
    html = TEMPLATE.format(
        run_id=path_jsonl.stem.replace("run_", ""),
        total_frames=len(data),
        avg_latency=avg_latency,
        p95_latency=p95_latency,
        p99_latency=p99_latency,
        data_json=json.dumps(data, ensure_ascii=False)
    )
    
    out = path_jsonl.with_suffix(".html")
    out.write_text(html, encoding="utf-8")
    print(f"✅ Dashboard 已生成: {out}")
    print(f"   在浏览器中打开查看")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 build_dashboard.py <jsonl_file>")
        sys.exit(1)
    
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"[ERROR] 文件不存在: {path}")
        sys.exit(1)
    
    build(path)


