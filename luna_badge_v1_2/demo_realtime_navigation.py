from core.logging import get_logger

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
log = get_logger("demo_realtime_navigation")
"""
Luna Badge v1.3.1
真实链路 Demo + 性能监控 + 压测模式

模式：
- interactive：实时导航 + 控制台输出（默认）
- stress      ：压测模式，持续跑 N 秒 / N 帧，记录热衰减

输出：
- perf_logs/realtime_perf_samples.csv     每帧性能采样
- perf_logs/realtime_perf_report.json     全局统计
"""

import time
import os
import json
import csv
import signal
import argparse
import sys

import cv2

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ============================
# 尝试导入内部模块
# ============================

# 摄像头模块
try:
    from utils.camera_handler import CameraHandler
    HAS_CAMERA_HANDLER = True
except ImportError:
    HAS_CAMERA_HANDLER = False

# YOLO 检测器
try:
    from core.yolo_detector import YoloDetector
    HAS_YOLO_DETECTOR = True
except ImportError:
    HAS_YOLO_DETECTOR = False

# 导航逻辑
try:
    from core.navigation_logic_v1_3 import NavigationLogicV1_3
    HAS_NAV_LOGIC = True
except ImportError:
    try:
        from core.navigation_logic import NavigationLogic
        HAS_NAV_LOGIC = True
        NavigationLogicV1_3 = NavigationLogic
    except ImportError:
        HAS_NAV_LOGIC = False

# TTS 模块
try:
    from core.tts_manager import TTSManager
    HAS_TTS_MANAGER = True
except ImportError:
    HAS_TTS_MANAGER = False

# ============================
# YOLO11-tiny fallback
# ============================

YOLO_MODEL_PATH = "yolo11-tiny.pt"  # ultralytics 会自动下载

yolo_model = None
if not HAS_YOLO_DETECTOR:
    try:
        from ultralytics import YOLO
        yolo_model = YOLO(YOLO_MODEL_PATH)
        log.info(f"[INFO] YOLO11-tiny loaded: {YOLO_MODEL_PATH}")
    except Exception as e:
        log.error(f"[WARN] YOLO model load failed: {e}")
        yolo_model = None


class DummyTTS:
    def speak(self, text: str):
        log.info(f"[TTS] {text}")


class NavCommand:
    def __init__(self, text: str, level: str = "info", raw=None):
        self.text = text
        self.level = level
        self.raw = raw or {}


class RealtimeNavDemo:
    def __init__(
        self,
        device_index: int = 0,
        enable_tts: bool = True,
        tag: str = "default",
        mode: str = "interactive",
        stress_duration: int = 30,
        stress_max_frames: int = None,
    ):
        self._stop = False
        self.mode = mode
        self.stress_duration = stress_duration
        self.stress_max_frames = stress_max_frames
        self.tag = tag
        self.enable_tts = enable_tts

        # 摄像头
        if HAS_CAMERA_HANDLER:
            try:
                self.camera = CameraHandler(camera_index=device_index)
                self.use_cv2 = False
                log.info("[INFO] 使用内部 CameraHandler")
            except Exception as e:
                log.warning(f"[WARN] CameraHandler 初始化失败: {e}，使用 OpenCV")
                self.camera = cv2.VideoCapture(device_index)
                self.use_cv2 = True
        else:
            self.camera = cv2.VideoCapture(device_index)
            self.use_cv2 = True
            log.info("[INFO] 使用 OpenCV VideoCapture")

        if self.use_cv2 and not self.camera.isOpened():
            raise RuntimeError(f"摄像头无法打开: {device_index}")

        # 检测模型
        if HAS_YOLO_DETECTOR:
            try:
                self.yolo_detector = YoloDetector()
                self.yolo_detector.load_model()
                self.use_internal_yolo = True
                log.info("[INFO] 使用内部 YoloDetector")
            except Exception as e:
                log.warning(f"[WARN] YoloDetector 初始化失败: {e}，使用 ultralytics")
                self.yolo_detector = None
                self.use_internal_yolo = False
        else:
            self.yolo_detector = None
            self.use_internal_yolo = False

        if not self.use_internal_yolo and yolo_model is None:
            raise RuntimeError("无可用 YOLO 模型（YoloDetector & ultralytics 均不可用）")

        # 导航
        if HAS_NAV_LOGIC:
            try:
                self.navigator = NavigationLogicV1_3()
                log.info("[INFO] 使用内部 NavigationLogic")
            except Exception as e:
                log.warning(f"[WARN] NavigationLogic 初始化失败: {e}，使用简单规则")
                self.navigator = None
        else:
            self.navigator = None
            log.warning("[WARN] 未找到 NavigationLogic，使用简单规则导航兜底")

        # TTS
        if HAS_TTS_MANAGER and enable_tts:
            try:
                self.tts = TTSManager(mode="normal")
                log.info("[INFO] 使用内部 TTSManager")
            except Exception as e:
                log.warning(f"[WARN] TTSManager 初始化失败: {e}，使用 DummyTTS")
                self.tts = DummyTTS()
        elif enable_tts:
            self.tts = DummyTTS()
            log.warning("[WARN] 未找到 TTSManager，使用 DummyTTS（仅打印）")
        else:
            self.tts = None
            log.info("[INFO] TTS 已关闭（--no-tts）")

        # 语音限流
        self.last_speak = 0.0
        self.speak_interval = 2.0
        self.last_text = ""

        # 性能采样
        self.perf_samples = []
        os.makedirs("perf_logs", exist_ok=True)

    # ========== 摄像头 ==========

    def _get_frame(self):
        if self.use_cv2:
            ret, frame = self.camera.read()
            return frame if ret else None
        else:
            return self.camera.read_frame()

    # ========== 检测 ==========

    def _detect(self, frame):
        if self.use_internal_yolo and self.yolo_detector is not None:
            try:
                result = self.yolo_detector.infer({"timestamp": time.time(), "data": frame})
                if "objects" not in result:
                    result["objects"] = result.get("detections", [])
                return result
            except Exception as e:
                log.warning(f"[WARN] 内部 YOLO 检测失败: {e}，尝试 ultralytics")

        # 使用 ultralytics YOLO
        if yolo_model is None:
            return {"objects": []}

        try:
            res = yolo_model(frame, verbose=False)
            objs = []
            for r in res:
                boxes = r.boxes
                if boxes is not None:
                    for b in boxes:
                        x1, y1, x2, y2 = b.xyxy[0].tolist()
                        cls_id = int(b.cls[0])
                        conf = float(b.conf[0])
                        cls_name = r.names.get(cls_id, "obj")
                        objs.append({
                            "cls": cls_name,
                            "conf": conf,
                            "bbox": [int(x1), int(y1), int(x2), int(y2)],
                        })
            return {"objects": objs}
        except Exception as e:
            log.error(f"[ERROR] YOLO 检测异常: {e}")
            return {"objects": []}

    # ========== 导航 ==========

    def _nav(self, frame, det):
        if self.navigator is not None:
            try:
                if hasattr(self.navigator, 'plan_route'):
                    nav_res = self.navigator.plan_route(
                        vision_result=det,
                        ground_state={"state": "safe"},
                        dispatch_result={}
                    )
                    if isinstance(nav_res, dict):
                        text = nav_res.get("message", "前方正常")
                    else:
                        text = str(nav_res)
                    return NavCommand(text, "info", raw={"nav": nav_res})
                elif hasattr(self.navigator, 'plan'):
                    nav_res = self.navigator.plan(detections=det, frame=frame)
                    text = getattr(nav_res, "text", "前方正常")
                    level = getattr(nav_res, "level", "info")
                    return NavCommand(text, level, raw={"nav": nav_res})
            except Exception as e:
                log.error(f"[WARN] Navigator error: {e}")

        # 兜底规则
        persons = sum(1 for o in det.get("objects", []) if o.get("cls") == "person")
        cars = sum(1 for o in det.get("objects", []) if o.get("cls") in ["car", "truck", "bus"])

        if cars > 0:
            return NavCommand("前方有车辆，请注意安全", "warn", raw={"num_car": cars})
        elif persons >= 3:
            return NavCommand("前方人多，请注意避让", "warn", raw={"num_person": persons})
        elif persons >= 1:
            return NavCommand("前方有人，请留意", "info", raw={"num_person": persons})
        return NavCommand("环境正常", "info", raw={"num_person": persons})

    # ========== TTS ==========

    def _speak(self, cmd: NavCommand):
        if not self.tts:
            return
        now = time.time()
        if cmd.text == self.last_text and (now - self.last_speak) < self.speak_interval:
            return
        self.tts.speak(cmd.text)
        self.last_text = cmd.text
        self.last_speak = now

    # ========== 性能采样 ==========

    def _record_sample(self, frame_no: int, det_ms: float, nav_ms: float, total_ms: float, fps: float, det: dict):
        self.perf_samples.append({
            "tag": self.tag,
            "mode": self.mode,
            "frame": frame_no,
            "det_ms": round(det_ms, 2),
            "nav_ms": round(nav_ms, 2),
            "total_ms": round(total_ms, 2),
            "fps": round(fps, 2),
            "objects": len(det.get("objects", [])),
        })

    # ========== 主循环：交互模式 ==========

    def run_interactive(self):
        log.info("\n" + "=" * 70)
        log.info("[INFO] 模式：interactive（实时导航），Ctrl+C 退出")
        log.info("=" * 70")
        log.info("")

        frame_no = 0
        while not self._stop:
            frame = self._get_frame()
            if frame is None:
                log.error("[ERROR] 无法获取 frame，退出")
                break

            t1 = time.perf_counter()
            det = self._detect(frame)
            t2 = time.perf_counter()
            cmd = self._nav(frame, det)
            t3 = time.perf_counter()

            self._speak(cmd)

            det_ms = (t2 - t1) * 1000
            nav_ms = (t3 - t2) * 1000
            total_ms = (t3 - t1) * 1000
            fps = 1.0 / max((t3 - t1), 1e-6)
            self._record_sample(frame_no, det_ms, nav_ms, total_ms, fps, det)

            # 每10帧输出一次，避免刷屏
            if frame_no % 10 == 0 or frame_no < 5:
                print(
                    f"[{frame_no:04d}] det={det_ms:.1f}ms nav={nav_ms:.1f}ms "
                    f"total={total_ms:.1f}ms fps={fps:.1f} | "
                    f"{cmd.level}: {cmd.text[:40]}"
                )

            frame_no += 1

        self._save_reports()

    # ========== 主循环：压测模式 ==========

    def run_stress(self):
        log.info("\n" + "=" * 70)
        log.info(f"[INFO] 模式：stress，持续 {self.stress_duration}s / max_frames={self.stress_max_frames}")
        log.info("=" * 70")
        log.info("")

        frame_no = 0
        t_start = time.time()

        while not self._stop:
            if self.stress_max_frames is not None and frame_no >= self.stress_max_frames:
                log.info("[INFO] 已达到最大帧数，结束压测")
                break
            if (time.time() - t_start) > self.stress_duration:
                log.info("[INFO] 已达到压测时长，结束压测")
                break

            frame = self._get_frame()
            if frame is None:
                log.error("[ERROR] 无法获取 frame，结束压测")
                break

            t1 = time.perf_counter()
            det = self._detect(frame)
            t2 = time.perf_counter()
            cmd = self._nav(frame, det)
            t3 = time.perf_counter()

            if self.enable_tts:
                self._speak(cmd)

            det_ms = (t2 - t1) * 1000
            nav_ms = (t3 - t2) * 1000
            total_ms = (t3 - t1) * 1000
            fps = 1.0 / max((t3 - t1), 1e-6)
            self._record_sample(frame_no, det_ms, nav_ms, total_ms, fps, det)

            # 压测模式下简化输出（每 10 帧打一条）
            if frame_no % 10 == 0:
                print(
                    f"[STRESS {frame_no:04d}] total={total_ms:.1f}ms fps={fps:.1f} "
                    f"(det={det_ms:.1f}ms nav={nav_ms:.1f}ms)"
                )

            frame_no += 1

        self._save_reports()

    # ========== 保存报告 ==========

    def _save_reports(self):
        if not self.perf_samples:
            log.info("[INFO] 无性能采样，跳过报告生成")
            return

        ts = time.strftime("%Y%m%d_%H%M%S")
        base = f"{self.tag}_{self.mode}_{ts}"

        csv_path = os.path.join("perf_logs", f"{base}_samples.csv")
        json_path = os.path.join("perf_logs", f"{base}_report.json")

        # CSV
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.perf_samples[0].keys())
            writer.writeheader()
            writer.writerows(self.perf_samples)

        # 统计
        totals = [s["total_ms"] for s in self.perf_samples]
        dets = [s["det_ms"] for s in self.perf_samples]
        navs = [s["nav_ms"] for s in self.perf_samples]

        totals_sorted = sorted(totals)
        n = len(totals_sorted)

        def pct(arr, p):
            if n == 0:
                return 0.0
            idx = max(min(int(p * n) - 1, n - 1), 0)
            return arr[idx]

        stats = {
            "tag": self.tag,
            "mode": self.mode,
            "count": n,
            "avg_total": round(sum(totals) / n, 2),
            "avg_det": round(sum(dets) / n, 2),
            "avg_nav": round(sum(navs) / n, 2),
            "p50": round(pct(totals_sorted, 0.50), 2),
            "p90": round(pct(totals_sorted, 0.90), 2),
            "p95": round(pct(totals_sorted, 0.95), 2),
            "p99": round(pct(totals_sorted, 0.99), 2),
            "min": round(min(totals_sorted), 2),
            "max": round(max(totals_sorted), 2),
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

        log.info("\n[INFO] 性能报告已生成：")
        log.info(" -", csv_path")
        log.info(" -", json_path")

    def _cleanup(self):
        """清理资源"""
        if self.use_cv2 and self.camera is not None:
            self.camera.release()
        elif not self.use_cv2 and self.camera is not None:
            if hasattr(self.camera, 'release'):
                self.camera.release()
        cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description="Luna Badge v1.3.1 Realtime Nav Demo")
    parser.add_argument("--mode", choices=["interactive", "stress"], default="interactive",
                        help="运行模式：interactive（实时导航）或 stress（压测）")
    parser.add_argument("--device", type=int, default=0, help="摄像头设备索引（默认: 0）")
    parser.add_argument("--no-tts", action="store_true", help="关闭 TTS 播报")
    parser.add_argument("--tag", type=str, default="default", help="测试标签（写入 perf_logs）")
    parser.add_argument("--stress-duration", type=int, default=60, help="压测模式：持续秒数")
    parser.add_argument("--stress-max-frames", type=int, default=None, help="压测模式：最大帧数")

    args = parser.parse_args()

    demo = RealtimeNavDemo(
        device_index=args.device,
        enable_tts=(not args.no_tts),
        tag=args.tag,
        mode=args.mode,
        stress_duration=args.stress_duration,
        stress_max_frames=args.stress_max_frames,
    )

    def sig_handler(signum, frame):
        log.info("\n[INFO] 收到中断信号，准备退出...")
        demo._stop = True

    signal.signal(signal.SIGINT, sig_handler)

    try:
        if args.mode == "interactive":
            demo.run_interactive()
        else:
            demo.run_stress()
    finally:
        demo._cleanup()


if __name__ == "__main__":
    main()
