from __future__ import annotations


def build_negative_guards() -> dict[str, bool]:
    return {
        "real_runtime_execution": False,
        "provider_invocation": False,
        "model_call": False,
        "camera_execution": False,
        "ocr_execution": False,
        "slam_execution": False,
        "audio_execution": False,
        "database_write": False,
        "vector_store_write": False,
        "embedding_execution": False,
        "scheduler_execution": False,
        "device_control": False,
        "source_owner_mutation": False,
        "field_state_direct_mutation": False,
        "context_direct_mutation": False,
        "intent_mutation": False,
        "decision_mutation": False,
        "task_external_mutation": False,
        "memory_mutation": False,
        "learning_execution": False,
        "self_mutation": False,
        "personality_mutation": False,
        "emotion_engine_execution": False,
        "b_route_execution": False,
        "semantic_compression_execution": False,
        "cross_user_transfer": False,
        "real_side_effect": False,
    }

