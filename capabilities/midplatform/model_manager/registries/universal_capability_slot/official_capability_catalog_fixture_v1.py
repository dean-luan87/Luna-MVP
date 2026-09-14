"""Synthetic catalog and CSA conformance cases; no runtime assets are loaded."""

from __future__ import annotations

from typing import Dict, List

from .official_capability_catalog_governance_v1 import build_official_capability_catalog, validate_catalog
from .official_capability_catalog_types_v1 import to_dict


def _case(case_id: str, title: str, passed: bool, details: Dict[str, object]) -> Dict[str, object]:
    return {"case_id": case_id, "title": title, "passed": bool(passed), "details": details}


def build_case_results() -> List[Dict[str, object]]:
    catalog = build_official_capability_catalog()
    issues = validate_catalog(catalog)
    entry_ids = {entry.module_ref for entry in catalog.entries}
    annotation_ids = {item.module_ref for item in catalog.annotations}
    mapping_classes = {item.classification for item in catalog.asset_mappings}
    safety = next(item for item in catalog.entries if item.requirement_class == "MANDATORY_SAFETY")
    cases = [
        _case("CAT-01", "catalog schema present", bool(catalog.catalog_id and catalog.catalog_version and catalog.entries), {"catalog_id": catalog.catalog_id}),
        _case("CAT-02", "official entries have CSA", len(entry_ids) == len(catalog.entries) and entry_ids == annotation_ids, {"entry_count": len(entry_ids), "annotation_count": len(annotation_ids)}),
        _case("CAT-03", "CSA references valid modules", all(item.module_ref in entry_ids for item in catalog.annotations), {}),
        _case("CAT-04", "CSA is minimal descriptive metadata", all(item.semantic_depth == "MINIMAL" and item.descriptive_only for item in catalog.annotations), {}),
        _case("CAT-05", "CSA has no authority", all(not item.semantic_authority and not item.world_truth_authority and not item.action_authority for item in catalog.annotations), {}),
        _case("CAT-06", "CSA dynamic semantic work deferred", all(item.srsk_consumption_deferred and not item.dynamic_semantic_expansion and not item.dynamic_semantic_folding and not item.semantic_sufficiency_execution for item in catalog.annotations), {}),
        _case("CAT-07", "mandatory safety is an Official Module", safety.origin == "OFFICIAL" and safety.requirement_class == "MANDATORY_SAFETY", {"module_ref": safety.module_ref}),
        _case("CAT-08", "mandatory safety uses generic Slot", all(item.generic_slot_only and not item.safety_slot_specialization for item in catalog.slot_mappings), {}),
        _case("CAT-09", "model assets remain separate", "MODEL" in mapping_classes and all(item.classification != "MODEL" or item.mapped_capability_module != item.existing_asset for item in catalog.asset_mappings), {}),
        _case("CAT-10", "provider assets remain separate", "PROVIDER" in mapping_classes and all(item.classification != "PROVIDER" or item.mapped_capability_module != item.existing_asset for item in catalog.asset_mappings), {}),
        _case("CAT-11", "basic object perception mapped", "object_detection" in entry_ids, {}),
        _case("CAT-12", "basic OCR mapped", "text_recognition" in entry_ids, {}),
        _case("CAT-13", "enhanced OCR mapped only where existing", "precise_ocr" in entry_ids, {}),
        _case("CAT-14", "spatial mapping mapped", "spatial_mapping" in entry_ids, {}),
        _case("CAT-15", "sensor health remains governed reference", "official.system.sensor_health" in entry_ids and any("visual_capability_system_types_v1.py" in item.existing_asset for item in catalog.asset_mappings), {}),
        _case(
            "CAT-16",
            "segmentation gap is explicit",
            any(
                item.existing_asset == "mobile_sam_v1"
                and item.classification == "MODEL"
                and item.mapped_capability_module == "MAPPING_REVIEW_REQUIRED:segmentation"
                and item.mapping_confidence in {"HIGH", "MEDIUM", "LOW"}
                and bool(item.mapping_reason)
                and bool(item.conflict_or_gap)
                and not item.csa_ref
                and not any(entry.module_ref == "segmentation" for entry in catalog.entries)
                for item in catalog.asset_mappings
            ),
            {"mapped_capability_module": "MAPPING_REVIEW_REQUIRED:segmentation", "catalog_entry_present": False},
        ),
        _case("CAT-17", "VIO gap is explicit", any("vio_pose_trajectory" in item.mapped_capability_module and item.mapping_confidence == "MAPPING_REVIEW_REQUIRED" for item in catalog.asset_mappings), {}),
        _case("CAT-18", "face gap is explicit", any("face_related" in item.mapped_capability_module and item.mapping_confidence == "MAPPING_REVIEW_REQUIRED" for item in catalog.asset_mappings), {}),
        _case("CAT-19", "slot compatibility is recorded", len(catalog.slot_mappings) == len(catalog.entries), {}),
        _case("CAT-20", "Capability Self can reference CSA", all(item.csa_ref for item in catalog.entries), {}),
        _case("CAT-21", "Capability is not Knowledge", all("knowledge" not in item.module_ref for item in catalog.entries), {}),
        _case("CAT-22", "Market remains deferred", catalog.market_governance_status == "DEFERRED", {"market_governance_status": catalog.market_governance_status}),
        _case("CAT-23", "uncertain mappings are not hidden", any(item.mapping_confidence == "MAPPING_REVIEW_REQUIRED" for item in catalog.asset_mappings), {}),
        _case("CAT-24", "no runtime/provider execution", catalog.candidate_only and not catalog.runtime_execution and not catalog.provider_invocation and not catalog.model_inference, {}),
    ]
    cases.append(_case("CAT-25", "catalog validator has no issues", not issues, {"issues": issues}))
    return cases


def build_runner_result() -> Dict[str, object]:
    catalog = build_official_capability_catalog()
    cases = build_case_results()
    failed = [item["case_id"] for item in cases if not item["passed"]]
    return {
        "phase": "Phase-Luna-Official-Capability-Module-Existing-Asset-Mapping-And-Conformance-v1-001",
        "mode": "CONTROLLED_CANDIDATE_ONLY",
        "owner": "Capability Registry / Capability Governance",
        "scenario_count": len(cases),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "catalog_id": catalog.catalog_id,
        "catalog_version": catalog.catalog_version,
        "official_module_count": len(catalog.entries),
        "csa_count": len(catalog.annotations),
        "asset_mapping_count": len(catalog.asset_mappings),
        "slot_mapping_count": len(catalog.slot_mappings),
        "mapping_review_required": sum(item.mapping_confidence == "MAPPING_REVIEW_REQUIRED" for item in catalog.asset_mappings),
        "market_governance_status": catalog.market_governance_status,
        "runtime_execution": False,
        "provider_invocation": False,
        "model_inference": False,
        "real_download": False,
        "real_install": False,
        "real_activation": False,
        "real_upgrade": False,
        "real_rollback": False,
        "brain_direct_capability_mutation": False,
        "user_direct_capability_mutation": False,
        "safety_baseline_bypass": False,
        "csa_semantic_authority": False,
        "csa_world_truth_authority": False,
        "csa_action_authority": False,
        "csa_dynamic_semantic_expansion": False,
        "csa_dynamic_semantic_folding": False,
        "csa_semantic_sufficiency_execution": False,
        "srsk_implementation": False,
        "knowledge_acquisition": False,
        "learning_execution": False,
        "memory_mutation": False,
        "capability_value_scoring": False,
        "automatic_capability_optimization": False,
        "automatic_capability_uninstall": False,
        "automatic_capability_acquisition": False,
        "parallel_capability_registry": False,
        "parallel_model_manager": False,
        "parallel_capability_self_owner": False,
        "specialized_universal_slot": False,
        "candidate_only": True,
        "catalog": to_dict(catalog),
        "cases": cases,
    }
