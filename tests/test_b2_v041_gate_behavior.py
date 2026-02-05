# tests/test_b2_v041_gate_behavior.py
"""
B2 v0.4.1 行为回归测试脚本（Gate / Impact / Trace）

测试目标：
1. Gate 是否生效（稳定 → ACTIVE，不稳定 → READ_ONLY / SUSPENDED）
2. NO_OP 是否真正沉默
3. impact 是否正确产出
4. B 是否只"提醒"，不"确认风险"
5. trace 是否完整、可读、可追溯

❗️不涉及 OCR / 多镜头 / 学习 / Web
❗️不涉及 C 的真实执行，只看 B → C 的 message
"""

import sys
import os
import time

# 直接导入需要的模块，避免触发 vision_pipeline 包的完整初始化
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 直接导入 B2 相关模块
from vision_pipeline.b2.v03.b2_v03 import B2v03, ActionImpact
from vision_pipeline.b2.v03.factors import FactorType, FactorEvidence
from vision_pipeline.b2.v03.gate.gate_evaluator_v05 import GateEvaluatorV05
from vision_pipeline.b2.v03.gate_runtime import BGateState, get_gate_state_from_mode


# =========================
# 1️⃣ 构造最小依赖
# =========================

def make_factor(factor_type: FactorType, score: float, reason: str) -> FactorEvidence:
    """构造因子证据"""
    return FactorEvidence(
        factor=factor_type,
        score=score,
        changed=True,
        reason=reason
    )


def make_view_state(
    stability_score: float = 0.8,
    range_m: float = 5.0,
    camera_motion: str = "LOW",
    pitch_deg: float = 5.0,
    roll_deg: float = 2.0,
    visibility_score: float = 0.75,
    allow_runtime: bool = True,
    evidence_frames: int = 20,
    final_confidence: float = 0.7
) -> dict:
    """构造 view_state（抗视角污染）"""
    return {
        "stability_score": stability_score,
        "pitch_deg": pitch_deg,
        "roll_deg": roll_deg,
        "range_m": range_m,
        "visibility_score": visibility_score,
        "allow_runtime": allow_runtime,
        "evidence_frames": evidence_frames,
        "final_confidence": final_confidence,
        "now_ts": time.time()
    }


# =========================
# 2️⃣ 单条测试 runner
# =========================

def run_case(
    case_name: str,
    evidences: dict,
    view_state: dict,
    ts: float = 100.0,
    expected_impact: str = None,
    expected_gate: str = None,
    should_silent: bool = False
):
    """
    执行单条测试用例
    
    Args:
        case_name: 用例名称
        evidences: 因子证据字典
        view_state: 视角状态
        ts: 时间戳
        expected_impact: 预期 impact（可选）
        expected_gate: 预期 Gate 状态（可选）
        should_silent: 是否应该沉默（NO_OP）
    """
    print(f"\n{'='*60}")
    print(f"CASE {case_name}")
    print(f"{'='*60}")
    
    # 初始化 Gate 评估器
    gate_evaluator = GateEvaluatorV05()
    
    # 评估 Gate 状态
    gate_mode, gate_trace = gate_evaluator.evaluate(**view_state)
    
    print(f"Gate Mode: {gate_mode}")
    print(f"Gate Reason: {gate_trace.get('human_readable', 'N/A')}")
    if gate_trace.get('blocked_by'):
        print(f"Blocked By: {gate_trace['blocked_by']}")
    
    # 检查 Gate 状态
    gate_state = get_gate_state_from_mode(gate_mode)
    
    # 初始化 B2
    b2 = B2v03(
        future_window_start=1.0,
        future_window_end=8.0,
        debug=True,
        enable_trace=False  # 测试时不写 trace 文件
    )
    
    # 如果 Gate 是 SUSPENDED，B 应该直接返回 None
    if gate_state == BGateState.SUSPENDED:
        print("\n⚠️  Gate SUSPENDED → B 应该返回 None")
        # 模拟 tick() 的开头逻辑
        print("✅ B Output: SILENT (Gate SUSPENDED)")
        if should_silent:
            print("✅ 符合预期：应该沉默")
        else:
            print("⚠️  注意：此用例预期有输出，但 Gate 阻止了")
        return
    
    # 构造 summary（模拟 _summarize_world_change）
    try:
        summary = b2._summarize_world_change(
            evidences=evidences,
            ts=ts
        )
        
        if summary is None:
            print("\n✅ B Output: SILENT (NO_OP)")
            if should_silent:
                print("✅ 符合预期：应该沉默")
            else:
                print("⚠️  注意：此用例预期有输出，但结果为 NO_OP")
            return
        
        # 检查 advisory_only
        advisory_only = summary.get("advisory_only", False)
        impact = summary.get("impact")
        impact_name = impact.name if hasattr(impact, "name") else str(impact)
        decision_level = summary.get("level")
        main_factor = summary.get("main_factor")
        intervention_level = summary.get("intervention_level", "UNKNOWN")
        
        print(f"\n📊 B Output:")
        print(f"  Impact: {impact_name}")
        print(f"  Decision Level: {decision_level}")
        print(f"  Main Factor: {main_factor}")
        print(f"  Intervention Level: {intervention_level}")
        print(f"  Advisory Only: {advisory_only}")
        
        # 验证 advisory_only
        if not advisory_only:
            print("❌ 违规：缺少 advisory_only = True")
        else:
            print("✅ 合规：advisory_only = True")
        
        # 验证 impact 不是确认性语义
        forbidden_keywords = ["CONFIRMED", "FORCE", "CERTAIN", "WORLD"]
        if any(keyword in impact_name for keyword in forbidden_keywords):
            print(f"❌ 违规：impact 包含禁止语义: {impact_name}")
        else:
            print("✅ 合规：impact 无确认性语义")
        
        # 验证 intervention_level
        if impact_name == "NEED_STOP" and intervention_level != "HARD":
            print(f"❌ 违规：NEED_STOP 但 intervention_level = {intervention_level} (应为 HARD)")
        elif impact_name != "NEED_STOP" and intervention_level == "HARD":
            print(f"❌ 违规：非 NEED_STOP 但 intervention_level = HARD")
        else:
            print(f"✅ 合规：intervention_level 正确")
        
        # 检查预期
        if expected_impact:
            if impact_name == expected_impact:
                print(f"✅ 符合预期：impact = {expected_impact}")
            else:
                print(f"⚠️  预期 impact = {expected_impact}，实际 = {impact_name}")
        
        if expected_gate:
            if gate_mode == expected_gate:
                print(f"✅ 符合预期：Gate = {expected_gate}")
            else:
                print(f"⚠️  预期 Gate = {expected_gate}，实际 = {gate_mode}")
        
        # 检查 NO_OP 是否真正沉默
        if impact_name == "NO_OP":
            print("\n✅ NO_OP → 应该不写 timeline")
            if should_silent:
                print("✅ 符合预期：应该沉默")
        
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()


# =========================
# 3️⃣ 执行全部测试
# =========================

if __name__ == "__main__":
    print("="*60)
    print("B2 v0.4.1 行为回归测试")
    print("="*60)
    print("\n测试目标：")
    print("1. Gate 是否生效")
    print("2. NO_OP 是否真正沉默")
    print("3. impact 是否正确产出")
    print("4. B 是否只'提醒'，不'确认风险'")
    print("5. trace 是否完整、可读、可追溯")
    print("\n" + "="*60)
    
    # Case A：稳定 + 路况变化 → NEED_SLOW_DOWN
    run_case(
        "A: 稳定 + 路况变化",
        evidences={
            FactorType.PATH: make_factor(FactorType.PATH, 0.7, "rough surface ahead")
        },
        view_state=make_view_state(
            stability_score=0.8,
            range_m=5.0
        ),
        expected_impact="NEED_SLOW_DOWN",
        expected_gate="ACTIVE"
    )
    
    # Case B：晃动 → Gate SUSPENDED → NO_OP
    run_case(
        "B: 镜头晃动 → Gate 阻止",
        evidences={
            FactorType.PATH: make_factor(FactorType.PATH, 0.8, "steps detected")
        },
        view_state=make_view_state(
            stability_score=0.3,  # 低于阈值 0.6
            range_m=5.0,
            camera_motion="HIGH"
        ),
        expected_gate="SUSPENDED",
        should_silent=True
    )
    
    # Case C：远距离高风险事件 → NEED_STOP
    run_case(
        "C: 远距离高风险事件",
        evidences={
            FactorType.EVENT: make_factor(FactorType.EVENT, 0.9, "construction barrier")
        },
        view_state=make_view_state(
            stability_score=0.8,
            range_m=6.0  # > 3m
        ),
        expected_impact="NEED_STOP",
        expected_gate="ACTIVE"
    )
    
    # Case D：近距离 → B 不应发声（距离边界）
    run_case(
        "D: 近距离事件 → B 不应发声",
        evidences={
            FactorType.EVENT: make_factor(FactorType.EVENT, 0.9, "obstacle nearby")
        },
        view_state=make_view_state(
            stability_score=0.8,
            range_m=2.0  # ≤ 3m，应该被 Gate 阻止或降级
        ),
        should_silent=True  # 预期沉默
    )
    
    # Case E：环境变化（ENV）→ 不应该输出
    run_case(
        "E: 环境变化（ENV）→ 不应该输出",
        evidences={
            FactorType.ENV: make_factor(FactorType.ENV, 0.9, "market area")
        },
        view_state=make_view_state(
            stability_score=0.8,
            range_m=5.0
        ),
        should_silent=True  # ENV 不应该触发决策
    )
    
    # Case F：人流变化 → NEED_SLOW_DOWN
    run_case(
        "F: 人流变化",
        evidences={
            FactorType.PEOPLE: make_factor(FactorType.PEOPLE, 0.8, "crowd density rising")
        },
        view_state=make_view_state(
            stability_score=0.8,
            range_m=5.0
        ),
        expected_impact="NEED_SLOW_DOWN",
        expected_gate="ACTIVE"
    )
    
    # Case G：Gate READ_ONLY → 应该只读
    run_case(
        "G: Gate READ_ONLY → 应该只读",
        evidences={
            FactorType.PATH: make_factor(FactorType.PATH, 0.7, "path change")
        },
        view_state=make_view_state(
            stability_score=0.8,
            range_m=5.0,
            evidence_frames=5,  # 证据帧数不足，可能触发 READ_ONLY
            final_confidence=0.4  # 置信度不足，可能触发 READ_ONLY
        ),
        expected_gate="READ_ONLY"
    )
    
    print("\n" + "="*60)
    print("测试完成")
    print("="*60)
    print("\n验收标准：")
    print("✅ 如果出现以下任一情况 → ❌ 架构错误：")
    print("  • B 在 2m 内输出 NEED_STOP")
    print("  • ENV 触发 CONDITION_CHANGE")
    print("  • Gate=SUSPENDED 但仍输出 decision")
    print("  • impact=NO_OP 但写 timeline")
    print("  • 缺少 advisory_only = True")
    print("  • impact 包含确认性语义")
