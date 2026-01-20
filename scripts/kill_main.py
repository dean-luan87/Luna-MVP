#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关闭 main.py 相关进程的脚本
"""

import subprocess
import sys

def kill_main_processes():
    """关闭所有 main.py 相关进程"""
    print("=" * 70)
    print("关闭 main.py 相关进程")
    print("=" * 70)
    print()
    
    try:
        # 查找进程
        result = subprocess.run(
            ["pgrep", "-f", "main.py"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            pids = [pid.strip() for pid in result.stdout.strip().split('\n') if pid.strip()]
            
            if pids:
                print(f"找到 {len(pids)} 个进程:")
                for pid in pids:
                    print(f"  PID: {pid}")
                print()
                
                # 尝试优雅关闭
                print("尝试优雅关闭...")
                subprocess.run(["pkill", "-f", "main.py"])
                
                # 等待一下
                import time
                time.sleep(1)
                
                # 检查是否还有进程
                result2 = subprocess.run(
                    ["pgrep", "-f", "main.py"],
                    capture_output=True,
                    text=True
                )
                
                if result2.returncode == 0:
                    print("⚠️  仍有进程在运行，强制关闭...")
                    subprocess.run(["pkill", "-9", "-f", "main.py"])
                    print("✅ 已强制关闭")
                else:
                    print("✅ 进程已关闭")
            else:
                print("✅ 没有找到相关进程")
        else:
            print("✅ 没有找到 main.py 相关进程")
            
    except Exception as e:
        print(f"❌ 关闭进程时出错: {e}")
        print()
        print("手动关闭方法:")
        print("  1. 在终端按 Ctrl+C")
        print("  2. 或使用: pkill -f 'main.py'")
        print("  3. 或使用: pkill -9 -f 'main.py' (强制关闭)")
        return False
    
    print()
    print("=" * 70)
    return True

if __name__ == "__main__":
    kill_main_processes()


