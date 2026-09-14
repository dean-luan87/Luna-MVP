#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Voice-Qianwen-000 — Qianwen Voice Provider Control Inventory v0

Static scan only. No runtime changes, no network, no TTS playback, no DashScope calls.

Outputs under: logs/voice_qianwen_provider_control_inventory_000_<timestamp>/
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, DefaultDict, Dict, Iterable, List, Optional, Sequence, Set, Tuple

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # type: ignore


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _utc_ts_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    ".eggs",
    "*.egg-info",
}

TEXT_SUFFIXES = (
    ".py",
    ".md",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".txt",
    ".sh",
    ".ini",
    ".cfg",
)


@dataclass(frozen=True)
class SearchPattern:
    key: str
    pattern: str
    is_regex: bool


# Mirrors user-suggested greps; `-i` semantics for non-regex substring.
SEARCH_PATTERNS: Tuple[SearchPattern, ...] = (
    SearchPattern("qianwen", r"qianwen", True),
    # match qwen/qianwen-dash/qwen.tts/etc. (boundary too strict would miss qwen-tts)
    SearchPattern("qwen", r"qwen", True),
    SearchPattern("qianwen_zh", "千问", False),
    SearchPattern("tongyi", r"tongyi", True),
    SearchPattern("dashscope", r"dashscope", True),
    SearchPattern("source_text", r"source_text", True),
    SearchPattern("spoken_text", r"spoken_text", True),
    SearchPattern("model_generated_text", r"model_generated_text", True),
    SearchPattern("rewrite_allowed", r"rewrite_allowed", True),
    SearchPattern("expression_only", r"expression_only", True),
    SearchPattern("no_fabrication", r"no_fabrication", True),
    SearchPattern("diff_audit", r"diff_audit", True),
    SearchPattern("text_diff", r"text_diff", True),
    SearchPattern("provider_selection", r"provider_selection", True),
    SearchPattern("primary_provider", r"primary\s+provider", True),
    SearchPattern("fallback_provider", r"fallback\s+provider", True),
    SearchPattern("tts_fallback", r"tts_fallback", True),
    SearchPattern("qianwen_fallback", r"qianwen.*fallback", True),
    SearchPattern("qwen_fallback", r"qwen.*fallback", True),
    SearchPattern("SpeechGate", r"SpeechGate", False),
    SearchPattern("guard_v1_speakable_text", r"guard_v1_speakable_text", True),
    SearchPattern("VoiceOutputGovernance", r"VoiceOutputGovernance", False),
    SearchPattern("real_tts_invoked", r"real_tts_invoked", True),
    SearchPattern("provider_health", r"provider_health", True),
)


def _should_skip_dir(name: str) -> bool:
    return name in SKIP_DIR_NAMES or name.endswith(".egg-info")


def _is_probably_text(p: Path) -> bool:
    if p.suffix.lower() in TEXT_SUFFIXES:
        return True
    # Files without suffix in tools/docs sometimes
    return p.parent.name in ("scripts",)


def iter_scan_files(scan_roots: Sequence[Path]) -> Iterable[Path]:
    for root in scan_roots:
        if not root.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dsp = Path(dirpath)
            dirnames[:] = [d for d in sorted(dirnames) if not _should_skip_dir(d)]
            for fn in sorted(filenames):
                fp = dsp / fn
                if fp.is_file() and _is_probably_text(fp):
                    yield fp


def compile_pat(sp: SearchPattern) -> Tuple[Optional[re.Pattern[str]], str]:
    if sp.is_regex:
        flags = re.IGNORECASE | re.MULTILINE
        return re.compile(sp.pattern, flags), sp.pattern
    return None, sp.pattern.lower()


def search_all(
    repo: Path,
    files: Iterable[Path],
    patterns: Sequence[SearchPattern],
    max_hits_per_pattern: int = 400,
) -> Dict[str, List[Dict[str, Any]]]:
    out: Dict[str, List[Dict[str, Any]]] = {p.key: [] for p in patterns}
    compiled = {p.key: compile_pat(p) for p in patterns}

    for fp in files:
        try:
            rel = str(fp.relative_to(repo))
        except ValueError:
            rel = str(fp)
        if rel.startswith("."):
            continue
        try:
            raw = fp.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            try:
                raw = fp.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue

        lines = raw.splitlines()
        for sp in patterns:
            if len(out[sp.key]) >= max_hits_per_pattern:
                continue
            cre, literal = compiled[sp.key]
            lit_lower = literal.lower()
            for i, line in enumerate(lines, start=1):
                if len(out[sp.key]) >= max_hits_per_pattern:
                    break
                hit = cre.search(line) if cre is not None else (lit_lower in line.lower())
                if hit:
                    out[sp.key].append({"path": rel, "line_no": i, "line": line[:500]})

    return out


def _uniq_paths(hits_by_pat: Dict[str, List[Dict[str, Any]]], keys: Sequence[str]) -> Set[str]:
    s: Set[str] = set()
    for k in keys:
        for h in hits_by_pat.get(k, []):
            s.add(str(h["path"]))
    return s


def classify_code_assets(repo: Path, scan_files: Iterable[Path]) -> Dict[str, Any]:
    buckets: DefaultDict[str, List[str]] = defaultdict(list)

    keywords = (
        ("qwen_tts_provider", ["qwen_tts_provider"]),
        ("qwen_tts_client_module", ["modules/qwen_tts"]),
        ("tts_unified_entry", ["tts_unified_entry"]),
        ("tts_fallback_manager", ["tts_fallback_manager"]),
        ("tts_provider_selector", ["tts_provider_selector"]),
        ("tts_provider_health", ["tts_provider_health"]),
        ("voice_output_plane_v1", ["voice_output_plane_v1"]),
        ("voice_output_governance", ["voice_output_governance"]),
        ("voice_governed_submit_shadow", ["voice_governed_submit_shadow"]),
        ("long_input_qwen_providers", ["qwen_long_input", "qwen_external_long_input"]),
    )

    for fp in scan_files:
        rel = fp.relative_to(repo)
        rp = rel.as_posix()
        if not rp.startswith("capabilities/voice"):
            continue
        for bucket, needles in keywords:
            if any(n in rp for n in needles):
                buckets[bucket].append(rp)

    for bucket in buckets:
        buckets[bucket] = sorted(set(buckets[bucket]))

    return {"capabilities_voice_buckets": dict(buckets)}


def classify_doc_assets(hits_by_pat: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    doc_paths: Set[str] = set()
    for lst in hits_by_pat.values():
        for h in lst:
            p = str(h["path"])
            if p.startswith("docs/") and p.endswith(".md"):
                doc_paths.add(p)
    return {"docs_matching_any_pattern": sorted(doc_paths)}


def _load_voice_tts_config(repo: Path) -> Optional[Dict[str, Any]]:
    p = repo / "capabilities/voice/config/voice_tts_config.yaml"
    if not p.exists() or yaml is None:
        return None
    try:
        with p.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return None


def _truthy_yaml_mode(cfg: Optional[Dict[str, Any]]) -> Tuple[str, Dict[str, Any]]:
    if not cfg:
        return "", {}
    mode = str(cfg.get("tts_runtime_mode") or "")
    modes = cfg.get("runtime_modes") if isinstance(cfg.get("runtime_modes"), dict) else {}
    return mode, modes


def _voice_hits(hits_by_pat: Dict[str, List[Dict[str, Any]]], key: str) -> List[Dict[str, Any]]:
    return [h for h in (hits_by_pat.get(key) or []) if str(h.get("path") or "").startswith("capabilities/voice/")]


def _file_has_snippet(repo: Path, rel: str, snippets: Sequence[str]) -> bool:
    p = repo / rel
    if not p.exists():
        return False
    try:
        txt = p.read_text(encoding="utf-8")
    except OSError:
        return False
    return all(s in txt for s in snippets)


def build_provider_role_matrix(
    repo: Path, hits_by_pat: Dict[str, List[Dict[str, Any]]]
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    cfg = _load_voice_tts_config(repo)
    mode_name, modes = _truthy_yaml_mode(cfg)

    opq = modes.get("online_prefer_qwen") if isinstance(modes, dict) else None
    opq_po = []
    ap_opq = ""
    if isinstance(opq, dict):
        opq_po = list(opq.get("provider_order") or [])
        ap_opq = str(opq.get("active_provider") or "")

    default_po = []
    if isinstance(cfg, dict):
        default_po = list(cfg.get("provider_order") or [])

    lr = cfg.get("local_runtime") if isinstance(cfg, dict) else {}
    qw_local = lr.get("qwen") if isinstance(lr, dict) and isinstance(lr.get("qwen"), dict) else {}
    qwen_enabled_default = isinstance(qw_local, dict) and bool(qw_local.get("enabled")) is True

    q_adapter = (repo / "capabilities/voice/providers/qwen_tts_provider.py").exists()

    docs_primary_signals = sorted(
        _uniq_paths(hits_by_pat, ("qwen", "dashscope")).intersection(
            {p for p in classify_doc_assets(hits_by_pat)["docs_matching_any_pattern"]}
        )
    )

    declared_doc_qwen_online_first = False
    for dp in docs_primary_signals:
        if not dp.startswith("docs/architecture/"):
            continue
        p = repo / dp
        try:
            t = p.read_text(encoding="utf-8").lower()
        except OSError:
            continue
        if any(
            k in t
            for k in (
                "online_prefer_qwen",
                "qwen preferred",
                "qwen first",
                "online-first",
                "online first",
                "首选",
                "优先",
                "primary voice",
                "preferred voice",
            )
        ):
            declared_doc_qwen_online_first = True

    yaml_declares_prefer_qwen = bool(opq_po and str(opq_po[0]).lower() == "qwen")
    tts_fallback_declared = yaml_declares_prefer_qwen and len(opq_po) >= 2 and ("piper" in [str(x) for x in opq_po])

    plane_bypass_sg = _file_has_snippet(
        repo,
        "capabilities/voice/output/voice_output_plane_v1.py",
        ("仍不接 speech_gate",),
    )

    gov_file = repo / "capabilities/voice/output/voice_output_governance_v0.py"
    gov_exists = gov_file.exists()

    # Participation / guard-speech linkage: VoiceOutputPlaneV1 注释指明 execute_tts 不经 SpeechGate，
    # 但无法用本静态盘点证明不存在其它外层包裹，故输出 unknown 并依赖 gap 登记表。
    tri_guard = "unknown"
    tri_gate = "unknown"
    participates = "unknown" if gov_exists else False

    role: Dict[str, Any] = {
        "qianwen_provider_exists": bool(q_adapter),
        "qianwen_voice_primary_declared": bool(yaml_declares_prefer_qwen or declared_doc_qwen_online_first),
        "tts_fallback_declared": bool(tts_fallback_declared),
        "provider_selection_supports_qianwen_first": bool(isinstance(cfg, dict) and yaml_declares_prefer_qwen),
        "qianwen_passes_guard": tri_guard,
        "qianwen_passes_speech_gate": tri_gate,
        "qianwen_participates_output_governance": participates,
        "qianwen_provider_health_defined": bool((repo / "capabilities/voice/runtime/tts_provider_health_v0.py").exists()),
        "qianwen_fallback_to_tts_defined": bool(
            yaml_declares_prefer_qwen
            or _file_has_snippet(repo, "capabilities/voice/providers/tts_fallback_manager.py", ("qwen",))
        ),
        # 需要语义化配对 schema，不仅仅是 token 共存
        "source_text_spoken_text_diff_defined": False,
        "rewrite_control_defined": bool(_voice_hits(hits_by_pat, "rewrite_allowed")),
        "no_fabrication_control_defined": bool(_voice_hits(hits_by_pat, "no_fabrication")),
        "real_qianwen_invocation_allowed_currently": False,
    }

    evidence: Dict[str, Any] = {
        "voice_default_baseline_yaml": {
            "tts_runtime_mode": mode_name or None,
            "top_level_provider_order": default_po or None,
            "top_level_active_provider": cfg.get("active_provider") if isinstance(cfg, dict) else None,
            "online_prefer_qwen_provider_order": opq_po or None,
            "online_prefer_qwen_active_provider": ap_opq or None,
            "local_runtime_qwen_enabled": bool(qw_local.get("enabled")) if isinstance(qw_local, dict) else None,
        },
        "default_baseline_qwen_voice_primary_strict": bool(
            default_po and str(default_po[0]).lower() == "qwen"
        )
        and str(mode_name) == "online_prefer_qwen"
        and qwen_enabled_default,
        "voice_output_plane_v1_explicit_no_speech_gate_comment": plane_bypass_sg,
        "voice_output_governance_module_present": gov_exists,
        "doc_hints_qwen_online_or_preferred_cn_en": declared_doc_qwen_online_first,
        "docs_matching_qwen_signals_sample": docs_primary_signals[:30],
        "hits_spoken_text_count": len(hits_by_pat.get("spoken_text") or []),
        "hits_source_text_count": len(hits_by_pat.get("source_text") or []),
        "hits_model_generated_text_count": len(hits_by_pat.get("model_generated_text") or []),
        "hits_diff_audit_count": len(hits_by_pat.get("diff_audit") or []),
        "hardcoded_paths_checked": [
            "capabilities/voice/providers/qwen_tts_provider.py",
            "capabilities/voice/config/voice_tts_config.yaml",
            "capabilities/voice/output/voice_output_plane_v1.py",
        ],
    }

    return role, evidence


def _hits_under_prefix(hits: List[Dict[str, Any]], prefix: str) -> List[Dict[str, Any]]:
    return [h for h in hits if str(h.get("path") or "").startswith(prefix)]


def build_gap_register(
    repo: Path,
    role: Dict[str, Any],
    evidence: Dict[str, Any],
    hits_by_pat: Dict[str, List[Dict[str, Any]]],
) -> List[Dict[str, Any]]:
    gaps: List[Dict[str, Any]] = []

    def add(
        gap_id: str,
        severity: str,
        gap_name: str,
        evidence: str,
        recommended_action: str,
        phase_to_fix: str,
    ) -> None:
        gaps.append(
            {
                "gap_id": gap_id,
                "severity": severity,
                "gap_name": gap_name,
                "evidence": evidence,
                "recommended_action": recommended_action,
                "phase_to_fix": phase_to_fix,
            }
        )

    bl = evidence.get("voice_default_baseline_yaml") if isinstance(evidence.get("voice_default_baseline_yaml"), dict) else {}

    add(
        "QWVoice-INV0-H-001",
        "hard",
        "无法证明 VoiceOutputPlaneV1.execute_tts 路径在 unified TTS 前串联 voice_output_governance_v0（guard/SpeechGate/治理字段）",
        "capabilities/voice/output/voice_output_plane_v1.py 注释明示 execute_tts 调用 run_tts_unified_entry 仍不接 SpeechGate/audio_worker。"
        + " _maybe_submit_real_output_v1 亦未调用 build_voice_output_governance_decision_v0。",
        "在下一阶段用显式接线与 RequestTrace/TRW stage 锚点证明 governance 先于 provider chain；或通过统一入口收口。",
        "Phase-Voice-Qianwen-001+",
    )

    if role.get("source_text_spoken_text_diff_defined") is not True:
        add(
            "QWVoice-INV0-H-002",
            "hard",
            "缺少可审计的 source_text vs spoken_text / model_generated_text 结构与 diff_audit 字段链路",
            "静态检索 spoken_text/source_text/model_generated_text/diff_audit 命中不足以构成成对审计 schema；未发现统一 diff audit 产物定义。",
            "定义 Speakability 表达式审计 payload（含 source/spoken/generation/edits）并联入 submit shadow/TRW export。",
            "Phase-Voice-Qianwen-010+",
        )

    expr_cv = _hits_under_prefix(hits_by_pat.get("expression_only") or [], "capabilities/voice/")
    rew_cv = _hits_under_prefix(hits_by_pat.get("rewrite_allowed") or [], "capabilities/voice/")
    if (not expr_cv) and (not rew_cv):
        add(
            "QWVoice-INV0-S-001",
            "soft",
            "capabilities/voice 下未发现 rewrite_allowed / expression_only 策略字段（与「模型表达改写边界」相关的显式控制）",
            "静态检索 expression_only / rewrite_allowed 在 voice 代码树无命中；长输入/LLM 链若独立存在，应在架构上显式声明与播报链关系。",
            "为 Qianwen「非纯 TTS」或 cross-provider 表达引入统一 policy 字段，并纳入 governance audit。",
            "Phase-Voice-Qianwen-020+",
        )

    if role.get("no_fabrication_control_defined") is False:
        add(
            "QWVoice-INV0-S-002",
            "soft",
            "no_fabrication 未形成独立策略开关（仅存局部启发式或未命中关键词）",
            "_maybe_submit_real_output_v1 含占位词启发式；不等同于结构化 no_fabrication policy。",
            "将编造防护提升为可追溯策略与审计字段（与 SpeechGate/expiry/priority 同级）。",
            "Phase-Voice-Qianwen-020+",
        )

    baseline_mode = str(bl.get("tts_runtime_mode") or "")
    dq = bool(bl) and baseline_mode == "offline_only"
    tops = bl.get("top_level_provider_order") or []
    if dq and tops and str(tops[0]).lower() != "qwen":
        add(
            "QWVoice-INV0-S-003",
            "soft",
            "默认 YAML 基线仍为 offline_only + offline provider-only；与「口述策略已调整为 Qwen 首选」易混淆",
            f"tts_runtime_mode={baseline_mode}; top-level provider_order 首个={tops[0] if tops else None}. "
            "`online_prefer_qwen` 位于 runtime_modes 模板，local_runtime.qwen.enabled 常为 false。",
            "在产品/运维口径中分层说明：policy template vs 运行时激活条件 vs 单机默认基线。",
            "Phase-Voice-Qianwen-005 (ops/docs alignment)",
        )

    add(
        "QWVoice-INV0-FUT-001",
        "future",
        "DashScope/Qwen SDK 运行时密钥与合规策略（_inventory 不涉及）",
        "local_runtime.qwen.requires_api_key/requires_network/dashscope 依赖外部环境。",
        "按组织密钥轮换、区域可用性与离线回退 SLA 复盘。",
        "Future governance",
    )

    return gaps


def build_notes_md(
    output_root: Path,
    role: Dict[str, Any],
    gaps: Sequence[Dict[str, Any]],
    summary: Dict[str, Any],
) -> str:
    lines = [
        "# Qianwen Voice Provider Control Inventory v0 — notes",
        "",
        f"- **output_root**: `{output_root}`",
        f"- **generated_at**: {summary.get('generated_at')}",
        "",
        "## Interpretation reminder",
        "",
        "三类证据必须分拆：**(1) 代码是否存在**、(2) **文档/配置是否声明**、(3) **主链是否在默认/激活条件下可证明**。",
        "本脚本对 `voice_output_plane_v1` 的注释与 `_maybe_submit_real_output_v1` 的快速浏览表明：**unified TTS 执行链路未与 `voice_output_governance_v0` 的证明性串联**。",
        "`QwenTTSProvider` 在模块 docstring 中声明 **只做 text→audio**，与「可作为模型改写/生成路径」的职责不同；若接入非纯 TTS 能力必须另建档。",
        "",
        "## provider_role_matrix (copy)",
        "",
        "```json",
        json.dumps(role, ensure_ascii=False, indent=2),
        "```",
        "",
        "## gap_register ids",
        "",
    ]
    for g in gaps:
        lines.append(f"- **{g['gap_id']}** ({g['severity']}): {g['gap_name']}")
    lines.append("")
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Qianwen voice provider control inventory v0")
    ap.add_argument(
        "--repo-root",
        default=str(_repo_root()),
        help="Repository root defaulting to parent of tools/",
    )
    ap.add_argument("--output-root", default="", help="If empty, derive timestamped logs path")
    args = ap.parse_args(list(argv) if argv is not None else None)

    repo = Path(args.repo_root).resolve()
    if yaml is None:
        print("[warn] PyYAML unavailable; YAML-derived fields may be weaker.", file=sys.stderr)

    ts_tag = _utc_ts_tag()
    out_root = Path(args.output_root) if args.output_root else repo / "logs" / f"voice_qianwen_provider_control_inventory_000_{ts_tag}"
    out_root.mkdir(parents=True, exist_ok=True)

    scan_roots = [
        repo / "capabilities",
        repo / "tools",
        repo / "docs",
        repo / "configs",
    ]

    scan_files = sorted(set(iter_scan_files(scan_roots)))

    hits = search_all(repo, scan_files, SEARCH_PATTERNS)

    ca = classify_code_assets(repo, iter_scan_files([repo / "capabilities"]))
    dm = classify_doc_assets(hits)
    matrix, role_evidence = build_provider_role_matrix(repo, hits)
    gaps = build_gap_register(repo, matrix, role_evidence, hits)

    def _rel_scan_root(r: Path) -> str:
        try:
            return str(r.relative_to(repo))
        except ValueError:
            return str(r)

    summary = {
        "inventory_id": "Phase-Voice-Qianwen-000",
        "inventory_kind": "Qianwen_Voice_Provider_Control_Inventory_v0",
        "generated_at": _now_iso(),
        "repo_root": str(repo),
        "scan_roots": [_rel_scan_root(r) for r in scan_roots],
        "files_scanned": len(scan_files),
        "patterns": [{"key": p.key, "pattern": p.pattern, "regex": p.is_regex} for p in SEARCH_PATTERNS],
        "hits_per_pattern_counts": {k: len(v) for k, v in hits.items()},
        "voice_qianwen_provider_role_matrix": matrix,
        "voice_qianwen_provider_role_evidence": role_evidence,
        "voice_qianwen_control_gap_register_counts": {
            "total": len(gaps),
            **{str(s): sum(1 for g in gaps if g["severity"] == s) for s in ("hard", "soft", "future")},
        },
        "constraints": {
            "inventory_static_only": True,
            "no_runtime_behavior_change": True,
            "no_live_qianwen_or_tts": True,
        },
        "go_pack_pointer": "docs/architecture/LUNA_VOICE_QIANWEN_PROVIDER_CONTROL_INVENTORY_GO_NO_GO_PACK_V0.md",
    }

    summary_path = out_root / "voice_qianwen_provider_inventory_summary.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    with (out_root / "voice_qianwen_code_asset_matrix.json").open("w", encoding="utf-8") as f:
        json.dump({"generated_at": _now_iso(), "repo_root": str(repo)} | ca, f, ensure_ascii=False, indent=2)

    with (out_root / "voice_qianwen_doc_asset_matrix.json").open("w", encoding="utf-8") as f:
        json.dump({"generated_at": _now_iso(), "repo_root": str(repo)} | dm, f, ensure_ascii=False, indent=2)

    with (out_root / "voice_qianwen_provider_role_matrix.json").open("w", encoding="utf-8") as f:
        json.dump(matrix, f, ensure_ascii=False, indent=2)

    with (out_root / "voice_qianwen_control_gap_register.json").open("w", encoding="utf-8") as f:
        json.dump(gaps, f, ensure_ascii=False, indent=2)

    with (out_root / "voice_qianwen_search_hits.json").open("w", encoding="utf-8") as f:
        json.dump(hits, f, ensure_ascii=False, indent=2)

    notes = build_notes_md(out_root, matrix, gaps, summary)
    (out_root / "inventory_notes.md").write_text(notes, encoding="utf-8")

    print(json.dumps({"ok": True, "output_root": str(out_root), "files_scanned": len(scan_files)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
