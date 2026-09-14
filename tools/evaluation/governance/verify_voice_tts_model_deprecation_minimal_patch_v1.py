#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Phase-Voice-TTS-Model-Deprecation-Minimal-Patch-v1-001 (static only, no TTS calls)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.model_profile_registry_planning_v1 import _tts_governance_overlay
from capabilities.governance.voice_tts_model_deprecation_minimal_patch_v1 import (
    FINAL_DECISION_GO,
    NON_CLAIMS,
    PATCH_SCOPE_FILES,
    PHASE_ID,
    TTS_CANDIDATE_GOVERNANCE,
)
from capabilities.voice.tts_model_constants_v0 import (
    DEFAULT_TTS_MODEL,
    LEGACY_QWEN_TTS_MODEL,
    LEGACY_QWEN_TTS_RETIREMENT_DATE,
    TRANSITIONAL_QWEN_TTS_FLASH_MODEL,
    resolve_tts_model,
    runtime_fallback_model,
)

MIN_CHECKS = 53

results: List[Dict[str, Any]] = []
passed = 0


def ok(name: str, cond: bool, **detail: Any) -> None:
    global passed
    if cond:
        passed += 1
    results.append({"check": name, "pass": bool(cond), **detail})


def _read(rel: str) -> str:
    return (_REPO_ROOT / rel).read_text(encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--patch-root", default="", help="output_root from run patch tool")
    ap.add_argument("--output", default="", help="verification JSON path")
    args = ap.parse_args()

    ok("phase.id", PHASE_ID.endswith("-001"))
    ok("constants.default", DEFAULT_TTS_MODEL == "cosyvoice-v3-flash")
    ok("constants.legacy", LEGACY_QWEN_TTS_MODEL == "qwen-tts")
    ok("constants.transitional", TRANSITIONAL_QWEN_TTS_FLASH_MODEL == "qwen-tts-flash")
    ok("constants.retirement", LEGACY_QWEN_TTS_RETIREMENT_DATE == "2026-09-07")

    default_resolved = resolve_tts_model()
    ok("resolve.default.model", default_resolved.model == DEFAULT_TTS_MODEL)
    ok("resolve.default.source", default_resolved.source == "default")
    ok("resolve.default.no_warn", len(default_resolved.warnings) == 0)

    legacy_resolved = resolve_tts_model(explicit=LEGACY_QWEN_TTS_MODEL)
    ok("resolve.legacy.deprecated", legacy_resolved.deprecated is True)
    ok("resolve.legacy.warn", any("deprecated_notice" in w for w in legacy_resolved.warnings))

    flash_resolved = resolve_tts_model(explicit=TRANSITIONAL_QWEN_TTS_FLASH_MODEL)
    ok("resolve.flash.transitional", flash_resolved.transitional is True)
    ok("resolve.flash.warn", any("transitional_notice" in w for w in flash_resolved.warnings))

    ok("fallback.default", runtime_fallback_model(DEFAULT_TTS_MODEL) == TRANSITIONAL_QWEN_TTS_FLASH_MODEL)
    ok("fallback.legacy", runtime_fallback_model(LEGACY_QWEN_TTS_MODEL) == TRANSITIONAL_QWEN_TTS_FLASH_MODEL)
    ok("fallback.flash_none", runtime_fallback_model(TRANSITIONAL_QWEN_TTS_FLASH_MODEL) is None)

    qwen_tts_src = _read("modules/qwen_tts.py")
    ok("module.imports_constants", "tts_model_constants_v0" in qwen_tts_src)
    ok("module.uses_resolve", "resolve_tts_model" in qwen_tts_src)
    ok("module.no_hard_default", 'self.model = "qwen-tts"' not in qwen_tts_src)

    provider_src = _read("capabilities/voice/providers/qwen_tts_provider.py")
    ok("provider.default_constant", "DEFAULT_TTS_MODEL" in provider_src)
    ok("provider.no_hard_default", 'model: str = "qwen-tts"' not in provider_src)
    ok("provider.uses_resolve", "resolve_tts_model" in provider_src)

    entry_src = _read("capabilities/voice/runtime/tts_unified_entry.py")
    ok("entry.helper", "_resolve_qwen_tts_model" in entry_src)
    ok("entry.no_hard_default", '"qwen-tts"' not in entry_src or 'or "qwen-tts"' not in entry_src)

    registry_src = _read("capabilities/governance/model_profile_registry_planning_v1.py")
    ok("registry.cosyvoice_seed", "cosyvoice_v3_flash_candidate" in registry_src)
    ok("registry.flash_seed", "qwen_tts_flash_candidate" in registry_src)
    ok("registry.overlay_fn", "_tts_governance_overlay" in registry_src)

    for cid, expected in TTS_CANDIDATE_GOVERNANCE.items():
        sample = _tts_governance_overlay({"model_profile_id": cid})
        for field, value in expected.items():
            ok(f"registry.{cid[:12]}.{field}", sample.get(field) == value)

    ok("non_claims.count", len(NON_CLAIMS) >= 4)
    for i, claim in enumerate(NON_CLAIMS):
        lowered = claim.lower()
        ok(
            f"non_claims.{i}",
            "≠" in claim or " not " in f" {lowered} " or lowered.startswith("no "),
        )

    for rel in PATCH_SCOPE_FILES:
        ok(f"scope.file.{Path(rel).name[:20]}", (_REPO_ROOT / rel).is_file())

    patch_root = Path(args.patch_root) if args.patch_root else (_REPO_ROOT / "_tmp_eval_out/voice_tts_model_deprecation_minimal_patch")
    summary_path = patch_root / "summary.json"
    ok("patch.summary.exists", summary_path.is_file())
    if summary_path.is_file():
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        ok("patch.summary.decision", summary.get("final_decision") == FINAL_DECISION_GO)
        ok("patch.summary.default", summary.get("default_tts_model") == DEFAULT_TTS_MODEL)

    all_pass = passed == len(results) and passed >= MIN_CHECKS
    out = {
        "phase": PHASE_ID,
        "min_checks": MIN_CHECKS,
        "checks_run": len(results),
        "checks_passed": passed,
        "all_pass": all_pass,
        "no_real_tts_calls": True,
        "results": results,
    }
    out_path = Path(args.output) if args.output else (patch_root / "verify_voice_tts_model_deprecation_minimal_patch_v1.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(out_path))
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
