# -*- coding: utf-8 -*-
"""Vision runtime — minimal video frame ingest skeleton (evaluation-only)."""

from .external_supervision_adapter_experiment_v0 import run_external_supervision_adapter_experiment_v0
from .video_frame_audit_v0 import build_default_video_frame_audit_v0
from .video_frame_envelope_v0 import build_video_frame_envelope_v0, fingerprint_png_bytes
from .video_frame_ingest_v0 import generate_test_video_mp4_v0, ingest_video_frames_offline_v0
from .video_frame_sampling_policy_v0 import VideoFrameSamplingParamsV0, run_sampling_plan_v0
from .vision_frame_input_governance_v0 import run_vision_frame_input_governance_v0
from .vision_frame_trace_v0 import run_vision_frame_trace_stream_registry_from_ingest_v0
from .vision_provider_adapter_contract_v0 import VisionProviderAdapterV0
from .vision_provider_input_pack_v0 import build_pack_for_frame_v0, build_coordinate_transform_v0
from .vision_provider_registry_v0 import build_default_vision_provider_registry_v0, snapshot_registry_v0
from .vision_provider_selection_v0 import run_vision_recognition_adapter_selection_skeleton_v0
from .vision_provider_stub_adapter_v0 import VisionStubAdapterV0, merge_stub_results_v0
from .vision_recognition_audit_v0 import build_vision_recognition_adapter_selection_audit_v0
from .vision_recognition_evidence_pack_v0 import (
    build_vision_recognition_evidence_pack_from_adapter_selection_v0,
)
from .vision_recognition_evidence_readonly_consumer_v0 import (
    run_vision_recognition_evidence_readonly_consumer_v0,
)
from .vision_roi_proposal_stub_v0 import (
    build_rule_stub_rois_for_frame_v0,
    run_vision_roi_proposal_stub_from_governance_v0,
)
from .vision_stream_registry_v0 import build_vision_stream_registry_v0

__all__ = [
    "build_default_video_frame_audit_v0",
    "build_video_frame_envelope_v0",
    "fingerprint_png_bytes",
    "generate_test_video_mp4_v0",
    "ingest_video_frames_offline_v0",
    "VideoFrameSamplingParamsV0",
    "run_sampling_plan_v0",
    "build_vision_stream_registry_v0",
    "run_external_supervision_adapter_experiment_v0",
    "run_vision_frame_input_governance_v0",
    "run_vision_frame_trace_stream_registry_from_ingest_v0",
    "build_coordinate_transform_v0",
    "build_pack_for_frame_v0",
    "VisionProviderAdapterV0",
    "build_default_vision_provider_registry_v0",
    "snapshot_registry_v0",
    "run_vision_recognition_adapter_selection_skeleton_v0",
    "VisionStubAdapterV0",
    "merge_stub_results_v0",
    "build_vision_recognition_adapter_selection_audit_v0",
    "build_vision_recognition_evidence_pack_from_adapter_selection_v0",
    "run_vision_recognition_evidence_readonly_consumer_v0",
    "build_rule_stub_rois_for_frame_v0",
    "run_vision_roi_proposal_stub_from_governance_v0",
]
