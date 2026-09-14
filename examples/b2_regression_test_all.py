# examples/b2_regression_test_all.py
from __future__ import annotations
import os
import json
import cv2
from typing import Dict, List, Any, Optional

# ------------------------------------------------
# 你已有的 B2 版本（按真实路径调整）
# ------------------------------------------------
from vision_pipeline.b2.v03.b2_v03 import B2v03

# ------------------------------------------------
# 基础配置
# ------------------------------------------------
VIDEO_PATH = "test_video_complex_6m42s.mp4"
OUT_ROOT = "reports/b2_regression"
MAX_FRAMES = None        # 可设上限，None = 全视频
FPS_OVERRIDE = None     # 一般不需要

# 版本映射（根据实际可用版本调整）
VERSIONS = {
    "v03": B2v03,
}

# ------------------------------------------------
# 工具函数
# ------------------------------------------------

def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def write_jsonl(path: str, rows: List[Dict[str, Any]]):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

# ------------------------------------------------
# ⚠️ 关键区别：模拟数据 vs 真实数据
# ------------------------------------------------

def build_perception_simulated(t_video: float) -> Dict[str, Any]:
    """
    【模拟数据】- 当前回归测试使用的方式
    
    这是硬编码的假数据，用于测试 B2 的逻辑是否正确。
    所有帧的 perception 都是预先定义好的，不依赖实际视频内容。
    
    优点：可控、可重复、快速
    缺点：不能反映真实场景，无法验证 B2 在实际环境中的表现
    """
    perception = {
        "path": {"surface": "concrete", "has_path": True},
        "env": {"scene": "road", "density": "low", "indoor": False},
        "people": {"count": 0, "moving": False},
        "events": [],
    }
    
    # 模拟变化区间
    if 120 < t_video < 160:
        perception["path"]["surface"] = "gravel"
    if 200 < t_video < 260:
        perception["env"]["scene"] = "market"
        perception["env"]["density"] = "high"
        perception["people"]["count"] = 15
        perception["people"]["moving"] = True
    if 300 < t_video < 305:
        perception["events"].append({"type": "construction", "severity": "high"})
    
    return perception


def build_perception_from_pipeline(
    frame: Any,
    frame_idx: int,
    t_video: float,
    pipeline_controller: Optional[Any] = None
) -> Dict[str, Any]:
    """
    【真实数据】- 从实际感知系统获取
    
    这个函数应该从真实的 PipelineController 或感知模块获取数据：
    1. 从 navigation_result 获取路径信息（path.surface, path.has_path）
    2. 从 modeling_result 获取场景信息（env.scene, env.density）
    3. 从 objects 检测结果统计人群（people.count, people.moving）
    4. 从事件检测器获取事件（events）
    
    优点：反映真实场景，能验证 B2 在实际环境中的表现
    缺点：需要完整的 pipeline，运行较慢
    
    使用方式：
        # 在回归测试中，需要先初始化 PipelineController
        from vision_pipeline.pipeline_controller import PipelineController
        controller = PipelineController(config)
        
        # 然后对每一帧调用 process_frame
        result = controller.process_frame(frame, frame_idx, t_video)
        
        # 从 result 中提取 perception（或直接使用 controller 内部构建的）
        perception = extract_perception_from_result(result)
    """
    # ⚠️ 当前是占位实现，需要接入真实的 PipelineController
    if pipeline_controller:
        # 方式 1: 调用 PipelineController.process_frame
        result = pipeline_controller.process_frame(
            frame=frame,
            frame_idx=frame_idx,
            timestamp=t_video
        )
        
        # 从 result 中提取 perception（需要根据实际结构调整）
        # 参考 pipeline_controller.py 第 432-458 行的逻辑
        perception = result.get("perception", {})
        
        # 如果 result 中没有直接的 perception，需要从各个模块结果中构建
        if not perception:
            perception = {
                "path": {},
                "env": {},
                "people": {},
                "events": [],
            }
            
            # 从 navigation_result 提取
            nav_result = result.get("navigation_result")
            if nav_result:
                if hasattr(nav_result, "path_type"):
                    perception["path"]["surface"] = nav_result.path_type
                if hasattr(nav_result, "has_path"):
                    perception["path"]["has_path"] = nav_result.has_path
            
            # 从 modeling_result 提取
            modeling_result = result.get("modeling_result")
            if modeling_result:
                scene = getattr(modeling_result, "scene_label", None) or getattr(modeling_result, "scene", None)
                if scene:
                    perception["env"]["scene"] = scene
                perception["env"]["density"] = "mid"  # 默认值
            
            # 从 objects 统计人群
            objects = result.get("objects", [])
            person_count = sum(1 for obj in objects if obj.get("class", "").lower() in ("person", "people", "human"))
            perception["people"] = {
                "count": person_count,
                "moving": False  # 需要从 tracker 获取
            }
            
            perception["events"] = result.get("events", [])
        
        return perception
    else:
        # 如果没有 pipeline_controller，回退到模拟数据
        print(f"[WARNING] 未提供 pipeline_controller，使用模拟数据")
        return build_perception_simulated(t_video)


# ------------------------------------------------
# 单版本跑视频
# ------------------------------------------------

def run_single_version(
    version_name: str,
    B2Class,
    frames: List,
    fps: float,
    use_real_perception: bool = False,
    pipeline_controller: Optional[Any] = None,
) -> List[Dict[str, Any]]:
    print(f"\n===== Running {version_name} =====")
    print(f"使用 {'真实' if use_real_perception else '模拟'} perception 数据")

    # 初始化 B2（根据实际接口调整）
    import time
    base_ts = time.time()
    
    if version_name == "v03":
        b2 = B2Class(debug=False, log_mode="video", log_base_ts=base_ts)
    else:
        b2 = B2Class(version=version_name)

    results: List[Dict[str, Any]] = []

    for frame_idx, frame in enumerate(frames):
        t_video = frame_idx / fps

        # 构建 perception（根据配置选择模拟或真实数据）
        if use_real_perception:
            perception = build_perception_from_pipeline(
                frame=frame,
                frame_idx=frame_idx,
                t_video=t_video,
                pipeline_controller=pipeline_controller
            )
        else:
            perception = build_perception_simulated(t_video)

        # 调用 B2 tick（根据实际接口调整）
        if version_name == "v03":
            frame_ts = base_ts + t_video
            out = b2.tick(frame_ts=frame_ts, perception=perception)
        else:
            out = b2.tick(frame=frame, frame_idx=frame_idx, t_video=t_video)

        if out and out.get("level"):  # v0.3 使用 "level" 而不是 "decision"
            record = {
                "version": version_name,
                "frame_idx": frame_idx,
                "t_video": t_video,
                "decision": out.get("level", out.get("decision", "UNKNOWN")),
            }

            # v0.3+ 可能有更多内容，全部旁路记录
            for k in ("confidence", "main_factor", "evidence_ref", "param_vector", "level", "impact"):
                if k in out:
                    record[k] = out[k]

            results.append(record)

        if MAX_FRAMES and frame_idx >= MAX_FRAMES:
            break

    return results

# ------------------------------------------------
# 主流程
# ------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="B2 全版本回归测试")
    parser.add_argument("--real", action="store_true", help="使用真实 perception 数据（需要 PipelineController）")
    parser.add_argument("--video", type=str, default=VIDEO_PATH, help="视频路径")
    args = parser.parse_args()
    
    ensure_dir(OUT_ROOT)

    video_path = args.video
    if not os.path.exists(video_path):
        print(f"[ERROR] Video not found: {video_path}")
        print("Please update VIDEO_PATH in the script or use --video")
        return

    cap = cv2.VideoCapture(video_path)
    fps = FPS_OVERRIDE or cap.get(cv2.CAP_PROP_FPS)
    assert fps > 0, "Invalid FPS"

    # 预读全部帧到内存，保证所有版本输入一致
    frames = []
    cap_tmp = cv2.VideoCapture(video_path)
    while True:
        ok, frame = cap_tmp.read()
        if not ok:
            break
        frames.append(frame)
    cap_tmp.release()
    cap.release()

    print(f"Loaded {len(frames)} frames @ {fps:.2f} fps")
    print(f"Testing {len(VERSIONS)} versions: {list(VERSIONS.keys())}")

    # 如果需要真实数据，初始化 PipelineController
    pipeline_controller = None
    if args.real:
        try:
            from vision_pipeline.pipeline_controller import PipelineController
            # 需要根据实际配置初始化
            config = {}  # 根据实际情况配置
            pipeline_controller = PipelineController(config)
            print("[INFO] PipelineController 已初始化，将使用真实 perception 数据")
        except Exception as e:
            print(f"[WARNING] 无法初始化 PipelineController: {e}")
            print("[WARNING] 回退到模拟数据")
            args.real = False

    for ver, cls in VERSIONS.items():
        ensure_dir(os.path.join(OUT_ROOT, ver))

        results = run_single_version(
            ver, cls, frames, fps,
            use_real_perception=args.real,
            pipeline_controller=pipeline_controller
        )

        out_path = os.path.join(OUT_ROOT, ver, "timeline.jsonl")
        write_jsonl(out_path, results)

        print(f"[{ver}] decisions={len(results)} → {out_path}")

    print("\n===== REGRESSION TEST DONE =====")
    print(f"Results saved to: {OUT_ROOT}")
    print("\nNext steps:")
    print("  1. Compare decision counts across versions")
    print("  2. Check decision timing alignment")
    print("  3. Analyze param_vector stability (v0.3+)")
    print("\n💡 提示：使用 --real 参数可以启用真实 perception 数据")

if __name__ == "__main__":
    main()
