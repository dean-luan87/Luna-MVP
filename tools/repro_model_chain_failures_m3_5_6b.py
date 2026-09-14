#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M3.5.6b 最小观测补证（model_chain 识别链）

原则：
- 只加观测、不改逻辑（观测由专项开关控制）
- 不扩灰、不修复、不改 prefilter/prompt/schema/validator/builder/fallback

复现方式（建议环境变量）：
  export LUNA_EXTERNAL_LLM_PROVIDER=qwen
  export DASHSCOPE_API_KEY=...
  export LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1
  export LUNA_QWEN_MODEL_TIMEOUT_MS=120000
  export LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG=1

运行：
  python3 tools/repro_model_chain_failures_m3_5_6b.py --rounds 6 --time-slot day

输出：
  logs/repro_model_chain_failures_m3_5_6b_<UTC>.json
  logs/repro_model_chain_failures_m3_5_6b_<UTC>.md
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _git_head() -> str:
    try:
        return (
            subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
    except Exception:
        return ""


@dataclass
class Row:
    time_slot: str
    case_id: str
    bucket: str
    routing_suggestion: str
    selected_provider_model_id: str
    used_model_chain: bool
    validator_ok: Optional[bool]
    fallback: bool
    e2e_ms: float
    backup_provider_used: bool
    provider_switch_reason: str
    raw_model_payload_present: Optional[bool]
    raw_json_present: Optional[bool]
    raw_json_top_level_keys: Optional[List[str]]
    model_chain_detection_reason: str
    model_chain_detection_failed_reason: str


def _is_model_route(sug: str) -> bool:
    return sug in ("route_to_turbo", "route_to_plus")


def _is_failure_row(r: Row) -> bool:
    if not _is_model_route(r.routing_suggestion):
        return False
    return (r.used_model_chain is False) or (r.validator_ok is not True) or (r.fallback is True)


def _is_success_row(r: Row) -> bool:
    if not _is_model_route(r.routing_suggestion):
        return False
    return (r.used_model_chain is True) and (r.validator_ok is True) and (r.fallback is False)


def main() -> None:
    ap = argparse.ArgumentParser(description="M3.5.6b minimal-proof repro runner (audit debug only)")
    ap.add_argument(
        "--cases-json",
        type=Path,
        default=ROOT / "configs" / "voice" / "voice_prefilter_routing_real_cases_m3_5_3.json",
        help="case 集（与 M3.5.6 同类，不新增类型）",
    )
    ap.add_argument("--rounds", type=int, default=6, help="每时段轮数（不需要大；目标复现 1～2 条失败）")
    ap.add_argument("--time-slot", choices=("day", "night"), default="day", help="仅跑单段（默认 day）")
    ap.add_argument("--out-json", type=Path, default=None, help="落盘路径（默认 logs/repro_model_chain_failures_m3_5_6b_<UTC>.json）")
    ap.add_argument("--out-dir", type=Path, default=Path.cwd() / "logs", help="输出目录（默认当前工作目录的 logs/）")
    ap.add_argument("--model-timeout-ms", type=int, default=120_000)
    args = ap.parse_args()

    # 强制本进程内开关（不影响产品默认）
    os.environ["LUNA_VOICE_ENABLE_PREFILTER_ROUTING"] = "1"
    os.environ["LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG"] = "1"
    if not (os.getenv("LUNA_QWEN_MODEL_TIMEOUT_MS") or "").strip():
        os.environ["LUNA_QWEN_MODEL_TIMEOUT_MS"] = str(int(args.model_timeout_ms))

    data = json.loads(args.cases_json.read_text(encoding="utf-8"))
    cases: List[Dict[str, Any]] = list(data.get("cases") or [])
    if not cases:
        raise SystemExit(f"no cases in {args.cases_json}")

    from capabilities.voice.runtime.voice_final_text_dispatcher import dispatch_voice_final_text
    from capabilities.voice.schemas.voice_input_event import VoiceInputEvent
    import capabilities.voice.bridge.voice_long_input_model_output_validator as vmod

    _last_vr: Dict[str, Any] = {"vr": None}
    _orig_val = vmod.validate_model_structured_output

    def _val_wrap(s: Any, *, cfg: Any):
        r = _orig_val(s, cfg=cfg)
        _last_vr["vr"] = r
        return r

    vmod.validate_model_structured_output = _val_wrap  # type: ignore[assignment]

    rows: List[Row] = []
    print("M3.5.6b repro starting…", flush=True)
    print(
        "  cases:",
        args.cases_json,
        "cases_n:",
        len(cases),
        "rounds:",
        args.rounds,
        "time_slot:",
        args.time_slot,
        "LUNA_QWEN_MODEL_TIMEOUT_MS:",
        os.getenv("LUNA_QWEN_MODEL_TIMEOUT_MS"),
        flush=True,
    )

    for r in range(1, max(1, int(args.rounds)) + 1):
        for c in cases:
            cid = str(c.get("id") or "")
            bucket = str(c.get("bucket") or "")
            text = str(c.get("text") or "")
            _last_vr["vr"] = None

            print(f"  [{args.time_slot}] [{r}/{args.rounds}] {cid} …", flush=True)

            ev = VoiceInputEvent(
                event_id=f"m356b_{args.time_slot}_{r}_{cid}",
                request_id=f"m356b_{args.time_slot}_{r}_{cid}",
                session_id=f"m356b_{args.time_slot}",
                router_decision="accept",
                raw_text=text,
                normalized_text=text,
                wake_word_stripped=text,
                is_task_mode=False,
                shortcut_id=None,
                wake_word_detected=False,
            )
            t0 = time.perf_counter()
            out = dispatch_voice_final_text(ev)
            e2e_ms = (time.perf_counter() - t0) * 1000.0

            meta = out.metadata or {}
            sug = str(meta.get("prefilter_routing_suggestion") or "")
            sel = str(meta.get("selected_provider_model_id") or "")
            backup_used = bool(meta.get("backup_provider_used", False))
            switch_rs = str(meta.get("provider_switch_reason") or "")

            long_notes = str(meta.get("long_input_notes") or "")
            used_model = long_notes.startswith("model_chain")
            vr = _last_vr["vr"]
            vok = bool(vr.ok) if (vr is not None) else None

            fallback = False
            if _is_model_route(sug):
                fallback = not (used_model and vok is True)

            rows.append(
                Row(
                    time_slot=args.time_slot,
                    case_id=cid,
                    bucket=bucket,
                    routing_suggestion=sug,
                    selected_provider_model_id=sel,
                    used_model_chain=used_model,
                    validator_ok=vok,
                    fallback=fallback,
                    e2e_ms=e2e_ms,
                    backup_provider_used=backup_used,
                    provider_switch_reason=switch_rs,
                    raw_model_payload_present=meta.get("raw_model_payload_present"),
                    raw_json_present=meta.get("raw_json_present"),
                    raw_json_top_level_keys=meta.get("raw_json_top_level_keys"),
                    model_chain_detection_reason=str(meta.get("model_chain_detection_reason") or ""),
                    model_chain_detection_failed_reason=str(meta.get("model_chain_detection_failed_reason") or ""),
                )
            )

    vmod.validate_model_structured_output = _orig_val  # type: ignore[assignment]

    failures = [asdict(x) for x in rows if _is_failure_row(x)]
    successes = [asdict(x) for x in rows if _is_success_row(x)]

    # 简要聚合（方便快速看“是否命中关键判断标准”）
    fail_by_case = Counter(x["case_id"] for x in failures)
    fail_by_reason = Counter((x.get("model_chain_detection_failed_reason") or "").strip() for x in failures)

    payload: Dict[str, Any] = {
        "schema": "luna.voice.repro_m3_5_6b_model_chain_proof.v1",
        "git_head": _git_head(),
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "cases_path": str(args.cases_json),
        "cases_n": len(cases),
        "rounds": int(args.rounds),
        "time_slot": args.time_slot,
        "env": {
            "LUNA_VOICE_ENABLE_PREFILTER_ROUTING": os.getenv("LUNA_VOICE_ENABLE_PREFILTER_ROUTING"),
            "LUNA_QWEN_MODEL_TIMEOUT_MS": os.getenv("LUNA_QWEN_MODEL_TIMEOUT_MS"),
            "LUNA_EXTERNAL_LLM_PROVIDER": os.getenv("LUNA_EXTERNAL_LLM_PROVIDER"),
            "LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG": os.getenv("LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG"),
        },
        "counts": {"rows_total": len(rows), "failure_rows": len(failures), "success_rows": len(successes)},
        "failure_summary": {
            "failure_by_case_top": fail_by_case.most_common(12),
            "failure_by_detection_failed_reason_top": fail_by_reason.most_common(12),
        },
        "rows": [asdict(x) for x in rows],
        "failures": failures,
        "success_controls": successes[:10],
    }

    out_path = args.out_json
    if out_path is None:
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"repro_model_chain_failures_m3_5_6b_{_utc_stamp()}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    # Markdown report
    md_path = out_path.with_suffix(".md")
    lines: List[str] = []
    lines.append("# M3.5.6b model_chain 最小观测补证（repro 报表）")
    lines.append("")
    lines.append(f"- out_json: `{out_path}`")
    lines.append(f"- git_head: `{payload['git_head']}`")
    lines.append(f"- time_slot: `{args.time_slot}` | rounds: **{args.rounds}** | cases_n: **{len(cases)}**")
    lines.append(f"- failure_rows: **{len(failures)}** | success_rows: **{len(successes)}**")
    lines.append("")
    lines.append("## 失败样本（筛选口径：仅 turbo/plus 且 used_model_chain=false 或 validator_ok!=true 或 fallback=true）")
    lines.append("")
    lines.append("| # | case_id | suggestion | selected_model | used_model_chain | validator_ok | fallback | raw_payload | raw_json | raw_json_top_level_keys | detect_reason | detect_failed_reason | e2e_ms |")
    lines.append("|---:|---------|------------|----------------|-----------------|-------------|----------|------------|----------|-------------------------|--------------|----------------------|------:|")
    for i, r in enumerate(failures[:60], 1):
        lines.append(
            "| {i} | `{cid}` | {sug} | {m} | {u} | {v} | {f} | {rp} | {rj} | {keys} | {dr} | {dfr} | {ms:.3f} |".format(
                i=i,
                cid=r.get("case_id"),
                sug=r.get("routing_suggestion"),
                m=r.get("selected_provider_model_id"),
                u=str(r.get("used_model_chain")),
                v=str(r.get("validator_ok")),
                f=str(r.get("fallback")),
                rp=str(r.get("raw_model_payload_present")),
                rj=str(r.get("raw_json_present")),
                keys=str(r.get("raw_json_top_level_keys")),
                dr=(str(r.get("model_chain_detection_reason") or "")[:48] or "—"),
                dfr=(str(r.get("model_chain_detection_failed_reason") or "")[:64] or "—"),
                ms=float(r.get("e2e_ms") or 0.0),
            )
        )
    lines.append("")
    lines.append("## 成功对照样本（前 10 条）")
    lines.append("")
    lines.append("| # | case_id | suggestion | selected_model | used_model_chain | validator_ok | fallback | raw_payload | raw_json | raw_json_top_level_keys | detect_reason | e2e_ms |")
    lines.append("|---:|---------|------------|----------------|-----------------|-------------|----------|------------|----------|-------------------------|--------------|------:|")
    for i, r in enumerate(successes[:10], 1):
        lines.append(
            "| {i} | `{cid}` | {sug} | {m} | {u} | {v} | {f} | {rp} | {rj} | {keys} | {dr} | {ms:.3f} |".format(
                i=i,
                cid=r.get("case_id"),
                sug=r.get("routing_suggestion"),
                m=r.get("selected_provider_model_id"),
                u=str(r.get("used_model_chain")),
                v=str(r.get("validator_ok")),
                f=str(r.get("fallback")),
                rp=str(r.get("raw_model_payload_present")),
                rj=str(r.get("raw_json_present")),
                keys=str(r.get("raw_json_top_level_keys")),
                dr=(str(r.get("model_chain_detection_reason") or "")[:48] or "—"),
                ms=float(r.get("e2e_ms") or 0.0),
            )
        )
    lines.append("")
    lines.append("## 关键判断标准（用于确认 B）")
    lines.append("")
    lines.append("- 若出现 `raw_model_payload_present=true` 且 `raw_json_present=true` 且 `raw_json_top_level_keys` 合理，但 `used_model_chain=false`：倾向 **B（识别/打标口径问题）**。")
    lines.append("- 若失败时 `raw_model_payload_present=false` 或 `raw_json_present=false`：再考虑 **A/C（provider/输出形态/模型侧问题）**。")
    md_path.write_text("\\n".join(lines) + "\\n", encoding="utf-8")

    print("M3.5.6b repro OK")
    print("  out_json:", str(out_path))
    print("  out_md  :", str(md_path))
    print("  failures:", len(failures), "success_controls:", len(successes))


if __name__ == "__main__":
    main()

