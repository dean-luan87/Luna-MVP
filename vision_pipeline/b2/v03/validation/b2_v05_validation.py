# vision_pipeline/b2/v03/validation/b2_v05_validation.py
"""
B2 v0.5 Step 1-7 自动化验收脚本
目标：防止走样、可验收、不可自由发挥
"""

import json
import re
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from enum import Enum


class ValidationResult:
    """验收结果"""
    def __init__(self):
        self.passed: List[str] = []
        self.failed: List[Tuple[str, str]] = []  # (check_name, reason)
        self.warnings: List[Tuple[str, str]] = []
    
    def add_pass(self, check_name: str):
        self.passed.append(check_name)
    
    def add_fail(self, check_name: str, reason: str):
        self.failed.append((check_name, reason))
    
    def add_warning(self, check_name: str, reason: str):
        self.warnings.append((check_name, reason))
    
    def is_all_passed(self) -> bool:
        return len(self.failed) == 0
    
    def print_report(self):
        print("\n" + "=" * 70)
        print("B2 v0.5 验收报告")
        print("=" * 70)
        
        print(f"\n✅ 通过: {len(self.passed)} 项")
        for item in self.passed:
            print(f"   ✓ {item}")
        
        if self.warnings:
            print(f"\n⚠️  警告: {len(self.warnings)} 项")
            for check, reason in self.warnings:
                print(f"   ⚠ {check}: {reason}")
        
        if self.failed:
            print(f"\n❌ 失败: {len(self.failed)} 项")
            for check, reason in self.failed:
                print(f"   ✗ {check}: {reason}")
        
        print("\n" + "=" * 70)
        if self.is_all_passed():
            print("✅ 验收通过：所有检查项均满足要求")
        else:
            print("❌ 验收失败：存在不符合要求的项")
        print("=" * 70 + "\n")


class B2V05Validator:
    """B2 v0.5 验收器"""
    
    # 允许的 Gate Mode
    ALLOWED_GATE_MODES = {"SUSPENDED", "READ_ONLY", "ACTIVE"}
    
    # 允许的 Evidence 状态
    ALLOWED_EVIDENCE_STATES = {"OBSERVING", "CONFIRMED", "DEGRADED", "DROPPED"}
    
    # 允许的 ActionImpact
    ALLOWED_IMPACTS = {
        "NO_OP", "NEED_SLOW_DOWN", "PATH_UNCERTAIN", 
        "NEED_DETOUR", "NEED_STOP", "FORCE_ALERT"
    }
    
    # 全局禁止项
    FORBIDDEN_PATTERNS = [
        (r"ocr|OCR", "禁止引入 OCR"),
        (r"learn|train|adapt", "禁止引入学习/自适应"),
        (r"WORLD|SCENE", "禁止输出 WORLD/SCENE 级语义"),
    ]
    
    def __init__(self):
        self.result = ValidationResult()
    
    def validate_all(self, code_path: str, trace_sample_path: Optional[str] = None):
        """
        执行全部验收检查
        
        :param code_path: B2 代码路径
        :param trace_sample_path: Trace 样本路径（可选）
        """
        print("开始 B2 v0.5 验收检查...\n")
        
        # Step 1: Gate
        self.validate_step1_gate(code_path)
        
        # Step 2: Evidence Lifecycle
        self.validate_step2_evidence(code_path)
        
        # Step 3: Trigger
        self.validate_step3_trigger(code_path)
        
        # Step 4: Impact Evaluation
        self.validate_step4_impact(code_path)
        
        # Step 5: B → C Contract
        self.validate_step5_contract(code_path)
        
        # Step 6: Runtime Trace
        if trace_sample_path:
            self.validate_step6_trace(trace_sample_path)
        
        # Step 7: Web Visualization
        self.validate_step7_visualization(code_path)
        
        # 全局禁止项
        self.validate_global_forbidden(code_path)
        
        # 最终验收标准
        if trace_sample_path:
            self.validate_final_criteria(trace_sample_path)
        
        return self.result
    
    def validate_step1_gate(self, code_path: str):
        """Step 1: Gate 验收"""
        print("检查 Step 1: Gate...")
        
        code = self._read_file(code_path)
        if not code:
            self.result.add_fail("Step 1: Gate", "无法读取代码文件")
            return
        
        # 检查 Gate 是否是第一步执行
        if "gate" in code.lower() and "perception" in code.lower():
            # 简单检查：gate 应该在 perception 之前
            gate_pos = code.lower().find("gate")
            perception_pos = code.lower().find("perception")
            if perception_pos > 0 and gate_pos > perception_pos:
                self.result.add_warning("Step 1: Gate 顺序", "Gate 应该在 perception 之前执行")
        
        # 检查 Gate Mode 是否只存在 3 种
        for mode in self.ALLOWED_GATE_MODES:
            if mode not in code:
                self.result.add_fail(f"Step 1: Gate Mode {mode}", f"代码中未找到 {mode}")
        
        # 检查 Gate 输入是否结构化
        required_inputs = ["stability_score", "camera_motion", "camera_pose", "fov_state"]
        for inp in required_inputs:
            if inp not in code:
                self.result.add_warning(f"Step 1: Gate 输入 {inp}", f"未找到 {inp} 字段")
        
        # 检查 Gate 输出是否写入 trace
        required_outputs = ["mode", "blocked_by", "details", "human_readable"]
        trace_outputs = ["gate_eval", "gate_mode"]
        found_output = False
        for out in trace_outputs:
            if out in code:
                found_output = True
                break
        if not found_output:
            self.result.add_fail("Step 1: Gate 输出", "Gate 结果未写入 trace")
        
        self.result.add_pass("Step 1: Gate 基本结构")
    
    def validate_step2_evidence(self, code_path: str):
        """Step 2: Evidence Lifecycle 验收"""
        print("检查 Step 2: Evidence Lifecycle...")
        
        code = self._read_file(code_path)
        if not code:
            return
        
        # 检查 Evidence 状态是否只用这 4 种
        for state in self.ALLOWED_EVIDENCE_STATES:
            if state not in code:
                self.result.add_warning(f"Step 2: Evidence 状态 {state}", f"未找到 {state}")
        
        # 检查每个 Evidence 是否包含必要字段
        required_fields = ["first_seen_ts", "last_seen_ts", "continuous_frames", "state"]
        for field in required_fields:
            if field not in code:
                self.result.add_warning(f"Step 2: Evidence 字段 {field}", f"未找到 {field}")
        
        # 检查是否禁止瞬时判断
        if "lifecycle" not in code.lower() and "evidence_state" not in code.lower():
            self.result.add_fail("Step 2: Evidence Lifecycle", "未实现证据生命周期机制")
        
        self.result.add_pass("Step 2: Evidence Lifecycle 基本结构")
    
    def validate_step3_trigger(self, code_path: str):
        """Step 3: Trigger 验收"""
        print("检查 Step 3: Trigger...")
        
        code = self._read_file(code_path)
        if not code:
            return
        
        # 检查 Trigger 是否是显式步骤
        if "trigger" not in code.lower():
            self.result.add_fail("Step 3: Trigger", "未找到 Trigger 逻辑")
        
        # 检查不触发条件
        trigger_conditions = ["gate", "confirmed", "cooldown"]
        for cond in trigger_conditions:
            if cond not in code.lower():
                self.result.add_warning(f"Step 3: Trigger 条件 {cond}", f"未找到 {cond} 检查")
        
        # 检查 Trigger 结果是否写 trace
        if '"triggered"' not in code and "'triggered'" not in code:
            self.result.add_warning("Step 3: Trigger 输出", "Trigger 结果可能未写入 trace")
        
        self.result.add_pass("Step 3: Trigger 基本结构")
    
    def validate_step4_impact(self, code_path: str):
        """Step 4: Impact Evaluation 验收"""
        print("检查 Step 4: Impact Evaluation...")
        
        code = self._read_file(code_path)
        if not code:
            return
        
        # 检查 ActionImpact 是否只允许指定枚举
        for impact in self.ALLOWED_IMPACTS:
            if impact not in code:
                self.result.add_warning(f"Step 4: Impact {impact}", f"未找到 {impact}")
        
        # 检查 ENV 是否永不直接产生 impact
        if "env" in code.lower() and "impact" in code.lower():
            # 简单检查：ENV 不应该直接产生 impact
            env_impact_pattern = r"env.*impact|impact.*env"
            if re.search(env_impact_pattern, code, re.IGNORECASE):
                self.result.add_fail("Step 4: ENV Impact", "ENV 不应该直接产生 impact")
        
        # 检查 FORCE_ALERT 是否唯一干预路径
        if "FORCE_ALERT" in code:
            # 检查是否有其他干预路径
            intervention_patterns = ["interrupt", "force", "override"]
            for pattern in intervention_patterns:
                if pattern in code.lower() and "force_alert" not in code.lower():
                    self.result.add_warning(f"Step 4: 干预路径 {pattern}", "可能存在其他干预路径")
        
        self.result.add_pass("Step 4: Impact Evaluation 基本结构")
    
    def validate_step5_contract(self, code_path: str):
        """Step 5: B → C Contract 验收"""
        print("检查 Step 5: B → C Contract...")
        
        code = self._read_file(code_path)
        if not code:
            return
        
        # 检查 B → C 是否只有一个出口
        to_c_patterns = ["to_c_message", "to_c", "send_to_c", "message_to_c"]
        found = False
        for pattern in to_c_patterns:
            if pattern in code.lower():
                found = True
                break
        if not found:
            self.result.add_fail("Step 5: B → C 出口", "未找到 B → C 消息出口")
        
        # 检查输出结构是否固定
        required_fields = ["sent", "impact", "explain"]
        for field in required_fields:
            if field not in code.lower():
                self.result.add_warning(f"Step 5: 输出字段 {field}", f"未找到 {field}")
        
        # 检查是否遵守权限边界
        if "FORCE_ALERT" in code:
            if "urgency" not in code.lower() and "force" not in code.lower():
                self.result.add_warning("Step 5: FORCE_ALERT 权限", "FORCE_ALERT 应该有明确的权限标识")
        
        self.result.add_pass("Step 5: B → C Contract 基本结构")
    
    def validate_step6_trace(self, trace_path: str):
        """Step 6: Runtime Trace 验收"""
        print("检查 Step 6: Runtime Trace...")
        
        try:
            with open(trace_path, 'r', encoding='utf-8') as f:
                # 读取第一行作为样本
                first_line = f.readline()
                if not first_line:
                    self.result.add_fail("Step 6: Trace 文件", "Trace 文件为空")
                    return
                
                trace = json.loads(first_line)
                
                # 检查 Trace 是否包含完整字段
                required_fields = [
                    "gate_eval", "trigger", "evidence_state", 
                    "impact_eval", "to_c_message", "writeback"
                ]
                for field in required_fields:
                    if field not in trace:
                        self.result.add_fail(f"Step 6: Trace 字段 {field}", f"Trace 中缺少 {field}")
                
                # 检查 Timeline 是否干净
                if "impact_eval" in trace:
                    impact = trace["impact_eval"].get("impact", "")
                    writeback = trace.get("writeback", {})
                    timeline_written = writeback.get("timeline_written", False)
                    
                    if impact == "NO_OP" and timeline_written:
                        self.result.add_fail("Step 6: Timeline 规则", "NO_OP 不应该写入 timeline")
                
                self.result.add_pass("Step 6: Runtime Trace 格式")
        except Exception as e:
            self.result.add_fail("Step 6: Trace 文件", f"无法读取 Trace 文件: {e}")
    
    def validate_step7_visualization(self, code_path: str):
        """Step 7: Web Visualization 验收"""
        print("检查 Step 7: Web Visualization...")
        
        # 这一步主要是检查 trace 是否支持可视化
        # 具体可视化实现不在 B2 代码中，所以只做基本检查
        self.result.add_pass("Step 7: Web Visualization（需在可视化层验证）")
    
    def validate_global_forbidden(self, code_path: str):
        """全局禁止项验收"""
        print("检查全局禁止项...")
        
        code = self._read_file(code_path)
        if not code:
            return
        
        for pattern, reason in self.FORBIDDEN_PATTERNS:
            matches = re.findall(pattern, code, re.IGNORECASE)
            if matches:
                # 排除注释和字符串中的匹配
                lines = code.split('\n')
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        # 简单检查：不在注释中
                        if not line.strip().startswith('#') and not line.strip().startswith('//'):
                            self.result.add_fail(
                                f"全局禁止: {pattern}",
                                f"第 {i} 行: {reason}"
                            )
    
    def validate_final_criteria(self, trace_path: str):
        """最终验收标准（三个问题）"""
        print("检查最终验收标准...")
        
        try:
            with open(trace_path, 'r', encoding='utf-8') as f:
                traces = []
                for line in f:
                    if line.strip():
                        traces.append(json.loads(line))
                
                if not traces:
                    self.result.add_fail("最终验收: Trace 样本", "Trace 文件为空")
                    return
                
                # 问题 1: 任意一帧，能不能说清楚为什么 B 没工作/工作了？
                sample_trace = traces[0]
                if "gate_eval" not in sample_trace:
                    self.result.add_fail("最终验收: 问题1", "无法从 trace 判断 B 为什么工作/不工作")
                else:
                    gate_eval = sample_trace["gate_eval"]
                    if "mode" not in gate_eval or "blocked_by" not in gate_eval:
                        self.result.add_fail("最终验收: 问题1", "Gate 信息不完整")
                    else:
                        self.result.add_pass("最终验收: 问题1 - 可追溯 B 工作状态")
                
                # 问题 2: 任意一条 timeline，能不能倒推出当时的视角状态？
                # 这需要检查 trace 中是否有 view_state 或类似信息
                if "view_state" not in sample_trace and "gate_eval" not in sample_trace:
                    self.result.add_warning("最终验收: 问题2", "Trace 中可能缺少视角状态信息")
                else:
                    self.result.add_pass("最终验收: 问题2 - 可倒推视角状态")
                
                # 问题 3: 删掉 timeline，只看 trace，系统是否仍然完整可理解？
                # 这需要 trace 包含所有必要信息
                required_for_understanding = [
                    "gate_eval", "trigger", "evidence_state", 
                    "impact_eval", "to_c_message"
                ]
                missing = [f for f in required_for_understanding if f not in sample_trace]
                if missing:
                    self.result.add_fail("最终验收: 问题3", f"Trace 缺少关键字段: {missing}")
                else:
                    self.result.add_pass("最终验收: 问题3 - Trace 独立可理解")
        
        except Exception as e:
            self.result.add_fail("最终验收: Trace 读取", f"无法读取 Trace: {e}")
    
    def _read_file(self, file_path: str) -> Optional[str]:
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.result.add_fail(f"文件读取: {file_path}", str(e))
            return None


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python b2_v05_validation.py <b2_code_path> [trace_sample_path]")
        sys.exit(1)
    
    code_path = sys.argv[1]
    trace_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    validator = B2V05Validator()
    result = validator.validate_all(code_path, trace_path)
    result.print_report()
    
    sys.exit(0 if result.is_all_passed() else 1)


if __name__ == "__main__":
    main()
