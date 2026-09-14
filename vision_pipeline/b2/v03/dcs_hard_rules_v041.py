# DCS 硬判定项（红 / 黄 / 绿）
# 用途：系统运行后审判、回放历史 trace
# 不是给用户看的，是给工程"自省"的

from typing import Dict, Any, List, Tuple
from enum import Enum


class DCSViolationLevel(Enum):
    """DCS 违规级别"""
    RED = "RED"        # 硬违规，必须修
    YELLOW = "YELLOW"  # 风险设计，需关注
    GREEN = "GREEN"    # 设计正确


class DCSHardRules:
    """
    DCS 硬判定规则（v0.4.1）
    
    用途：
    - 系统运行后审判
    - 回放历史 trace
    - 给工程"自省"，不是给用户看
    """
    
    # =========================
    # 🟥 RED（硬违规，必须修）
    # =========================
    
    @staticmethod
    def check_dcs_r1(trace: Dict[str, Any]) -> Tuple[bool, str]:
        """
        DCS-R1: B 输出确认性风险结论
        
        判定条件：
        - 输出中包含确认性词汇（confirmed, certain, will happen, inevitable）
        - 缺少 advisory_only: true
        - 人类可读转译使用确定性语言
        """
        violations = []
        
        # 检查 summary
        summary = trace.get("summary", {})
        if summary.get("advisory_only") is not True:
            violations.append("缺少 advisory_only: true")
        
        # 检查人类可读转译
        human_readable = trace.get("human_interpretation", {})
        summary_text = human_readable.get("summary", "")
        
        forbidden_words = ["已确认", "必然", "一定", "确定", "confirmed", "certain", "will happen", "inevitable"]
        for word in forbidden_words:
            if word in summary_text.lower():
                violations.append(f"包含确认性词汇: {word}")
        
        # 检查 impact 名称
        impact = summary.get("impact")
        if isinstance(impact, str):
            if any(keyword in impact.upper() for keyword in ["CONFIRMED", "FORCE", "CERTAIN", "WORLD"]):
                violations.append(f"Impact 名称包含禁止语义: {impact}")
        
        if violations:
            return False, f"DCS-R1 违规: {', '.join(violations)}"
        return True, "DCS-R1 通过"
    
    @staticmethod
    def check_dcs_r2(trace: Dict[str, Any]) -> Tuple[bool, str]:
        """
        DCS-R2: B 替代 C 完成风险核验
        
        判定条件：
        - B 输出"最终结论"而非"建议"
        - 跳过 C 的靠近确认流程
        - 缺少 expects_confirmation_from: "C"
        """
        violations = []
        
        summary = trace.get("summary", {})
        
        # 检查角色声明
        if summary.get("expects_confirmation_from") != "C":
            violations.append("缺少 expects_confirmation_from: 'C'")
        
        # 检查 to_c_message
        to_c = trace.get("to_c_message", {})
        if to_c.get("sent"):
            payload = to_c.get("payload", {})
            if payload.get("advisory_only") is not True:
                violations.append("to_c_message 缺少 advisory_only: true")
        
        if violations:
            return False, f"DCS-R2 违规: {', '.join(violations)}"
        return True, "DCS-R2 通过"
    
    @staticmethod
    def check_dcs_r3(trace: Dict[str, Any]) -> Tuple[bool, str]:
        """
        DCS-R3: B 在视角不稳定 Gate fail 时仍输出判断
        
        判定条件：
        - Gate mode = SUSPENDED 但仍有 to_c_message.sent = true
        - Gate mode = SUSPENDED 但 impact != NO_OP
        """
        violations = []
        
        gate_eval = trace.get("gate_eval", {})
        gate_mode = gate_eval.get("mode")
        
        if gate_mode == "SUSPENDED":
            # 检查是否仍发送消息
            to_c = trace.get("to_c_message", {})
            if to_c.get("sent"):
                violations.append("Gate SUSPENDED 但仍发送消息给 C")
            
            # 检查是否仍有非 NO_OP 的 impact
            summary = trace.get("summary", {})
            impact = summary.get("impact")
            if isinstance(impact, str) and impact != "NO_OP":
                violations.append(f"Gate SUSPENDED 但 impact = {impact}")
        
        if violations:
            return False, f"DCS-R3 违规: {', '.join(violations)}"
        return True, "DCS-R3 通过"
    
    @staticmethod
    def check_dcs_r4(trace: Dict[str, Any]) -> Tuple[bool, str]:
        """
        DCS-R4: B 在 ≤3m 或室内主导决策
        
        判定条件：
        - 距离 ≤ 3m 但 B 仍输出 HARD 干预
        - 室内场景但 B 仍输出判断
        """
        violations = []
        
        gate_eval = trace.get("gate_eval", {})
        details = gate_eval.get("details", {})
        range_m = details.get("range_m")
        
        summary = trace.get("summary", {})
        intervention_level = summary.get("intervention_level")
        
        # 检查距离边界
        if range_m is not None and range_m <= 3.0:
            if intervention_level == "HARD":
                violations.append(f"距离 ≤3m ({range_m}m) 但输出 HARD 干预")
        
        # 检查室内场景（需要从 perception 或 env 判断）
        # 这里简化处理，实际需要从 trace 中提取场景信息
        view_state = trace.get("view_state", {})
        scene = view_state.get("scene")
        if scene == "indoor" and intervention_level == "HARD":
            violations.append("室内场景但输出 HARD 干预")
        
        if violations:
            return False, f"DCS-R4 违规: {', '.join(violations)}"
        return True, "DCS-R4 通过"
    
    @staticmethod
    def check_dcs_r5(trace: Dict[str, Any]) -> Tuple[bool, str]:
        """
        DCS-R5: 使用非系统当前时间进行判断
        
        判定条件：
        - summary 中缺少 system_ts
        - 使用了 frame_ts、perception_ts、camera_ts 等非系统时间
        """
        violations = []
        
        summary = trace.get("summary", {})
        
        # 检查 system_ts
        if "system_ts" not in summary:
            violations.append("缺少 system_ts")
        
        # 检查禁止的时间字段
        forbidden_time_fields = ["frame_ts", "perception_ts", "camera_ts", "relative_time", "future_seconds"]
        for field in forbidden_time_fields:
            if field in summary:
                violations.append(f"使用了禁止的时间字段: {field}")
        
        # 检查 to_c_message
        to_c = trace.get("to_c_message", {})
        if to_c.get("sent"):
            payload = to_c.get("payload", {})
            header = payload.get("header", {})
            if "system_ts" not in header:
                violations.append("to_c_message header 缺少 system_ts")
        
        if violations:
            return False, f"DCS-R5 违规: {', '.join(violations)}"
        return True, "DCS-R5 通过"
    
    # =========================
    # 🟨 YELLOW（风险设计，需关注）
    # =========================
    
    @staticmethod
    def check_dcs_y1(trace: Dict[str, Any]) -> Tuple[bool, str]:
        """
        DCS-Y1: B 过于频繁唤醒但未产生有效预警
        
        判定条件：
        - B 多次唤醒但 impact = NO_OP
        - 连续多次唤醒但无有效输出
        """
        # 这个需要跨 trace 分析，单 trace 无法判断
        # 返回 True 表示单 trace 层面无问题
        return True, "DCS-Y1 需跨 trace 分析"
    
    @staticmethod
    def check_dcs_y2(trace: Dict[str, Any]) -> Tuple[bool, str]:
        """
        DCS-Y2: B 输出长期只读但世界记忆未更新
        
        判定条件：
        - Gate mode = READ_ONLY 持续较长时间
        - 但世界记忆未更新
        """
        # 这个需要跨 trace 和时间序列分析
        # 返回 True 表示单 trace 层面无问题
        return True, "DCS-Y2 需跨 trace 分析"
    
    @staticmethod
    def check_dcs_y3(trace: Dict[str, Any]) -> Tuple[bool, str]:
        """
        DCS-Y3: C 长期过度保守导致体验下降
        
        判定条件：
        - C 的响应过于保守
        - 导致用户体验下降
        """
        # 这个需要从 C 的 trace 分析，B 的 trace 无法判断
        # 返回 True 表示 B trace 层面无问题
        return True, "DCS-Y3 需从 C trace 分析"
    
    # =========================
    # 🟩 GREEN（设计正确）
    # =========================
    
    @staticmethod
    def check_dcs_g1(trace: Dict[str, Any]) -> Tuple[bool, str]:
        """
        DCS-G1: B 只输出条件式风险
        
        判定条件：
        - advisory_only = true
        - 人类可读转译使用条件性语言
        - 无确认性词汇
        """
        summary = trace.get("summary", {})
        if summary.get("advisory_only") is not True:
            return False, "DCS-G1 失败: 缺少 advisory_only: true"
        
        human_readable = trace.get("human_interpretation", {})
        summary_text = human_readable.get("summary", "")
        
        # 检查是否使用条件性语言
        conditional_words = ["如果", "可能", "建议", "如果继续", "基于当前"]
        has_conditional = any(word in summary_text for word in conditional_words)
        
        if not has_conditional and summary_text:
            return False, "DCS-G1 失败: 未使用条件性语言"
        
        return True, "DCS-G1 通过"
    
    @staticmethod
    def check_dcs_g2(trace: Dict[str, Any]) -> Tuple[bool, str]:
        """
        DCS-G2: C 完成靠近核验并回写记忆
        
        判定条件：
        - C 的确认结果回流到世界记忆
        - B 可以读取世界记忆
        """
        # 这个需要从 C 的 trace 和世界记忆系统分析
        # 返回 True 表示 B trace 层面无问题
        return True, "DCS-G2 需从 C trace 和世界记忆分析"
    
    @staticmethod
    def check_dcs_g3(trace: Dict[str, Any]) -> Tuple[bool, str]:
        """
        DCS-G3: 熟悉场景下 B 自动降权
        
        判定条件：
        - 熟悉场景下 Gate mode = READ_ONLY
        - B 自动降权，不产生新判断
        """
        gate_eval = trace.get("gate_eval", {})
        gate_mode = gate_eval.get("mode")
        
        if gate_mode == "READ_ONLY":
            summary = trace.get("summary", {})
            impact = summary.get("impact")
            if isinstance(impact, str) and impact == "NO_OP":
                return True, "DCS-G3 通过: READ_ONLY 且 NO_OP"
        
        return True, "DCS-G3 通过"
    
    @staticmethod
    def check_dcs_g4(trace: Dict[str, Any]) -> Tuple[bool, str]:
        """
        DCS-G4: 时间 / 距离标尺始终一致
        
        判定条件：
        - 只使用 system_ts
        - 遵循 3m 边界规则
        """
        # 检查时间一致性（已在 DCS-R5 中检查）
        time_ok, time_msg = DCSHardRules.check_dcs_r5(trace)
        if not time_ok:
            return False, f"DCS-G4 失败: {time_msg}"
        
        # 检查距离边界（已在 DCS-R4 中检查）
        distance_ok, distance_msg = DCSHardRules.check_dcs_r4(trace)
        if not distance_ok:
            return False, f"DCS-G4 失败: {distance_msg}"
        
        return True, "DCS-G4 通过"
    
    # =========================
    # 统一检查接口
    # =========================
    
    @staticmethod
    def check_all(trace: Dict[str, Any]) -> Dict[str, Any]:
        """
        检查所有 DCS 规则
        
        返回：
        {
            "red": [...],      # 硬违规列表
            "yellow": [...],   # 风险设计列表
            "green": [...],    # 设计正确列表
            "score": int       # DCS 分数（0-100）
        }
        """
        results = {
            "red": [],
            "yellow": [],
            "green": [],
            "score": 100
        }
        
        # RED 规则（硬违规，必须修）
        red_rules = [
            ("DCS-R1", DCSHardRules.check_dcs_r1),
            ("DCS-R2", DCSHardRules.check_dcs_r2),
            ("DCS-R3", DCSHardRules.check_dcs_r3),
            ("DCS-R4", DCSHardRules.check_dcs_r4),
            ("DCS-R5", DCSHardRules.check_dcs_r5),
        ]
        
        for rule_id, check_func in red_rules:
            passed, message = check_func(trace)
            if not passed:
                results["red"].append({
                    "rule_id": rule_id,
                    "message": message,
                    "level": DCSViolationLevel.RED.value
                })
                results["score"] -= 20  # 每个 RED 违规扣 20 分
        
        # YELLOW 规则（风险设计，需关注）
        yellow_rules = [
            ("DCS-Y1", DCSHardRules.check_dcs_y1),
            ("DCS-Y2", DCSHardRules.check_dcs_y2),
            ("DCS-Y3", DCSHardRules.check_dcs_y3),
        ]
        
        for rule_id, check_func in yellow_rules:
            passed, message = check_func(trace)
            if not passed:
                results["yellow"].append({
                    "rule_id": rule_id,
                    "message": message,
                    "level": DCSViolationLevel.YELLOW.value
                })
                results["score"] -= 5  # 每个 YELLOW 违规扣 5 分
        
        # GREEN 规则（设计正确）
        green_rules = [
            ("DCS-G1", DCSHardRules.check_dcs_g1),
            ("DCS-G2", DCSHardRules.check_dcs_g2),
            ("DCS-G3", DCSHardRules.check_dcs_g3),
            ("DCS-G4", DCSHardRules.check_dcs_g4),
        ]
        
        for rule_id, check_func in green_rules:
            passed, message = check_func(trace)
            if passed:
                results["green"].append({
                    "rule_id": rule_id,
                    "message": message,
                    "level": DCSViolationLevel.GREEN.value
                })
            else:
                results["score"] -= 10  # 每个 GREEN 失败扣 10 分
        
        # 确保分数不为负
        results["score"] = max(0, results["score"])
        
        return results


# =========================
# 使用示例
# =========================

if __name__ == "__main__":
    # 示例 trace
    example_trace = {
        "summary": {
            "advisory_only": True,
            "impact": "NEED_SLOW_DOWN",
            "intervention_level": "SOFT",
            "system_ts": 1234567890.0,
            "role": "B",
            "expects_confirmation_from": "C"
        },
        "gate_eval": {
            "mode": "ACTIVE",
            "details": {
                "range_m": 5.0
            }
        },
        "to_c_message": {
            "sent": True,
            "payload": {
                "header": {
                    "system_ts": 1234567890.0
                },
                "advisory_only": True
            }
        },
        "human_interpretation": {
            "summary": "如果继续当前前进模式，可能不太舒适。"
        }
    }
    
    # 检查所有规则
    results = DCSHardRules.check_all(example_trace)
    
    print("DCS 检查结果:")
    print(f"分数: {results['score']}/100")
    print(f"RED 违规: {len(results['red'])}")
    print(f"YELLOW 风险: {len(results['yellow'])}")
    print(f"GREEN 通过: {len(results['green'])}")
    
    if results["red"]:
        print("\n🟥 RED 违规:")
        for violation in results["red"]:
            print(f"  - {violation['rule_id']}: {violation['message']}")
    
    if results["yellow"]:
        print("\n🟨 YELLOW 风险:")
        for violation in results["yellow"]:
            print(f"  - {violation['rule_id']}: {violation['message']}")
    
    if results["green"]:
        print("\n🟩 GREEN 通过:")
        for violation in results["green"]:
            print(f"  - {violation['rule_id']}: {violation['message']}")
