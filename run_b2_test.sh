#!/bin/bash
# B2 v0.2 缓存逻辑测试脚本

echo "=" | head -c 70; echo
echo "B2 v0.2 缓存逻辑测试"
echo "=" | head -c 70; echo
echo

# 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    exit 1
fi

echo "✅ 找到 python3: $(which python3)"
echo

# 检查 main.py
if [ ! -f "main.py" ]; then
    echo "❌ 错误: 未找到 main.py"
    exit 1
fi

echo "✅ 找到 main.py"
echo

# 运行 pipeline 并输出日志
echo "📋 开始运行 pipeline..."
echo "   日志将保存到: b2_log.txt"
echo "   按 Ctrl+C 停止运行"
echo

python3 main.py > b2_log.txt 2>&1 &
PIPELINE_PID=$!

echo "   Pipeline PID: $PIPELINE_PID"
echo "   运行中... (等待几秒后按 Ctrl+C 停止)"
echo

# 等待几秒
sleep 5

# 停止 pipeline
kill $PIPELINE_PID 2>/dev/null
wait $PIPELINE_PID 2>/dev/null

echo
echo "✅ Pipeline 已停止"
echo

# 检查日志
if [ -f "b2_log.txt" ]; then
    LOG_SIZE=$(wc -l < b2_log.txt)
    echo "📋 日志文件: b2_log.txt ($LOG_SIZE 行)"
    echo
    
    # 查找 B2 相关日志
    echo "📋 B2 相关日志:"
    grep -E "\[B2\]|\[B2-v0\.2\]" b2_log.txt | head -20 || echo "   未找到 B2 日志"
    echo
    
    # 使用观测工具分析
    echo "📋 使用观测工具分析..."
    python3 -m vision_pipeline.b2.b2_cache_observer b2_log.txt 2>&1 || echo "   观测工具运行失败（可能需要更多日志数据）"
else
    echo "❌ 日志文件未生成"
fi

echo
echo "=" | head -c 70; echo
echo "✅ 测试完成"
echo "=" | head -c 70; echo

