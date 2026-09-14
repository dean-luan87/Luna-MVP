# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-010 — OCR Stage-2 Provider Dependency / Credentials /
Input Snapshot & Approval Gate v0.

Freezes dependency snapshot, credential presence (no secret values), input sample
metadata + sha256, fallback, runbook snapshot, and approval gate — without invoking
OCR providers/models, network, camera, or video streams.

Voice interaction main chain is NOT wired; this module does not integrate Voice/TTS.
"""

from __future__ import annotations

import hashlib
import importlib
import importlib.util
import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE = "Phase-Mainline-GuardedTrial-010"

ALLOWED_IMAGE_EXTENSIONS = frozenset({".png", ".jpg", ".jpeg", ".webp"})

# Env keys that may gate cloud OCR (checked for presence only; never logged).
_OPTIONAL_CLOUD_CREDENTIAL_KEYS = (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "GOOGLE_APPLICATION_CREDENTIALS",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def compute_file_sha256_v0(path: str | Path) -> str:
    """Streaming SHA-256 of file bytes (integrity only; not OCR pixel decode)."""
    p = Path(path).expanduser().resolve()
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_python_import_available_v0(module_name: str) -> Tuple[bool, Optional[str]]:
    """Try import module; return (ok, version_or_none). Does not invoke OCR."""
    try:
        m = importlib.import_module(module_name)
        ver = getattr(m, "__version__", None)
        if ver is None and hasattr(m, "version"):
            ver = str(getattr(m, "version", "")) or None
        return True, str(ver) if ver is not None else None
    except Exception:
        return False, None


def check_module_spec_available_v0(module_name: str) -> bool:
    """Lightweight availability probe without importing heavy runtimes (e.g. paddle)."""
    try:
        return importlib.util.find_spec(module_name) is not None
    except Exception:
        return False


def validate_ocr_provider_dependency_snapshot_v0(*, repo_root: Optional[Path] = None) -> Dict[str, Any]:
    """
    Static import probes for libraries commonly used by local OCR adapters.
    No OCR model inference.
    """
    root = repo_root or _repo_root()
    # Heavy / optional: use find_spec only to avoid importing large frameworks during approval gate.
    spec_only = {"paddle", "torch", "onnxruntime", "rapidocr_onnxruntime", "rapidocr"}
    full_import = [
        ("numpy", "numpy"),
        ("PIL", "PIL"),
        ("cv2", "cv2"),
    ]
    rows: List[Dict[str, Any]] = []
    for name, mod in full_import:
        ok, ver = check_python_import_available_v0(mod)
        rows.append(
            {
                "name": name,
                "import_available": ok,
                "version": ver,
                "required_for_next_phase": name in {"numpy", "cv2"},
                "notes": "import probe only; no OCR invocation",
            }
        )
    for name in sorted(spec_only):
        ok = check_module_spec_available_v0(name)
        rows.append(
            {
                "name": name,
                "import_available": ok,
                "version": None,
                "required_for_next_phase": False,
                "notes": "find_spec only (avoid heavy import side effects in Phase-010)",
            }
        )
    return {
        "repo_root": str(root),
        "dependencies": rows,
        "snapshot_complete": True,
    }


def validate_ocr_provider_credentials_snapshot_v0() -> Dict[str, Any]:
    """
    Check presence of optional credential env vars without logging values.
    Local offline OCR may be not_required.
    """
    import os

    checked_keys = list(_OPTIONAL_CLOUD_CREDENTIAL_KEYS)
    present_any = False
    for k in checked_keys:
        v = os.environ.get(k)
        if v is not None and str(v).strip():
            present_any = True
    # Local guarded trial default: credentials not strictly required if policy stays offline/local.
    credential_status = "present" if present_any else "not_required"
    return {
        "required": False,
        "present": present_any,
        "checked_keys": checked_keys,
        "secret_values_logged": False,
        "credential_status": credential_status,
    }


def validate_ocr_input_sample_snapshot_v0(input_image_path: str) -> Dict[str, Any]:
    """
    File existence, extension, basic metadata, sha256. No pixel decode / no OCR.
    """
    p = Path(input_image_path).expanduser()
    blockers: List[str] = []
    ext = p.suffix.lower()
    exists = p.exists()
    is_file = p.is_file() if exists else False
    extension_allowed = ext in ALLOWED_IMAGE_EXTENSIONS
    if not p.is_absolute():
        blockers.append("input_image_must_be_absolute_path")
    if not exists:
        blockers.append("input_image_missing")
    elif not is_file:
        blockers.append("input_image_not_a_file")
    elif not extension_allowed:
        blockers.append("input_image_extension_not_allowed")

    sha256_hex = ""
    size_bytes = 0
    if is_file and extension_allowed:
        try:
            size_bytes = p.stat().st_size
            sha256_hex = compute_file_sha256_v0(p)
        except OSError as e:
            blockers.append(f"input_image_stat_or_hash_failed:{e!r}")

    will_read_pixels = False
    will_invoke_ocr = False

    return {
        "path": str(p.resolve()) if exists else str(input_image_path),
        "exists": exists,
        "is_file": is_file,
        "extension_allowed": extension_allowed,
        "sha256": sha256_hex or None,
        "size_bytes": size_bytes,
        "will_read_pixels": will_read_pixels,
        "will_invoke_ocr": will_invoke_ocr,
        "blockers": blockers,
    }


def validate_ocr_fallback_snapshot_v0(*, repo_root: Optional[Path] = None) -> Dict[str, Any]:
    root = repo_root or _repo_root()
    sel_doc = root / "docs/architecture/LUNA_OCR_OFFLINE_SOURCE_SELECTION_AND_FALLBACK_POLICY_V0.md"
    policy_py = root / "capabilities/model_ocr/offline_source_policy_v0.py"
    return {
        "not_available_supported": sel_doc.is_file() and policy_py.is_file(),
        "provider_error_fallback_supported": True,
        "governance_leakage_blocked": True,
        "refs": {
            "selection_doc": str(sel_doc),
            "selector_module": str(policy_py),
        },
    }


def validate_ocr_controlled_provider_runbook_snapshot_v0(static_config_root: Path) -> Dict[str, Any]:
    """Read Phase-009 runbook JSON from static config output directory."""
    root = static_config_root.expanduser().resolve()
    candidates = [
        root / "ocr_stage2_controlled_provider_runbook.json",
        root / "ocr_stage2_controlled_provider_runbook_009.json",
    ]
    chosen = next((p for p in candidates if p.is_file()), None)
    if chosen is None:
        return {"found": False, "path": None, "runbook": None, "blockers": ["controlled_provider_runbook_missing_in_static_config_root"]}
    try:
        obj = json.loads(chosen.read_text(encoding="utf-8"))
    except Exception as e:
        return {"found": False, "path": str(chosen), "runbook": None, "blockers": [f"runbook_unparseable:{e!r}"]}
    return {"found": True, "path": str(chosen), "runbook": obj, "blockers": []}


def build_ocr_stage2_provider_approval_gate_v0(
    *,
    dependency_snapshot: Dict[str, Any],
    credentials_snapshot: Dict[str, Any],
    input_sample_snapshot: Dict[str, Any],
    fallback_snapshot: Dict[str, Any],
    runbook_snapshot: Dict[str, Any],
    blockers: List[str],
    warnings: List[str],
) -> Dict[str, Any]:
    verdict = "NO_GO"
    if not blockers:
        verdict = "GO" if not warnings else "CONDITIONAL_GO"

    hard_audit = {
        "runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocr_model_invoked": False,
        "network_request_invoked": False,
        "semantic_interpretation_enabled": False,
        "midplatform_invoked": False,
        "scene_delta_invoked": False,
        "world_context_invoked": False,
        "qwen_invoked": False,
        "real_tts_invoked": False,
        "playback_invoked": False,
        "downstream_invocation_count": 0,
        "navigation_action": None,
        "world_write_invoked": False,
        "hive_upload_invoked": False,
    }

    provider_deps = []
    for d in dependency_snapshot.get("dependencies") or []:
        provider_deps.append(
            {
                "name": d.get("name"),
                "import_available": d.get("import_available"),
                "version": d.get("version"),
                "required_for_next_phase": d.get("required_for_next_phase"),
            }
        )

    cred = credentials_snapshot
    inp = input_sample_snapshot
    fb = fallback_snapshot
    rb_ok = bool(runbook_snapshot.get("found"))

    return {
        "approval_id": f"ocr_s2_approve_{uuid.uuid4().hex[:16]}",
        "capability": "ocr",
        "stage": "stage2_ocr_guarded_trial",
        "approval_mode": "pre_execution_approval_gate",
        "phase": PHASE,
        "voice_interaction_main_chain_note": "Voice output governance / RequestTrace shadow are not full voice interaction; main voice I/O chain not wired.",
        "provider_invocation_allowed_by_this_phase": False,
        "semantic_interpretation_allowed_by_this_phase": False,
        "midplatform_forward_allowed_by_this_phase": False,
        "ocr_provider_invoked": False,
        "ocr_model_invoked": False,
        "network_request_invoked": False,
        "provider_dependencies": provider_deps,
        "credentials": {
            "required": bool(cred.get("required")),
            "present": bool(cred.get("present")),
            "checked_keys": list(cred.get("checked_keys") or []),
            "secret_values_logged": False,
            "credential_status": cred.get("credential_status"),
        },
        "input_sample": {
            "path": inp.get("path"),
            "exists": inp.get("exists"),
            "is_file": inp.get("is_file"),
            "extension_allowed": inp.get("extension_allowed"),
            "sha256": inp.get("sha256"),
            "size_bytes": inp.get("size_bytes"),
            "will_read_pixels": inp.get("will_read_pixels"),
            "will_invoke_ocr": inp.get("will_invoke_ocr"),
        },
        "fallback": {
            "not_available_supported": bool(fb.get("not_available_supported")),
            "provider_error_fallback_supported": bool(fb.get("provider_error_fallback_supported")),
            "governance_leakage_blocked": bool(fb.get("governance_leakage_blocked")),
        },
        "controlled_provider_runbook_snapshot": runbook_snapshot,
        "approval_gate_result": verdict if not blockers else "NO_GO",
        "blockers": blockers,
        "warnings": warnings,
        "hard_audit": hard_audit,
        "runbook_present": rb_ok,
    }


def run_ocr_stage2_provider_approval_gate_v0(
    *,
    static_config_root: str,
    input_image_path: str,
    repo_root: Optional[Path] = None,
) -> Dict[str, Any]:
    rr = repo_root or _repo_root()
    blockers: List[str] = []
    warnings: List[str] = []

    scr = Path(static_config_root).expanduser().resolve()
    if not scr.is_dir():
        blockers.append("static_config_root_not_readable")

    dep = validate_ocr_provider_dependency_snapshot_v0(repo_root=rr)
    cred = validate_ocr_provider_credentials_snapshot_v0()
    inp = validate_ocr_input_sample_snapshot_v0(input_image_path)
    fb = validate_ocr_fallback_snapshot_v0(repo_root=rr)
    rb = validate_ocr_controlled_provider_runbook_snapshot_v0(scr)

    blockers.extend(inp.get("blockers") or [])
    if not fb.get("not_available_supported"):
        blockers.append("fallback_not_ready")
    blockers.extend(rb.get("blockers") or [])
    if cred.get("credential_status") == "unknown":
        warnings.append("credential_status_unknown")

    for d in dep.get("dependencies") or []:
        if d.get("name") == "numpy" and not d.get("import_available"):
            warnings.append("numpy_import_missing_reverify_on_target_machine")
        if d.get("name") == "cv2" and not d.get("import_available"):
            warnings.append("opencv_import_missing_reverify_on_target_machine")

    gate = build_ocr_stage2_provider_approval_gate_v0(
        dependency_snapshot=dep,
        credentials_snapshot=cred,
        input_sample_snapshot={k: v for k, v in inp.items() if k != "blockers"},
        fallback_snapshot=fb,
        runbook_snapshot=rb,
        blockers=blockers,
        warnings=warnings,
    )
    gate["static_config_root"] = str(scr)
    gate["provider_dependency_snapshot"] = dep
    gate["provider_credentials_snapshot"] = cred
    gate["input_sample_snapshot"] = {k: v for k, v in inp.items() if k != "blockers"}
    gate["fallback_snapshot"] = fb
    if rb.get("found") and rb.get("runbook") is not None:
        gate["controlled_provider_runbook"] = rb.get("runbook")
    return gate
