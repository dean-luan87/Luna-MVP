from __future__ import annotations
import re
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Stats:
    world_sig_total: int = 0
    world_sig_changes: int = 0

    recompute: int = 0
    reused: int = 0

    # NEW
    peek_reuse: int = 0
    peek_miss: int = 0

    advisory_emitted: int = 0
    advisory_suppressed: int = 0

    # NEW
    advisory_peek_suppress: int = 0
    advisory_peek_miss: int = 0

    # intervals
    intervals: List[float] = None  # Step 1-B: 直接存储 interval，而不是 timestamps
    last_emit_ts: Optional[float] = None  # Step 1-B: 上次 emit 的时间戳
    same_tick_emit: int = 0  # Step 1-B: 同 tick 内的 emit 计数

    def __post_init__(self):
        if self.intervals is None:
            self.intervals = []


WORLD_SIG_RE = re.compile(r"\[B2\]\s+world_signature=(\d+)")
FUTURE_REUSED_RE = re.compile(r"\[B2\]\s+future_cache=reused age=([\d\.]+)s")
FUTURE_EXPIRED_RE = re.compile(r"\[B2\]\s+future_cache=expired recompute")
FUTURE_PEEK_REUSE_RE = re.compile(r"\[B2\]\s+future_cache=peek reused age=([\d\.]+)s")
FUTURE_PEEK_MISS_RE = re.compile(r"\[B2\]\s+future_cache=peek miss")

ADVISORY_EMIT_RE = re.compile(r"\[B2-v0\.2\]\[(\d+\.\d+)\]\s+(PREWARN|DEESCALATE|WORLD_NOTE)")
ADVISORY_SUPPRESS_RE = re.compile(r"\[B2\]\s+advisory suppressed")
# 我们把 suppress 默认视为 peek suppress（因为 v0.2 的 suppress 多来自 TIME_ADVANCE/peek）
# 若你未来需要区分，可在日志里打印 trigger


def is_advisory_emit(line: str) -> bool:
    """
    判断是否是真正的 advisory emit（排除 suppress / peek / debug）
    只统计真正输出给 C 的 advisory
    """
    return (
        "[B2-v0.2]" in line
        and ("DEESCALATE" in line or "PREWARN" in line or "WORLD_NOTE" in line)
        and "suppressed" not in line
    )


def analyze(lines: List[str]) -> Stats:
    st = Stats()
    last_sig: Optional[str] = None

    for line in lines:
        m = WORLD_SIG_RE.search(line)
        if m:
            sig = m.group(1)
            st.world_sig_total += 1
            if last_sig is None:
                last_sig = sig
            elif sig != last_sig:
                st.world_sig_changes += 1
                last_sig = sig

        if FUTURE_EXPIRED_RE.search(line):
            st.recompute += 1

        if FUTURE_REUSED_RE.search(line):
            st.reused += 1

        if FUTURE_PEEK_REUSE_RE.search(line):
            st.peek_reuse += 1

        if FUTURE_PEEK_MISS_RE.search(line):
            st.peek_miss += 1

        m = ADVISORY_EMIT_RE.search(line)
        if m:
            st.advisory_emitted += 1
            # Step 1-B: 只统计真正的 advisory emit，不统计 suppress / peek / debug
            if is_advisory_emit(line):
                ts = float(m.group(1))
                # Step 1-B: 修复 interval 统计口径
                # 原则：第一次 emit 只作为时间锚点，不产生 interval
                EPS = 1e-3  # 1 毫秒，足够区分不同 tick
                
                if st.last_emit_ts is None:
                    # 第一次 emit：只记录，不计算 interval
                    st.last_emit_ts = ts
                else:
                    delta = ts - st.last_emit_ts
                    
                    # 同 tick emit：折叠
                    if delta <= EPS:
                        st.same_tick_emit += 1
                    else:
                        # 真正有效的 interval
                        st.intervals.append(delta)
                        st.last_emit_ts = ts

        if ADVISORY_SUPPRESS_RE.search(line):
            st.advisory_suppressed += 1
            st.advisory_peek_suppress += 1

    return st


def interval_stats(intervals: List[float]) -> Dict[str, float]:
    """
    Step 1-B: 直接统计 intervals，不再从 timestamps 差分
    intervals 已经是过滤后的有效间隔列表
    """
    if len(intervals) == 0:
        return {}
    return {
        "min": min(intervals),
        "avg": sum(intervals) / len(intervals),
        "max": max(intervals),
    }


def verdict(st: Stats) -> str:
    # "方向正确"的自动判断标准（你要的 3.5.2）
    # 重点：peek_reuse 和 suppress 必须出现，否则就是没进入"稳定态 peek 复用"
    total_future_ops = st.recompute + st.reused + st.peek_reuse + st.peek_miss
    reuse_ratio = 0.0
    if (st.recompute + st.reused) > 0:
        reuse_ratio = st.reused / max(1, (st.recompute + st.reused))

    cond_peek = st.peek_reuse > 0  # 必须出现
    cond_suppress = st.advisory_suppressed > 0  # 必须出现
    cond_not_over_recompute = st.recompute <= max(1, st.advisory_emitted)  # 不应疯狂重算

    if cond_peek and cond_suppress and cond_not_over_recompute:
        return "✅ 方向正确：已进入 TIME_ADVANCE/peek -> reuse/suppress 运行态"
    return "❌ 方向不对：仍未形成有效 peek 复用或 suppress（请看 peek_reuse / suppressed 是否为 0）"


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 -m vision_pipeline.b2.b2_cache_observer <logfile>")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    st = analyze(lines)
    itv = interval_stats(st.intervals)

    print("======================================================================")
    print("B2 v0.2 缓存逻辑观测报告")
    print("======================================================================\n")

    print("📋 一、WorldSignature 层（世界是否稳定）\n")
    print("① WorldSignature 变化频率")
    print(f"   - 总数: {st.world_sig_total}")
    print(f"   - 变化次数: {st.world_sig_changes}")
    if st.world_sig_total > 0:
        # 粗估：每出现一次 world_signature 日志算一次"签名片段"
        # 精准持续时间需要你在日志里输出 ts，这里保持兼容
        avg = 0.0
        print(f"   - 平均持续时间: (需结合运行时长手算/后续增强)")
    print()

    print("📋 二、FutureCache 层（是否真的在'复用未来'）\n")
    print("② FutureCache 命中率（最重要指标之一）")
    print(f"   - reused 次数: {st.reused}")
    print(f"   - recompute 次数: {st.recompute}")
    total = max(1, st.reused + st.recompute)
    print(f"   - reuse 比例: {st.reused/total*100:.1f}%\n")

    print("② FutureCache Peek 命中率（新增）")
    print(f"   - peek_reuse: {st.peek_reuse}")
    print(f"   - peek_miss: {st.peek_miss}\n")

    print("📋 三、AdvisoryCache 层（是否'克制地说话'）\n")
    print("④ Advisory 输出总次数")
    print(f"   - emitted: {st.advisory_emitted}")
    print(f"   - suppressed: {st.advisory_suppressed}")
    print(f"   - total: {st.advisory_emitted + st.advisory_suppressed}\n")

    print("⑤ Advisory Peek Suppress（新增）")
    print(f"   - peek_suppress: {st.advisory_peek_suppress}")
    print(f"   - peek_miss: {st.advisory_peek_miss}\n")

    print("📋 四、时间结构层（B2 的'节奏感'）\n")
    print("⑥ B2 输出间隔分布")
    if itv:
        print(f"   - min: {itv['min']:.2f}s")
        print(f"   - avg: {itv['avg']:.2f}s")
        print(f"   - max: {itv['max']:.2f}s")
        if st.same_tick_emit > 0:
            print(f"   - 同 tick emit 被折叠: {st.same_tick_emit} 次\n")
        else:
            print()
    else:
        print("   - (输出不足，无法统计)\n")

    print("======================================================================")
    print("六、综合判断标准")
    print("======================================================================\n")
    print("1️⃣ B2 是否明显减少了'未来推演次数'？")
    if st.reused + st.peek_reuse > 0:
        print("   ✅ YES - 出现复用/peek 复用")
    else:
        print("   ❌ NO - 未出现复用/peek 复用")

    print("\n3️⃣ 在场景变化时是否能果断重算？")
    if st.recompute > 0:
        print("   ✅ YES - 有 recompute")
    else:
        print("   ⚠️  可能没有触发重算（需结合场景）")

    print("\n4️⃣ 是否完全没有干扰 C？")
    print("   ⚠️  需要手动检查 C 的决策间隔和 decision 数（B2 旁路不应影响 C）\n")

    print("🎯 方向判断：")
    print(f"   {verdict(st)}")


if __name__ == "__main__":
    main()
