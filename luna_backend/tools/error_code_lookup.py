#!/usr/bin/env python3
"""
错误码查询工具
用法: python tools/error_code_lookup.py <错误码>
示例: python tools/error_code_lookup.py 2006
"""

import sys
import os
import subprocess

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.error_codes import ERR, ERROR_MESSAGES, get_module_name

def lookup_error_code(code: int):
    """查询错误码信息"""
    module = get_module_name(code)
    message = ERROR_MESSAGES.get(code, "未知错误码")
    
    print("=" * 60)
    print(f"错误码: {code}")
    print(f"模块: {module}")
    print(f"消息: {message}")
    print("=" * 60)
    
    # 查找常量定义
    print("\n📝 常量定义:")
    for attr_name in dir(ERR):
        if not attr_name.startswith("_"):
            attr_value = getattr(ERR, attr_name)
            if attr_value == code:
                print(f"  ERR.{attr_name} = {code}")
                break
    
    # 查找使用位置
    print("\n🔍 使用位置:")
    try:
        result = subprocess.run(
            ["grep", "-rn", f"ERR\\.[A-Z_]+.*=.*{code}", "luna_backend/"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        if result.stdout:
            for line in result.stdout.strip().split("\n"):
                if line:
                    print(f"  {line}")
        else:
            print("  (未找到定义)")
    except:
        print("  (无法搜索)")
    
    # 查找错误码使用
    print("\n📂 代码中使用:")
    try:
        result = subprocess.run(
            ["grep", "-rn", f"ERR\\.[A-Z_]+", "luna_backend/"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        if result.stdout:
            matching_lines = []
            for line in result.stdout.strip().split("\n"):
                if line and str(code) in line:
                    matching_lines.append(line)
            
            if matching_lines:
                for line in matching_lines[:10]:  # 最多显示10个
                    print(f"  {line}")
            else:
                print("  (未找到使用)")
        else:
            print("  (未找到使用)")
    except:
        print("  (无法搜索)")
    
    print("\n" + "=" * 60)

def list_all_error_codes():
    """列出所有错误码"""
    print("=" * 80)
    print("Luna Backend 错误码列表")
    print("=" * 80)
    
    modules = {}
    for attr_name in dir(ERR):
        if not attr_name.startswith("_"):
            code = getattr(ERR, attr_name)
            if isinstance(code, int) and code > 0:
                module = get_module_name(code)
                if module not in modules:
                    modules[module] = []
                modules[module].append((code, attr_name, ERROR_MESSAGES.get(code, "未知")))
    
    for module in sorted(modules.keys()):
        print(f"\n📦 {module} 模块:")
        for code, name, message in sorted(modules[module]):
            print(f"  {code:4d}  {name:30s}  {message}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python error_code_lookup.py <错误码>")
        print("示例: python error_code_lookup.py 2006")
        print("\n或使用 --list 列出所有错误码:")
        print("示例: python error_code_lookup.py --list")
        sys.exit(1)
    
    if sys.argv[1] == "--list":
        list_all_error_codes()
    else:
        try:
            code = int(sys.argv[1])
            lookup_error_code(code)
        except ValueError:
            print(f"错误: '{sys.argv[1]}' 不是有效的错误码")
            sys.exit(1)



