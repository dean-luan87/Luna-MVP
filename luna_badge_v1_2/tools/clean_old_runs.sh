#!/bin/bash
# -*- coding: utf-8 -*-
#
# 清理旧测试脚本
#
# 功能：
# - 清理指定天数之前的测试日志
# - 保留最新的 N 个测试
# - 安全删除（先显示预览）
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

LOG_DIR="perf_logs"

# 默认参数
DAYS_OLD=30
KEEP_LATEST=10
DRY_RUN=true

usage() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -d, --days N          删除 N 天前的日志（默认: 30）"
    echo "  -k, --keep N           保留最新的 N 个测试（默认: 10）"
    echo "  -f, --force            实际执行删除（默认: 仅预览）"
    echo "  -h, --help             显示帮助"
    echo ""
    echo "示例:"
    echo "  $0                     # 预览：删除 30 天前的日志，保留最新 10 个"
    echo "  $0 -d 7 -k 5           # 预览：删除 7 天前的日志，保留最新 5 个"
    echo "  $0 -d 7 -k 5 -f        # 实际执行删除"
    exit 1
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--days)
            DAYS_OLD="$2"
            shift 2
            ;;
        -k|--keep)
            KEEP_LATEST="$2"
            shift 2
            ;;
        -f|--force)
            DRY_RUN=false
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "未知参数: $1"
            usage
            ;;
    esac
done

echo "=========================================="
echo "  Luna Badge 日志清理工具"
echo "=========================================="
echo ""
echo "配置:"
echo "  - 删除 $DAYS_OLD 天前的日志"
echo "  - 保留最新的 $KEEP_LATEST 个测试"
echo "  - 模式: $([ "$DRY_RUN" = true ] && echo "预览（不会实际删除）" || echo "执行（将实际删除）")"
echo ""

if [ ! -d "$LOG_DIR" ]; then
    echo "❌ 日志目录不存在: $LOG_DIR"
    exit 1
fi

# 查找所有 JSONL 文件
FILES=($(ls -t "$LOG_DIR"/run_*.jsonl 2>/dev/null || true))

if [ ${#FILES[@]} -eq 0 ]; then
    echo "ℹ️  未找到任何日志文件"
    exit 0
fi

echo "找到 ${#FILES[@]} 个日志文件"
echo ""

# 按时间过滤
CUTOFF_DATE=$(date -v-${DAYS_OLD}d +%s 2>/dev/null || date -d "${DAYS_OLD} days ago" +%s)
TO_DELETE=()
TO_KEEP=()

for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        continue
    fi
    
    FILE_DATE=$(stat -f %m "$file" 2>/dev/null || stat -c %Y "$file" 2>/dev/null || echo 0)
    
    # 检查是否超过天数
    if [ $FILE_DATE -lt $CUTOFF_DATE ]; then
        TO_DELETE+=("$file")
    else
        TO_KEEP+=("$file")
    fi
done

# 保留最新的 N 个
if [ ${#TO_KEEP[@]} -gt $KEEP_LATEST ]; then
    # 按修改时间排序，保留最新的
    SORTED_KEEP=($(printf '%s\n' "${TO_KEEP[@]}" | xargs -I {} sh -c 'echo "$(stat -f %m "{}" 2>/dev/null || stat -c %Y "{}" 2>/dev/null || echo 0) {}"' | sort -rn | head -n $KEEP_LATEST | cut -d' ' -f2-))
    
    # 找出需要删除的
    for file in "${TO_KEEP[@]}"; do
        KEEP_THIS=false
        for keep_file in "${SORTED_KEEP[@]}"; do
            if [ "$file" = "$keep_file" ]; then
                KEEP_THIS=true
                break
            fi
        done
        if [ "$KEEP_THIS" = false ]; then
            TO_DELETE+=("$file")
        fi
    done
fi

# 显示结果
echo "将保留的文件 (${#TO_KEEP[@]} 个):"
for file in "${TO_KEEP[@]}"; do
    if printf '%s\n' "${TO_DELETE[@]}" | grep -q "^$file$"; then
        continue  # 这个文件实际上会被删除（因为要保留最新的 N 个）
    fi
    echo "  ✅ $(basename "$file")"
done
echo ""

if [ ${#TO_DELETE[@]} -eq 0 ]; then
    echo "✅ 没有需要删除的文件"
    exit 0
fi

echo "将删除的文件 (${#TO_DELETE[@]} 个):"
TOTAL_SIZE=0
for file in "${TO_DELETE[@]}"; do
    SIZE=$(stat -f %z "$file" 2>/dev/null || stat -c %s "$file" 2>/dev/null || echo 0)
    TOTAL_SIZE=$((TOTAL_SIZE + SIZE))
    echo "  ❌ $(basename "$file") ($(numfmt --to=iec-i --suffix=B $SIZE 2>/dev/null || echo "${SIZE}B"))"
    
    # 同时删除相关文件
    BASE="${file%.jsonl}"
    for ext in csv html; do
        if [ -f "${BASE}.${ext}" ]; then
            EXT_SIZE=$(stat -f %z "${BASE}.${ext}" 2>/dev/null || stat -c %s "${BASE}.${ext}" 2>/dev/null || echo 0)
            TOTAL_SIZE=$((TOTAL_SIZE + EXT_SIZE))
            echo "     └─ $(basename "${BASE}.${ext}") ($(numfmt --to=iec-i --suffix=B $EXT_SIZE 2>/dev/null || echo "${EXT_SIZE}B"))"
        fi
    done
    
    # 删除报告文件
    REPORT="${LOG_DIR}/report_$(basename "$file" .jsonl | sed 's/^run_//').md"
    if [ -f "$REPORT" ]; then
        REPORT_SIZE=$(stat -f %z "$REPORT" 2>/dev/null || stat -c %s "$REPORT" 2>/dev/null || echo 0)
        TOTAL_SIZE=$((TOTAL_SIZE + REPORT_SIZE))
        echo "     └─ $(basename "$REPORT") ($(numfmt --to=iec-i --suffix=B $REPORT_SIZE 2>/dev/null || echo "${REPORT_SIZE}B"))"
    fi
done

echo ""
echo "预计释放空间: $(numfmt --to=iec-i --suffix=B $TOTAL_SIZE 2>/dev/null || echo "${TOTAL_SIZE}B")"
echo ""

# 执行删除
if [ "$DRY_RUN" = true ]; then
    echo "ℹ️  这是预览模式，不会实际删除文件"
    echo "   要实际执行删除，请使用: $0 -f"
else
    read -p "确认删除以上文件? (yes/no) " -r
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        echo "❌ 已取消"
        exit 0
    fi
    
    DELETED=0
    for file in "${TO_DELETE[@]}"; do
        if rm -f "$file"; then
            DELETED=$((DELETED + 1))
        fi
        
        # 删除相关文件
        BASE="${file%.jsonl}"
        rm -f "${BASE}.csv" "${BASE}.html"
        
        # 删除报告文件
        REPORT="${LOG_DIR}/report_$(basename "$file" .jsonl | sed 's/^run_//').md"
        rm -f "$REPORT"
    done
    
    echo ""
    echo "✅ 已删除 $DELETED 个日志文件及其相关文件"
fi

echo ""
echo "=========================================="


