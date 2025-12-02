#!/bin/bash
# -*- coding: utf-8 -*-
#
# 日志提取/打包脚本
#
# 功能：
# - 收集指定 run_id 的所有相关文件
# - 打包为 tar.gz 便于分享或归档
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

if [ $# -eq 0 ]; then
    echo "用法: $0 <run_id> [output_dir]"
    echo ""
    echo "示例:"
    echo "  $0 run_20251202_143022"
    echo "  $0 run_20251202_143022 /tmp/luna_logs"
    exit 1
fi

RUN_ID="$1"
OUTPUT_DIR="${2:-/tmp/luna_logs_${RUN_ID}}"

LOG_DIR="perf_logs"
JSONL_FILE="$LOG_DIR/${RUN_ID}.jsonl"
CSV_FILE="$LOG_DIR/${RUN_ID}.csv"
HTML_FILE="$LOG_DIR/${RUN_ID}.html"
REPORT_FILE="$LOG_DIR/report_${RUN_ID}.md"

echo "=========================================="
echo "  Luna Badge 日志收集工具"
echo "=========================================="
echo ""
echo "Run ID: $RUN_ID"
echo "输出目录: $OUTPUT_DIR"
echo ""

mkdir -p "$OUTPUT_DIR"

# 收集文件
FILES_COLLECTED=0

if [ -f "$JSONL_FILE" ]; then
    cp "$JSONL_FILE" "$OUTPUT_DIR/"
    echo "✅ 已复制: $JSONL_FILE"
    FILES_COLLECTED=$((FILES_COLLECTED + 1))
else
    echo "⚠️  未找到: $JSONL_FILE"
fi

if [ -f "$CSV_FILE" ]; then
    cp "$CSV_FILE" "$OUTPUT_DIR/"
    echo "✅ 已复制: $CSV_FILE"
    FILES_COLLECTED=$((FILES_COLLECTED + 1))
else
    echo "⚠️  未找到: $CSV_FILE"
fi

if [ -f "$HTML_FILE" ]; then
    cp "$HTML_FILE" "$OUTPUT_DIR/"
    echo "✅ 已复制: $HTML_FILE"
    FILES_COLLECTED=$((FILES_COLLECTED + 1))
else
    echo "⚠️  未找到: $HTML_FILE"
fi

if [ -f "$REPORT_FILE" ]; then
    cp "$REPORT_FILE" "$OUTPUT_DIR/"
    echo "✅ 已复制: $REPORT_FILE"
    FILES_COLLECTED=$((FILES_COLLECTED + 1))
else
    echo "⚠️  未找到: $REPORT_FILE"
fi

echo ""
if [ $FILES_COLLECTED -eq 0 ]; then
    echo "❌ 未找到任何文件，请检查 run_id 是否正确"
    exit 1
fi

# 创建 README
cat > "$OUTPUT_DIR/README.txt" <<EOF
Luna Badge 性能测试日志包

Run ID: $RUN_ID
收集时间: $(date "+%Y-%m-%d %H:%M:%S")

文件说明:
- ${RUN_ID}.jsonl: 原始性能日志（JSONL 格式）
- ${RUN_ID}.csv: CSV 格式数据（供 Excel 分析）
- ${RUN_ID}.html: 交互式 Dashboard（在浏览器中打开）
- report_${RUN_ID}.md: 运营测试报告（Markdown 格式）

使用方法:
1. 打开 Dashboard: 在浏览器中打开 ${RUN_ID}.html
2. 查看报告: 打开 report_${RUN_ID}.md
3. 数据分析: 使用 Excel 或其他工具打开 ${RUN_ID}.csv
EOF

echo "✅ 已创建 README.txt"
echo ""

# 打包
ARCHIVE="${OUTPUT_DIR}.tar.gz"
cd "$(dirname "$OUTPUT_DIR")"
tar -czf "$ARCHIVE" "$(basename "$OUTPUT_DIR")" 2>/dev/null || {
    echo "⚠️  打包失败，但文件已收集到: $OUTPUT_DIR"
    exit 0
}

echo "=========================================="
echo "  日志收集完成！"
echo "=========================================="
echo ""
echo "📦 收集的文件数: $FILES_COLLECTED"
echo "📁 输出目录: $OUTPUT_DIR"
echo "📦 压缩包: $ARCHIVE"
echo ""
echo "💡 提示:"
echo "  - 查看文件: ls -lh $OUTPUT_DIR"
echo "  - 解压包: tar -xzf $ARCHIVE"
echo ""


