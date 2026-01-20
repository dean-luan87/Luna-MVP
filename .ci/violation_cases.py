"""
BC Architecture Violation Test Cases
反例测试集 - 架构回归免疫系统

用途：
- 防止历史越权反例重新出现
- 作为 CI 回归测试
- 任何反例重新出现 → CI FAIL
"""

import unittest
import re
from pathlib import Path
from typing import List, Dict, Any


class BCArchitectureViolationTests(unittest.TestCase):
    """BC 架构违规反例测试集"""
    
    def setUp(self):
        """设置测试环境"""
        self.b2_code_dir = Path("vision_pipeline/b2")
        self.c1_code_dir = Path("c1_controller")
        self.gate_code_dir = Path("vision_pipeline/b2/v03/gate")
    
    def _scan_file(self, file_path: Path, patterns: List[str]) -> List[Dict[str, Any]]:
        """扫描文件中的违规模式"""
        violations = []
        try:
            content = file_path.read_text(encoding="utf-8")
            for i, line in enumerate(content.splitlines(), 1):
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        violations.append({
                            "file": str(file_path),
                            "line": i,
                            "pattern": pattern,
                            "content": line.strip()
                        })
        except Exception as e:
            # 文件不存在或无法读取，跳过
            pass
        return violations
    
    def test_no_confirmative_risk_semantics(self):
        """反例 1: B 输出确认性风险语义"""
        patterns = [
            r"确认.*危险",
            r"一定.*坑",
            r"不能走",
            r"confirmed.*risk",
            r"certain.*danger",
            r"must.*stop.*because.*danger"
        ]
        
        violations = []
        if self.b2_code_dir.exists():
            for py_file in self.b2_code_dir.rglob("*.py"):
                violations.extend(self._scan_file(py_file, patterns))
        
        self.assertEqual(
            len(violations), 0,
            f"发现确认性风险语义违规：\n" + 
            "\n".join([f"  {v['file']}:{v['line']} - {v['content']}" for v in violations])
        )
    
    def test_no_direct_behavior_control(self):
        """反例 2: B 直接控制行为"""
        patterns = [
            r"force.*stop",
            r"强制.*停止",
            r"强制.*转向",
            r"强制.*绕行",
            r"must.*stop",
            r"must.*turn"
        ]
        
        violations = []
        if self.b2_code_dir.exists():
            for py_file in self.b2_code_dir.rglob("*.py"):
                violations.extend(self._scan_file(py_file, patterns))
        
        self.assertEqual(
            len(violations), 0,
            f"发现直接控制行为违规：\n" + 
            "\n".join([f"  {v['file']}:{v['line']} - {v['content']}" for v in violations])
        )
    
    def test_no_gate_bypass(self):
        """反例 3: B 绕过 Gate 输出"""
        patterns = [
            r"gate.*SUSPENDED.*decision",
            r"gate.*SUSPENDED.*output",
            r"if.*gate.*SUSPENDED.*:.*return.*summary",
            r"if.*gate_mode.*==.*SUSPENDED.*:.*emit.*decision"
        ]
        
        violations = []
        if self.b2_code_dir.exists():
            for py_file in self.b2_code_dir.rglob("*.py"):
                violations.extend(self._scan_file(py_file, patterns))
        
        self.assertEqual(
            len(violations), 0,
            f"发现 Gate 绕过违规：\n" + 
            "\n".join([f"  {v['file']}:{v['line']} - {v['content']}" for v in violations])
        )
    
    def test_no_close_range_need_stop(self):
        """反例 4: B 在 ≤3m 距离内输出 NEED_STOP"""
        patterns = [
            r"distance.*<.*3.*NEED_STOP",
            r"range.*<=.*3.*NEED_STOP",
            r"if.*distance.*<=.*3.*and.*NEED_STOP",
            r"if.*range.*<.*3.*and.*impact.*==.*NEED_STOP"
        ]
        
        violations = []
        if self.b2_code_dir.exists():
            for py_file in self.b2_code_dir.rglob("*.py"):
                violations.extend(self._scan_file(py_file, patterns))
        
        self.assertEqual(
            len(violations), 0,
            f"发现近距离 NEED_STOP 违规：\n" + 
            "\n".join([f"  {v['file']}:{v['line']} - {v['content']}" for v in violations])
        )
    
    def test_no_env_trigger_decision(self):
        """反例 5: ENV 因子触发 CONDITION_CHANGE / INTERRUPT"""
        patterns = [
            r"FactorType\.ENV.*CONDITION_CHANGE",
            r"FactorType\.ENV.*INTERRUPT",
            r"ENV.*decision",
            r"ENV.*impact.*!=.*NO_OP",
            r"if.*ENV.*:.*impact.*=.*NEED"
        ]
        
        violations = []
        if self.b2_code_dir.exists():
            for py_file in self.b2_code_dir.rglob("*.py"):
                violations.extend(self._scan_file(py_file, patterns))
        
        self.assertEqual(
            len(violations), 0,
            f"发现 ENV 触发决策违规：\n" + 
            "\n".join([f"  {v['file']}:{v['line']} - {v['content']}" for v in violations])
        )
    
    def test_advisory_only_required(self):
        """反例 6: B 输出缺少 advisory_only"""
        # 检查所有 B 输出 summary 的地方
        patterns = [
            r"advisory_only.*=.*False",
            r"advisory_only.*=.*None",
            r"return.*\{.*impact.*\}.*#.*缺少.*advisory_only"
        ]
        
        violations = []
        if self.b2_code_dir.exists():
            for py_file in self.b2_code_dir.rglob("*.py"):
                violations.extend(self._scan_file(py_file, patterns))
        
        self.assertEqual(
            len(violations), 0,
            f"发现缺少 advisory_only 违规：\n" + 
            "\n".join([f"  {v['file']}:{v['line']} - {v['content']}" for v in violations])
        )
    
    def test_no_forbidden_impacts(self):
        """反例 7: B 输出非法 Impact"""
        forbidden_impacts = [
            "CONFIRMED_DANGER",
            "FORCE_STOP",
            "CERTAIN_RISK",
            "WORLD_CHANGE"
        ]
        
        violations = []
        if self.b2_code_dir.exists():
            for py_file in self.b2_code_dir.rglob("*.py"):
                content = py_file.read_text(encoding="utf-8")
                for impact in forbidden_impacts:
                    if impact in content:
                        violations.append({
                            "file": str(py_file),
                            "forbidden_impact": impact
                        })
        
        self.assertEqual(
            len(violations), 0,
            f"发现非法 Impact 违规：\n" + 
            "\n".join([f"  {v['file']} - {v['forbidden_impact']}" for v in violations])
        )


if __name__ == "__main__":
    unittest.main()
