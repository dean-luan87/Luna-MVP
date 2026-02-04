from .c_threshold_registry import THRESHOLD_REGISTRY


def resolve_c_threshold_profile(system_snapshot: dict) -> str:
    """
    Phase-2 阈值选择规则：
    - 不读 Authority
    - 不读 BC
    - 不基于结果
    """
    if not isinstance(system_snapshot, dict):
        return "default"

    user_pref = system_snapshot.get("user_preference")
    if user_pref and user_pref in THRESHOLD_REGISTRY:
        return user_pref

    context = system_snapshot.get("context_mode")
    if context and context in THRESHOLD_REGISTRY:
        return context

    return "default"
