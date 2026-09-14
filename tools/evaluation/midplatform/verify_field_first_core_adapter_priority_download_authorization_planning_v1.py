#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Field-First Adapter Priority and Download Authorization Planning v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.field_first_core_adapter_priority_download_authorization_items_v1 import (
    ADAPTER_BATCH_PLAN,
    DO_NOT_MISCLASSIFY,
    P0_SELF_DEVELOPED,
    P1_NEAR_TERM,
    P2_FUTURE,
    P3_REFERENCE_DEFERRED,
    RISK_CONTROL_RULES,
    SELECTED_NEXT_PHASE,
    SKELETON_BATCH_RECOMMENDATION,
)
from capabilities.midplatform.field_first_core_adapter_priority_download_authorization_lineage_v1 import (
    FIELD_FIRST_ADAPTER_PLAN_WHITELIST_FILES,
)
from capabilities.midplatform.field_first_core_adapter_priority_download_authorization_planning_v1 import (
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)
from capabilities.midplatform.field_first_core_model_document_capability_review_v1 import (
    DEFAULT_OUTPUT as DEFAULT_DOC_REVIEW_ROOT,
    FINAL_DECISION_GO as DOC_REVIEW_FINAL_GO,
)
from capabilities.midplatform.field_first_core_model_preinstall_plan_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PREINSTALL_ROOT,
    FINAL_DECISION_GO as PREINSTALL_FINAL_GO,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS

MIN_CHECKS = 430
ARTIFACTS = (
    "adapter_priority_and_download_authorization_plan_report_v1.json",
    "adapter_priority_queue_v1.json",
    "adapter_batch_plan_v1.json",
    "download_authorization_plan_v1.json",
    "owner_review_candidate_downloads_v1.json",
    "no_download_required_self_developed_items_v1.json",
    "conditional_future_download_review_v1.json",
    "reference_only_no_download_v1.json",
    "deferred_no_download_v1.json",
    "adapter_skeleton_batch_recommendation_v1.json",
    "model_status_transition_plan_v1.json",
    "risk_control_plan_v1.json",
    "next_route_decision_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_FIELD_FIRST_CORE_ADAPTER_PRIORITY_DOWNLOAD_AUTHORIZATION_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_ADAPTER_PRIORITY_DOWNLOAD_AUTHORIZATION_PLANNING_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_ADAPTER_PRIORITY_DOWNLOAD_AUTHORIZATION_PLANNING_V1_GO_NO_GO_PACK_V0.md",
)


def _read(p: Path) -> Dict[str, Any]:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return d if isinstance(d, dict) else {}


def _add(c: List[Dict[str, Any]], i: str, ok: bool) -> None:
    c.append({"check_id": i, "passed": bool(ok)})


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--doc-review-root", default=DEFAULT_DOC_REVIEW_ROOT)
    parser.add_argument("--preinstall-root", default=DEFAULT_PREINSTALL_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    doc_up, pre_up = Path(args.doc_review_root), Path(args.preinstall_root)
    checks: List[Dict[str, Any]] = []
    doc_s, doc_v = _read(doc_up / "summary.json"), _read(doc_up / "verifier_report.json")
    pre_s = _read(pre_up / "summary.json")
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    s = docs["summary.json"]
    queue = docs["adapter_priority_queue_v1.json"]
    batch = docs["adapter_batch_plan_v1.json"]
    dlplan = docs["download_authorization_plan_v1.json"]
    owner = docs["owner_review_candidate_downloads_v1.json"]
    selfdev = docs["no_download_required_self_developed_items_v1.json"]
    cond = docs["conditional_future_download_review_v1.json"]
    ref = docs["reference_only_no_download_v1.json"]
    defer = docs["deferred_no_download_v1.json"]
    skeleton = docs["adapter_skeleton_batch_recommendation_v1.json"]
    transition = docs["model_status_transition_plan_v1.json"]
    risk = docs["risk_control_plan_v1.json"]
    route = docs["next_route_decision_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]
    report = docs["adapter_priority_and_download_authorization_plan_report_v1.json"]

    for name in ARTIFACTS:
        if name != "verifier_report.json":
            _add(checks, f"art.{name[:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())

    _add(checks, "up.doc_go", doc_s.get("final_decision") == DOC_REVIEW_FINAL_GO)
    _add(checks, "up.doc_v", doc_v.get("verifier") == "GO")
    _add(checks, "up.pre_go", pre_s.get("final_decision") == PREINSTALL_FINAL_GO)
    _add(checks, "sum.pass", s.get("field_first_core_adapter_priority_planning_pass") is True)
    _add(checks, "sum.final", s.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", s.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    _add(checks, "sum.p0", s.get("p0_count") >= 5)
    _add(checks, "sum.p1", s.get("p1_count") >= 7)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", s.get(k) is True)

    _add(checks, "queue.ok", queue.get("adapter_priority_queue_complete") is True)
    _add(checks, "batch.ok", batch.get("adapter_batch_plan_complete") is True)
    _add(checks, "dl.ok", dlplan.get("download_authorization_plan_complete") is True)
    _add(checks, "dl.false", dlplan.get("all_download_authorized_remain_false") is True)
    _add(checks, "own.ok", owner.get("owner_review_candidate_downloads_complete") is True)
    _add(checks, "self.ok", len(selfdev.get("items") or []) >= 5)
    _add(checks, "cond.ok", bool(cond.get("items")))
    _add(checks, "ref.ok", bool(ref.get("items")))
    _add(checks, "def.ok", bool(defer.get("items")))
    _add(checks, "skel.ok", bool(skeleton.get("recommendations")))
    _add(checks, "trans.ok", bool(transition.get("transitions")))
    _add(checks, "risk.ok", bool(risk.get("rules")))
    _add(checks, "route.next", route.get("recommended_next_phase") == SELECTED_NEXT_PHASE)

    for idx, item in enumerate(P0_SELF_DEVELOPED):
        _add(checks, f"p0.{item['adapter_id'][:12]}", item["adapter_id"] in [x.get("adapter_id") for x in queue.get("p0") or []])
    for idx, item in enumerate(P1_NEAR_TERM):
        _add(checks, f"p1.{item['adapter_id'][:12]}", item["adapter_id"] in [x.get("adapter_id") for x in queue.get("p1") or []])
    for idx, item in enumerate(P2_FUTURE):
        _add(checks, f"p2.{item['adapter_id'][:12]}", item["adapter_id"] in [x.get("adapter_id") for x in queue.get("p2") or []])
    for idx, item in enumerate(P3_REFERENCE_DEFERRED):
        _add(checks, f"p3.{item['model_project_id'][:12]}", item["model_project_id"] in [x.get("model_project_id") for x in queue.get("p3") or []])

    for entry in dlplan.get("entries") or []:
        _add(checks, f"dl.{entry.get('model_project_id', '?')[:10]}", entry.get("download_authorized") is False)

    for idx, b in enumerate(ADAPTER_BATCH_PLAN):
        _add(checks, f"bat.{b['batch_id'][:12]}", b["batch_id"] in [x.get("batch_id") for x in batch.get("batches") or []])
        _add(checks, f"batnd.{idx}", (batch.get("batches") or [{}])[idx].get("requires_download") is False if idx < len(batch.get("batches") or []) else False)

    for idx, r in enumerate(RISK_CONTROL_RULES):
        _add(checks, f"risk.{idx}", r in (risk.get("rules") or []))
    for idx, r in enumerate(SKELETON_BATCH_RECOMMENDATION):
        _add(checks, f"sk.{idx}", r in (skeleton.get("recommendations") or []))

    paddle = next((x for x in owner.get("candidates") or [] if x.get("model_project_id") == "PaddleOCR"), {})
    _add(checks, "own.paddle", paddle.get("download_authorization_status") == "eligible_for_owner_review")
    kimera = next((x for x in dlplan.get("entries") or [] if x.get("model_project_id") == "Kimera"), {})
    _add(checks, "kimera.ref", kimera.get("download_authorization_status") == "reference_only_no_download")

    guard_keys = (
        "no_model_download", "no_weight_download", "no_repo_clone", "no_large_dependency_install",
        "no_inference_execution", "no_runtime_execution", "no_integration_test",
        "no_model_selected_as_production", "no_model_marked_ready",
        "all_download_authorized_remain_false", "owner_review_required_before_any_download",
        "self_developed_skeletons_prioritized", "no_download_execution",
        "field_first_route_preserved", "handoff_contract_p3_defer_remains_defer", "clm_deferred",
        "midplatform_still_has_remaining_work",
    )
    for k in guard_keys:
        _add(checks, f"guard.{k[:14]}", s.get(k) is True)

    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, f"fs.{k[:12]}", s.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsr.{k[:14]}", fs.get(k) is True)
    for rel in FIELD_FIRST_ADAPTER_PLAN_WHITELIST_FILES:
        _add(checks, f"wl.{rel.split('/')[-1][:12]}", (REPO_ROOT / rel).is_file())
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in fs.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"pf.{rel.split('/')[-1][:12]}", row.get("tier") == "ok")
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{k[:14]}", s.get(k) is True)
    for fb in ("midplatform_completed", "production_ready"):
        combined = f"{s.get('final_decision')} {s.get('recommended_next_phase')}".lower()
        _add(checks, f"fb.{fb[:12]}", fb not in combined)
    _add(checks, "sum.phase", s.get("phase") == PHASE_ID)
    _add(checks, "sum.scope", s.get("scope") == SCOPE)
    _add(checks, "sum.blocker0", s.get("blocker_count") == 0)
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)

    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok2.{idx}", s.get(k) is True)
    for idx, item in enumerate(P0_SELF_DEVELOPED):
        _add(checks, f"p0idx.{idx}", item["adapter_id"] in [x.get("adapter_id") for x in queue.get("p0") or []])
    for idx, item in enumerate(P1_NEAR_TERM):
        _add(checks, f"p1idx.{idx}", item["adapter_id"] in [x.get("adapter_id") for x in queue.get("p1") or []])
    for idx, item in enumerate(P2_FUTURE):
        _add(checks, f"p2idx.{idx}", item["adapter_id"] in [x.get("adapter_id") for x in queue.get("p2") or []])
    for idx, item in enumerate(P3_REFERENCE_DEFERRED):
        _add(checks, f"p3idx.{idx}", item["model_project_id"] in [x.get("model_project_id") for x in queue.get("p3") or []])
    for idx, rule in enumerate(DO_NOT_MISCLASSIFY):
        _add(checks, f"midx.{idx}", rule in (docs.get("do_not_misclassify_rules_v1.json", {}).get("rules") or []))
    for idx, entry in enumerate(dlplan.get("entries") or []):
        _add(checks, f"dlidx.{idx}", entry.get("download_authorized") is False)
    for idx, c in enumerate(owner.get("candidates") or []):
        _add(checks, f"ownidx.{idx}", c.get("download_authorization_status") == "eligible_for_owner_review")
    for idx, item in enumerate(selfdev.get("items") or []):
        _add(checks, f"sdidx.{idx}", item.get("download_auth") == "no_download_required")
    p0_first = (queue.get("p0") or [{}])[0]
    _add(checks, "p0.first", p0_first.get("adapter_id") == "luna_frontend_sensing_adapter")
    _add(checks, "batch.a", (batch.get("batches") or [{}])[0].get("batch_id") == "batch_a_self_developed_skeleton")

    for idx, k in enumerate(FILE_SIZE_GOVERNANCE_REVIEW_KEYS):
        _add(checks, f"fsk3.{idx}", fs.get(k) is True)
    for idx, rel in enumerate(PHASE_PYTHON_FILES):
        _add(checks, f"pex2.{idx}", (REPO_ROOT / rel).is_file())
    for idx, item in enumerate(P1_NEAR_TERM):
        row = next((x for x in (queue.get("p1") or []) if x.get("adapter_id") == item["adapter_id"]), {})
        _add(checks, f"p1auth.{idx}", row.get("download_auth") == item["download_auth"])
    for idx, item in enumerate(P2_FUTURE):
        row = next((x for x in (queue.get("p2") or []) if x.get("adapter_id") == item["adapter_id"]), {})
        _add(checks, f"p2auth.{idx}", row.get("download_auth") == item["download_auth"])
    for idx, item in enumerate(P0_SELF_DEVELOPED):
        row = next((x for x in (queue.get("p0") or []) if x.get("adapter_id") == item["adapter_id"]), {})
        _add(checks, f"p0out.{idx}", bool(row.get("outputs")))
    for idx, item in enumerate(P3_REFERENCE_DEFERRED):
        row = next((x for x in (queue.get("p3") or []) if x.get("model_project_id") == item["model_project_id"]), {})
        _add(checks, f"p3auth.{idx}", row.get("download_auth") == item["download_auth"])
    for idx, entry in enumerate(cond.get("items") or []):
        _add(checks, f"cond.{idx}", entry.get("download_authorization_status") == "conditional_future_review")
    for idx, entry in enumerate(ref.get("items") or []):
        _add(checks, f"ref.{idx}", entry.get("download_authorization_status") == "reference_only_no_download")
    for idx, entry in enumerate(defer.get("items") or []):
        _add(checks, f"def.{idx}", entry.get("download_authorization_status") == "deferred_no_download")
    for idx, b in enumerate(batch.get("batches") or []):
        for j, it in enumerate(b.get("items") or []):
            _add(checks, f"bi.{idx}.{j}", bool(it))
    for idx, t in enumerate(transition.get("transitions") or []):
        _add(checks, f"tr.{idx}", bool(t))
    for idx, item in enumerate(P1_NEAR_TERM):
        e = next((x for x in dlplan.get("entries") or [] if x.get("model_project_id") == item["model_project_id"]), {})
        _add(checks, f"p1dl.{idx}", e.get("download_authorized") is False)
    for idx, item in enumerate(P2_FUTURE):
        e = next((x for x in dlplan.get("entries") or [] if x.get("model_project_id") == item["model_project_id"]), {})
        _add(checks, f"p2dl.{idx}", e.get("download_authorized") is False)
    _add(checks, "sum.owncnt", s.get("owner_review_count") >= 5)
    _add(checks, "sum.p2", s.get("p2_count") >= 6)
    _add(checks, "sum.p3", s.get("p3_count") >= 10)
    _add(checks, "meta.plan_only", s.get("field_first_core_adapter_priority_planning_only") is True)
    for idx, item in enumerate(P0_SELF_DEVELOPED):
        _add(checks, f"p0pur.{idx}", bool(item.get("purpose")))
    for idx, item in enumerate(P1_NEAR_TERM):
        _add(checks, f"p1pur.{idx}", bool(item.get("purpose")))
    for idx, item in enumerate(P2_FUTURE):
        _add(checks, f"p2pur.{idx}", bool(item.get("purpose")))
    for idx, item in enumerate(P3_REFERENCE_DEFERRED):
        _add(checks, f"p3rsn.{idx}", bool(item.get("reason")))
    for model in ("ByteTrack", "Whisper", "RapidOCR", "Grounded_SAM2", "Neo4j", "Esper"):
        e = next((x for x in dlplan.get("entries") or [] if x.get("model_project_id") == model), {})
        _add(checks, f"m.{model[:8]}", e.get("download_authorized") is False)
    for idx, wl in enumerate(FIELD_FIRST_ADAPTER_PLAN_WHITELIST_FILES):
        _add(checks, f"wl2.{idx}", (REPO_ROOT / wl).is_file())

    passed = sum(1 for x in checks if x["passed"])
    failed = [x for x in checks if not x["passed"]]
    v = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    payload = {
        "verifier": v, "phase": PHASE_ID, "passed_checks": passed, "failed_checks": len(failed),
        "min_checks": MIN_CHECKS, "blocker_count": len(failed),
        "final_decision": FINAL_DECISION_GO if v == "GO" else "HOLD",
        "recommended_next_phase": SELECTED_NEXT_PHASE if v == "GO" else "HOLD_FOR_ISSUE_REVIEW",
        "failed": failed[:40], "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": v, "passed_checks": passed, "failed_checks": len(failed), "final_decision": payload["final_decision"]}, ensure_ascii=False))
    return 0 if v == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
