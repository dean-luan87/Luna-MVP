# -*- coding: utf-8 -*-
"""Action Hint Whitebox Trace M0 单测：遮挡流无互动、容器流有反馈、4 步推理与用户可见解释层。"""

from types import SimpleNamespace

from decision_monitor.action_hint_whitebox_trace import build_action_hint_whitebox_trace


def _ns(**kwargs):
    return SimpleNamespace(**kwargs)


def test_action_hint_whitebox_occlusion_no_interaction():
    """图2：遮挡流，无互动。primary 解释为「先移开遮挡」；exclusion 说明没选容器/一般搜索；user_visible_reason_primary 有值；interaction_trace = no_interaction_this_frame。"""
    ah = _ns(
        action_hint_primary="先把中间偏左位置前面的遮挡物移开看看",
        action_hint_followup="移开后再看看那个位置",
        action_hint_confirmation="看看遮挡后面有没有目标",
        action_hint_stage="guidance",
        action_hint_reason="occlusion_clear_flow+near_field",
        action_hint_applied=True,
    )
    osi = _ns(interaction_flow_type="occlusion_clear_flow")
    sidecar = _ns(focus_target_expression="中间偏左", focus_target_actionable_expression=None)
    grid_exp = _ns(grid_search_expansion_hint=None)
    cib = _ns(
        confirmation_input_raw_text=None,
        confirmation_input_type=None,
        confirmation_bridge_next_effect=None,
    )
    grid = _ns(recommended_search_cell_human_label=None)

    out = build_action_hint_whitebox_trace(
        action_hint_copy=ah,
        object_search_interaction=osi,
        spatial_expression_sidecar=sidecar,
        grid_search_expansion=grid_exp,
        confirmation_input_bridge=cib,
        local_task_space_grid=grid,
    )

    assert out.whitebox_applied is True
    assert len(out.reasoning_steps) == 4
    assert out.weight_allocation
    primary_item = next((w for w in out.weight_allocation if w.hint_id == "primary_occlusion"), None)
    assert primary_item is not None, "应选中 primary_occlusion"
    assert out.exclusion_log
    excluded_ids = [e.excluded_hint_id for e in out.exclusion_log]
    assert "primary_container" in excluded_ids or "primary_general_search" in excluded_ids
    assert out.interaction_trace
    assert out.interaction_trace[0].interaction_effect_on_hint == "no_interaction_this_frame"
    assert out.user_visible_explanation is not None
    assert out.user_visible_explanation.user_visible_reason_primary is not None
    assert "移开遮挡" in (out.user_visible_explanation.user_visible_reason_primary or "")


def test_action_hint_whitebox_container_with_feedback():
    """图3：容器流，有反馈（如 opened_container 或 confirmed_no）。primary 解释为「先看杯子里」；feedback 影响解释有值；user_visible_changed_by_feedback 有值。"""
    ah = _ns(
        action_hint_primary="先看中间偏右那个杯子里",
        action_hint_followup="如果没看到，再回到最后可信位置继续找",
        action_hint_confirmation="确认一下杯子里是不是目标",
        action_hint_stage="guidance",
        action_hint_reason="container_check_flow+actionable_expression+container_candidate",
        action_hint_applied=True,
    )
    osi = _ns(interaction_flow_type="container_check_flow")
    sidecar = _ns(focus_target_expression="中间偏右", focus_target_actionable_expression="右边")
    grid_exp = _ns(grid_search_expansion_hint=None)
    cib = _ns(
        confirmation_input_raw_text="打开了",
        confirmation_input_type="opened_container",
        confirmation_bridge_next_effect="advance_to_recheck",
    )
    grid = _ns(recommended_search_cell_human_label=None)

    out = build_action_hint_whitebox_trace(
        action_hint_copy=ah,
        object_search_interaction=osi,
        spatial_expression_sidecar=sidecar,
        grid_search_expansion=grid_exp,
        confirmation_input_bridge=cib,
        local_task_space_grid=grid,
    )

    assert out.whitebox_applied is True
    primary_item = next((w for w in out.weight_allocation if w.hint_id == "primary_container"), None)
    assert primary_item is not None, "应选中 primary_container"
    assert out.interaction_trace
    assert out.interaction_trace[0].interaction_effect_on_hint != "no_interaction_this_frame"
    assert out.user_visible_explanation is not None
    assert out.user_visible_explanation.user_visible_changed_by_feedback is not None
    assert "打开" in (out.user_visible_explanation.user_visible_changed_by_feedback or "") or "反馈" in (out.user_visible_explanation.user_visible_changed_by_feedback or "")


def test_action_hint_whitebox_user_visible_explanation_present():
    """固定 4 步推理；weight_allocation 含 selected primary + 至少 1 排除；user_visible_explanation 完整。"""
    ah = _ns(
        action_hint_primary="先看中间偏左的位置",
        action_hint_followup="如果没看到，再往附近找一找",
        action_hint_confirmation="看看那个位置是不是目标",
        action_hint_stage="guidance",
        action_hint_reason="general_search+focus_location",
        action_hint_applied=True,
    )
    osi = _ns(interaction_flow_type="general")
    sidecar = _ns(focus_target_expression="中间偏左", focus_target_actionable_expression=None)
    cib = _ns(confirmation_input_raw_text=None, confirmation_input_type=None, confirmation_bridge_next_effect=None)

    out = build_action_hint_whitebox_trace(
        action_hint_copy=ah,
        object_search_interaction=osi,
        spatial_expression_sidecar=sidecar,
        confirmation_input_bridge=cib,
    )

    assert len(out.reasoning_steps) == 4
    step_names = [s.step_name for s in out.reasoning_steps]
    assert "read_hint_context" in step_names
    assert "select_primary_hint" in step_names
    assert "select_followup_and_confirmation" in step_names
    assert "compose_hint_outcome" in step_names
    assert len(out.weight_allocation) >= 2
    assert len(out.exclusion_log) >= 1
    uv = out.user_visible_explanation
    assert uv is not None
    assert uv.user_visible_reason_primary is not None
    assert uv.user_visible_reason_followup is not None
    assert uv.user_visible_reason_confirmation is not None
    assert uv.user_visible_changed_by_feedback is not None
    assert uv.user_visible_excluded_alternative is not None


def test_action_hint_whitebox_bootstrap_path():
    """描述引导流：primary 为 bootstrap_description；exclusion 含其他主提示类型。"""
    ah = _ns(
        action_hint_primary="请先描述一下目标的大概外观",
        action_hint_followup="比如颜色、大小或放在什么附近",
        action_hint_confirmation="描述后我再帮你缩小范围",
        action_hint_stage="reasoning",
        action_hint_reason="target_unclear_or_description_bootstrap",
        action_hint_applied=True,
    )
    osi = _ns(interaction_flow_type="description_bootstrap_flow")
    sidecar = _ns(focus_target_expression=None, focus_target_actionable_expression=None)
    cib = _ns(confirmation_input_raw_text=None, confirmation_input_type=None, confirmation_bridge_next_effect=None)

    out = build_action_hint_whitebox_trace(
        action_hint_copy=ah,
        object_search_interaction=osi,
        spatial_expression_sidecar=sidecar,
        confirmation_input_bridge=cib,
    )

    primary_item = next((w for w in out.weight_allocation if w.hint_id == "bootstrap_description"), None)
    assert primary_item is not None
    assert out.user_visible_explanation is not None
    assert "描述" in (out.user_visible_explanation.user_visible_reason_primary or "")
