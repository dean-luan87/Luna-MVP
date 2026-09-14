"""Static caller-wiring inspection for the real YOLO11n/FPO seam.

This verifier reads source text and checks actual call-site wiring.  It does
not import the runtime path, execute a model, or infer correctness from
synthetic records.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Mapping


ENTRYPOINT_RELATIVE = Path(
    "capabilities/midplatform/field_perception_orchestrator/integration/"
    "yolo11n_single_frame_execution/run_yolo11n_real_single_frame_provider_execution_v1.py"
)
PROVIDER_RELATIVE = Path(
    "capabilities/midplatform/field_perception_orchestrator/integration/"
    "field_perception_real_vision_provider_adapter_v1.py"
)
BUILDER_RELATIVE = Path(
    "capabilities/midplatform/field_perception_orchestrator/integration/"
    "canonical_yolo11n_context_builder_v1.py"
)
LEGACY_REAL_CALLER_RELATIVES = (
    Path("capabilities/midplatform/field_perception_orchestrator/integration/run_a_route_s3_real_vision_yolo_evidence_controlled_replacement_v1.py"),
    Path("capabilities/midplatform/core/cognitive_flow/integration/dynamic_cognitive_flow_real_capability_single_invocation_trial/dynamic_cognitive_flow_real_capability_trial_adapter_v1.py"),
)
TARGETED_UPSTREAM_CALLER_RELATIVES = LEGACY_REAL_CALLER_RELATIVES
RUNTIME_ADMISSION_PRODUCTION_RELATIVE = Path(
    "capabilities/midplatform/core/cognitive_flow/integration/"
    "runtime_admission_production_controlled/producer_v1.py"
)
RUNTIME_ADMISSION_YOLO_SOURCE_RELATIVE = Path(
    "capabilities/midplatform/core/cognitive_flow/integration/"
    "runtime_admission_production_controlled/yolo11n_source_v1.py"
)
GOVERNED_PRODUCER_RELATIVE = Path(
    "capabilities/midplatform/core/cognitive_flow/integration/"
    "governed_capability_execution_record_production_controlled/yolo11n_producer_entry_v1.py"
)
CLOSURE_RUNNER_RELATIVE = Path(
    "capabilities/midplatform/core/cognitive_flow/integration/"
    "yolo11n_governed_execution_chain_closure_controlled/runner_v1.py"
)


def _contains_all(source: str, markers: Iterable[str]) -> bool:
    return all(marker in source for marker in markers)


def _source(repo_root: Path, relative: Path) -> str:
    path = repo_root / relative
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _inspect_governed_chain_linkage_v1(repo_root: Path) -> Dict[str, object]:
    runtime_source = _source(repo_root, RUNTIME_ADMISSION_PRODUCTION_RELATIVE)
    yolo_source = _source(repo_root, RUNTIME_ADMISSION_YOLO_SOURCE_RELATIVE)
    governed_source = _source(repo_root, GOVERNED_PRODUCER_RELATIVE)
    closure_source = _source(repo_root, CLOSURE_RUNNER_RELATIVE)
    checks = {
        "runtime_admission_production_symbol": "def assess_runtime_admission_production_v1" in runtime_source,
        "runtime_source_to_repository_yolo_source": _contains_all(
            yolo_source,
            ("build_repository_runtime_admission_input_v1", "assess_runtime_admission_production_v1", "build_governed_execution_record_bundle_v1"),
        ),
        "governed_producer_calls_repository_bundle_source": "produce_repository_backed_yolo11n_bundle_v1" in governed_source,
        "governed_producer_exposes_canonical_translation": _contains_all(
            governed_source,
            ("GovernedExecutionRecordBundleV1", "adapt_governed_bundle_to_canonical_yolo11n_records_v1", "CanonicalYOLO11nUpstreamRecordsV1"),
        ),
        "closure_runner_consumes_governed_chain": _contains_all(
            closure_source,
            ("produce_yolo11n_governed_execution_records_v1", "adapt_governed_bundle_to_canonical_yolo11n_records_v1", "build_canonical_yolo11n_context_v1", "build_canonical_yolo11n_provider_admission_v1"),
        ),
    }
    return {"checks": checks, "governed_chain_linked": all(checks.values())}


def inspect_real_yolo11n_caller_wiring_v1(repo_root: Path) -> Dict[str, object]:
    entrypoint = (repo_root / ENTRYPOINT_RELATIVE).read_text(encoding="utf-8")
    provider = (repo_root / PROVIDER_RELATIVE).read_text(encoding="utf-8")
    builder = (repo_root / BUILDER_RELATIVE).read_text(encoding="utf-8")
    legacy_sources: Mapping[str, str] = {
        str(path): (repo_root / path).read_text(encoding="utf-8")
        for path in LEGACY_REAL_CALLER_RELATIVES
        if (repo_root / path).is_file()
    }
    governed_chain = _inspect_governed_chain_linkage_v1(repo_root)
    checks = {
        "real_entrypoint_accepts_canonical_binding_context": _contains_all(
            entrypoint,
            ("canonical_binding: Optional[CanonicalYOLO11nBindingContextV1]", "def run("),
        ),
        "real_entrypoint_uses_canonical_adapter": _contains_all(
            entrypoint,
            ("build_canonical_yolo11n_provider_admission_v1", "if source_mode == \"REAL\":", "context=canonical_binding"),
        ),
        "provider_guard_requires_canonical_chain": _contains_all(
            provider,
            ("execute_real_provider and admission is not None and not admission.canonical_chain_validated", "canonical_binding_seam"),
        ),
        "provider_guard_preserves_invalidation_block": "canonical_invalidation_refs" in provider,
        "context_builder_requires_governed_records": _contains_all(
            builder,
            ("CanonicalYOLO11nUpstreamRecordsV1", "build_canonical_yolo11n_context_v1", "all canonical upstream records must be supplied"),
        ),
        "targeted_upstream_caller_constructs_context": bool(legacy_sources) and any(
            "build_canonical_yolo11n_context_v1(" in source for source in legacy_sources.values()
        ),
        "targeted_upstream_caller_injects_context": bool(legacy_sources) and any(
            "build_canonical_yolo11n_context_v1(" in source and "effective_binding" in source and "_real_case(" in source
            for source in legacy_sources.values()
        ),
        "governed_upstream_record_producer_found": bool(governed_chain["governed_chain_linked"]),
        "legacy_real_callers_delegate_to_shared_provider_guard": bool(legacy_sources) and all(
            "run_authorized_vision_provider_v1" in source for source in legacy_sources.values()
        ) and "canonical_chain_validated" in provider,
    }
    return {
        "entrypoint": str(ENTRYPOINT_RELATIVE),
        "provider": str(PROVIDER_RELATIVE),
        "builder": str(BUILDER_RELATIVE),
        "legacy_real_callers": sorted(legacy_sources),
        "targeted_upstream_callers": [str(path) for path in TARGETED_UPSTREAM_CALLER_RELATIVES if (repo_root / path).is_file()],
        "governed_chain_sources": {
            "runtime_admission_production": str(RUNTIME_ADMISSION_PRODUCTION_RELATIVE),
            "runtime_admission_yolo_source": str(RUNTIME_ADMISSION_YOLO_SOURCE_RELATIVE),
            "governed_producer": str(GOVERNED_PRODUCER_RELATIVE),
            "closure_runner": str(CLOSURE_RUNNER_RELATIVE),
        },
        "governed_chain_linkage": governed_chain,
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "runtime_executed": False,
        "model_loaded": False,
        "provider_invoked": False,
    }


__all__ = ["inspect_real_yolo11n_caller_wiring_v1"]
