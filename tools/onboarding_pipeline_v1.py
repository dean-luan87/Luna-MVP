#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新模型接入流水线固定入口 V1（只串联，不改底层逻辑）

目标：
- 复用现有脚本，一键跑完最小流程：
  1) contract diff
  2) baseline smoke
  3) 评审补项（P95 / timeout sweep / tokens 代理）
- 统一命名落盘到 logs/
- 自动生成 onboarding summary（接入记录/归档结论骨架 + 引用产物路径 + 关键数值）

原则：
- 只做流水线串联，不改底层测试逻辑
- 不改主链运行逻辑
- 不改 prefilter / prompt / schema / validator / builder / fallback
- 不做自动裁决器，只生成结论骨架

说明（配额）：千问 3.6 等候选模型若账号配额紧张，日常请勿用其做 pipeline 反复调试；可改用 qwen-turbo 等低消耗模型验证入口与 summary 解析。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple


ROOT = Path(__file__).resolve().parent.parent


def _utc_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _safe_tag(s: str) -> str:
    s2 = re.sub(r"[^a-zA-Z0-9._-]+", "_", s.strip())
    return s2.strip("_") or "tag"


def _run_cmd(*, argv: List[str], env: Dict[str, str]) -> Tuple[int, str]:
    p = subprocess.run(
        argv,
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return int(p.returncode), p.stdout or ""


@dataclass
class StepResult:
    name: str
    ok: bool
    exit_code: int
    out_path: Optional[str]
    note: str


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _parse_smoke_compare(stdout: str) -> Dict[str, Dict[str, str]]:
    """
    解析 smoke 输出末尾的：
    - model=qwen-plus avg_e2e_ms=... json=... val=... fallback=... mixed_preserve=...
    """
    out: Dict[str, Dict[str, str]] = {}
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("- model="):
            continue
        # 示例：
        # - model=qwen-plus avg_e2e_ms=7459.5 json=100.0% val=100.0% fallback=0.0% mixed_preserve=True
        m = re.search(
            r"model=(?P<model>\S+)\s+avg_e2e_ms=(?P<avg>[\d.]+)\s+json=(?P<json>[\d.]+%)\s+val=(?P<val>[\d.]+%)\s+fallback=(?P<fb>[\d.]+%)\s+mixed_preserve=(?P<mixed>\S+)",
            line,
        )
        if not m:
            continue
        out[m.group("model")] = {
            "avg_e2e_ms": m.group("avg"),
            "json": m.group("json"),
            "val": m.group("val"),
            "fallback": m.group("fb"),
            "mixed_preserve": m.group("mixed"),
        }
    return out


def _extract_json_object_from(s: str, start_brace: int) -> Optional[str]:
    """从 start_brace 指向的 '{' 起，做括号平衡截取到匹配的 '}'。"""
    if start_brace < 0 or start_brace >= len(s) or s[start_brace] != "{":
        return None
    depth = 0
    in_str = False
    esc = False
    for i in range(start_brace, len(s)):
        ch = s[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return s[start_brace : i + 1]
    return None


def _parse_contract_summary(stdout: str) -> Dict[str, Dict[str, object]]:
    """
    解析 diagnose_qwen_contract_diff 的输出（best-effort）：
    - 每个 model 段落里抓取：
      - validate_model_structured_output 是否 ok（缺失则为 unknown）
      - 摘要 JSON 内的 top_level_keys（严格 json.loads；失败则 parse_failed，不伪造）
    """
    out: Dict[str, Dict[str, object]] = {}

    header_re = re.compile(r"=+ model=(?P<model>[^ |\n]+)\s+\|")
    lines = stdout.splitlines()
    cur_model: Optional[str] = None
    buf: List[str] = []

    def _flush() -> None:
        nonlocal cur_model, buf
        if not cur_model:
            buf = []
            return
        blob = "\n".join(buf)

        validator_ok: Optional[bool] = None
        validator_status = "unknown"
        for ln in buf:
            if "validate_model_structured_output:" in ln:
                tail = ln.split("validate_model_structured_output:", 1)[-1].strip()
                if tail == "ok":
                    validator_ok = True
                    validator_status = "ok"
                else:
                    validator_ok = False
                    validator_status = "not_ok"
                break

        top_keys: Optional[List[str]] = None
        parse_status = "parse_failed"
        # 摘要 JSON：优先从「摘要:」后的第一个 { 起做括号平衡截取，再 json.loads
        idx = blob.find("摘要:")
        if idx >= 0:
            brace = blob.find("{", idx)
            if brace >= 0:
                jtxt = _extract_json_object_from(blob, brace)
                if jtxt:
                    try:
                        obj = json.loads(jtxt)
                        if isinstance(obj, dict) and isinstance(obj.get("top_level_keys"), list):
                            ks = [str(x) for x in obj.get("top_level_keys") if isinstance(x, str)]
                            top_keys = ks
                            parse_status = "ok"
                        else:
                            parse_status = "parse_failed_top_level_keys_missing"
                    except Exception:
                        parse_status = "parse_failed_json"
                else:
                    parse_status = "parse_failed_no_balanced_json"
            else:
                parse_status = "parse_failed_no_brace_after_summary"
        else:
            parse_status = "parse_failed_no_summary_marker"

        out[cur_model] = {
            "validator_ok": validator_ok,
            "validator_status": validator_status,
            "top_level_keys": top_keys,
            "top_level_keys_parse_status": parse_status,
        }

        cur_model = None
        buf = []

    for ln in lines:
        hm = header_re.search(ln)
        if hm:
            _flush()
            cur_model = hm.group("model").strip()
            buf = [ln]
            continue
        if cur_model is None:
            continue
        buf.append(ln)
    _flush()

    return out


def _read_review_md_table(md_text: str) -> List[Dict[str, str]]:
    """
    解析 review md 中的汇总表（按行分解字段）。
    """
    rows: List[Dict[str, str]] = []
    in_table = False
    for ln in md_text.splitlines():
        if ln.startswith("| model | timeout_ms |"):
            in_table = True
            continue
        if in_table and ln.startswith("|---"):
            continue
        if not in_table:
            continue
        if not ln.strip().startswith("|"):
            break
        parts = [x.strip() for x in ln.strip().strip("|").split("|")]
        if len(parts) < 12:
            continue
        rows.append(
            {
                "model": parts[0],
                "timeout_ms": parts[1],
                "n": parts[2],
                "json_rate": parts[3],
                "val_rate": parts[4],
                "fallback_rate": parts[5],
                "e2e_avg": parts[6],
                "e2e_p95": parts[7],
                "provider_p95": parts[8],
                "tok_in_avg": parts[9],
                "tok_out_avg": parts[10],
                "tok_total_avg": parts[11],
            }
        )
    return rows


def _pick_review_highlights(rows: List[Dict[str, str]], *, model: str) -> Dict[str, str]:
    # 选择 timeout_ms=30000 的行做“边界更紧”的代表；找不到则取第一条
    cand = [r for r in rows if r.get("model") == model]
    if not cand:
        return {}
    tight = next((r for r in cand if r.get("timeout_ms") == "30000"), cand[0])
    return {
        "timeout_ms": tight.get("timeout_ms", ""),
        "e2e_p95": tight.get("e2e_p95", ""),
        "fallback_rate": tight.get("fallback_rate", ""),
        "tok_total_avg": tight.get("tok_total_avg", ""),
        "tok_out_avg": tight.get("tok_out_avg", ""),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="新模型接入流水线固定入口 V1（只串联，不改底层逻辑）")

    ap.add_argument("--model-plus", default="qwen-plus", help="在役/对照 plus 模型名（默认 qwen-plus）")
    ap.add_argument("--model-turbo", default="qwen-turbo", help="（可选）turbo 模型名（当前仅记录，不强绑定）")
    ap.add_argument(
        "--candidate-model",
        default="qwen3.6-plus",
        help="候选模型名（默认 qwen3.6-plus）。日常调试/重复跑批若千问 3.6 配额紧张，请改用其他模型 ID（如 qwen-turbo）验证 pipeline，勿用 3.6 消耗调试额度",
    )

    ap.add_argument("--iters", type=int, default=3, help="review 多轮次数（默认 3；可加大以稳定 P95）")
    ap.add_argument("--timeout-sweep", default="30000,60000,120000", help="review 的 timeout_ms sweep（逗号分隔）")

    ap.add_argument("--tag", default="onboarding_v1", help="产物 tag（用于命名）")
    ap.add_argument("--phase", default="pipeline", help="阶段标识（用于命名）")
    ap.add_argument("--out-dir", default=str(ROOT / "logs"), help="输出目录（默认 repo/logs）")

    ap.add_argument(
        "--role",
        default="评审候选",
        help="接入角色（默认：评审候选；例如：观察池/评审候选/主选候选）",
    )
    args = ap.parse_args()

    model_plus = str(args.model_plus).strip()
    model_turbo = str(args.model_turbo).strip()
    candidate = str(args.candidate_model).strip()
    iters = int(args.iters)
    timeout_sweep = str(args.timeout_sweep).strip()
    tag = _safe_tag(str(args.tag))
    phase = _safe_tag(str(args.phase))

    out_dir = Path(str(args.out_dir)).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    ts = _utc_ts()
    model_tag = _safe_tag(f"{candidate}")

    # 产物命名（V1）
    contract_md = out_dir / f"diagnose_{model_tag}_{tag}_{phase}_{ts}.md"
    smoke_md = out_dir / f"smoke_{model_tag}_{tag}_{phase}_{ts}.md"
    review_md = out_dir / f"review_{model_tag}_{tag}_{phase}_{ts}.md"
    review_json = out_dir / f"review_{model_tag}_{tag}_{phase}_{ts}.json"
    summary_md = out_dir / f"onboarding_{model_tag}_{tag}_{phase}_{ts}.md"

    env = os.environ.copy()
    # 不强制注入 provider/key；由用户环境决定。这里仅确保子进程能找到 repo import
    env.setdefault("PYTHONPATH", str(ROOT))

    steps: List[StepResult] = []

    # Step 1: contract diff
    code, out = _run_cmd(
        argv=[
            sys.executable,
            str(ROOT / "tools" / "diagnose_qwen_contract_diff.py"),
            "--models",
            f"{model_plus},{candidate}",
        ],
        env=env,
    )
    _write_text(contract_md, out)
    steps.append(
        StepResult(
            name="contract_diff",
            ok=(code == 0),
            exit_code=code,
            out_path=str(contract_md),
            note="ok" if code == 0 else "failed (see output)",
        )
    )
    contract_summary = _parse_contract_summary(out)

    # Step 2: baseline smoke
    env2 = env.copy()
    env2["LUNA_SMOKE_QWEN_MODELS"] = f"{model_plus},{candidate}"
    code2, out2 = _run_cmd(
        argv=[sys.executable, str(ROOT / "tools" / "smoke_qwen_long_input_baseline.py")],
        env=env2,
    )
    _write_text(smoke_md, out2)
    steps.append(
        StepResult(
            name="baseline_smoke",
            ok=(code2 == 0),
            exit_code=code2,
            out_path=str(smoke_md),
            note="ok" if code2 == 0 else "failed (see output)",
        )
    )
    smoke_compare = _parse_smoke_compare(out2)

    # Step 3: review perf eval（复用现有脚本：会写出 review_*_UTC.{json,md}）
    # 为了命名规范一致性：先写到 out_dir，然后再复制/重命名到 review_{model_tag}_{tag}_{phase}_{ts}.{md,json}
    code3, out3 = _run_cmd(
        argv=[
            sys.executable,
            str(ROOT / "tools" / "review_qwen3_6_plus_perf_eval_v1.py"),
            "--models",
            f"{model_plus},{candidate}",
            "--iters",
            str(iters),
            "--timeout-sweep",
            timeout_sweep,
            "--out-dir",
            str(out_dir),
        ],
        env=env,
    )
    # review 脚本 stdout 里会打印 wrote: ...json / ...md
    wrote_json = None
    wrote_md = None
    for ln in out3.splitlines():
        ln = ln.strip()
        if ln.startswith("wrote:"):
            p = ln.replace("wrote:", "", 1).strip()
            if p.endswith(".json"):
                wrote_json = p
            if p.endswith(".md"):
                wrote_md = p

    review_note = "ok" if code3 == 0 else "failed (see stdout; partial outputs may exist)"
    steps.append(
        StepResult(
            name="review_perf_eval",
            ok=(code3 == 0),
            exit_code=code3,
            out_path=(wrote_md or wrote_json),
            note=review_note,
        )
    )

    review_rows: List[Dict[str, str]] = []
    if wrote_md and Path(wrote_md).exists():
        md_text = Path(wrote_md).read_text(encoding="utf-8")
        review_rows = _read_review_md_table(md_text)
        # 重命名/拷贝到规范文件名
        Path(wrote_md).replace(review_md)
    else:
        _write_text(review_md, out3)  # fallback：至少保留 stdout

    if wrote_json and Path(wrote_json).exists():
        Path(wrote_json).replace(review_json)
    else:
        # 如果 json 没写出，也不强求；summary 里会标注
        pass

    # 生成 summary（只写骨架，不裁决）
    plus_smoke = smoke_compare.get(model_plus, {})
    cand_smoke = smoke_compare.get(candidate, {})

    plus_review = _pick_review_highlights(review_rows, model=model_plus) if review_rows else {}
    cand_review = _pick_review_highlights(review_rows, model=candidate) if review_rows else {}

    def _fmt_kv(d: Dict[str, str]) -> str:
        if not d:
            return "（未解析到；见产物原文）"
        return ", ".join(f"{k}={v}" for k, v in d.items())

    lines: List[str] = []
    lines.append("## 新模型接入流水线 Summary（V1｜自动生成骨架，不自动拍板）")
    lines.append("")
    lines.append("### 1) 输入参数")
    lines.append(f"- model_plus: `{model_plus}`")
    lines.append(f"- model_turbo: `{model_turbo}`")
    lines.append(f"- candidate_model: `{candidate}`")
    lines.append(f"- role: **{args.role}**")
    lines.append(f"- iters: {iters}")
    lines.append(f"- timeout_sweep: `{timeout_sweep}`")
    lines.append(f"- tag: `{tag}`")
    lines.append(f"- phase: `{phase}`")
    lines.append(f"- utc_ts: `{ts}`")
    lines.append("")

    lines.append("### 2) 产物路径（自动落盘）")
    lines.append(f"- contract diff: `{contract_md}`")
    lines.append(f"- baseline smoke: `{smoke_md}`")
    lines.append(f"- review (md): `{review_md}`")
    lines.append(f"- review (json): `{review_json}`")
    lines.append(f"- onboarding summary: `{summary_md}`")
    lines.append("")

    lines.append("### 3) 步骤状态（失败也要保留已完成产物）")
    for s in steps:
        p = f"`{s.out_path}`" if s.out_path else "（无）"
        lines.append(f"- **{s.name}**: ok={s.ok} exit_code={s.exit_code} out={p} note={s.note}")
    lines.append("")

    lines.append("### 4) 关键数值摘要（best-effort 自动填充）")
    lines.append("")
    lines.append("#### 4.1 contract diff（摘要）")
    if contract_summary:

        def _one_contract_line(*, role: str, model_id: str) -> None:
            info = contract_summary.get(model_id) or {}
            vok = info.get("validator_ok")
            vstat = info.get("validator_status", "unknown")
            ks = info.get("top_level_keys")
            pstat = info.get("top_level_keys_parse_status", "unknown")
            if not info:
                lines.append(
                    f"- **{role}** (`{model_id}`): contract_section=missing（未在 stdout 中解析到该模型段落；见 diagnose 产物原文）"
                )
                return
            if isinstance(ks, list) and pstat == "ok":
                lines.append(
                    f"- **{role}** (`{model_id}`): validator_ok={vok} validator_status={vstat} "
                    f"top_level_keys_count={len(ks)} top_level_keys_parse_status={pstat}"
                )
            else:
                lines.append(
                    f"- **{role}** (`{model_id}`): validator_ok={vok} validator_status={vstat} "
                    f"top_level_keys_count=unknown top_level_keys_parse_status={pstat}"
                )

        _one_contract_line(role="baseline", model_id=model_plus)
        _one_contract_line(role="candidate", model_id=candidate)

        # 额外给一行“keyset 差异”摘要：仅当两侧均成功解析出 keys；否则提示 unknown，避免误报“一致”
        plus_keys = contract_summary.get(model_plus, {}).get("top_level_keys")
        cand_keys = contract_summary.get(candidate, {}).get("top_level_keys")
        pstat_plus = contract_summary.get(model_plus, {}).get("top_level_keys_parse_status")
        pstat_cand = contract_summary.get(candidate, {}).get("top_level_keys_parse_status")
        if isinstance(plus_keys, list) and isinstance(cand_keys, list) and pstat_plus == "ok" and pstat_cand == "ok":
            only_in_cand = sorted(set(cand_keys) - set(plus_keys))
            only_in_plus = sorted(set(plus_keys) - set(cand_keys))
            if only_in_cand or only_in_plus:
                lines.append(
                    f"- keyset_diff: only_in_candidate={only_in_cand[:12]}{'...' if len(only_in_cand) > 12 else ''} "
                    f"only_in_baseline={only_in_plus[:12]}{'...' if len(only_in_plus) > 12 else ''}"
                )
            else:
                lines.append("- keyset_diff: 两者 top_level_keys 集合一致（本次样本；以真实解析结果为准）")
        else:
            lines.append(
                f"- keyset_diff: unknown（无法比较：baseline_parse={pstat_plus} candidate_parse={pstat_cand}）"
            )
    else:
        lines.append("- contract_summary=empty（未解析到任何模型段落；见 contract diff 产物原文）")
    lines.append("")

    lines.append("#### 4.2 baseline smoke（对比汇总）")
    lines.append(f"- `{model_plus}`: {_fmt_kv(plus_smoke)}")
    lines.append(f"- `{candidate}`: {_fmt_kv(cand_smoke)}")
    lines.append("")

    lines.append("#### 4.3 review（P95 / timeout / tokens 代理；以 timeout_ms=30000 行为代表，best-effort）")
    lines.append(f"- `{model_plus}`: {_fmt_kv(plus_review)}")
    lines.append(f"- `{candidate}`: {_fmt_kv(cand_review)}")
    lines.append("")

    lines.append("### 5) 两句话结论骨架（只生成骨架，不自动裁决）")
    lines.append("1. `<candidate_model>` 已完成标准接入流水线最小流程（contract diff / smoke / review），具备进入评审讨论的基础材料。")
    lines.append("2. 基于 smoke 的稳定性与 review 的 P95/超时边界/tokens 代理结果，下一步建议：进入主链评审 / 继续观察 / 暂不建议接入（按本次数据手填）。")
    lines.append("")

    lines.append("### 6) 下一步建议（占位，不自动拍板）")
    lines.append("- 若 smoke 出现非绿：先修契约/解析链路，禁止直接讨论灰度替换。")
    lines.append("- 若 review 显示 P95/timeout 边界风险：先做性能/超时专项，再决定是否进入灰度替换评审。")
    lines.append("- 若 tokens 代理显著上升：补成本评估口径（计费/限额/输出长度）后再进入评审。")
    lines.append("")

    _write_text(summary_md, "\n".join(lines))
    print("wrote:", summary_md)


if __name__ == "__main__":
    main()

