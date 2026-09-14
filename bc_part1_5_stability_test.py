from dataclasses import dataclass, asdict
from typing import List, Dict, Any

# ===== 根据你工程实际路径调整这三个 import =====
from luna_badge_v1_2.governance.output_controller.controller import ModelOutputController
from luna_badge_v1_2.governance.output_controller.authority import resolve_authority

# =================================================


# ---------- Mock 基础结构 ----------

@dataclass
class SystemSnapshot:
    perception_state: str
    calibration_state: str
    control_distortion: bool
    hardware_state: str
    risk_level: str
    context_mode: str


def mock_model_outputs() -> List[Dict[str, Any]]:
    """固定 B 候选，不关心内容，只要非空"""
    return [
        {
            "model_id": "b_candidate_v1",
            "model_version": "v1",
            "data": {"candidate": "stub"},
            "confidence": 0.8,
            "assumptions": {"test": True},
            "cost_estimate": {"risk_proxy": 0.2},
            "explanation": "mock candidate",
        }
    ]


# ---------- 核心测试函数 ----------

def run_case(name: str, snapshot: SystemSnapshot):
    controller = ModelOutputController()

    result = controller.process(
        task_domain="navigation",
        model_outputs=mock_model_outputs(),
        system_snapshot=asdict(snapshot),
    )

    bc_snapshot = result.get("decision_trace", {}).get("bc_snapshot")

    print(f"\n=== {name} ===")
    print("Authority:", bc_snapshot["authority"])
    print("Abilities:", bc_snapshot["abilities"])
    print("Gate:", bc_snapshot["gate"])
    print("Used candidates:", len(bc_snapshot["used_candidates"]))

    # --- 关键断言（结构性，不看业务） ---
    assert bc_snapshot is not None, "BCSnapshot missing"
    assert "authority" in bc_snapshot
    assert "abilities" in bc_snapshot
    assert "gate" in bc_snapshot

    # A5 硬约束
    if bc_snapshot["authority"]["effective"] == "A5":
        assert len(bc_snapshot["used_candidates"]) == 0, "A5 must produce zero output"


# ---------- 测试用例 ----------

def main():
    print("\nRunning BC-Part-1.5 Stability Tests")

    # T-01 感知稳定性
    run_case(
        "T1-1 perception STABLE",
        SystemSnapshot(
            perception_state="STABLE",
            calibration_state="READY",
            control_distortion=False,
            hardware_state="OK",
            risk_level="LOW",
            context_mode="NORMAL",
        ),
    )

    run_case(
        "T1-2 perception UNSTABLE",
        SystemSnapshot(
            perception_state="UNSTABLE",
            calibration_state="READY",
            control_distortion=False,
            hardware_state="OK",
            risk_level="LOW",
            context_mode="NORMAL",
        ),
    )

    # T-02 校准未完成
    run_case(
        "T2 calibration NOT_READY",
        SystemSnapshot(
            perception_state="STABLE",
            calibration_state="NOT_READY",
            control_distortion=False,
            hardware_state="OK",
            risk_level="LOW",
            context_mode="NORMAL",
        ),
    )

    # T-03 控制失真
    run_case(
        "T3 control distortion",
        SystemSnapshot(
            perception_state="STABLE",
            calibration_state="READY",
            control_distortion=True,
            hardware_state="OK",
            risk_level="LOW",
            context_mode="NORMAL",
        ),
    )

    # T-04 硬件失败 → A5
    run_case(
        "T4 hardware FAILED",
        SystemSnapshot(
            perception_state="STABLE",
            calibration_state="READY",
            control_distortion=False,
            hardware_state="FAILED",
            risk_level="LOW",
            context_mode="NORMAL",
        ),
    )

    print("\nALL BC-Part-1.5 TESTS COMPLETED")


if __name__ == "__main__":
    main()
