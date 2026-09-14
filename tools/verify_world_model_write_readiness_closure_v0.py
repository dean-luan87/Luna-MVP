#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import os
import re
import time
from typing import Any, Dict, List, Tuple

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in __import__("sys").path:
    __import__("sys").path.insert(0, REPO_ROOT)


def _resolve(p: str) -> str:
    return p if os.path.isabs(p) else os.path.abspath(os.path.join(REPO_ROOT, p))


def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _case(name: str, ok: bool, details: Any = None) -> Dict[str, Any]:
    return {"case": name, "ok": bool(ok), "details": details}


def _contains_any(text: str, needles: List[str]) -> Tuple[bool, List[str]]:
    missing = [n for n in needles if n not in text]
    return (len(missing) == 0, missing)


def _contains_regex(text: str, pattern: str) -> bool:
    try:
        return re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) is not None
    except Exception:
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    out_root = _resolve(args.output_root)
    os.makedirs(out_root, exist_ok=True)

    docs_required = [
        "docs/architecture/LUNA_WORLD_MODEL_WRITE_READINESS_DEFINITION_V0.md",
        "docs/architecture/LUNA_WORLD_MODEL_WRITE_LEVEL_AND_STATE_POLICY_V0.md",
        "docs/architecture/LUNA_WORLD_MODEL_WRITE_READINESS_CHECK_SCHEMA_V0.md",
        "docs/architecture/LUNA_WORLD_MODEL_CONTAMINATION_GUARD_POLICY_V0.md",
        "docs/architecture/LUNA_WORLD_MODEL_ROLLBACK_AND_REVISION_POLICY_V0.md",
        "docs/architecture/LUNA_WORLD_MODEL_WRITE_AUDIT_REQUIREMENTS_V0.md",
        "docs/architecture/LUNA_WORLD_MODEL_COMMIT_LAYER_CONTRACT_V0.md",
        "docs/architecture/LUNA_COMMITTED_WORLD_MEMORY_RECORD_SCHEMA_V0.md",
        "docs/architecture/LUNA_WORLD_MEMORY_REVISION_SEMANTICS_V0.md",
        "docs/architecture/LUNA_WORLD_MEMORY_QUARANTINE_STORE_POLICY_V0.md",
        "docs/architecture/LUNA_WORLD_MEMORY_READ_VISIBILITY_POLICY_V0.md",
        "docs/architecture/LUNA_WORLD_MODEL_COMMIT_AUDIT_ENVELOPE_V0.md",
        "docs/architecture/LUNA_PROVISIONAL_WRITE_AND_SUSPICION_FIRST_COMMIT_POLICY_V0.md",
        "docs/architecture/LUNA_WORLD_MODEL_SPATIOTEMPORAL_BINDING_CONSTITUTION_V0.md",
    ]

    results: List[Dict[str, Any]] = []
    missing_docs = [p for p in docs_required if not os.path.isfile(_resolve(p))]
    results.append(_case("A_required_docs_exist", len(missing_docs) == 0, {"missing": missing_docs}))
    if missing_docs:
        report = {
            "verifier": "verify_world_model_write_readiness_closure_v0",
            "verdict": "NO_GO",
            "generated_at_ms": int(time.time() * 1000),
            "hard_blockers": [f"missing_docs:{len(missing_docs)}"],
            "results": results,
        }
        _write_json(os.path.join(out_root, "verification_result.json"), report)
        return 2

    # Merge all docs into a searchable corpus (static)
    corpus = ""
    per_doc: Dict[str, str] = {}
    for p in docs_required:
        txt = _read_text(_resolve(p))
        per_doc[p] = txt
        corpus += "\n\n" + txt

    keyword_checks = [
        "WriteReadinessCheck",
        "WorldEvidenceWriteState",
        "WorldModelWriteLevel",
        "Contamination",
        "Rollback",
        "Revision",
        "Quarantine",
        "CommitAuditEnvelope",
        "CommittedWorldMemoryRecord",
        "spatiotemporal_binding",
        "spatiotemporal_anchor_ref",
        "spatiotemporal_binding_check",
        "provisional_world_memory",
        "suspicion_status",
        "read_visibility",
        "source_reference_chain",
        "requires_revalidation",
    ]
    ok_kw, missing_kw = _contains_any(corpus, keyword_checks)
    results.append(_case("B_keywords_present", ok_kw, {"missing_keywords": missing_kw}))

    # Boundary phrases: allowlist patterns (we require clear statements, not exact wording)
    boundary_patterns = [
        r"不实现\s*runtime",
        r"不真实写入",
        r"不上传蜂巢",
        r"不接推荐",
        r"不执行导航",
        r"不真实播报",
        r"不进入\s*SceneTask/Fusion/Output",
    ]
    boundary_ok = all(_contains_regex(corpus, pat) for pat in boundary_patterns)
    results.append(_case("C_boundaries_stated", boundary_ok, {"patterns": boundary_patterns}))

    # Provisional-first principle must be present in commit layer contract or policy
    commit_contract = per_doc["docs/architecture/LUNA_WORLD_MODEL_COMMIT_LAYER_CONTRACT_V0.md"]
    prov_policy = per_doc["docs/architecture/LUNA_PROVISIONAL_WRITE_AND_SUSPICION_FIRST_COMMIT_POLICY_V0.md"]
    prov_ok = ("占位" in commit_contract or "provisional" in commit_contract) and ("provisional_world_memory" in (commit_contract + prov_policy))
    results.append(_case("D_provisional_first_principle_present", prov_ok, {"files": ["commit_layer_contract", "provisional_policy"]}))

    # NO_GO coverage: must explicitly forbid direct committed facts and quarantine readability
    nogo_ok = (
        ("NO_GO" in prov_policy)
        and ("quarantined" in corpus or "隔离" in corpus)
        and ("未通过" in corpus and "WriteReadinessCheck" in corpus)
    )
    results.append(_case("E_no_go_coverage_present", nogo_ok, {"notes": "static presence check"}))

    # Spatiotemporal binding hard rule must be stated in committed memory schema
    committed_schema = per_doc["docs/architecture/LUNA_COMMITTED_WORLD_MEMORY_RECORD_SCHEMA_V0.md"]
    stb_ok = ("spatiotemporal_binding" in committed_schema) and ("不允许缺" in committed_schema or "不允许缺" in corpus or "must" in committed_schema)
    results.append(_case("F_spatiotemporal_binding_required_for_committed", stb_ok, {"file": "LUNA_COMMITTED_WORLD_MEMORY_RECORD_SCHEMA_V0.md"}))

    verdict = "GO" if all(r["ok"] for r in results) else "NO_GO"
    report = {
        "verifier": "verify_world_model_write_readiness_closure_v0",
        "verdict": verdict,
        "generated_at_ms": int(time.time() * 1000),
        "results": results,
    }
    _write_json(os.path.join(out_root, "verification_result.json"), report)
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

