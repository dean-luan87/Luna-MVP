# vision_pipeline/b2/v03/b2_audit/test_audit.py
"""
测试 Audit Runner
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from context import AuditContext
from report import AuditReport
from audit_runner import RULES, run_audit

def test_imports():
    """测试导入"""
    print("测试导入...")
    try:
        print(f"✅ 成功导入 {len(RULES)} 个规则")
        for rule in RULES:
            print(f"   - {rule.rule_id}: {rule.description[:60]}")
        return True
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_context():
    """测试 Context"""
    print("\n测试 Context...")
    try:
        # 创建一个空的 trace 文件用于测试
        ctx = AuditContext("nonexistent.jsonl")
        print(f"✅ Context 创建成功（traces: {len(ctx.traces)}）")
        return True
    except Exception as e:
        print(f"❌ Context 测试失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("B2 v0.5 Audit Runner 测试")
    print("=" * 70)
    
    success = True
    success &= test_imports()
    success &= test_context()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ 所有测试通过")
    else:
        print("❌ 测试失败")
    print("=" * 70)
