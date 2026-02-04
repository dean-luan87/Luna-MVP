# vision_pipeline/b2/v03/b2_audit/report.py
"""
统一输出格式
"""

import json
from typing import List, Dict, Any
from collections import defaultdict


class AuditReport:
    """验收报告"""
    
    def __init__(self):
        self.failures: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.stats = defaultdict(int)
    
    def add_result(self, result: Dict[str, Any]):
        """添加验收结果"""
        status = result.get("status")
        if status == "FAIL":
            self.failures.append(result)
            self.stats["failed"] += 1
        elif status == "WARN":
            self.warnings.append(result)
            self.stats["warned"] += 1
        else:
            self.stats["passed"] += 1
    
    def print_report(self):
        """打印报告"""
        print("\n" + "=" * 70)
        print("B2 v0.5 自动化验收报告")
        print("=" * 70)
        
        total = self.stats["passed"] + self.stats["warned"] + self.stats["failed"]
        print(f"\n总检查项: {total}")
        print(f"✅ 通过: {self.stats['passed']}")
        print(f"⚠️  警告: {self.stats['warned']}")
        print(f"❌ 失败: {self.stats['failed']}")
        
        if self.failures:
            print("\n" + "-" * 70)
            print("失败项详情:")
            print("-" * 70)
            for f in self.failures:
                print(f"\n❌ {f['rule_id']}: {f['message']}")
                evidence = f.get("evidence", {})
                if "trace_index" in evidence:
                    print(f"   Trace Index: {evidence['trace_index']}")
                if "frame_id" in evidence:
                    print(f"   Frame ID: {evidence['frame_id']}")
                if "human_time" in evidence:
                    print(f"   时间: {evidence['human_time']}")
        
        if self.warnings:
            print("\n" + "-" * 70)
            print("警告项详情:")
            print("-" * 70)
            for w in self.warnings[:10]:  # 只显示前 10 个警告
                print(f"\n⚠️  {w['rule_id']}: {w['message']}")
        
        print("\n" + "=" * 70)
        if self.stats["failed"] == 0:
            print("✅ AUDIT PASSED")
        else:
            print("❌ AUDIT FAILED")
        print("=" * 70 + "\n")
    
    def save_json(self, path: str = "b2_audit_report.json"):
        """保存 JSON 报告"""
        report = {
            "stats": dict(self.stats),
            "failures": self.failures,
            "warnings": self.warnings
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return path
    
    def has_failures(self) -> bool:
        """是否有失败项"""
        return len(self.failures) > 0
