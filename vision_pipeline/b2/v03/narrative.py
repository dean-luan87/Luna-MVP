# vision_pipeline/b2/v03/narrative.py
from __future__ import annotations
from typing import Dict, Any, List, Tuple

from .narrative_templates import TEMPLATES, FACTOR_CN


def _fmt_factor(k: str, v: float) -> str:
    name = FACTOR_CN.get(k, k)
    return f"{name}({v:.2f})"


def _top_k(d: Dict[str, float], k: int = 2) -> List[Tuple[str, float]]:
    return sorted(d.items(), key=lambda x: x[1], reverse=True)[:k]


def _infer_sequence(window_records: List[Dict[str, Any]]) -> str:
    """
    从窗口 records 粗略推断"先后变化顺序"（不做复杂学习，v0.4 先可用）
    规则：找到各因子 confidence 首次超过 0.2 的时间点排序。
    """
    first_hit: Dict[str, float] = {}
    for r in window_records:
        t = r.get("t_video")
        conf = r.get("confidence") or {}
        for k, v in conf.items():
            if v is None:
                continue
            if v >= 0.2 and k not in first_hit:
                first_hit[k] = t
    if not first_hit:
        return "无明显顺序"

    seq = sorted(first_hit.items(), key=lambda x: x[1])
    parts = [FACTOR_CN.get(k, k) for k, _ in seq]
    return " → ".join(parts)


def build_narrative(
    evidence_pack: Dict[str, Any],
    window_detail: Dict[str, Any] | None = None,
    level: str = "M",
) -> str:
    """
    输入：
      - evidence_pack：Step3 的表达级压缩包
      - window_detail：可选，窗口完整 records（用于推断变化顺序）
    输出：自然语言压缩叙述
    """
    decision = evidence_pack.get("decision", "UNKNOWN")
    main = evidence_pack.get("main_factor", "")
    conf = float(evidence_pack.get("confidence", 0.0) or 0.0)

    window = evidence_pack.get("window", {})
    w_str = f"{window.get('start_t')}–{window.get('end_t')}"

    dominant = evidence_pack.get("dominant_factors") or {}
    top = _top_k(dominant, 2)
    dom_str = "、".join([_fmt_factor(k, v) for k, v in top]) if top else "无"

    main_cn = FACTOR_CN.get(main, main) if main else "未知"
    summary = f"我判断为{decision}，主要由{main_cn}驱动，置信度{conf:.2f}"

    seq = "无"
    if window_detail and window_detail.get("records"):
        seq = _infer_sequence(window_detail["records"])

    tpl = TEMPLATES.get(level, TEMPLATES["M"])
    return tpl.format(summary=summary, dominant=dom_str, window=w_str, sequence=seq)

