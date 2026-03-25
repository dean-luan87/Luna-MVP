# -*- coding: utf-8 -*-

from decision_monitor.memory_novel_information_channel import build_memory_novel_information_channel


def test_memory_driven_dominant():
    frame = {
        "object_temporal_ledger": {"focus_object_entry": {"last_confirmed_location": "table", "last_confirmed_ts": 1.0}},
        "visual_candidate_audit": {"detector_candidate_labels": []},
    }
    out = build_memory_novel_information_channel(frame).to_dict()
    assert out["dominant_reasoning_channel"] == "memory_derived"


def test_new_observed_dominant():
    frame = {"visual_candidate_audit": {"mapped_candidate_labels": ["cup", "bottle"]}}
    out = build_memory_novel_information_channel(frame).to_dict()
    assert out["dominant_reasoning_channel"] in ("newly_observed", "inferred_from_exclusion", "user_provided")
    assert out["novel_channel_count"] >= 1


def test_inferred_from_exclusion_creates_candidate():
    frame = {
        "reasoning_structure_tree": {"nodes": [{"node_id": "a", "status": "pruned"}], "pruned_node_ids": ["a"]},
        "confirmation_input_bridge": {"confirmation_bridge_next_effect": "advance_to_recheck"},
        "object_search_interaction": {"search_target_label": "维生素药瓶"},
    }
    out = build_memory_novel_information_channel(frame).to_dict()
    types = [c["channel_type"] for c in out["information_channels"]]
    assert "inferred_from_exclusion" in types
    assert out["novel_memory_candidate"] is not None


def test_user_provided_channel_exists():
    frame = {"confirmation_input_bridge": {"confirmation_input_raw_text": "我打开了", "confirmation_input_type": "opened_container"}}
    out = build_memory_novel_information_channel(frame).to_dict()
    types = [c["channel_type"] for c in out["information_channels"]]
    assert "user_provided" in types
    assert out["dominant_decision_channel"] == "user_provided"


def test_hybrid_present():
    frame = {
        "object_temporal_ledger": {"focus_object_entry": {"last_confirmed_location": "drawer", "last_confirmed_ts": 2.0}},
        "visual_candidate_audit": {"mapped_candidate_labels": ["drawer", "bottle"]},
    }
    out = build_memory_novel_information_channel(frame).to_dict()
    assert out["hybrid_channel_count"] >= 1
    assert out["dominant_decision_channel"] in ("hybrid", "memory_derived", "newly_observed")

