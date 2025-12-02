#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动测试路由：百度抓图 + 自动测试场景描述
"""

from flask import Blueprint, jsonify, request, Response
from backend.auto_image_fetcher import AutoImageFetcher
from backend.local_image_loader import LocalImageLoader
from backend.auto_test_judger import AutoTestJudger
from backend.auto_test.auto_test_judger import AutoTestJudger as NewAutoTestJudger
from backend.auto_test_runner import AutoTestRunner
from backend.auto_training_store import TrainingSampleStore
from backend.auto_image_search import search_images
from config.auto_test_config import AutoTestConfig
from backend.utils.scene_description_helper import call_scene_description_api
from backend.video_frame_extractor import VideoFrameExtractor
from backend.auto_test_metrics import log_auto_test_result, compute_summary
from backend.auto_playlists import list_playlists, get_playlist
from backend.auto_sort.auto_sorter import AutoSorter
from backend.rl.feedback_store import FeedbackStore
import base64
import requests
import csv
import io
import os
import tempfile
import logging

logger = logging.getLogger(__name__)

# 尝试导入 log_manager（如果存在）
try:
    from web_test_server import log_manager
except Exception:
    log_manager = None
    logger.warning("log_manager 未找到，批量测试上报功能将使用简单日志")

# 全局反馈存储器
feedback_store = FeedbackStore()

# 延迟导入 ErrorClustering（避免 sklearn 依赖问题导致整个模块无法加载）
try:
    from backend.auto_test_clustering import ErrorClustering
    ERROR_CLUSTERING_AVAILABLE = True
except Exception as e:
    ERROR_CLUSTERING_AVAILABLE = False
    ErrorClustering = None
    import logging
    logging.getLogger(__name__).warning(f"ErrorClustering 不可用: {e}")

auto_test_api = Blueprint("auto_test_api", __name__)

# 全局训练样本存储器（简单单例）
training_store = TrainingSampleStore()

# 关键词库（可扩展）
TEST_KEYWORDS = [
    "人行道", "盲道", "过马路", "地铁入口", "商场入口", "自动扶梯",
    "医院挂号大厅", "排队", "服务台", "便利店门口",
    "公交站", "井盖打开", "道路施工", "电动车乱停",
    "医院走廊", "候诊区", "电梯", "洗手间", "收银台",
    "超市货架", "地铁站台", "人行横道", "红绿灯路口",
    "医院大厅", "挂号窗口", "取号机", "咨询台", "药房",
    "商场扶梯", "商场入口", "超市入口", "收银台排队",
    "地铁闸机", "地铁站厅", "站台指示牌", "出口指示",
    "医院科室", "病房走廊", "手术室门口", "急诊室",
    "商场中庭", "商场导览图", "店铺招牌", "促销海报",
    "超市生鲜区", "超市收银区", "购物车", "货架通道",
    "地铁车厢", "地铁站内", "换乘通道", "无障碍电梯",
    "医院停车场", "医院入口", "医院标识", "科室指示牌",
    "商场停车场", "商场出口", "商场服务台", "商场休息区",
    "超市入口", "超市出口", "超市服务台", "超市收银通道",
    "地铁站外", "地铁站入口", "地铁站出口", "地铁站标识"
]


@auto_test_api.route("/keyword_list", methods=['GET'])
def keyword_list():
    """返回关键词列表"""
    return jsonify({"success": True, "keywords": TEST_KEYWORDS})


@auto_test_api.route("/keywords", methods=['GET'])
def get_keywords():
    """
    返回支持自动测试的关键词列表（从 AutoTestJudger 获取）
    """
    keys = list(AutoTestJudger.MATCH_RULES.keys())
    return jsonify({"success": True, "keywords": keys})


@auto_test_api.route("/fetch_and_test/<kw>", methods=['GET'])
def fetch_and_test(kw):
    """
    1. 用关键字抓图
    2. 返回 base64 给前端
    3. 前端自动送入 Luna 进行场景描述
    """
    img_bytes, err = AutoImageFetcher.fetch_image(kw)

    if err:
        return jsonify({"success": False, "error": err}), 500

    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    return jsonify({
        "success": True,
        "keyword": kw,
        "image_base64": img_b64
    })


@auto_test_api.route("/run_full_test/<kw>", methods=['GET'])
def run_full_test(kw):
    """
    自动测试：本地图片 → Luna → 自动判断 → 返回匹配/不匹配
    """
    # 优先使用本地图库，如果失败则尝试百度抓图
    img_bytes, err = LocalImageLoader.load_random(kw)
    if err:
        # 如果本地图库不存在，尝试百度抓图
        img_bytes, err = AutoImageFetcher.fetch_image(kw)
        if err:
            return jsonify({"success": False, "error": err}), 500

    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    # --- 调用 Luna 场景描述接口 ----
    desc, raw_data = call_scene_description_api(img_b64)
    if desc is None:
        desc = ""

    # --- 自动判断 ---
    match, hit_word = AutoTestJudger.judge(kw, desc)

    # v2.0: 记录测试结果
    log_auto_test_result({
        "type": "single",
        "keyword": kw,
        "match": match,
    })

    return jsonify({
        "success": True,
        "keyword": kw,
        "description": desc,
        "match": match,
        "hit": hit_word,
        "image_base64": img_b64
    })


@auto_test_api.route("/run_batch_test", methods=["POST"])
def run_batch_test():
    """
    批量自动测试：
    body: {
      "keywords": ["人行道", "地铁入口", ...],
      "max_per_keyword": 20   # 每个 keyword 最多测试几张
    }
    """
    data = request.get_json() or {}
    keywords = data.get("keywords") or []
    max_per_keyword = data.get("max_per_keyword")

    if not isinstance(keywords, list) or len(keywords) == 0:
        return jsonify({"success": False, "error": "keywords 不能为空"}), 400

    runner = AutoTestRunner()
    result = runner.run_batch(keywords, max_per_keyword=max_per_keyword)

    return jsonify({
        "success": True,
        "summary": result["summary"],
        "error_clusters": result["error_clusters"],
        # 保留 samples 给前端做更深层的分析（如需要）
        "samples": result["samples"]
    })


@auto_test_api.route("/training_samples/add", methods=["POST"])
def add_training_sample():
    """
    V6：从前端"加入训练集"按钮过来的数据
    结构示例：
    {
      "keyword": "医院挂号大厅",
      "description": "...",
      "match_auto": false,
      "human_label": "wrong",   # "correct" / "wrong"
      "image_base64": "...",
      "hit": "挂号",
      "cluster": "挂号窗口识别错误",  # 前端可选填
      "note": "医生门口识别成收费窗口"
    }
    """
    try:
        data = request.get_json(force=True) or {}

        keyword = data.get("keyword") or ""
        description = data.get("description") or ""
        match_auto = bool(data.get("match_auto"))
        human_label = data.get("human_label") or "unknown"
        image_base64 = data.get("image_base64") or ""
        hit = data.get("hit")
        cluster = data.get("cluster") or ""
        note = data.get("note") or ""

        if not keyword or not description:
            return jsonify({
                "success": False,
                "error": "缺少 keyword 或 description"
            }), 400

        # 这里不做 image 的大小检查，后面如有需要可加

        sample = {
            "keyword": keyword,
            "description": description,
            "match_auto": match_auto,
            "human_label": human_label,   # 人工判断：correct / wrong
            "hit_word": hit,
            "cluster": cluster,           # 人工聚类标签
            "note": note,
            "source": "auto_test_v6",
            "image_base64": image_base64,
        }

        training_store.add_sample(sample)

        return jsonify({
            "success": True,
            "data": {"saved": True}
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@auto_test_api.route("/training_samples/export", methods=["GET"])
def export_training_samples():
    """
    导出训练样本：
      /api/auto/training_samples/export?format=csv
      /api/auto/training_samples/export?format=json
    """
    fmt = request.args.get("format", "csv").lower()
    limit = request.args.get("limit", type=int)  # 可选：只导出最近 N 条

    samples = training_store.list_samples(limit=limit)

    if fmt == "json":
        # 直接返回 JSON
        return jsonify({
            "success": True,
            "data": samples
        })

    # 默认导出 CSV
    # 统一字段顺序
    fieldnames = [
        "keyword",
        "description",
        "match_auto",
        "human_label",
        "hit_word",
        "cluster",
        "note",
        "source",
        "created_at"
        # image_base64 不放进 CSV（太大），如有需要可以加
    ]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for s in samples:
        row = {
            "keyword": s.get("keyword", ""),
            "description": s.get("description", "").replace("\n", " "),
            "match_auto": s.get("match_auto", False),
            "human_label": s.get("human_label", ""),
            "hit_word": s.get("hit_word", ""),
            "cluster": s.get("cluster", ""),
            "note": s.get("note", ""),
            "source": s.get("source", ""),
            "created_at": s.get("created_at", 0),
        }
        writer.writerow(row)

    csv_data = output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": "attachment; filename=luna_training_samples.csv"
        }
    )


@auto_test_api.route("/auto_search_images", methods=["POST"])
def auto_search_images():
    """
    V6.1：自动搜索并下载图片
    body: {
      "keywords": ["电梯", "斑马线", ...],
      "max_per_keyword": 20
    }
    """
    try:
        data = request.get_json() or {}
        keywords = data.get("keywords") or []
        max_per_keyword = data.get("max_per_keyword", 20)
        
        if not isinstance(keywords, list) or len(keywords) == 0:
            return jsonify({"success": False, "error": "keywords 不能为空"}), 400
        
        results = {}
        total_downloaded = 0
        
        for kw in keywords:
            paths = search_images(kw, max_results=max_per_keyword)
            results[kw] = {
                "count": len(paths),
                "paths": paths
            }
            total_downloaded += len(paths)
        
        return jsonify({
            "success": True,
            "total_downloaded": total_downloaded,
            "results": results
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@auto_test_api.route("/run_batch_with_clustering", methods=["POST"])
def run_batch_with_clustering():
    """
    V6.1：批量测试 + 错误聚类 + 自动生成训练数据
    body: {
      "keywords": ["电梯", "斑马线", ...],
      "max_per_keyword": 20,
      "n_clusters": 3
    }
    """
    try:
        data = request.get_json() or {}
        keywords = data.get("keywords") or []
        max_per_keyword = data.get("max_per_keyword", 20)
        n_clusters = data.get("n_clusters", 3)
        
        if not isinstance(keywords, list) or len(keywords) == 0:
            return jsonify({"success": False, "error": "keywords 不能为空"}), 400
        
        # 1. 运行批量测试
        runner = AutoTestRunner()
        result = runner.run_batch(keywords, max_per_keyword=max_per_keyword)
        
        # 2. 提取错误样本
        error_samples = [s for s in result["samples"] if not s.get("match", False)]
        
        # 3. 错误聚类
        if ERROR_CLUSTERING_AVAILABLE and ErrorClustering:
            clustering = ErrorClustering()
            clustered_errors = clustering.cluster_errors(error_samples, n_clusters=n_clusters)
            cluster_summary = clustering.get_cluster_summary(clustered_errors)
        else:
            # 降级：使用简化聚类（按关键词分组）
            clustered_errors = error_samples
            cluster_id = 0
            keyword_to_cluster = {}
            for sample in clustered_errors:
                kw = sample.get("keyword", "unknown")
                if kw not in keyword_to_cluster:
                    keyword_to_cluster[kw] = cluster_id
                    cluster_id += 1
                sample["cluster"] = keyword_to_cluster[kw]
            
            # 生成简化版摘要
            clusters = {}
            for sample in clustered_errors:
                cid = sample.get("cluster", 0)
                if cid not in clusters:
                    clusters[cid] = {
                        "cluster_id": cid,
                        "count": 0,
                        "keywords": set(),
                        "sample_descriptions": []
                    }
                clusters[cid]["count"] += 1
                clusters[cid]["keywords"].add(sample.get("keyword", "unknown"))
                desc = sample.get("description", "")
                if desc and len(clusters[cid]["sample_descriptions"]) < 3:
                    clusters[cid]["sample_descriptions"].append(desc[:50])
            
            cluster_summary = {
                "clusters": [
                    {
                        "cluster_id": cid,
                        "count": info["count"],
                        "keywords": list(info["keywords"]),
                        "sample_descriptions": info["sample_descriptions"]
                    }
                    for cid, info in clusters.items()
                ]
            }
        
        # 4. 自动保存到训练数据
        for sample in clustered_errors:
            training_sample = {
                "keyword": sample.get("keyword", ""),
                "description": sample.get("description", ""),
                "match_auto": False,
                "human_label": "wrong",
                "image_base64": sample.get("image_base64", ""),
                "hit": sample.get("hit"),
                "cluster": f"cluster_{sample.get('cluster', 0)}",
                "note": f"自动聚类错误样本",
                "source": "auto_test_v6.1_batch"
            }
            training_store.add_sample(training_sample)
        
        return jsonify({
            "success": True,
            "summary": result["summary"],
            "error_clusters": result["error_clusters"],
            "clustering_summary": cluster_summary,
            "auto_saved_samples": len(clustered_errors)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ====== v1.1: 单张图片自动测试 ======
@auto_test_api.route("/run_full_test", methods=["POST"])
def run_full_test_v1_1():
    """
    v1.1: 单次：上传图片 + 关键词 → 场景描述 → 自动匹配
    前端用在 /test 页面里。
    """
    try:
        data = request.get_json() or {}
        keyword = data.get("keyword", "").strip()
        image_base64 = data.get("image_base64")
        
        if not keyword or not image_base64:
            return jsonify({
                "success": False,
                "error": "缺少 keyword 或 image_base64",
                "code": "E_AUTO_TEST_PARAM"
            }), 400
        
        try:
            # 解码 base64
            raw = image_base64.split(",")[-1] if "," in image_base64 else image_base64
            img_bytes = base64.b64decode(raw)
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"图片解码失败: {e}",
                "code": "E_AUTO_TEST_B64"
            }), 400
        
        # 调用场景描述引擎
        try:
            import cv2
            import numpy as np
            
            # 将 bytes 转换为 numpy array
            nparr = np.frombuffer(img_bytes, np.uint8)
            image_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image_np is None:
                return jsonify({
                    "success": False,
                    "error": "图片格式错误",
                    "code": "E_AUTO_TEST_IMG_FORMAT"
                }), 400
            
            # 调用场景描述引擎（直接调用，避免 HTTP 开销）
            from web_test_server import scene_description_engine
            from backend.utils.scene_description_helper import call_scene_description_engine_direct
            
            description, description_result = call_scene_description_engine_direct(
                image_np, 
                scene_description_engine
            )
            
            if description is None:
                description = ""
            
        except Exception as e:
            import traceback
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"场景描述失败: {e}\n{traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": f"场景描述失败: {e}",
                "code": "E_AUTO_TEST_DESC"
            }), 500
        
        # 使用新的 AutoTestJudger
        match, hit = NewAutoTestJudger.judge(keyword, description)
        
        return jsonify({
            "success": True,
            "data": {
                "keyword": keyword,
                "description": description,
                "match": match,
                "hit_word": hit,
            }
        })
    except Exception as e:
        import traceback
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"run_full_test_v1_1 失败: {e}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "error": str(e),
            "code": "E_AUTO_TEST_UNKNOWN"
        }), 500


# ====== v1.2: 视频自动测试 ======
@auto_test_api.route("/run_video_test", methods=["POST"])
def run_video_test():
    """
    v1.2: 视频自动测试
    - form-data: video_file, keyword
    - 抽帧 → 场景描述 → 匹配统计
    """
    try:
        keyword = request.form.get("keyword", "").strip()
        file = request.files.get("video_file")
        
        if not keyword or not file:
            return jsonify({
                "success": False,
                "error": "缺少 keyword 或 video_file",
                "code": "E_VIDEO_TEST_PARAM"
            }), 400
        
        video_bytes = file.read()
        
        # 提取帧
        from backend.auto_test.video_frame_extractor import VideoFrameExtractor
        frames = VideoFrameExtractor.iter_frames_from_bytes(
            video_bytes, 
            step=AutoTestConfig.VIDEO_FRAME_STEP, 
            max_frames=AutoTestConfig.VIDEO_MAX_FRAMES
        )
        
        if not frames:
            return jsonify({
                "success": False,
                "error": "无法从视频中提取帧",
                "code": "E_VIDEO_TEST_EXTRACT"
            }), 400
        
        # 处理每一帧
        results = []
        match_count = 0
        
        from web_test_server import scene_description_engine
        if scene_description_engine is None:
            return jsonify({
                "success": False,
                "error": "场景描述引擎未初始化",
                "code": "E_VIDEO_TEST_ENGINE"
            }), 500
        
        import cv2
        
        from backend.utils.scene_description_helper import call_scene_description_engine_direct
        
        for idx, frame in enumerate(frames):
            try:
                # 调用场景描述引擎（直接调用，避免 HTTP 开销）
                desc, desc_result = call_scene_description_engine_direct(frame, scene_description_engine)
                
                if desc is None:
                    desc = ""
                
                # 判断匹配
                match, hit = NewAutoTestJudger.judge(keyword, desc)
                
                if match:
                    match_count += 1
                
                results.append({
                    "index": idx,
                    "description": desc,
                    "match": match,
                    "hit_word": hit,
                })
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"处理视频帧 {idx} 失败: {e}")
                continue
        
        total = len(results)
        accuracy = (match_count / total) if total > 0 else 0.0
        
        return jsonify({
            "success": True,
            "data": {
                "keyword": keyword,
                "total_frames": total,
                "match_frames": match_count,
                "accuracy": accuracy,
                "frames": results
            }
        })
    except Exception as e:
        import traceback
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"run_video_test 失败: {e}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "error": str(e),
            "code": "E_VIDEO_TEST_UNKNOWN"
        }), 500


# ====== v1.2: 视频自动检测 ======
@auto_test_api.route("/video_describe", methods=["POST"])
def video_describe():
    """
    v1.2：上传视频 → 抽帧 → 调场景描述 API → 返回每帧描述
    """
    if "video" not in request.files:
        return jsonify({"success": False, "error": "未上传视频"}), 400

    file = request.files["video"]

    # 临时保存视频文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        file.save(tmp.name)
        video_path = tmp.name

    try:
        extractor = VideoFrameExtractor(
            step=AutoTestConfig.VIDEO_FRAME_STEP, 
            max_frames=AutoTestConfig.VIDEO_MAX_FRAMES
        )
        frames = extractor.extract_frames(video_path)

        if not frames:
            return jsonify({
                "success": False,
                "error": "无法从视频中提取帧"
            }), 400

        results = []
        for idx, frame_bytes in enumerate(frames):
            img_b64 = base64.b64encode(frame_bytes).decode("utf-8")

            # 复用现有场景描述 API
            desc, raw_data = call_scene_description_api(img_b64)
            if desc is None:
                desc = ""

            results.append({
                "frame_index": idx,
                "image_base64": img_b64,
                "description": desc,
            })

        # v2.0: 记录测试结果（简单策略：只要有 frame，且至少一帧有描述，就记一次）
        any_desc = any(bool(f.get("description")) for f in results)
        log_auto_test_result({
            "type": "video",
            "match": any_desc,
        })

        return jsonify({
            "success": True,
            "frame_count": len(results),
            "frames": results,
        })
    finally:
        try:
            os.unlink(video_path)
        except Exception:
            pass


# ====== v1.3: Playlist 多场景测试 ======
@auto_test_api.route("/playlists", methods=["GET"])
def api_list_playlists():
    """v1.3：获取所有可用的测试场景组"""
    return jsonify({"success": True, "data": list_playlists()})


@auto_test_api.route("/run_playlist/<name>", methods=["POST"])
def api_run_playlist(name):
    """
    v1.3：执行一个场景Playlist：
    - 对应多个 keyword
    - 每个 keyword 调用一次 run_full_test 流程
    """
    kws = get_playlist(name)
    if not kws:
        return jsonify({"success": False, "error": f"未知场景组: {name}"}), 404

    results = []
    for kw in kws:
        # 优先使用本地图库，如果失败则尝试百度抓图
        img_bytes, err = LocalImageLoader.load_random(kw)
        if err:
            # 如果本地图库不存在，尝试百度抓图
            img_bytes, err = AutoImageFetcher.fetch_image(kw)
            if err:
                results.append({
                    "keyword": kw,
                    "success": False,
                    "error": err,
                })
                continue

        img_b64 = base64.b64encode(img_bytes).decode("utf-8")

        # 调用场景描述接口
        desc, raw_data = call_scene_description_api(img_b64)
        if desc is None:
            desc = ""

        match, hit = AutoTestJudger.judge(kw, desc)

        results.append({
            "keyword": kw,
            "success": True,
            "image_base64": img_b64,
            "description": desc,
            "match": match,
            "hit": hit,
        })

    # v2.0: 批量记录测试结果
    for r in results:
        if not r.get("success"):
            continue
        log_auto_test_result({
            "type": "playlist",
            "keyword": r["keyword"],
            "playlist": name,
            "match": r["match"],
        })

    return jsonify({"success": True, "results": results, "playlist": name})


# ====== v2.0: 测试统计 ======
@auto_test_api.route("/batch/report", methods=["POST"])
def batch_report():
    """
    接收前端批量测试汇总结果，用于后端记录和后续分析
    这里只做轻量处理，不做复杂逻辑。
    """
    try:
        data = request.get_json() or {}
        scene_tag = data.get("scene_tag", "unknown")
        total = int(data.get("total") or 0)
        passed = int(data.get("pass") or 0)
        failed = int(data.get("fail") or 0)
        items = data.get("items") or []

        # 记录日志，方便后续看"哪个场景经常出错"
        if log_manager:
            try:
                log_manager.log_system_event(
                    event="batch_test_report",
                    metadata={
                        "scene_tag": scene_tag,
                        "total": total,
                        "passed": passed,
                        "failed": failed,
                        "sample_items": items[:5],  # 只记一小部分样本
                    },
                )
            except Exception as e:
                # 日志失败不能影响主流程
                logger.warning(f"[batch_report] 记录日志失败: {e}")
        else:
            # 如果没有 log_manager，使用简单日志
            logger.info(
                f"[batch_report] scene_tag={scene_tag}, total={total}, passed={passed}, failed={failed}"
            )

        return jsonify(
            {
                "success": True,
                "data": {
                    "scene_tag": scene_tag,
                    "total": total,
                    "passed": passed,
                    "failed": failed,
                },
            }
        )
    except Exception as e:
        logger.error(f"[batch_report] 处理失败: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@auto_test_api.route("/auto_sort", methods=["POST"])
def auto_sort_images():
    """
    自动识别 + 分类 test_images 目录下的图片到 auto_sorted 目录
    请求体可选字段：
        - input_dir: 默认 "test_images"
        - output_dir: 默认 "auto_sorted"
    """
    try:
        data = request.get_json(silent=True) or {}
        input_dir = data.get("input_dir") or "test_images"
        output_dir = data.get("output_dir") or "auto_sorted"

        # 尝试使用全局 scene_description_engine（如果可用）
        try:
            from web_test_server import scene_description_engine
            sorter = AutoSorter(scene_description_engine=scene_description_engine)
        except Exception:
            # 如果全局引擎不可用，使用默认初始化
            sorter = AutoSorter()

        stats = sorter.scan_and_classify(input_dir=input_dir, output_dir=output_dir)

        return jsonify(
            {
                "success": True,
                "data": stats,
            }
        )
    except Exception as e:
        logger.exception("自动分类失败")
        return jsonify({"success": False, "error": str(e)}), 500


@auto_test_api.route("/feedback", methods=["POST"])
def submit_feedback():
    """
    人工反馈接口：
    前端在测试界面点击 "AI判断错误 → 人工修正标签" 后，把数据 POST 过来
    """
    try:
        data = request.get_json() or {}
        # 允许的字段：前端按需传
        feedback_item = {
            "image_path": data.get("image_path"),
            "keyword": data.get("keyword"),
            "ai_description": data.get("ai_description"),
            "ai_tags": data.get("ai_tags") or [],
            "ai_decision": data.get("ai_decision"),
            "human_label": data.get("human_label"),
            "context": data.get("context") or {},
        }
        feedback_store.append_feedback(feedback_item)
        return jsonify({"success": True})
    except Exception as e:
        logger.exception("提交反馈失败")
        return jsonify({"success": False, "error": str(e)}), 500


@auto_test_api.route("/metrics_summary", methods=["GET"])
def api_metrics_summary():
    """v2.0：获取测试统计摘要"""
    summary = compute_summary()
    return jsonify({"success": True, "data": summary})
