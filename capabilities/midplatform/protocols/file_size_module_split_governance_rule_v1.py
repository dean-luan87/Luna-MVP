# -*- coding: utf-8 -*-
"""File Size & Module Split Governance Rule — canonical definition.

Human-readable source of truth:
  docs/architecture/governance/LUNA_FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_V1.md

Companion rule:
  Reuse-First Protocol Engineering Rule
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

RULE_ID = "file_size_module_split_governance_rule_v1"
RULE_NAME_EN = "File Size & Module Split Governance Rule"
RULE_NAME_ZH = "工程文件大小与模块拆分治理规则"

REUSE_FIRST_RULE_REF = "Reuse-First Protocol Engineering Rule"

DEFINITION_EN = (
    "A single engineering file must not carry too many responsibilities. "
    "Large constants, matrices, protocol tables, template whitelists, error-code maps, and "
    "classification registries must be split into shared modules or indexed data artifacts. "
    "Capability, runner, and verifier files must not become monolithic. "
    "Rigor comes from standardization, reuse, layering, and clear boundaries — not from "
    "stacking files and checks."
)

DEFINITION_ZH = (
    "单个工程文件不得承载过多职责。"
    "大常量、大矩阵、大协议表、大模板白名单、大 error code map、大 classification registry "
    "应拆分到独立模块或数据产物中。"
    "runner / verifier / capability 不得变成 monolithic file。"
    "严谨应靠标准化、复用、分层和边界清楚来实现，而不是靠堆文件和堆检查。"
)

PYTHON_LINE_THRESHOLDS: Dict[str, int] = {
    "suggest_max": 600,
    "warning": 800,
    "blocker_candidate": 1200,
}

MARKDOWN_LINE_THRESHOLDS: Dict[str, int] = {
    "suggest_max": 800,
    "warning": 1200,
    "blocker_candidate": 1800,
}

DEFAULT_SCAN_ROOTS: Tuple[str, ...] = ("capabilities", "tools", "docs")
DEFAULT_SCAN_SKIP_DIRS: Tuple[str, ...] = (
    "__pycache__",
    ".git",
    "node_modules",
    "_tmp_eval_out",
    ".venv",
    "venv",
    "dist",
    "build",
)

CAPABILITY_SPLIT_RULES: Tuple[str, ...] = (
    "keep only phase build logic in capability",
    "move large protocol matrices and constants to shared modules",
    "read registry/index/manifest instead of embedding full tables",
)

RUNNER_SPLIT_RULES: Tuple[str, ...] = (
    "orchestrate and write artifacts only",
    "do not embed large schema/registry/document bodies",
)

VERIFIER_SPLIT_RULES: Tuple[str, ...] = (
    "check logic only; no monolithic whitelist or full protocol corpus",
    "read rules from shared helpers or registry index",
    "prefer summary.json, verifier_report.json, manifest, and index files",
    "never full-repo scan; never read unrelated large files",
    "when historical large files are needed, read index/summary only",
)

TEMPLATE_LINEAGE_SPLIT_RULES: Tuple[str, ...] = (
    "do not grow without bound in one file",
    "split by family / domain / phase group",
    "keep a single aggregation entrypoint",
)

PROTOCOL_REGISTRY_SPLIT_RULES: Tuple[str, ...] = (
    "split L1 / L2 / L3 across files",
    "split input/output/traceability/error-code across files",
    "registry index stores summaries and references only",
)

JSON_ARTIFACT_RULES: Tuple[str, ...] = (
    "do not hard-cap JSON by line count",
    "large registry/matrix must use index + detail files",
    "verifier reads summary/index/manifest first",
)

ENGINEERING_SIMPLICITY_CONSTRAINTS_ZH: Tuple[str, ...] = (
    "能复用 shared helper 就不复制",
    "能 registry patch 就不新开长链",
    "能轻量引用就不完整重验",
    "能拆分文件就不堆进单文件",
    "verifier 读取 summary/index，不读超大文件",
)

FILE_SIZE_GOVERNANCE_REVIEW_KEYS: Tuple[str, ...] = (
    "file_size_governance_review_exists",
    "monolithic_file_absent",
    "large_file_read_avoidance_ok",
    "summary_index_first_reading_ok",
    "template_lineage_growth_controlled",
    "shared_constants_split_ok",
    "verifier_large_file_scan_absent",
)

PHASE_FILE_SIZE_CONSTRAINTS_ZH: Tuple[str, ...] = (
    "不得创建 monolithic file",
    "新增 Python 文件应尽量控制在 600 行以内",
    "超过 800 行必须在 summary 中说明拆分理由",
    "超过 1200 行应判定为 file_size_governance_warning 或 blocker candidate",
    "大型常量/协议表/error map/classification map/template whitelist/matrix schema 必须拆分到 shared module 或独立 JSON",
    "verifier 不得通过读取超大单文件完成检查",
    "禁止全库扫描，禁止读取无关大文件",
    "必须生成 file_size_governance_review_v1.json",
)


def classify_python_line_count(line_count: int) -> str:
    if line_count > PYTHON_LINE_THRESHOLDS["blocker_candidate"]:
        return "blocker_candidate"
    if line_count > PYTHON_LINE_THRESHOLDS["warning"]:
        return "warning"
    if line_count > PYTHON_LINE_THRESHOLDS["suggest_max"]:
        return "above_suggest"
    return "ok"


def classify_markdown_line_count(line_count: int) -> str:
    if line_count > MARKDOWN_LINE_THRESHOLDS["blocker_candidate"]:
        return "blocker_candidate"
    if line_count > MARKDOWN_LINE_THRESHOLDS["warning"]:
        return "warning"
    if line_count > MARKDOWN_LINE_THRESHOLDS["suggest_max"]:
        return "above_suggest"
    return "ok"


def build_file_size_module_split_governance_rule_document(**extra: Any) -> Dict[str, Any]:
    return {
        "rule_id": RULE_ID,
        "rule_name_en": RULE_NAME_EN,
        "rule_name_zh": RULE_NAME_ZH,
        "definition_en": DEFINITION_EN,
        "definition_zh": DEFINITION_ZH,
        "reuse_first_rule_ref": REUSE_FIRST_RULE_REF,
        "python_line_thresholds": dict(PYTHON_LINE_THRESHOLDS),
        "markdown_line_thresholds": dict(MARKDOWN_LINE_THRESHOLDS),
        "capability_split_rules": list(CAPABILITY_SPLIT_RULES),
        "runner_split_rules": list(RUNNER_SPLIT_RULES),
        "verifier_split_rules": list(VERIFIER_SPLIT_RULES),
        "template_lineage_split_rules": list(TEMPLATE_LINEAGE_SPLIT_RULES),
        "protocol_registry_split_rules": list(PROTOCOL_REGISTRY_SPLIT_RULES),
        "json_artifact_rules": list(JSON_ARTIFACT_RULES),
        "engineering_simplicity_constraints_zh": list(ENGINEERING_SIMPLICITY_CONSTRAINTS_ZH),
        "phase_file_size_constraints_zh": list(PHASE_FILE_SIZE_CONSTRAINTS_ZH),
        "file_size_governance_review_keys": list(FILE_SIZE_GOVERNANCE_REVIEW_KEYS),
        "file_size_module_split_governance_rule_complete": True,
        **extra,
    }
