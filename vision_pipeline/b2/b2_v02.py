from __future__ import annotations

import time
import hashlib
import zlib
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


# -----------------------------
# Enums / Data Structures
# -----------------------------

class TriggerReason(str, Enum):
    INIT = "INIT"
    WORLD_CHANGE = "WORLD_CHANGE"
    TTL_EXPIRE = "TTL_EXPIRE"
    TIME_ADVANCE = "TIME_ADVANCE"   # NEW: 世界没变，但时间在走 → peek 未来


class AdvisoryType(str, Enum):
    PREWARN = "PREWARN"
    DEESCALATE = "DEESCALATE"
    WORLD_NOTE = "WORLD_NOTE"


@dataclass
class ImpactEvent:
    kind: str
    severity: float = 0.0
    t_plus_sec: float = 0.0
    meta: Dict[str, Any] = None


@dataclass
class Advisory:
    advisory_type: AdvisoryType
    confidence: float
    trigger: TriggerReason
    impacts: List[ImpactEvent]
    message: str = ""


@dataclass
class FutureSnapshot:
    # 你现阶段无需理解世界，只做"未来剧本缓存"
    world_signature: str
    created_ts: float
    horizon_sec: float
    # 这里先留空/轻量字段，后续你可以把预演轨迹、占用区域等填进来
    payload: Dict[str, Any]


# -----------------------------
# Future Cache
# -----------------------------

class FutureCache:
    """
    v0.2 核心：支持 peek（不 recompute），并可复用 future snapshot。
    """
    def __init__(self, ttl_sec: float = 10.0):
        self.ttl_sec = float(ttl_sec)
        self._snapshot: Optional[FutureSnapshot] = None

        # metrics
        self.reused = 0
        self.recompute = 0

        # NEW metrics
        self.peek_reuse = 0
        self.peek_miss = 0

    def _age(self, now_ts: float) -> float:
        if not self._snapshot:
            return 0.0
        return max(0.0, now_ts - self._snapshot.created_ts)

    def is_valid(self, now_ts: float, world_signature: str) -> bool:
        if not self._snapshot:
            return False
        if self._snapshot.world_signature != world_signature:
            return False
        return self._age(now_ts) <= self.ttl_sec

    def get_or_recompute(
        self,
        now_ts: float,
        world_signature: str,
        recompute_fn,
        *args, **kwargs
    ) -> Tuple[FutureSnapshot, bool]:
        """
        返回 (snapshot, reused_flag)
        """
        if self.is_valid(now_ts, world_signature):
            self.reused += 1
            return self._snapshot, True

        # expired / miss → recompute
        self.recompute += 1
        snapshot = recompute_fn(now_ts, world_signature, *args, **kwargs)
        self._snapshot = snapshot
        return snapshot, False

    def peek(self, now_ts: float, world_signature: str) -> Tuple[Optional[FutureSnapshot], bool]:
        """
        轻量检查：不触发 recompute，只返回是否可复用。
        """
        if self.is_valid(now_ts, world_signature):
            self.peek_reuse += 1
            return self._snapshot, True
        self.peek_miss += 1
        return None, False

    def force_set(self, snapshot: FutureSnapshot) -> None:
        self._snapshot = snapshot

    def debug_state(self, now_ts: float) -> Dict[str, Any]:
        return {
            "ttl_sec": self.ttl_sec,
            "has_snapshot": self._snapshot is not None,
            "age": self._age(now_ts) if self._snapshot else None,
            "world_signature": self._snapshot.world_signature if self._snapshot else None,
            "created_ts": self._snapshot.created_ts if self._snapshot else None,
            "reused": self.reused,
            "recompute": self.recompute,
            "peek_reuse": self.peek_reuse,
            "peek_miss": self.peek_miss,
        }


# -----------------------------
# Advisory Cache
# -----------------------------

class AdvisoryCache:
    """
    "克制说话"缓存：相同 advisory 在 TTL 内 suppress。
    """
    def __init__(self, ttl_sec: float = 12.0):
        self.ttl_sec = float(ttl_sec)
        self._last_key: Optional[str] = None
        self._last_emit_ts: Optional[float] = None

        # metrics
        self.emitted = 0
        self.suppressed = 0

        # NEW peek metrics（给 observer）
        self.peek_suppress = 0
        self.peek_miss = 0

    def _hash_advisory(self, advisory: Advisory) -> str:
        # 只用"语义关键字段"做去重
        base = {
            "type": advisory.advisory_type.value,
            "trigger": advisory.trigger.value,
            "impacts_n": len(advisory.impacts),
            "msg": advisory.message[:64] if advisory.message else "",
        }
        s = str(base).encode("utf-8")
        return hashlib.md5(s).hexdigest()

    def _age(self, now_ts: float) -> float:
        if self._last_emit_ts is None:
            return 1e9
        return max(0.0, now_ts - self._last_emit_ts)

    def should_emit(self, now_ts: float, advisory: Advisory) -> Tuple[bool, str]:
        """
        返回 (should_emit, reason)
        """
        key = self._hash_advisory(advisory)
        if self._last_key is None:
            return True, "first_emit"

        age = self._age(now_ts)
        if key == self._last_key and age < self.ttl_sec:
            return False, f"same_as_last age={age:.1f}s < ttl={self.ttl_sec:.1f}s"

        return True, f"changed_or_ttl age={age:.1f}s"

    def record_emit(self, now_ts: float, advisory: Advisory) -> None:
        self._last_key = self._hash_advisory(advisory)
        self._last_emit_ts = now_ts
        self.emitted += 1

    def record_suppress(self) -> None:
        self.suppressed += 1

    def record_peek_suppress(self) -> None:
        self.peek_suppress += 1

    def record_peek_miss(self) -> None:
        self.peek_miss += 1


# -----------------------------
# Future Simulator (lightweight placeholder)
# -----------------------------

class FutureSimulator:
    """
    v0.2：不做复杂理解，仅提供"未来剧本"结构。
    后续你要接任务链预演、路线重叠判定、碰撞预警，在这里扩展。
    """
    def __init__(self, horizon_sec: float = 8.0):
        self.horizon_sec = float(horizon_sec)

    def simulate(
        self,
        now_ts: float,
        world_signature: str,
        objects: Optional[List[Dict[str, Any]]] = None,
        texts: Optional[List[Dict[str, Any]]] = None,
        navigation_result: Any = None,
        modeling_result: Any = None,
    ) -> FutureSnapshot:
        payload: Dict[str, Any] = {
            "objects_n": len(objects) if objects else 0,
            "texts_n": len(texts) if texts else 0,
            # 你可以把 nav path、ego direction 等塞进来
            "nav_present": navigation_result is not None,
            "modeling_present": modeling_result is not None,
        }
        return FutureSnapshot(
            world_signature=world_signature,
            created_ts=now_ts,
            horizon_sec=self.horizon_sec,
            payload=payload,
        )


# -----------------------------
# B2 v0.2 Main
# -----------------------------

class B2V02:
    """
    你现有 PipelineController 里已经在调用 tick()。
    这里用 **kwargs 兼容你的现有调用参数，避免签名不匹配。
    """

    def __init__(
        self,
        future_ttl_sec: float = 10.0,
        advisory_ttl_sec: float = 12.0,
        peek_interval_sec: float = 2.0,   # NEW: WORLD_STABLE 时周期性 peek
        min_interval_sec: float = 0.0,    # 如果你需要节流，保留
        horizon_sec: float = 8.0,
        debug_tick_log: bool = False,
    ):
        self.future_cache = FutureCache(ttl_sec=future_ttl_sec)
        self.advisory_cache = AdvisoryCache(ttl_sec=advisory_ttl_sec)
        self.simulator = FutureSimulator(horizon_sec=horizon_sec)

        self.peek_interval_sec = float(peek_interval_sec)
        self.min_interval_sec = float(min_interval_sec)
        self.debug_tick_log = bool(debug_tick_log)

        self._inited = False
        self._has_initialized = False  # Step 1: INIT 阶段强制只输出一次
        self._last_world_signature: Optional[str] = None
        self._last_tick_ts: Optional[float] = None
        self._last_peek_ts: Optional[float] = None
        
        # Step 1: tick 内单次决策锁
        self._last_decision_tick_ts: Optional[float] = None
        self._decision_emitted_in_tick: bool = False

    # ---------- world signature helper ----------
    def compute_world_signature(self, objects: Optional[List[Dict[str, Any]]], texts: Optional[List[Dict[str, Any]]]) -> str:
        """
        你现阶段的 signature 只要"粗粒度稳定"，不能对抖动敏感。
        这里采用数量 + 前K类目的组合，避免 frame-level 抖动导致 signature 乱跳。
        """
        obj_n = len(objects) if objects else 0
        txt_n = len(texts) if texts else 0

        # 取前几个 kind/category/class 做粗粒度
        kinds: List[str] = []
        if objects:
            for o in objects[:8]:
                k = (o.get("label") or o.get("class") or o.get("kind") or "obj").strip()
                kinds.append(k)
        if texts:
            for t in texts[:4]:
                k = (t.get("text") or t.get("label") or "txt").strip()
                kinds.append(k)

        base = f"n{obj_n}_t{txt_n}_" + "_".join(kinds)
        return str(zlib.crc32(base.encode("utf-8")) & 0xFFFFFFFF)

    # ---------- main tick ----------
    def tick(self, now_ts: Optional[float] = None, **kwargs) -> Optional[Dict[str, Any]]:
        """
        kwargs 兼容输入：
        - objects, texts
        - navigation_result, modeling_result
        - world_signature（若上游算好了）
        """
        now_ts = float(now_ts if now_ts is not None else time.time())

        # Step 1: tick 起点，重置 tick 状态
        if self._last_decision_tick_ts != now_ts:
            self._last_decision_tick_ts = now_ts
            self._decision_emitted_in_tick = False

        if self._last_tick_ts is not None and self.min_interval_sec > 0:
            if (now_ts - self._last_tick_ts) < self.min_interval_sec:
                if self.debug_tick_log:
                    print(f"[B2-SKIP] min_interval 未到: age={(now_ts-self._last_tick_ts):.3f}s < {self.min_interval_sec}s")
                return None

        self._last_tick_ts = now_ts

        objects = kwargs.get("objects")
        texts = kwargs.get("texts")
        navigation_result = kwargs.get("navigation_result", None)
        modeling_result = kwargs.get("modeling_result", None)

        world_signature = kwargs.get("world_signature")
        if not world_signature:
            # 如果上游没提供，就用 B2 自己的粗粒度 signature
            world_signature = self.compute_world_signature(objects, texts)

        # 打印 world signature（observer 用）
        # Step 1: 只在 state change 时打印
        if self._last_world_signature != world_signature:
            print(f"[B2] world_signature={world_signature}")

        # trigger 判定
        if not self._inited:
            trigger = TriggerReason.INIT
            # Step 1: INIT 阶段强制只输出一次
            if self._has_initialized:
                return None
            self._has_initialized = True
        elif self._last_world_signature != world_signature:
            trigger = TriggerReason.WORLD_CHANGE
        else:
            # 世界稳定：看 future cache 是否过期，或时间推进 peek
            if not self.future_cache.is_valid(now_ts, world_signature):
                trigger = TriggerReason.TTL_EXPIRE
            else:
                # NEW: TIME_ADVANCE peek
                if self._last_peek_ts is None or (now_ts - self._last_peek_ts) >= self.peek_interval_sec:
                    trigger = TriggerReason.TIME_ADVANCE
                else:
                    # 无事发生：不输出、不打扰
                    return None

        self._inited = True
        self._last_world_signature = world_signature

        # 路径 A：TIME_ADVANCE（peek-only，不 recompute）
        if trigger == TriggerReason.TIME_ADVANCE:
            # Step 1: 同 tick 直接短路
            if self._decision_emitted_in_tick:
                return None
            
            self._last_peek_ts = now_ts

            snap, ok = self.future_cache.peek(now_ts, world_signature)
            if ok and snap is not None:
                age = now_ts - snap.created_ts
                print(f"[B2] future_cache=peek reused age={age:.1f}s")
                # advisory 也走"克制"：通常稳定场景都是 DEESCALATE 或 WORLD_NOTE
                advisory = self._build_advisory(trigger, snap, impacts=[])
                should_emit, reason = self.advisory_cache.should_emit(now_ts, advisory)
                if not should_emit:
                    self.advisory_cache.record_suppress()
                    self.advisory_cache.record_peek_suppress()
                    print(f"[B2] advisory suppressed ({reason})")
                    return None
                
                # Step 1: tick 内单次决策锁
                if self._decision_emitted_in_tick:
                    return None
                self._decision_emitted_in_tick = True
                
                self.advisory_cache.record_emit(now_ts, advisory)
                self._print_advisory(now_ts, advisory)
                return self._pack_output(now_ts, world_signature, trigger, advisory, snap, reused=True)

            # peek miss：不 recompute（这是关键）
            print("[B2] future_cache=peek miss")
            self.advisory_cache.record_peek_miss()
            return None

        # 路径 B：INIT / WORLD_CHANGE / TTL_EXPIRE（允许 recompute）
        # Step 1: 同 tick 直接短路
        if self._decision_emitted_in_tick:
            return None
        
        # 这里才会触发真正 simulate
        if trigger == TriggerReason.TTL_EXPIRE:
            print("[B2] future_cache=expired recompute")

        snap, reused = self.future_cache.get_or_recompute(
            now_ts,
            world_signature,
            self._recompute_future,
            objects=objects,
            texts=texts,
            navigation_result=navigation_result,
            modeling_result=modeling_result,
        )
        if reused:
            age = now_ts - snap.created_ts
            print(f"[B2] future_cache=reused age={age:.1f}s")

        impacts = self._extract_impacts(snap, objects, texts, navigation_result, modeling_result)
        advisory = self._build_advisory(trigger, snap, impacts=impacts)

        should_emit, reason = self.advisory_cache.should_emit(now_ts, advisory)
        if not should_emit:
            self.advisory_cache.record_suppress()
            print(f"[B2] advisory suppressed ({reason})")
            return None

        # Step 1: tick 内单次决策锁
        if self._decision_emitted_in_tick:
            return None
        self._decision_emitted_in_tick = True

        self.advisory_cache.record_emit(now_ts, advisory)
        self._print_advisory(now_ts, advisory)

        return self._pack_output(now_ts, world_signature, trigger, advisory, snap, reused=reused)

    # ---------- internals ----------
    def _recompute_future(self, now_ts: float, world_signature: str, **kwargs) -> FutureSnapshot:
        return self.simulator.simulate(
            now_ts=now_ts,
            world_signature=world_signature,
            objects=kwargs.get("objects"),
            texts=kwargs.get("texts"),
            navigation_result=kwargs.get("navigation_result"),
            modeling_result=kwargs.get("modeling_result"),
        )

    def _extract_impacts(
        self,
        snap: FutureSnapshot,
        objects: Optional[List[Dict[str, Any]]],
        texts: Optional[List[Dict[str, Any]]],
        navigation_result: Any,
        modeling_result: Any,
    ) -> List[ImpactEvent]:
        """
        v0.2 先空实现：你的预期是"B2 不深度理解"，所以这里可以先不产出 impacts。
        后续接任务链预演/路线重叠后再产出 PREWARN。
        """
        return []

    def _build_advisory(self, trigger: TriggerReason, snap: FutureSnapshot, impacts: List[ImpactEvent]) -> Advisory:
        # 目前 impacts 为空 → 统一 DEESCALATE，未来有 impacts 再 PREWARN
        if impacts:
            adv_type = AdvisoryType.PREWARN
            conf = 0.75
            msg = "Potential impact ahead (simulated)."
        else:
            adv_type = AdvisoryType.DEESCALATE
            conf = 0.30
            msg = "Environment appears stable; keep calm."

        return Advisory(
            advisory_type=adv_type,
            confidence=conf,
            trigger=trigger,
            impacts=impacts,
            message=msg,
        )

    def _print_advisory(self, now_ts: float, advisory: Advisory) -> None:
        # 保持你现有日志格式
        print(
            f"[B2-v0.2][{now_ts:.2f}] {advisory.advisory_type.value} | "
            f"trigger={advisory.trigger.value} | confidence={advisory.confidence:.2f} | impacts={len(advisory.impacts)}"
        )

    def _pack_output(
        self,
        now_ts: float,
        world_signature: str,
        trigger: TriggerReason,
        advisory: Advisory,
        snap: FutureSnapshot,
        reused: bool,
    ) -> Dict[str, Any]:
        return {
            "ts": now_ts,
            "world_signature": world_signature,
            "trigger": trigger.value,
            "advisory": {
                "type": advisory.advisory_type.value,
                "confidence": advisory.confidence,
                "message": advisory.message,
                "impacts": [asdict(x) for x in advisory.impacts],
            },
            "future": {
                "created_ts": snap.created_ts,
                "horizon_sec": snap.horizon_sec,
                "payload": snap.payload,
                "reused": bool(reused),
            },
            "metrics": {
                "future_cache": self.future_cache.debug_state(now_ts),
                "advisory_emitted": self.advisory_cache.emitted,
                "advisory_suppressed": self.advisory_cache.suppressed,
                "peek_suppress": self.advisory_cache.peek_suppress,
                "peek_miss": self.advisory_cache.peek_miss,
            },
        }
