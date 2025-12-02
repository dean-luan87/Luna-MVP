#!/bin/bash
# -*- coding: utf-8 -*-
#
# Luna Badge 超级一键运营测试脚本（含自动启动服务器）
#
# 功能：
# - 自动启动后端服务器
# - 自动生成 run_id
# - 引导测试流程
# - 自动分析 + Dashboard + 对比报告
# - 生成 Markdown 运营报告
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

#############################################
# 可配置区域：按你实际项目改这几行
#############################################

# 后端启动命令
SERVER_CMD=${SERVER_CMD:-"python3 realtime_server.py --host 0.0.0.0 --port 8899 --model yolo11n.pt --ssl-keyfile ssl_certs/key.pem --ssl-certfile ssl_certs/cert.pem"}

# Web 端测试页面路径
TEST_PAGE_PATH=${TEST_PAGE_PATH:-"/static/ios_realtime_test.html"}

# 性能日志目录
LOG_DIR=${LOG_DIR:-"perf_logs"}

# 分析脚本
ANALYZE_SCRIPT=${ANALYZE_SCRIPT:-"scripts/analyze_perf.py"}
DASHBOARD_SCRIPT=${DASHBOARD_SCRIPT:-"scripts/build_dashboard.py"}
COMPARE_SCRIPT=${COMPARE_SCRIPT:-"scripts/compare_models.py"}

#############################################
# 以下代码一般不用改
#############################################

mkdir -p "$LOG_DIR"

RUN_ID="run_$(date +%Y%m%d_%H%M%S)"
SERVER_LOG="$LOG_DIR/server_${RUN_ID}.log"
REPORT_MD="$LOG_DIR/report_${RUN_ID}.md"

echo "============================================"
echo "  Luna Badge 一键运营测试启动"
echo "  RUN_ID: $RUN_ID"
echo "============================================"
echo ""

# 1. 启动后端服务器
if pgrep -f "realtime_server.py" > /dev/null; then
    echo "ℹ️  后端服务已在运行"
    SERVER_PID=$(pgrep -f "realtime_server.py" | head -1)
    echo "   后端 PID: $SERVER_PID"
else
    echo "▶ 启动后端服务器（日志：$SERVER_LOG）"
    echo "  命令：$SERVER_CMD"
    nohup $SERVER_CMD > "$SERVER_LOG" 2>&1 &
    SERVER_PID=$!
    echo "  后端 PID: $SERVER_PID"
    echo ""
    
    # 等待服务器就绪
    echo "▶ 等待服务器启动..."
    sleep 5
fi

# 2. 提示手机访问地址
LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
if [ -z "$LOCAL_IP" ]; then
    LOCAL_IP="你的电脑IP"
fi

echo "============================================"
echo "请在 iPhone Safari 中打开以下地址进行真实测试："
echo ""
echo "  https://${LOCAL_IP}:8899${TEST_PAGE_PATH}"
echo ""
echo "建议：边走边测试 30–120 秒，让系统持续推理。"
echo "============================================"
echo ""
read -p "测试完成后按回车继续数据分析… " _

# 3. 找最新一条 JSONL 日志

LATEST_JSONL=$(ls -t "$LOG_DIR"/run_*.jsonl 2>/dev/null | head -n 1 || true)

if [ -z "$LATEST_JSONL" ]; then
    echo "⚠ 未找到 perf_logs/run_*.jsonl 日志文件，请确认后端写日志逻辑。"
    echo "   分析步骤将跳过。"
    echo ""
    echo "如需停止后端，可执行： kill $SERVER_PID"
    exit 0
fi

echo ""
echo "▶ 使用日志文件进行分析：$LATEST_JSONL"

# 4. 运行分析脚本
if [ -f "$ANALYZE_SCRIPT" ]; then
    echo "▶ analyze_perf.py"
    ANALYZE_OUTPUT=$(python3 "$ANALYZE_SCRIPT" "$LATEST_JSONL" 2>&1 || echo "⚠ analyze_perf.py 运行失败")
    echo "$ANALYZE_OUTPUT"
else
    echo "⚠ 未找到 $ANALYZE_SCRIPT，跳过性能分析。"
    ANALYZE_OUTPUT=""
fi

# 5. 生成 Dashboard
DASHBOARD_HTML="${LATEST_JSONL%.jsonl}.html"
if [ -f "$DASHBOARD_SCRIPT" ]; then
    echo ""
    echo "▶ build_dashboard.py"
    python3 "$DASHBOARD_SCRIPT" "$LATEST_JSONL" || echo "⚠ build_dashboard.py 运行失败"
    echo "Dashboard: $DASHBOARD_HTML"
else
    echo "⚠ 未找到 $DASHBOARD_SCRIPT，跳过 Dashboard。"
fi

# 6. 模型对比（如果有多次 run_*.jsonl）
if [ -f "$COMPARE_SCRIPT" ]; then
    echo ""
    echo "▶ compare_models.py"
    COMPARE_OUTPUT=$(python3 "$COMPARE_SCRIPT" "$LOG_DIR"/run_*.jsonl 2>&1 || echo "⚠ compare_models.py 运行失败")
    echo "$COMPARE_OUTPUT"
else
    echo "⚠ 未找到 $COMPARE_SCRIPT，跳过模型对比。"
    COMPARE_OUTPUT=""
fi

# 7. 生成 Markdown 报告
echo ""
echo "▶ 生成运营报告：$REPORT_MD"

# 提取关键统计信息（如果分析输出可用）
TOTAL_FRAMES=$(echo "$ANALYZE_OUTPUT" | grep "总帧数:" | awk '{print $2}' || echo "N/A")
AVG_LATENCY=$(echo "$ANALYZE_OUTPUT" | grep "平均:" | awk '{print $2}' | sed 's/ms//' || echo "N/A")
P95_LATENCY=$(echo "$ANALYZE_OUTPUT" | grep "P95:" | awk '{print $2}' | sed 's/ms//' || echo "N/A")
P99_LATENCY=$(echo "$ANALYZE_OUTPUT" | grep "P99:" | awk '{print $2}' | sed 's/ms//' || echo "N/A")
BOTTLENECK=$(echo "$ANALYZE_OUTPUT" | grep "建议优先优化:" | awk -F': ' '{print $2}' || echo "N/A")

cat <<EOF > "$REPORT"
# Luna Badge - 一键运营测试报告

**Run ID:** \`$RUN_ID\`

**日期：** $(date "+%Y-%m-%d %H:%M:%S")

---

## 1. 测试目的

验证以下内容是否达到正式版要求：

- ✅ 端到端延迟是否稳定 < 250ms
- ✅ 自动导航模式的稳定性
- ✅ 真实设备（iPhone）拍照 + YOLOv11 推理链路的性能
- ✅ 网络波动下的稳健性
- ✅ 推理瓶颈定位
- ✅ 模型与模型之间的性能差异

---

## 2. 测试环境

- **设备：** iPhone Safari
- **模型：** YOLOv11-tiny (yolo11n.pt)
- **运行方式：** WebSocket 实时流
- **连续导航模式：** 开启（200ms/frame）
- **心跳：** 开启
- **SSL：** 已启用（HTTPS）

---

## 3. 性能结果摘要

### 基础统计

- **总帧数：** $TOTAL_FRAMES
- **平均延迟：** ${AVG_LATENCY}ms
- **P95 延迟：** ${P95_LATENCY}ms
- **P99 延迟：** ${P99_LATENCY}ms

### 延迟目标达成情况

- **目标：** < 250ms
- **平均延迟：** ${AVG_LATENCY}ms $(if [ "$AVG_LATENCY" != "N/A" ] && (( $(echo "$AVG_LATENCY < 250" | bc -l 2>/dev/null || echo 0) )); then echo "✅ 达成"; else echo "⚠️ 未达成"; fi)
- **P95 延迟：** ${P95_LATENCY}ms $(if [ "$P95_LATENCY" != "N/A" ] && (( $(echo "$P95_LATENCY < 250" | bc -l 2>/dev/null || echo 0) )); then echo "✅ 达成"; else echo "⚠️ 未达成"; fi)

### Dashboard

📊 **交互式 Dashboard：** [$DASHBOARD_HTML]($DASHBOARD_HTML)

在浏览器中打开查看详细的可视化分析。

---

## 4. 模型对比结果

\`\`\`
$COMPARE_OUTPUT
\`\`\`

---

## 5. 瓶颈分析

### 主要瓶颈

**建议优先优化：** $BOTTLENECK

### 详细分析

\`\`\`
$ANALYZE_OUTPUT
\`\`\`

---

## 6. 总结 & 建议

### 性能评估

- **是否达成 250ms KPI：** 
  - 平均延迟：${AVG_LATENCY}ms $(if [ "$AVG_LATENCY" != "N/A" ] && (( $(echo "$AVG_LATENCY < 250" | bc -l 2>/dev/null || echo 0) )); then echo "✅"; else echo "❌"; fi)
  - P95 延迟：${P95_LATENCY}ms $(if [ "$P95_LATENCY" != "N/A" ] && (( $(echo "$P95_LATENCY < 250" | bc -l 2>/dev/null || echo 0) )); then echo "✅"; else echo "❌"; fi)

### 优化建议

1. **瓶颈优化：** 优先优化 $BOTTLENECK
2. **网络优化：** $(if echo "$ANALYZE_OUTPUT" | grep -q "net_"; then echo "检查网络延迟，考虑优化图像压缩或使用更快的网络"; else echo "网络延迟正常"; fi)
3. **客户端优化：** $(if echo "$ANALYZE_OUTPUT" | grep -q "client_encode"; then echo "考虑优化图像编码速度"; else echo "客户端处理正常"; fi)
4. **服务端优化：** $(if echo "$ANALYZE_OUTPUT" | grep -q "server_infer"; then echo "考虑使用更轻量的模型或优化推理速度"; else echo "服务端推理正常"; fi)

### YOLO 模型选择建议

根据本次测试结果：
- 当前模型：YOLOv11-tiny
- 性能表现：${AVG_LATENCY}ms 平均延迟
- 建议：$(if [ "$AVG_LATENCY" != "N/A" ] && (( $(echo "$AVG_LATENCY < 200" | bc -l 2>/dev/null || echo 0) )); then echo "当前模型性能良好，可继续使用"; else echo "可考虑测试更轻量的模型或优化推理流程"; fi)

---

## 7. 附件

- **原始日志：** \`$LATEST_JSONL\`
- **CSV 数据：** \`${LATEST_JSONL%.jsonl}.csv\`
- **Dashboard：** \`$DASHBOARD_HTML\`
- **后端日志：** \`$SERVER_LOG\`

---

**报告生成时间：** $(date "+%Y-%m-%d %H:%M:%S")

EOF

echo "✅ 报告已生成: $REPORT"
echo ""
echo "============================================"
echo "  一键运营测试完成"
echo "============================================"
echo ""
echo "📊 生成的文件："
echo "  - 日志：$LATEST_JSONL"
echo "  - Dashboard：$DASHBOARD_HTML"
echo "  - 报告：$REPORT_MD"
echo "  - 后端日志：$SERVER_LOG"
echo ""
echo "🌐 打开 Dashboard:"
echo "  open $DASHBOARD_HTML"
echo ""
echo "📝 查看报告:"
echo "  cat $REPORT_MD"
echo ""
echo "💡 提示："
echo "  - 如需停止后端，可执行： kill $SERVER_PID"
echo ""
