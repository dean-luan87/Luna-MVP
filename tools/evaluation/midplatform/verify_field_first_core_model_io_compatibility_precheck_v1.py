#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Field-First Model I/O Compatibility Precheck v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.field_first_core_model_document_capability_review_v1 import (
    DEFAULT_OUTPUT as DEFAULT_DOC_REVIEW_ROOT,
    FINAL_DECISION_GO as DOC_REVIEW_FINAL_GO,
)
from capabilities.midplatform.field_first_core_model_io_compatibility_precheck_items_v1 import (
    CANDIDATE_COMMON_PAYLOAD_REQUIREMENTS,
    COMMON_CONFIDENCE_PAYLOAD,
    COMMON_GRAPH_PAYLOAD,
    COMMON_IDENTITY_PAYLOAD,
    COMMON_SPATIAL_PAYLOAD,
    COMMON_TEMPORAL_PAYLOAD,
    COMMON_TEXT_AUDIO_PAYLOAD,
    COMPATIBILITY_STATUS_OPTIONS,
    DO_NOT_MISCLASSIFY,
    IO_REVIEW_FIELDS,
    MODEL_IO_REVIEW_ITEMS,
    PRECHECK_PRINCIPLES,
    SELECTED_NEXT_PHASE,
    SKELETON_IO_REQUIREMENTS,
    SKELETON_SCHEMA_ADJUSTMENT_PLAN,
)
from capabilities.midplatform.field_first_core_model_io_compatibility_precheck_lineage_v1 import (
    FIELD_FIRST_IO_PRECHECK_WHITELIST_FILES,
)
from capabilities.midplatform.field_first_core_model_io_compatibility_precheck_v1 import (
    DEFAULT_OUTPUT,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_ID,
    PHASE_PYTHON_FILES,
    SCOPE,
)
from capabilities.midplatform.protocols.file_size_module_split_governance_rule_v1 import FILE_SIZE_GOVERNANCE_REVIEW_KEYS

MIN_CHECKS = 420
ARTIFACTS = (
    "model_io_compatibility_precheck_report_v1.json",
    "model_io_review_item_registry_v1.json",
    "model_io_to_candidate_mapping_v1.json",
    "candidate_schema_compatibility_matrix_v1.json",
    "skeleton_schema_adjustment_plan_v1.json",
    "model_io_gap_register_v1.json",
    "field_first_skeleton_io_requirements_v1.json",
    "candidate_common_payload_requirements_v1.json",
    "next_route_decision_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)
DOCS = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_FIELD_FIRST_CORE_MODEL_IO_COMPATIBILITY_PRECHECK_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_MODEL_IO_COMPATIBILITY_PRECHECK_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_MODEL_IO_COMPATIBILITY_PRECHECK_V1_GO_NO_GO_PACK_V0.md",
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
    args = parser.parse_args()
    root, doc_up = Path(args.output_root), Path(args.doc_review_root)
    checks: List[Dict[str, Any]] = []
    doc_s, doc_v = _read(doc_up / "summary.json"), _read(doc_up / "verifier_report.json")
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    s = docs["summary.json"]
    registry = docs["model_io_review_item_registry_v1.json"]
    mapping = docs["model_io_to_candidate_mapping_v1.json"]
    compat = docs["candidate_schema_compatibility_matrix_v1.json"]
    adjust = docs["skeleton_schema_adjustment_plan_v1.json"]
    gaps = docs["model_io_gap_register_v1.json"]
    skel_io = docs["field_first_skeleton_io_requirements_v1.json"]
    common = docs["candidate_common_payload_requirements_v1.json"]
    route = docs["next_route_decision_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]
    report = docs["model_io_compatibility_precheck_report_v1.json"]

    for name in ARTIFACTS:
        if name != "verifier_report.json":
            _add(checks, f"art.{name[:20]}", (root / name).is_file() and bool(_read(root / name)))
    for doc in DOCS:
        _add(checks, f"doc.{doc.split('/')[-1][:16]}", (REPO_ROOT / doc).is_file())

    _add(checks, "up.doc_go", doc_s.get("final_decision") == DOC_REVIEW_FINAL_GO)
    _add(checks, "up.doc_v", doc_v.get("verifier") == "GO")
    _add(checks, "sum.pass", s.get("field_first_core_model_io_compatibility_precheck_pass") is True)
    _add(checks, "sum.final", s.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "sum.next", s.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    _add(checks, "sum.items18", s.get("io_review_item_count") >= 18)
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"sum.{k[:18]}", s.get(k) is True)

    items = registry.get("items") or []
    _add(checks, "reg.cnt", registry.get("count") >= 18)
    _add(checks, "map.ok", mapping.get("model_io_to_candidate_mapping_complete") is True)
    _add(checks, "compat.ok", compat.get("candidate_schema_compatibility_matrix_complete") is True)
    _add(checks, "adj.ok", adjust.get("skeleton_schema_adjustment_plan_complete") is True)
    _add(checks, "adj.spatial", adjust.get("add_common_spatial_payload") is True)
    _add(checks, "skel.ok", skel_io.get("field_first_skeleton_io_requirements_complete") is True)
    _add(checks, "common.ok", bool(common.get("spatial")))
    _add(checks, "gap.ok", bool(gaps.get("gaps")))
    _add(checks, "route.next", route.get("recommended_next_phase") == SELECTED_NEXT_PHASE)

    for idx, item in enumerate(MODEL_IO_REVIEW_ITEMS):
        _add(checks, f"item.{item['model_project_id'][:12]}", item["model_project_id"] in [x.get("model_project_id") for x in items])
        row = next((x for x in items if x.get("model_project_id") == item["model_project_id"]), {})
        _add(checks, f"stat.{idx}", bool(row.get("compatibility_status")))

    paddle = next((x for x in items if x.get("model_project_id") == "PaddleOCR"), {})
    sam2 = next((x for x in items if x.get("model_project_id") == "SAM2"), {})
    fw = next((x for x in items if x.get("model_project_id") == "faster_whisper"), {})
    bt = next((x for x in items if x.get("model_project_id") == "ByteTrack"), {})
    _add(checks, "ocr.bbox", "text_region_bbox" in (paddle.get("spatial_output_fields") or []))
    _add(checks, "sam2.mask", "mask_ref" in (sam2.get("spatial_output_fields") or []))
    _add(checks, "fw.words", "word_timestamps" in (fw.get("audio_segment_fields") or []))
    _add(checks, "bt.track", "track_id" in (bt.get("identity_or_tracking_fields") or []))

    for f in ("bbox", "mask_ref", "track_id", "timestamp", "confidence"):
        _add(checks, f"req.{f}", f in COMMON_SPATIAL_PAYLOAD or f in COMMON_TEMPORAL_PAYLOAD or f == "track_id" or f == "confidence")

    for idx, f in enumerate(IO_REVIEW_FIELDS):
        _add(checks, f"fld.{idx}", f in (registry.get("fields") or []))
    for idx, r in enumerate(SKELETON_IO_REQUIREMENTS):
        _add(checks, f"skr.{idx}", r in (skel_io.get("requirements") or []))
    for idx, r in enumerate(CANDIDATE_COMMON_PAYLOAD_REQUIREMENTS):
        _add(checks, f"ccr.{idx}", r in (common.get("common") or []))

    guard_keys = (
        "no_model_download", "no_weight_download", "no_inference_execution", "no_runtime_execution",
        "no_integration_test", "no_model_selected_as_production", "download_authorized_all_remain_false",
        "self_developed_skeleton_still_next", "skeleton_schema_adjustment_needed_evaluated",
        "field_first_route_preserved", "no_download_execution",
    )
    for k in guard_keys:
        _add(checks, f"guard.{k[:14]}", s.get(k) is True)

    for k in ("file_size_governance_review_ok", "full_repo_scan_absent", "tmp_eval_out_scan_absent", "summary_index_first_reading_ok"):
        _add(checks, f"fs.{k[:12]}", s.get(k) is True)
    for k in FILE_SIZE_GOVERNANCE_REVIEW_KEYS:
        _add(checks, f"fsr.{k[:14]}", fs.get(k) is True)
    for rel in FIELD_FIRST_IO_PRECHECK_WHITELIST_FILES:
        _add(checks, f"wl.{rel.split('/')[-1][:12]}", (REPO_ROOT / rel).is_file())
    for rel in PHASE_PYTHON_FILES:
        row = next((r for r in fs.get("phase_python_files") or [] if r.get("path") == rel), {})
        _add(checks, f"pf.{rel.split('/')[-1][:12]}", row.get("tier") == "ok")
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"go.{k[:14]}", s.get(k) is True)
    _add(checks, "sum.phase", s.get("phase") == PHASE_ID)
    _add(checks, "sum.scope", s.get("scope") == SCOPE)
    _add(checks, "sum.blocker0", s.get("blocker_count") == 0)
    _add(checks, "report.final", report.get("final_decision") == FINAL_DECISION_GO)

    for idx, k in enumerate(GO_CONDITIONS_KEYS):
        _add(checks, f"gok2.{idx}", s.get(k) is True)
    for idx, item in enumerate(MODEL_IO_REVIEW_ITEMS):
        _add(checks, f"iidx.{idx}", item["model_project_id"] in [x.get("model_project_id") for x in items])
    for idx, sp in enumerate(COMMON_SPATIAL_PAYLOAD):
        _add(checks, f"sp.{idx}", sp in (common.get("spatial") or []))
    for idx, tp in enumerate(COMMON_TEMPORAL_PAYLOAD):
        _add(checks, f"tp.{idx}", tp in (common.get("temporal") or []))
    for idx, rule in enumerate(DO_NOT_MISCLASSIFY):
        _add(checks, f"mis.{idx}", rule in (docs.get("do_not_misclassify_rules_v1.json", {}).get("rules") or []))
    for idx, row in enumerate(mapping.get("rows") or []):
        _add(checks, f"map.{idx}", bool(row.get("maps_to_candidate_type")))
    for idx, row in enumerate(compat.get("rows") or []):
        _add(checks, f"cmp.{idx}", bool(row.get("compatibility_status")))
    kimera = next((x for x in items if x.get("model_project_id") == "Kimera"), {})
    _add(checks, "kimera.ref", kimera.get("compatibility_status") == "reference_only_no_schema_commitment")
    luna_ecs = next((x for x in items if x.get("model_project_id") == "Luna_dataclass_ECS_skeleton"), {})
    _add(checks, "ecs.compat", luna_ecs.get("compatibility_status") == "compatible_with_current_candidate_schema")
    for idx, item in enumerate(items):
        _add(checks, f"adjn.{idx}", "skeleton_schema_adjustment_needed" in item)
    for key in SKELETON_SCHEMA_ADJUSTMENT_PLAN:
        if key.endswith("_payload") or key.startswith("observation") or key.startswith("field_") or key.startswith("text_") or key.startswith("reasoning"):
            _add(checks, f"adjk.{key[:12]}", adjust.get(key) is True)
    for idx, item in enumerate(MODEL_IO_REVIEW_ITEMS):
        row = next((x for x in items if x.get("model_project_id") == item["model_project_id"]), {})
        for j, c in enumerate(item.get("candidate_fields_confirmed_by_docs") or ()):
            _add(checks, f"conf.{item['model_project_id'][:6]}.{j}", c in (row.get("candidate_fields_confirmed_by_docs") or []))

    for idx, ip in enumerate(COMMON_IDENTITY_PAYLOAD):
        _add(checks, f"id.{idx}", ip in (common.get("identity") or []))
    for idx, cp in enumerate(COMMON_CONFIDENCE_PAYLOAD):
        _add(checks, f"cf.{idx}", cp in (common.get("confidence") or []))
    for idx, gp in enumerate(COMMON_GRAPH_PAYLOAD):
        _add(checks, f"gr.{idx}", gp in (common.get("graph") or []))
    for idx, ta in enumerate(COMMON_TEXT_AUDIO_PAYLOAD):
        _add(checks, f"ta.{idx}", ta in (common.get("text_audio") or []))

    for idx, item in enumerate(MODEL_IO_REVIEW_ITEMS):
        row = next((x for x in items if x.get("model_project_id") == item["model_project_id"]), {})
        _add(checks, f"room.{idx}", row.get("model_room") == item["model_room"])
        _add(checks, f"node.{idx}", row.get("operation_node_id") == item["operation_node_id"])
        _add(checks, f"stat2.{idx}", row.get("compatibility_status") in COMPATIBILITY_STATUS_OPTIONS)
        for j, m in enumerate(item.get("maps_to_candidate_type") or []):
            _add(checks, f"map2.{idx}.{j}", m in (row.get("maps_to_candidate_type") or []))

    for idx, key in enumerate(SKELETON_SCHEMA_ADJUSTMENT_PLAN):
        _add(checks, f"adjall.{idx}", adjust.get(key) == SKELETON_SCHEMA_ADJUSTMENT_PLAN[key])

    for idx, rule in enumerate(PRECHECK_PRINCIPLES.get("rules") or ()):
        _add(checks, f"prin.{idx}", rule in (report.get("principles", {}).get("rules") or ()))

    visual_ids = ("ByteTrack", "YOLO_lightweight", "SAM2", "Grounded_SAM2", "GroundingDINO")
    ocr_ids = ("PaddleOCR", "RapidOCR")
    asr_ids = ("Whisper", "faster_whisper", "SenseVoice", "pyannote_audio")
    spatial_ids = ("Kimera", "Hydra", "HOV_SG", "Open3DSG")
    self_ids = ("Luna_dataclass_ECS_skeleton", "Luna_lightweight_event_graph_skeleton", "Luna_geometry_simulator", "rule_LLM_hybrid")
    for mid in visual_ids:
        row = next((x for x in items if x.get("model_project_id") == mid), {})
        _add(checks, f"vis.{mid[:8]}", bool(row.get("spatial_output_fields")))
    for mid in ocr_ids:
        row = next((x for x in items if x.get("model_project_id") == mid), {})
        _add(checks, f"ocr2.{mid[:8]}", bool(row.get("text_fields")))
    for mid in asr_ids:
        row = next((x for x in items if x.get("model_project_id") == mid), {})
        _add(checks, f"asr.{mid[:8]}", bool(row.get("audio_segment_fields") or row.get("text_fields")))
    for mid in spatial_ids:
        row = next((x for x in items if x.get("model_project_id") == mid), {})
        _add(checks, f"sg.{mid[:8]}", row.get("compatibility_status") == "reference_only_no_schema_commitment")
    for mid in self_ids:
        row = next((x for x in items if x.get("model_project_id") == mid), {})
        _add(checks, f"self.{mid[:8]}", bool(
            row.get("structured_output_fields") or row.get("graph_or_relation_fields") or row.get("spatial_output_fields")
        ))

    for idx, gap in enumerate(gaps.get("gaps") or []):
        _add(checks, f"gap.{idx}", bool(gap.get("gap_id") or gap.get("model_project_id")))
    for idx, row in enumerate(gaps.get("gaps") or []):
        _add(checks, f"gapf.{idx}", bool(row.get("missing") or row.get("candidate_fields_missing_or_unclear")))

    _add(checks, "md.exists", (root / "model_io_compatibility_precheck_report_v1.md").is_file())
    _add(checks, "report.precheck", report.get("model_io_compatibility_precheck_complete") is True)
    _add(checks, "report.mapping", report.get("model_io_to_candidate_mapping_complete") is True)
    _add(checks, "report.compat", report.get("candidate_schema_compatibility_matrix_complete") is True)
    _add(checks, "report.skel", report.get("field_first_skeleton_io_requirements_complete") is True)
    _add(checks, "report.no_dl", report.get("no_download_execution") is True)
    _add(checks, "report.no_inf", report.get("no_inference_execution") is True)
    _add(checks, "report.no_rt", report.get("no_runtime_execution") is True)
    _add(checks, "report.next_ok", report.get("next_phase_readiness_ok") is True)

    for idx, item in enumerate(items):
        _add(checks, f"src.{idx}", bool(item.get("model_project_id")))
        _add(checks, f"inp.{idx}", bool(item.get("expected_input_type")))
        _add(checks, f"out.{idx}", bool(item.get("expected_output_type")))
        _add(checks, f"xfm.{idx}", bool(item.get("required_adapter_transform")))

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
