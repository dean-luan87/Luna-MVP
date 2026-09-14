#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Voice-Qianwen-001 — Static verifier for Governed Qwen/TTS Unified Entry Contract v0.

Static read-only checks: no network, no provider SDK imports, no audio playback.
Writes logs/voice_qwen_governed_entry_contract_001_<timestamp>/verification_result.json by default.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # type: ignore


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _utc_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _read_text_if_exists(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def _require(cond: bool, msg: str, errors: List[str]) -> None:
    if not cond:
        errors.append(msg)


def _require_sub(txt: str, sub: str, msg: str, errors: List[str]) -> None:
    _require(sub in txt, msg, errors)


def _verify_self_static(source: str, errors: List[str]) -> None:
    """I/J: verifier must stay dry-run (no imports of voice runtime / SDK clients)."""
    for line in source.splitlines():
        s = line.strip()
        if s.startswith("from capabilities") or s.startswith("import capabilities"):
            errors.append("IJ: verifier must not import capabilities.* runtime modules")
            return
        if re.match(r"^import\s+dashscope\b", s) or re.match(r"^from\s+dashscope\b", s):
            errors.append("IJ: verifier must not import dashscope")
            return


def run_verify(*, repo: Path, output_root: Path) -> Dict[str, Any]:
    errors: List[str] = []
    checks: List[Dict[str, Any]] = []

    arch = repo / "docs/architecture"
    p_role = arch / "LUNA_VOICE_QWEN_TTS_PROVIDER_ROLE_AND_BOUNDARY_V0.md"
    p_contract = arch / "LUNA_VOICE_GOVERNED_PROVIDER_ENTRY_CONTRACT_V0.md"
    p_schema = arch / "LUNA_VOICE_SOURCE_TEXT_SPOKEN_TEXT_DIFF_AUDIT_SCHEMA_V0.md"
    p_policy = arch / "LUNA_VOICE_QWEN_FIRST_TTS_FALLBACK_POLICY_V0.md"
    p_go = arch / "LUNA_VOICE_QWEN_PROVIDER_CONTROL_GO_NO_GO_PACK_V0.md"
    qwen_py = repo / "capabilities/voice/providers/qwen_tts_provider.py"
    vt_cfg = repo / "capabilities/voice/config/voice_tts_config.yaml"

    # A-D
    a_ok = p_role.is_file() and p_role.stat().st_size > 0
    checks.append({"id": "A", "name": "qwen_provider_role_doc", "ok": a_ok})
    _require(a_ok, "A: missing LUNA_VOICE_QWEN_TTS_PROVIDER_ROLE_AND_BOUNDARY_V0.md", errors)

    b_ok = p_contract.is_file()
    checks.append({"id": "B", "name": "governed_entry_contract_doc", "ok": b_ok})
    _require(b_ok, "B: missing LUNA_VOICE_GOVERNED_PROVIDER_ENTRY_CONTRACT_V0.md", errors)

    c_ok = p_schema.is_file()
    checks.append({"id": "C", "name": "diff_audit_schema_doc", "ok": c_ok})
    _require(c_ok, "C: missing LUNA_VOICE_SOURCE_TEXT_SPOKEN_TEXT_DIFF_AUDIT_SCHEMA_V0.md", errors)

    d_ok = p_policy.is_file()
    checks.append({"id": "D", "name": "qwen_first_fallback_policy_doc", "ok": d_ok})
    _require(d_ok, "D: missing LUNA_VOICE_QWEN_FIRST_TTS_FALLBACK_POLICY_V0.md", errors)

    role_txt = _read_text_if_exists(p_role)
    contract_txt = _read_text_if_exists(p_contract)
    schema_txt = _read_text_if_exists(p_schema)
    policy_txt = _read_text_if_exists(p_policy)
    _require_sub(policy_txt, "QW001_POLICY_TEMPLATE_ONLINE_PREFER_QWEN", "D: policy anchor missing", errors)
    _require_sub(policy_txt, "QW001_POLICY_DEFAULT_BASELINE_OFFLINE_ONLY_PIPER", "D: default baseline anchor missing", errors)
    go_txt = _read_text_if_exists(p_go)
    qwen_src = _read_text_if_exists(qwen_py)

    # E: role doc + adapter header
    e1 = "QW001_ROLE_TEXT_TO_AUDIO_NOT_EXPRESSION" in role_txt
    e2 = "QW001_ROLE_EXPRESSION_SEPARATE_CHAIN" in role_txt
    e3 = bool(
        re.search(r"text\s*[-→>]\s*audio", qwen_src, re.I)
        or re.search(r"only\s+text\s*->\s*audio", qwen_src, re.I)
        or ("Never generates text" in qwen_src)
        or ("Only text" in qwen_src and "audio" in qwen_src.lower())
    )
    e_ok = e1 and e2 and e3
    checks.append({"id": "E", "name": "qwen_tts_text_to_audio_not_expression", "ok": e_ok})
    _require(e1, "E: role anchor QW001_ROLE_TEXT_TO_AUDIO_NOT_EXPRESSION missing", errors)
    _require(e2, "E: role anchor QW001_ROLE_EXPRESSION_SEPARATE_CHAIN missing", errors)
    _require(e3, "E: QwenTTSProvider source missing text->audio boundary markers", errors)

    # F schema fields（JSON 中使用 "field"，`field` prose 亦可）
    def _field_markers(txt: str, name: str) -> bool:
        return f'"{name}"' in txt or f"`{name}`" in txt

    f_ok = (
        "QW001_SCHEMA_VOICE_DIFF_AUDIT_V0" in schema_txt
        and ("QW001_SCHEMA_QWEN_TTS_INVARIANT_PROVIDER_INPUT_EQUALS_SOURCE" in schema_txt)
        and _field_markers(schema_txt, "source_text")
        and _field_markers(schema_txt, "spoken_text")
        and _field_markers(schema_txt, "provider_input_text")
        and _field_markers(schema_txt, "provider_output_audio_ref")
        and _field_markers(schema_txt, "text_diff_audit")
    )
    checks.append({"id": "F", "name": "source_spoken_provider_diff_schema_defined", "ok": f_ok})
    _require(f_ok, "F: schema anchors/fields incomplete in DIFF_AUDIT doc", errors)

    # G
    g_ok = (
        "QW001_CONTRACT_BEFORE_RUN_TTS_UNIFIED_ENTRY" in contract_txt
        and "QW001_CONTRACT_GOVERNED_VOICE_PROVIDER_ENTRY" in contract_txt
    )
    checks.append({"id": "G", "name": "governance_before_provider_rule_defined", "ok": g_ok})
    _require(g_ok, "G: contract anchors for governed entry / before unified entry missing", errors)

    # H default YAML policy baseline (explicit invariants expected by Phase-001)
    h_ok = False
    h_detail: Dict[str, Any] = {}
    if yaml is None:
        errors.append("H: PyYAML unavailable; cannot assert voice_tts_config baseline")
        checks.append({"id": "H", "name": "default_provider_policy_not_modified", "ok": False})
    else:
        cfg = yaml.safe_load(_read_text_if_exists(vt_cfg)) or {}
        h_detail = {
            "tts_runtime_mode": cfg.get("tts_runtime_mode"),
            "active_provider": cfg.get("active_provider"),
            "provider_order_top": cfg.get("provider_order"),
            "offline_only_top": cfg.get("offline_only"),
            "local_runtime_qwen_enabled": ((cfg.get("local_runtime") or {}).get("qwen") or {}).get("enabled"),
        }
        h_ok = (
            str(cfg.get("tts_runtime_mode") or "") == "offline_only"
            and str(cfg.get("active_provider") or "") == "piper"
            and isinstance(cfg.get("provider_order"), list)
            and [str(x) for x in cfg.get("provider_order") or []] == ["piper"]
            and cfg.get("offline_only") is True
            and ((cfg.get("local_runtime") or {}).get("qwen") or {}).get("enabled") is False
        )
        checks.append({"id": "H", "name": "default_provider_policy_not_modified", "ok": h_ok, "detail": h_detail})
        _require(h_ok, f"H: voice_tts_config baseline drifted or unexpected: {h_detail!r}", errors)

    # go pack exists + scope anchor
    go_ok = p_go.is_file() and "QW001_GO_PACK_PHASE_001_SCOPE" in go_txt
    checks.append({"id": "GO_PACK", "name": "go_no_go_pack_present", "ok": go_ok})
    _require(go_ok, "GO_PACK: missing pack file or QW001_GO_PACK_PHASE_001_SCOPE", errors)

    self_path = Path(__file__).resolve()
    self_src = self_path.read_text(encoding="utf-8")
    dry_errs: List[str] = []
    _verify_self_static(self_src, dry_errs)
    ij_ok = len(dry_errs) == 0
    checks.append({"id": "I", "name": "verifier_no_real_qwen_invocation", "ok": ij_ok, "detail": dry_errs or None})
    checks.append({"id": "J", "name": "verifier_no_real_tts_invocation", "ok": ij_ok, "detail": dry_errs or None})
    errors.extend(dry_errs)

    ok = len(errors) == 0
    out: Dict[str, Any] = {
        "phase": "Phase-Voice-Qianwen-001",
        "verifier": "verify_voice_qwen_governed_entry_contract_v0",
        "repo_root": str(repo),
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "ok": ok,
        "errors": errors,
        "checks": sorted(checks, key=lambda x: x.get("id", "")),
    }
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "verification_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(_repo_root()))
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()
    repo = Path(args.repo_root).resolve()
    tag = _utc_tag()
    out = Path(args.output_root) if args.output_root else repo / "logs" / f"voice_qwen_governed_entry_contract_001_{tag}"
    res = run_verify(repo=repo, output_root=out)
    print(json.dumps({"ok": res["ok"], "output_root": str(out)}, ensure_ascii=False))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
