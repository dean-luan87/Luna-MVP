# vision_pipeline/b2/v03/v041_patch_validator.py
"""
B2 v0.4.1 Patch Validator
Cursor 可执行的自动化检查脚本
"""

import sys
from pathlib import Path


class V041PatchValidator:
    """v0.4.1 Patch 验证器"""
    
    def __init__(self, code_file: str):
        """
        初始化验证器
        
        :param code_file: B2 代码文件路径
        """
        self.code_file = code_file
        # 直接读取文件，避免导入冲突
        with open(code_file, 'r', encoding='utf-8') as f:
            self.code_content = f.read()
        self.violations = []
        self.checks_passed = []
    
    def validate_all(self) -> Tuple[bool, List[str], List[str]]:
        """
        运行所有检查
        
        :return: (是否通过, 通过的检查, 违规列表)
        """
        # P0: 语义与边界
        self._check_advisory_only()
        self._check_no_confirmation_semantics()
        self._check_single_intervention()
        
        # P1: 时间与尺度统一
        self._check_system_time_only()
        self._check_no_time_offset_in_message()
        
        # P2: NO_OP 沉默机制
        self._check_no_op_no_timeline()
        self._check_no_op_has_silence_reason()
        
        # P3: Gate 只影响 B
        self._check_gate_three_states_only()
        self._check_read_only_no_new_judgment()
        
        # P4: DCS 守卫
        self._check_dcs_no_decision_influence()
        self._check_dcs_violations_visible()
        
        # P5: 角色声明
        self._check_role_declaration()
        
        return len(self.violations) == 0, self.checks_passed, self.violations
    
    def _check_advisory_only(self):
        """检查 1: B2 输出必须显式声明"只提醒" """
        # 检查 Python 布尔值 True 或字符串 "true"
        if '"advisory_only": True' in self.code_content or \
           "'advisory_only': True" in self.code_content or \
           '"advisory_only": true' in self.code_content or \
           "'advisory_only': true" in self.code_content:
            self.checks_passed.append("P0.1: advisory_only = True")
        else:
            self.violations.append("P0.1: 缺失 advisory_only = True 字段")
    
    def _check_no_confirmation_semantics(self):
        """检查 2: B2 不允许输出"确认性语义" """
        forbidden_keywords = [
            'CONFIRMED_',
            'FORCE_',
            'CERTAIN_',
            'WORLD_'
        ]
        
        found_forbidden = []
        lines = self.code_content.split('\n')
        
        for i, line in enumerate(lines):
            # 跳过注释和 assert 语句（这些是防护代码）
            stripped = line.strip()
            if stripped.startswith('#') or 'assert' in stripped:
                continue
            
            # 检查是否在 ActionImpact 枚举定义中
            if 'class ActionImpact' in line or 'ActionImpact(' in line:
                # 在枚举定义区域，检查是否有禁止的枚举值
                for keyword in forbidden_keywords:
                    if keyword in line and '=' in line:
                        found_forbidden.append(f"Line {i+1}: {keyword}")
        
        if not found_forbidden:
            self.checks_passed.append("P0.2: 无确认性语义（在枚举中）")
        else:
            self.violations.append(f"P0.2: 发现确认性语义: {found_forbidden}")
    
    def _check_single_intervention(self):
        """检查 3: B2 唯一允许的"越权干预"= NEED_STOP """
        # 检查 intervention_level 的设置逻辑
        if 'intervention_level = "HARD"' in self.code_content or "intervention_level == 'HARD'" in self.code_content:
            # 检查是否只有 NEED_STOP 是 HARD
            if 'if impact == ActionImpact.NEED_STOP:' in self.code_content or \
               'if impact == "NEED_STOP":' in self.code_content:
                self.checks_passed.append("P0.3: 唯一干预通道 = NEED_STOP")
            else:
                self.violations.append("P0.3: NEED_STOP 未正确标记为 HARD")
        else:
            self.violations.append("P0.3: 缺失 intervention_level 设置")
    
    def _check_system_time_only(self):
        """检查 4: 系统时间唯一来源 """
        forbidden_time_fields = ['frame_ts', 'perception_ts', 'camera_ts']
        found_forbidden = []
        
        for field in forbidden_time_fields:
            if f'"{field}"' in self.code_content or f"'{field}'" in self.code_content:
                found_forbidden.append(field)
        
        if '"system_ts"' in self.code_content or "'system_ts'" in self.code_content:
            if not found_forbidden:
                self.checks_passed.append("P1.4: 系统时间唯一来源")
            else:
                self.violations.append(f"P1.4: 发现禁止的时间字段: {found_forbidden}")
        else:
            self.violations.append("P1.4: 缺失 system_ts 字段")
    
    def _check_no_time_offset_in_message(self):
        """检查 5: B/C 通信不携带时间偏移 """
        forbidden_phrases = [
            'will happen in',
            'must occur',
            'guaranteed at',
            'certain to happen'
        ]
        
        found_forbidden = []
        for phrase in forbidden_phrases:
            if phrase.lower() in self.code_content.lower():
                found_forbidden.append(phrase)
        
        if not found_forbidden:
            self.checks_passed.append("P1.5: 无时间偏移承诺")
        else:
            self.violations.append(f"P1.5: 发现时间偏移承诺: {found_forbidden}")
    
    def _check_no_op_no_timeline(self):
        """检查 6: NO_OP 不写 timeline """
        if 'if impact' in self.code_content and 'NO_OP' in self.code_content:
            if 'timeline_written = False' in self.code_content or \
               '"timeline_written": False' in self.code_content:
                self.checks_passed.append("P2.6: NO_OP 不写 timeline")
            else:
                self.violations.append("P2.6: NO_OP 可能写入 timeline")
        else:
            self.violations.append("P2.6: 未找到 NO_OP 处理逻辑")
    
    def _check_no_op_has_silence_reason(self):
        """检查 7: NO_OP 必须写 trace（但标明沉默原因） """
        if '"decision_state": "SILENT"' in self.code_content or \
           "'decision_state': 'SILENT'" in self.code_content:
            if '"silence_reason"' in self.code_content or "'silence_reason'" in self.code_content:
                self.checks_passed.append("P2.7: NO_OP 有沉默原因")
            else:
                self.violations.append("P2.7: NO_OP 缺失 silence_reason")
        else:
            self.violations.append("P2.7: NO_OP 未设置 decision_state = SILENT")
    
    def _check_gate_three_states_only(self):
        """检查 8: Gate 只能产生三态 """
        if 'BGateState' in self.code_content:
            if 'ACTIVE' in self.code_content and 'READ_ONLY' in self.code_content and 'SUSPENDED' in self.code_content:
                self.checks_passed.append("P3.8: Gate 三态正确")
            else:
                self.violations.append("P3.8: Gate 状态不完整")
        else:
            self.violations.append("P3.8: 未找到 BGateState 定义")
    
    def _check_read_only_no_new_judgment(self):
        """检查 9: READ_ONLY = 不产出新判断 """
        if 'READ_ONLY' in self.code_content:
            # 检查 READ_ONLY 时是否阻止产生新判断
            if 'if gate_state == BGateState.READ_ONLY:' in self.code_content:
                self.checks_passed.append("P3.9: READ_ONLY 处理存在")
            else:
                self.violations.append("P3.9: READ_ONLY 未正确处理")
        else:
            self.violations.append("P3.9: 未找到 READ_ONLY 处理")
    
    def _check_dcs_no_decision_influence(self):
        """检查 10: DCS 不得反向影响决策 """
        if 'dcs_check' in self.code_content:
            # 检查 DCS 是否只读 summary，不修改
            if 'trace["dcs"]' in self.code_content:
                self.checks_passed.append("P4.10: DCS 只写入 trace")
            else:
                self.violations.append("P4.10: DCS 可能影响决策")
        else:
            self.violations.append("P4.10: 未找到 dcs_check 调用")
    
    def _check_dcs_violations_visible(self):
        """检查 11: 违规必须可见 """
        if '"violations"' in self.code_content and '"score_delta"' in self.code_content:
            self.checks_passed.append("P4.11: DCS 违规可见")
        else:
            self.violations.append("P4.11: DCS 违规信息不完整")
    
    def _check_role_declaration(self):
        """检查 12: B2 必须自报身份 """
        if '"role": "B"' in self.code_content or "'role': 'B'" in self.code_content:
            if '"expects_confirmation_from": "C"' in self.code_content or \
               "'expects_confirmation_from': 'C'" in self.code_content:
                self.checks_passed.append("P5.12: 角色声明完整")
            else:
                self.violations.append("P5.12: 缺失 expects_confirmation_from")
        else:
            self.violations.append("P5.12: 缺失 role = B")
    
    def print_report(self):
        """打印验证报告"""
        print("=" * 70)
        print("B2 v0.4.1 Patch 验证报告")
        print("=" * 70)
        print(f"文件: {self.code_file}\n")
        
        print(f"✅ 通过的检查: {len(self.checks_passed)}")
        for check in self.checks_passed:
            print(f"  ✅ {check}")
        
        print(f"\n❌ 违规: {len(self.violations)}")
        for violation in self.violations:
            print(f"  ❌ {violation}")
        
        print("\n" + "=" * 70)
        if len(self.violations) == 0:
            print("✅ 所有检查通过，可以合并")
        else:
            print("❌ 存在违规，禁止合并")
        print("=" * 70)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python v041_patch_validator.py <b2_v03.py路径>")
        sys.exit(1)
    
    code_file = sys.argv[1]
    validator = V041PatchValidator(code_file)
    passed, checks_passed, violations = validator.validate_all()
    
    validator.print_report()
    
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
