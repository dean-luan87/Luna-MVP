from .ability_matrix import AuthorityLevel


def _norm(value) -> str:
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if value is None:
        return ""
    return str(value).upper()


def resolve_authority(system_snapshot: dict) -> AuthorityLevel:
    """
    只读 system_snapshot
    不读模型输出
    不写状态
    Authority 只能降级
    """
    if not isinstance(system_snapshot, dict):
        return AuthorityLevel.A3

    hardware = _norm(system_snapshot.get("hardware_state") or system_snapshot.get("hardware"))
    calibration = _norm(system_snapshot.get("calibration_state") or system_snapshot.get("calibration"))
    control_distortion = _norm(system_snapshot.get("control_distortion"))
    perception = _norm(system_snapshot.get("perception_state") or system_snapshot.get("perception"))
    risk = _norm(system_snapshot.get("risk_level") or system_snapshot.get("risk"))
    context = _norm(system_snapshot.get("context_mode") or system_snapshot.get("context"))

    if hardware in {"FAULT", "FAILED"}:
        return AuthorityLevel.A5
    if calibration in {"FAILED", "NOT_READY"}:
        return AuthorityLevel.A5
    if control_distortion in {"FAIL_SAFE", "TRUE"}:
        return AuthorityLevel.A5

    if perception == "UNSTABLE":
        return AuthorityLevel.A4
    if control_distortion == "DEGRADED":
        return AuthorityLevel.A4

    if risk == "HIGH" and context != "SURVIVAL":
        return AuthorityLevel.A2
    if risk == "HIGH" and context == "SURVIVAL":
        return AuthorityLevel.A4

    return AuthorityLevel.A1
