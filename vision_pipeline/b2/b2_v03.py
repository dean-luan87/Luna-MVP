# vision_pipeline/b2/b2_v03.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import time
import hashlib
import math


# ----------------------------
# Data contracts (B2 -> C)
# ----------------------------

@dataclass
class WorldTransition:
    prev_signature: int
    curr_signature: int
    reason: str  # e.g. "SIGNATURE_CHANGE"


@dataclass
class ImpactEvent:
    event_type: str            # e.g. "CROWD", "CROSSWALK", "LOW_LIGHT"
    severity: int              # 1-5
    eta_sec: float             # estimated time-to-contact within horizon
    summary: str               # short human-readable summary
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class B2AdvisoryBundle:
    ts: float
    world_signature: int
    future_horizon_sec: float
    trigger_reason: str        # INIT/TIME_ADVANCE/WORLD_CHANGE/EVENT_SPIKE
    confidence: float
    world_transition: Optional[WorldTransition] = None
    events: List[ImpactEvent] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


# ----------------------------
# Internal cache entries
# ----------------------------

@dataclass
class _FutureCacheEntry:
    ts: float
    signature: int
    horizon_sec: float
    future_window: Dict[str, Any]  # store whatever you need
    events: List[ImpactEvent]
    confidence: float


@dataclass
class _AdvisoryCacheEntry:
    ts: float
    signature: int
    advisory_key: str  # e.g. "WORLD_NOTE|sig=xxx|events=N"
    bundle: B2AdvisoryBundle


class B2V03:
    """
    B2 v0.3 (8s horizon): God-view future window advisor.
    - Does NOT control C.
    - Emits sparse advisory bundles with cache reuse & suppression.
    """

    # -------- default parameters (8s profile)
    FUTURE_HORIZON_SEC = 8.0

    PEEK_INTERVAL_SEC = 2.0
    EMIT_MIN_INTERVAL_SEC = 8.0
    EMIT_MAX_STALENESS_SEC = 12.0

    FUTURE_CACHE_TTL_SEC = 10.0
    ADVISORY_TTL_SEC = 10.0

    SIGNATURE_GRID = 32
    SIGNATURE_OBJ_TOPK = 6
    SIGNATURE_TEXT_TOPK = 3

    TICK_EPS_SEC = 0.03  # 30ms considered same tick

    def __init__(self, debug: bool = False):
        self.debug = debug

        # ⚠️ 硬保护：v0.3 不允许调用 v0.2 observer
        # 彻底切断 v0.3 路径对 v0.2 observer 的任何调用
        self.observer = None

        # signature tracking
        self._last_signature: Optional[int] = None
        self._last_signature_ts: Optional[float] = None

        # decision throttles
        self._has_initialized: bool = False
        self._last_peek_ts: float = 0.0
        self._last_emit_ts: float = 0.0

        # tick-level emit lock
        self._last_tick_ts: float = 0.0
        self._emitted_in_tick: bool = False

        # caches
        self._future_cache: Optional[_FutureCacheEntry] = None
        self._advisory_cache: Optional[_AdvisoryCacheEntry] = None

    # ----------------------------
    # Public entry
    # ----------------------------
    def tick(
        self,
        frame_ts: float,
        objects: List[Dict[str, Any]],
        texts: List[str],
        nav_result: Optional[Any],
        modeling_result: Optional[Any],
        c1_state: Optional[Any],
    ) -> Optional[B2AdvisoryBundle]:
        # ✅ 3️⃣ v0.3 日志前缀要能一眼识别
        if self.debug:
            print(f"[B2-v0.3] tick frame_ts={frame_ts:.2f}")

        now = frame_ts if frame_ts else time.time()

        # tick lock reset
        if (now - self._last_tick_ts) > self.TICK_EPS_SEC:
            self._last_tick_ts = now
            self._emitted_in_tick = False

        # INIT: only once
        if not self._has_initialized:
            self._has_initialized = True
            sig = self._compute_world_signature(objects, texts, nav_result, modeling_result, c1_state)
            self._update_signature(sig, now)
            bundle = self._emit_or_suppress(
                now=now,
                signature=sig,
                trigger_reason="INIT",
                world_transition=None,
                objects=objects,
                texts=texts,
                nav_result=nav_result,
                modeling_result=modeling_result,
                c1_state=c1_state,
                force_emit=True
            )
            return bundle

        # signature
        sig = self._compute_world_signature(objects, texts, nav_result, modeling_result, c1_state)
        world_transition = None
        if self._last_signature is not None and sig != self._last_signature:
            world_transition = WorldTransition(
                prev_signature=self._last_signature,
                curr_signature=sig,
                reason="SIGNATURE_CHANGE"
            )
        self._update_signature(sig, now)

        # gating: peek interval
        if (now - self._last_peek_ts) < self.PEEK_INTERVAL_SEC:
            return None
        self._last_peek_ts = now

        # Step A: peek future cache
        future_entry, cache_status = self._get_or_recompute_future(sig, now, objects, texts, nav_result, modeling_result, c1_state)

        # Step B: decide if we should emit
        should_emit, reason = self._should_emit(now, sig, world_transition, future_entry)

        if not should_emit:
            if self.debug:
                print(f"[B2-v0.3] suppress reason={reason} sig={sig}")
            return None

        bundle = self._emit_or_suppress(
            now=now,
            signature=sig,
            trigger_reason=reason,
            world_transition=world_transition,
            objects=objects,
            texts=texts,
            nav_result=nav_result,
            modeling_result=modeling_result,
            c1_state=c1_state,
            force_emit=False,
            future_entry=future_entry,
            cache_status=cache_status
        )
        return bundle

    # ----------------------------
    # Signature / state
    # ----------------------------
    def _update_signature(self, sig: int, now: float) -> None:
        if self._last_signature != sig:
            self._last_signature = sig
            self._last_signature_ts = now

    def _compute_world_signature(
        self,
        objects: List[Dict[str, Any]],
        texts: List[str],
        nav_result: Optional[Any],
        modeling_result: Optional[Any],
        c1_state: Optional[Any],
    ) -> int:
        """
        Coarse signature to be stable across jitter:
        - objects: topK class names + coarse bbox grid bins
        - texts: topK hashed OCR snippets
        - nav/modeling flags only
        """
        parts: List[str] = []

        nav_active = "1" if getattr(nav_result, "is_active", False) else "0"
        modeling_active = "1" if getattr(modeling_result, "did_run", False) else "0"
        parts.append(f"nav={nav_active}")
        parts.append(f"model={modeling_active}")

        # objects
        obj_feats: List[Tuple[str, int, int]] = []
        for o in objects or []:
            cls = str(o.get("label") or o.get("class") or o.get("name") or "obj")
            bbox = o.get("bbox") or o.get("box") or None  # expected [x1,y1,x2,y2] or dict
            cx, cy = 0, 0
            if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
                x1, y1, x2, y2 = bbox[:4]
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)
            gx = int(cx / self.SIGNATURE_GRID)
            gy = int(cy / self.SIGNATURE_GRID)
            obj_feats.append((cls, gx, gy))

        obj_feats.sort(key=lambda x: (x[0], x[1], x[2]))
        obj_feats = obj_feats[: self.SIGNATURE_OBJ_TOPK]
        for cls, gx, gy in obj_feats:
            parts.append(f"o:{cls}@{gx},{gy}")

        # texts
        t = [s.strip() for s in (texts or []) if s and s.strip()]
        t = t[: self.SIGNATURE_TEXT_TOPK]
        for s in t:
            h = hashlib.md5(s.encode("utf-8")).hexdigest()[:6]
            parts.append(f"t:{h}")

        raw = "|".join(parts)
        return int(hashlib.md5(raw.encode("utf-8")).hexdigest()[:8], 16)

    # ----------------------------
    # Future cache
    # ----------------------------
    def _get_or_recompute_future(
        self,
        sig: int,
        now: float,
        objects: List[Dict[str, Any]],
        texts: List[str],
        nav_result: Optional[Any],
        modeling_result: Optional[Any],
        c1_state: Optional[Any],
    ) -> Tuple[_FutureCacheEntry, str]:
        """
        Return a future cache entry. If valid cache exists, reuse; else recompute.
        """
        # reuse if same signature and TTL valid
        if self._future_cache and self._future_cache.signature == sig:
            age = now - self._future_cache.ts
            if age <= self.FUTURE_CACHE_TTL_SEC:
                if self.debug:
                    print(f"[B2-v0.3] future_cache=peek_reuse age={age:.2f}s sig={sig}")
                return self._future_cache, "PEEK_REUSE"

        # recompute
        entry = self._compute_future_window(sig, now, objects, texts, nav_result, modeling_result, c1_state)
        self._future_cache = entry
        if self.debug:
            print(f"[B2-v0.3] future_cache=recompute sig={sig}")
        return entry, "RECOMPUTE"

    def _compute_future_window(
        self,
        sig: int,
        now: float,
        objects: List[Dict[str, Any]],
        texts: List[str],
        nav_result: Optional[Any],
        modeling_result: Optional[Any],
        c1_state: Optional[Any],
    ) -> _FutureCacheEntry:
        """
        Placeholder future simulation:
        - v0.3 baseline: cheap heuristics, no heavy model.
        - You will replace this later with real preplay.
        """
        events: List[ImpactEvent] = []

        # Example cheap heuristics (keep conservative)
        # 1) low light from modeling_result/c1_state (if any field exists)
        light = getattr(modeling_result, "light_level", None)
        if isinstance(light, (int, float)) and light < 0.3:
            events.append(ImpactEvent(
                event_type="LOW_LIGHT",
                severity=2,
                eta_sec=2.0,
                summary="光线偏暗，注意脚下与前方障碍",
            ))

        # 2) crosswalk / traffic light from texts (OCR)
        joined = " ".join(texts or []).lower()
        if "exit" in joined or "出口" in joined:
            events.append(ImpactEvent(
                event_type="TRANSIT_EXIT",
                severity=2,
                eta_sec=4.0,
                summary="疑似地铁/出口区域，注意人流与台阶",
            ))

        # confidence: conservative baseline
        confidence = 0.30 if len(events) == 0 else 0.45

        future_window = {
            "signature": sig,
            "horizon_sec": self.FUTURE_HORIZON_SEC,
            "events_count": len(events),
        }

        return _FutureCacheEntry(
            ts=now,
            signature=sig,
            horizon_sec=self.FUTURE_HORIZON_SEC,
            future_window=future_window,
            events=events,
            confidence=confidence
        )

    # ----------------------------
    # Emit / Suppress policy
    # ----------------------------
    def _should_emit(
        self,
        now: float,
        sig: int,
        world_transition: Optional[WorldTransition],
        future_entry: _FutureCacheEntry
    ) -> Tuple[bool, str]:
        # hard tick lock
        if self._emitted_in_tick:
            return False, "TICK_LOCK"

        # world transition has higher priority (but still respect emit min interval loosely)
        if world_transition is not None:
            # allow faster emit on transition, but avoid spam within 2s
            if (now - self._last_emit_ts) >= 2.0:
                return True, "WORLD_CHANGE"
            return False, "WORLD_CHANGE_THROTTLED"

        # event spike (placeholder: any events severity>=4)
        if any(e.severity >= 4 for e in future_entry.events):
            if (now - self._last_emit_ts) >= 2.0:
                return True, "EVENT_SPIKE"
            return False, "EVENT_SPIKE_THROTTLED"

        # time advance: sparse emit
        since_emit = now - self._last_emit_ts
        if since_emit >= self.EMIT_MIN_INTERVAL_SEC:
            return True, "TIME_ADVANCE"
        if since_emit >= self.EMIT_MAX_STALENESS_SEC:
            return True, "TIME_ADVANCE_STALE"

        return False, "MIN_INTERVAL"

    def _emit_or_suppress(
        self,
        now: float,
        signature: int,
        trigger_reason: str,
        world_transition: Optional[WorldTransition],
        objects: List[Dict[str, Any]],
        texts: List[str],
        nav_result: Optional[Any],
        modeling_result: Optional[Any],
        c1_state: Optional[Any],
        force_emit: bool,
        future_entry: Optional[_FutureCacheEntry] = None,
        cache_status: Optional[str] = None
    ) -> Optional[B2AdvisoryBundle]:
        # tick lock
        if self._emitted_in_tick and not force_emit:
            return None

        # build bundle using future_entry (compute if missing)
        if future_entry is None:
            future_entry = self._compute_future_window(signature, now, objects, texts, nav_result, modeling_result, c1_state)
            cache_status = "RECOMPUTE"

        bundle = B2AdvisoryBundle(
            ts=now,
            world_signature=signature,
            future_horizon_sec=self.FUTURE_HORIZON_SEC,
            trigger_reason=trigger_reason,
            confidence=future_entry.confidence,
            world_transition=world_transition,
            events=future_entry.events,
            notes=self._compose_notes(future_entry.events, world_transition)
        )

        advisory_key = self._advisory_key(bundle)

        # suppression by advisory cache
        if not force_emit and self._advisory_cache and self._advisory_cache.advisory_key == advisory_key:
            age = now - self._advisory_cache.ts
            if age <= self.ADVISORY_TTL_SEC:
                if self.debug:
                    print(f"[B2-v0.3] advisory_suppress age={age:.2f}s key={advisory_key}")
                return None

        # emit
        self._last_emit_ts = now
        self._emitted_in_tick = True
        self._advisory_cache = _AdvisoryCacheEntry(
            ts=now,
            signature=signature,
            advisory_key=advisory_key,
            bundle=bundle
        )

        if self.debug:
            evn = len(bundle.events)
            wt = "Y" if bundle.world_transition else "N"
            print(f"[B2-v0.3] emit reason={trigger_reason} sig={signature} cache={cache_status} transition={wt} events={evn}")

        return bundle

    def _compose_notes(self, events: List[ImpactEvent], world_transition: Optional[WorldTransition]) -> List[str]:
        notes: List[str] = []
        if world_transition is not None:
            notes.append("大环境变化：注意重新确认方向与行进空间。")
        # top-2 events
        for e in (events or [])[:2]:
            notes.append(e.summary)
        if not notes:
            notes.append("环境稳定：可降低警戒，保持匀速前进。")
        return notes

    def _advisory_key(self, bundle: B2AdvisoryBundle) -> str:
        # stable key for suppression
        etypes = ",".join([e.event_type for e in bundle.events[:3]])
        transition = "1" if bundle.world_transition else "0"
        return f"{transition}|{etypes}|h={int(bundle.future_horizon_sec)}|sig={bundle.world_signature}"

