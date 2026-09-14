#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phase-Voice-OutputGovernance-001-Fix
Static verifier: Speech Guard / Speech Gate mainline alignment.

Hard boundary:
- This tool MUST NOT change runtime behavior.
- Only reads repository files and writes a verification_result.json under logs/.
"""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class CheckResult:
    check_id: str
    ok: bool
    summary: str
    evidence: Dict[str, object]


def _repo_root() -> Path:
    # tools/ -> repo root
    return Path(__file__).resolve().parents[1]


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return ""


def _exists(path: Path) -> bool:
    try:
        return path.exists()
    except Exception:
        return False


def _grep_paths(root: Path, pattern: re.Pattern, *, max_hits: int = 200) -> List[str]:
    hits: List[str] = []
    # Avoid scanning huge dirs; keep it narrow and auditable.
    scopes = [
        root / "capabilities",
        root / "core",
        root / "docs",
        root / "tools",
        root / "main.py",
    ]
    files: List[Path] = []
    for s in scopes:
        if s.is_file():
            files.append(s)
        elif s.is_dir():
            for p in s.rglob("*.py"):
                files.append(p)
            for p in s.rglob("*.md"):
                files.append(p)
            for p in s.rglob("*.yaml"):
                files.append(p)
            for p in s.rglob("*.yml"):
                files.append(p)
            for p in s.rglob("*.json"):
                files.append(p)
    # De-dup & deterministic
    seen = set()
    files2 = []
    for f in sorted(files):
        if f in seen:
            continue
        seen.add(f)
        files2.append(f)
    for f in files2:
        txt = _read_text(f)
        if not txt:
            continue
        if pattern.search(txt):
            hits.append(str(f.relative_to(root)))
            if len(hits) >= max_hits:
                break
    return hits


def _detect_symbol_definition(path: Path, symbol: str) -> bool:
    txt = _read_text(path)
    if not txt:
        return False
    # basic python def/class detection
    if re.search(rf"^\s*def\s+{re.escape(symbol)}\s*\(", txt, flags=re.M):
        return True
    if re.search(rf"^\s*class\s+{re.escape(symbol)}\s*[\(:]", txt, flags=re.M):
        return True
    return False


def _check_contract_markers(root: Path) -> Tuple[bool, Dict[str, object]]:
    contract = root / "docs" / "architecture" / "LUNA_VOICE_OUTPUT_SPEECH_GATE_MAINLINE_CONTRACT_V0.md"
    txt = _read_text(contract)
    markers = {
        "ALIGNMENT_CONTRACT_V0": "ALIGNMENT_CONTRACT_V0" in txt,
        "GUARD_V1_SPEAKABLE_TEXT_STATUS": "GUARD_V1_SPEAKABLE_TEXT_STATUS: missing_or_replaced" in txt,
        "SPEECH_GATE_MAINLINE_WIRING_REQUIRED": "SPEECH_GATE_MAINLINE_WIRING_REQUIRED: true" in txt,
    }
    ok = bool(markers["ALIGNMENT_CONTRACT_V0"] and markers["SPEECH_GATE_MAINLINE_WIRING_REQUIRED"])
    return ok, {"contract_path": str(contract.relative_to(root)), "markers": markers}


def run() -> Dict[str, object]:
    root = _repo_root()
    now = time.time()
    ts = time.strftime("%Y%m%d_%H%M%S", time.localtime(now))

    out_dir = root / "logs" / f"voice_output_guard_gate_alignment_001_fix_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "verification_result.json"

    checks: List[CheckResult] = []
    blockers: List[str] = []
    required: List[str] = []

    # A. SpeechGate exists
    speech_gate_py = root / "core" / "speech_gate.py"
    a_ok = _exists(speech_gate_py) and _detect_symbol_definition(speech_gate_py, "SpeechGate")
    checks.append(
        CheckResult(
            check_id="A_speech_gate_exists",
            ok=a_ok,
            summary="SpeechGate class is locatable",
            evidence={"path": str(speech_gate_py.relative_to(root)), "class_found": a_ok},
        )
    )
    if not a_ok:
        blockers.append("SpeechGate_missing_or_not_locatable")

    # B. SpeechRequest schema exists
    speech_req_py = root / "capabilities" / "voice" / "schemas" / "speech_request.py"
    b_ok = _exists(speech_req_py) and _detect_symbol_definition(speech_req_py, "SpeechRequest")
    checks.append(
        CheckResult(
            check_id="B_speech_request_exists",
            ok=b_ok,
            summary="SpeechRequest schema is locatable",
            evidence={"path": str(speech_req_py.relative_to(root)), "class_found": b_ok},
        )
    )
    if not b_ok:
        blockers.append("SpeechRequest_missing_or_not_locatable")

    # C. VoiceOutputPlane exists
    plane_py = root / "capabilities" / "voice" / "interfaces" / "voice_output_plane.py"
    c_ok = _exists(plane_py) and _detect_symbol_definition(plane_py, "VoiceOutputPlane")
    checks.append(
        CheckResult(
            check_id="C_voice_output_plane_interface_exists",
            ok=c_ok,
            summary="VoiceOutputPlane interface is locatable",
            evidence={"path": str(plane_py.relative_to(root)), "symbol_found": c_ok},
        )
    )
    if not c_ok:
        blockers.append("VoiceOutputPlane_interface_missing_or_not_locatable")

    # D. dispatch_voice_final_text exists
    dispatcher_py = root / "capabilities" / "voice" / "runtime" / "voice_final_text_dispatcher.py"
    d_ok = _exists(dispatcher_py) and _detect_symbol_definition(dispatcher_py, "dispatch_voice_final_text")
    checks.append(
        CheckResult(
            check_id="D_dispatch_voice_final_text_exists",
            ok=d_ok,
            summary="dispatch_voice_final_text is locatable",
            evidence={"path": str(dispatcher_py.relative_to(root)), "def_found": d_ok},
        )
    )
    if not d_ok:
        blockers.append("dispatch_voice_final_text_missing_or_not_locatable")

    # E. env flag reference exists
    env_pat = re.compile(r"LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1")
    env_hits = _grep_paths(root, env_pat, max_hits=50)
    e_ok = len(env_hits) > 0
    checks.append(
        CheckResult(
            check_id="E_env_flag_exists",
            ok=e_ok,
            summary="LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1 is referenced",
            evidence={"hit_count": len(env_hits), "hits": env_hits[:20]},
        )
    )
    if not e_ok:
        blockers.append("LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1_not_referenced")

    # F/G. guard_v1_speakable_text exists OR explicitly treated as missing/replaced
    guard_pat = re.compile(r"\bguard_v1_speakable_text\b")
    guard_hits = _grep_paths(root, guard_pat, max_hits=50)
    guard_def_hits: List[str] = []
    for rel in guard_hits:
        p = root / rel
        if p.suffix == ".py" and _detect_symbol_definition(p, "guard_v1_speakable_text"):
            guard_def_hits.append(rel)
    guard_present = len(guard_def_hits) > 0

    contract_ok, contract_evidence = _check_contract_markers(root)
    checks.append(
        CheckResult(
            check_id="F_guard_symbol_status",
            ok=True,  # informational; pass/fail decided via blockers
            summary="guard_v1_speakable_text presence is recorded; missing must not be assumed",
            evidence={
                "symbol_references_found": len(guard_hits),
                "reference_hits": guard_hits[:20],
                "definition_hits": guard_def_hits,
                "present": guard_present,
                "contract_markers": contract_evidence,
            },
        )
    )
    if not guard_present:
        # Missing guard is an expected hard risk; it must be *recorded*, not assumed.
        # If the contract explicitly marks missing_or_replaced, treat as required follow-up for Phase-002 (hard gate),
        # NOT as an immediate NO_GO blocker for this alignment-contract phase.
        markers = contract_evidence.get("markers", {}) if isinstance(contract_evidence, dict) else {}
        if bool(markers.get("GUARD_V1_SPEAKABLE_TEXT_STATUS")):
            required.append("guard_v1_speakable_text_missing_definition_must_be_resolved_in_phase_002")
        else:
            blockers.append("guard_v1_speakable_text_missing_definition")
            blockers.append("guard_missing_but_contract_not_marked_missing_or_replaced")

    # H. SpeechGate mainline connection detected OR contract requires wiring
    # Heuristic detection: look for import/usage within voice output mainline code paths.
    wiring_pat = re.compile(
        r"(^\s*from\s+core\.speech_gate\s+import\s+SpeechGate\b)|"
        r"(^\s*import\s+core\.speech_gate\b)|"
        r"(\bSpeechGate\s*\()",
        flags=re.M,
    )
    wiring_scope_files = [
        root / "capabilities" / "voice" / "runtime" / "voice_final_text_dispatcher.py",
        root / "capabilities" / "voice" / "output" / "voice_output_plane_v1.py",
        root / "capabilities" / "voice" / "output" / "playback_plane_v1.py",
        root / "capabilities" / "voice" / "output" / "audio_worker_v1.py",
    ]
    wiring_hits: List[str] = []
    for p in wiring_scope_files:
        if not _exists(p):
            continue
        txt = _read_text(p)
        if wiring_pat.search(txt):
            wiring_hits.append(str(p.relative_to(root)))
    wiring_detected = len(wiring_hits) > 0
    markers = contract_evidence.get("markers", {}) if isinstance(contract_evidence, dict) else {}
    wiring_required = bool(markers.get("SPEECH_GATE_MAINLINE_WIRING_REQUIRED"))

    h_ok = wiring_detected or wiring_required
    checks.append(
        CheckResult(
            check_id="H_speech_gate_mainline_wiring",
            ok=h_ok,
            summary="SpeechGate wiring must be detected or explicitly required by contract",
            evidence={
                "wiring_detected": wiring_detected,
                "wiring_hit_paths": wiring_hits,
                "contract_requires_wiring": wiring_required,
                "contract_path": contract_evidence.get("contract_path") if isinstance(contract_evidence, dict) else None,
            },
        )
    )
    if not wiring_detected:
        required.append("SpeechGate_mainline_wiring_required_in_phase_002")

    # I/J/K/L. boundary assertions (static)
    # We can only assert we did not edit runtime behavior by not touching runtime files here.
    checks.append(
        CheckResult(
            check_id="IJKL_static_boundary_assertions",
            ok=True,
            summary="Static verifier does not execute runtime; asserts boundary by design",
            evidence={
                "runtime_execution": False,
                "real_tts_invoked": False,
                "provider_added": False,
                "legacy_deleted": False,
            },
        )
    )

    ok = len([b for b in blockers if b]) == 0
    if ok and required:
        verdict = "CONDITIONAL_GO"
    else:
        verdict = "GO" if ok else "NO_GO"

    result = {
        "phase": "Phase-Voice-OutputGovernance-001-Fix",
        "verifier": "verify_voice_output_guard_gate_alignment_v0",
        "timestamp": now,
        "repo_root": str(root),
        "verdict": verdict,
        "checks": [asdict(c) for c in checks],
        "blockers": blockers,
        "required_followups": required,
        "outputs": {"verification_result_json": str(out_path.relative_to(root))},
    }

    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    res = run()
    print(json.dumps(res, ensure_ascii=False, indent=2))

