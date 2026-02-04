#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JS自动结构审计脚本（规范要求）
审计extracted_javascript.js，找出违反Luna规范的地方
"""

import os
import sys
import json
import re
from typing import Dict, Any, List
from collections import defaultdict

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 报告路径
REPORT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs', 'js_audit_report.json')

# JS文件路径
JS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'extracted_javascript.js')

def read_js_file():
    """读取JS文件"""
    if not os.path.exists(JS_FILE):
        print(f"⚠️ JS文件不存在: {JS_FILE}")
        return None
    
    with open(JS_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def find_violations(js_content: str):
    """查找违反规范的地方"""
    violations = {
        "missing_taskchain_calls": [],
        "missing_unified_events": [],
        "unregistered_intervals": [],
        "direct_tts_calls": [],
        "unsafe_async_blocks": [],
        "raw_console_logs": [],
        "duplicate_code_candidates": []
    }
    
    lines = js_content.split('\n')
    
    # 1. 查找未通过taskChain.enqueue的任务逻辑
    taskchain_pattern = r'taskChain\.enqueue|taskChainEnqueue'
    for i, line in enumerate(lines, 1):
        # 查找可能应该是任务链调用的地方
        if re.search(r'(hazard|step|navigation|tts|ui_update|log)', line, re.IGNORECASE):
            if not re.search(taskchain_pattern, line):
                # 检查是否是函数调用或赋值
                if re.search(r'(function|=>|async|await)', line):
                    violations["missing_taskchain_calls"].append({
                        "line": i,
                        "code": line.strip()[:100],
                        "type": "potential_taskchain_missing"
                    })
    
    # 2. 查找未通过统一事件的事件处理
    unified_event_pattern = r'emitHazardEvent|emitStepEvent|emitNavigationEvent|EventBridge\.dispatch'
    for i, line in enumerate(lines, 1):
        if re.search(r'(危险|台阶|左转|右转|导航|hazard|step|navigation)', line, re.IGNORECASE):
            if not re.search(unified_event_pattern, line):
                if re.search(r'(speakText|speak|TTS|播报)', line, re.IGNORECASE):
                    violations["missing_unified_events"].append({
                        "line": i,
                        "code": line.strip()[:100],
                        "type": "direct_event_handling"
                    })
    
    # 3. 查找未注册到window.__intervals的setInterval
    interval_pattern = r'setInterval\s*\('
    registered_pattern = r'window\.__intervals\.\w+\s*='
    for i, line in enumerate(lines, 1):
        if re.search(interval_pattern, line):
            # 检查前后5行是否有注册
            context_start = max(0, i - 5)
            context_end = min(len(lines), i + 5)
            context = '\n'.join(lines[context_start:context_end])
            if not re.search(registered_pattern, context):
                violations["unregistered_intervals"].append({
                    "line": i,
                    "code": line.strip()[:100],
                    "type": "unregistered_interval"
                })
    
    # 4. 查找直接调用TTS底层函数
    direct_tts_patterns = [
        r'speakText\s*\(',
        r'\.speak\s*\(',
        r'_playTTS\s*\(',
        r'priorityTTSQueue\.play\s*\('
    ]
    for pattern in direct_tts_patterns:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                # 检查是否通过taskChain或EventBridge
                if not re.search(r'taskChain|EventBridge|emitHazardEvent|emitStepEvent|emitNavigationEvent', line):
                    violations["direct_tts_calls"].append({
                        "line": i,
                        "code": line.strip()[:100],
                        "type": "direct_tts_call",
                        "pattern": pattern
                    })
    
    # 5. 查找async函数中没有try/catch的await调用
    async_function_start = None
    for i, line in enumerate(lines, 1):
        if re.search(r'async\s+function|async\s*\(', line):
            async_function_start = i
        
        if async_function_start:
            if re.search(r'await\s+', line):
                # 检查函数内是否有try/catch
                if i > async_function_start:
                    # 查找最近的try块
                    try_found = False
                    for j in range(async_function_start, i):
                        if 'try' in lines[j]:
                            try_found = True
                            break
                    
                    if not try_found:
                        violations["unsafe_async_blocks"].append({
                            "line": i,
                            "code": line.strip()[:100],
                            "function_start": async_function_start,
                            "type": "unsafe_await"
                        })
            
            # 函数结束
            if re.search(r'^\s*\}\s*$|^\s*\)\s*$', line) and i > async_function_start + 5:
                async_function_start = None
    
    # 6. 查找console.log（建议改为统一日志函数）
    for i, line in enumerate(lines, 1):
        if re.search(r'console\.log\s*\(', line):
            violations["raw_console_logs"].append({
                "line": i,
                "code": line.strip()[:100],
                "type": "raw_console_log",
                "suggestion": "建议改为 lunaLog('info', message, meta)"
            })
    
    # 7. 查找重复代码段（简化版：查找相似函数）
    function_pattern = r'function\s+(\w+)\s*\([^)]*\)\s*\{'
    functions = {}
    for i, line in enumerate(lines, 1):
        match = re.search(function_pattern, line)
        if match:
            func_name = match.group(1)
            # 提取函数体（简化：取接下来20行）
            func_body = '\n'.join(lines[i-1:min(i+20, len(lines))])
            if func_name in functions:
                # 检查相似度
                similarity = calculate_similarity(func_body, functions[func_name]["body"])
                if similarity > 0.8:
                    violations["duplicate_code_candidates"].append({
                        "line": i,
                        "function_name": func_name,
                        "similarity": similarity,
                        "previous_line": functions[func_name]["line"],
                        "type": "duplicate_function"
                    })
            else:
                functions[func_name] = {"line": i, "body": func_body}
    
    return violations

def calculate_similarity(str1: str, str2: str) -> float:
    """计算字符串相似度（简化版）"""
    if len(str1) == 0 or len(str2) == 0:
        return 0.0
    
    # 使用简单的字符重叠度
    set1 = set(str1)
    set2 = set(str2)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0.0

def main():
    """主审计函数"""
    print("=" * 70)
    print("🔍 Luna JS结构审计")
    print("=" * 70)
    
    js_content = read_js_file()
    if not js_content:
        print("❌ 无法读取JS文件，审计终止")
        return
    
    print(f"📄 文件: {JS_FILE}")
    print(f"📏 总行数: {len(js_content.split(chr(10)))}\n")
    
    violations = find_violations(js_content)
    
    # 统计
    total_violations = sum(len(v) for v in violations.values())
    
    print("=" * 70)
    print("📊 审计结果")
    print("=" * 70)
    print(f"未通过taskChain的任务逻辑: {len(violations['missing_taskchain_calls'])}")
    print(f"未通过统一事件的事件处理: {len(violations['missing_unified_events'])}")
    print(f"未注册的setInterval: {len(violations['unregistered_intervals'])}")
    print(f"直接TTS调用: {len(violations['direct_tts_calls'])}")
    print(f"不安全的async/await: {len(violations['unsafe_async_blocks'])}")
    print(f"原始console.log: {len(violations['raw_console_logs'])}")
    print(f"重复代码候选: {len(violations['duplicate_code_candidates'])}")
    print(f"总计: {total_violations} 处潜在问题\n")
    
    # 保存报告
    report = {
        "audit_time": __import__('datetime').datetime.now().isoformat(),
        "file": JS_FILE,
        "total_lines": len(js_content.split('\n')),
        "violations": violations,
        "summary": {
            "total_violations": total_violations,
            "by_type": {k: len(v) for k, v in violations.items()}
        }
    }
    
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 报告已保存: {REPORT_PATH}")
    print("=" * 70)
    
    return report

if __name__ == "__main__":
    main()


