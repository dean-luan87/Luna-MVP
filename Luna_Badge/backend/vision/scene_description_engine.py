#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
场景元素抽取与基础推理引擎（不负责自然语言，只负责结构化信息）
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# 多模型融合相关导入（可选，失败不影响原有功能）
try:
    from backend.vision.scene_fusion_engine import SceneFusionEngine
    from backend.vision.local_vision_adapter import LocalVisionAdapter
    from backend.vision.cloud_vision_adapter import CloudVisionAdapter
    from config.vision_fusion_config import VisionFusionConfig
    FUSION_AVAILABLE = True
except Exception as e:
    FUSION_AVAILABLE = False
    logger.warning(f"多模型融合模块导入失败，将使用原有逻辑: {e}")


class SceneDescriptionEngine:
    """
    负责把 YOLO / 视觉模块的结果，转换成「场景元素」和「基础标签」。
    不做复杂 NLG，只做：
      - 物体 / 文字 / 设施 / 危险 / 台阶 / 人群
      - 场景类型粗分类（室内/室外/走廊/大厅 等）
    """

    def __init__(
        self,
        vision_engine=None,
        signboard_detector=None,
        facility_detector=None,
        hazard_detector=None,
        step_detector=None,
        crowd_density_detector=None,
    ):
        self.vision_engine = vision_engine
        self.signboard_detector = signboard_detector
        self.facility_detector = facility_detector
        self.hazard_detector = hazard_detector
        self.step_detector = step_detector
        self.crowd_density_detector = crowd_density_detector
        self.initialized = True
        
        # ✅ 新增：本地 + 云端融合引擎
        self.fusion_engine = None
        if FUSION_AVAILABLE:
            try:
                local_adapter = LocalVisionAdapter(vision_engine=self.vision_engine, ocr_engine=None)
                cloud_adapter = CloudVisionAdapter()
                self.fusion_engine = SceneFusionEngine(local_adapter, cloud_adapter)
                logger.info("✅ SceneDescriptionEngine: 多模型融合引擎已初始化")
            except Exception as e:
                logger.warning(f"⚠️ SceneDescriptionEngine: 多模型融合引擎初始化失败: {e}")
                self.fusion_engine = None
        
        logger.info("✅ SceneDescriptionEngine 初始化完成")

    # ======= 对外主入口 =======

    def analyze_scene(self, image_np) -> Dict[str, Any]:
        """
        综合调用各视觉模块，输出统一结构：
        {
          objects: [...],
          texts: [...],
          facilities: [...],
          signboards: [...],
          hazards: [...],
          step: {...} or None,
          crowd: {...} or None,
          scene_tags: [...],
          quick_summary: "一段简短文字"
        }
        """
        result: Dict[str, Any] = {
            "objects": [],
            "texts": [],
            "facilities": [],
            "signboards": [],
            "hazards": [],
            "step": None,
            "crowd": None,
            "scene_tags": [],
            "quick_summary": "",
        }

        # 1) 基础视觉识别
        if self.vision_engine is not None:
            try:
                vres = self.vision_engine.detect_and_recognize(image_np)
                result["objects"] = vres.get("detections", []) or []
                result["texts"] = vres.get("ocr_results", []) or []
            except Exception as e:
                # 不抛出异常，避免整条链路挂掉
                result["vision_error"] = str(e)

        # 2) 标识牌
        if self.signboard_detector is not None:
            try:
                # SignboardDetector 的方法名是 detect_signboard (单数)
                if hasattr(self.signboard_detector, "detect_signboard"):
                    s_res = self.signboard_detector.detect_signboard(image_np) or []
                elif hasattr(self.signboard_detector, "detect_signboards"):
                    s_res = self.signboard_detector.detect_signboards(image_np) or []
                else:
                    s_res = []
                result["signboards"] = [self._safe_to_dict(r) for r in s_res]
            except Exception as e:
                result["signboard_error"] = str(e)

        # 3) 公共设施
        if self.facility_detector is not None:
            try:
                f_res = self.facility_detector.detect_facility(image_np) or []
                result["facilities"] = [self._safe_to_dict(r) for r in f_res]
            except Exception as e:
                result["facility_error"] = str(e)

        # 4) 危险区域
        if self.hazard_detector is not None:
            try:
                # 这里如果有 YOLO 结果可以传入，但为了简单，用 None
                h_res = self.hazard_detector.detect_hazards(image_np, detected_objects=None) or []
                result["hazards"] = [self._safe_to_dict(h) for h in h_res]
            except Exception as e:
                result["hazard_error"] = str(e)

        # 5) 台阶
        if self.step_detector is not None:
            try:
                step_res = self.step_detector.detect_step(image_np)
                if step_res:
                    # step_res 本身通常就是 dict
                    result["step"] = step_res
            except Exception as e:
                result["step_error"] = str(e)

        # 6) 人群密度
        if self.crowd_density_detector is not None:
            try:
                # 从检测结果中提取人员位置
                person_positions = []
                for obj in result.get("objects", []):
                    if obj.get("class") in ("person", "人"):
                        bbox = obj.get("bbox") or obj.get("box")
                        if bbox and isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
                            center_x = (bbox[0] + bbox[2]) / 2
                            center_y = (bbox[1] + bbox[3]) / 2
                            person_positions.append((float(center_x), float(center_y)))
                
                if person_positions and image_np is not None:
                    image_shape = (image_np.shape[0], image_np.shape[1])  # (height, width)
                    c_res = self.crowd_density_detector.detect_density(person_positions, image_shape)
                    if c_res:
                        result["crowd"] = self._safe_to_dict(c_res)
            except Exception as e:
                result["crowd_error"] = str(e)

        # 7) 场景类型推理 + 简要总结
        tags = self._infer_scene_tags(result)
        result["scene_tags"] = tags
        result["quick_summary"] = self._build_quick_summary(result, tags)

        return result

    # ======= 内部小工具 =======

    def _safe_to_dict(self, obj: Any) -> Dict[str, Any]:
        """兼容 .to_dict() / __dict__ / str(obj) 三种情况"""
        if obj is None:
            return {}
        if hasattr(obj, "to_dict"):
            try:
                return obj.to_dict()
            except Exception:
                pass
        if hasattr(obj, "__dict__"):
            try:
                return dict(obj.__dict__)
            except Exception:
                pass
        # 兜底：只给一个字符串表示
        return {"value": str(obj)}

    def _collect_all_texts(self, result: Dict[str, Any]) -> str:
        """收集 OCR 文本 + 标识牌 label，串成一个大字符串用于规则匹配"""
        texts: List[str] = []

        for t in result.get("texts") or []:
            if isinstance(t, dict):
                txt = t.get("text") or t.get("content") or ""
                if txt:
                    texts.append(str(txt))

        for sb in result.get("signboards") or []:
            if isinstance(sb, dict):
                label = sb.get("label") or sb.get("text") or ""
                if label:
                    texts.append(str(label))

        return " ".join(texts)

    def _infer_scene_tags(self, result: Dict[str, Any]) -> List[str]:
        """
        非常简单的规则推理：
        - 室内 / 室外
        - 医院 / 商场 / 地铁 / 洗手间 / 走廊 / 大厅 等
        后续可以不断追加规则，但不用改 API 结构。
        """
        tags: List[str] = []

        all_text = self._collect_all_texts(result).lower()

        # 粗分类：室内 vs 室外（非常粗略）
        indoor_keywords = ["电梯", "出口", "收银", "挂号", "候诊", "大厅", "站台", "商场", "超市", "地铁", "卫生间", "洗手间"]
        outdoor_keywords = ["马路", "人行道", "crosswalk", "十字路口", "广场", "park", "公园"]

        if any(k.lower() in all_text for k in indoor_keywords):
            tags.append("indoor")
        if any(k.lower() in all_text for k in outdoor_keywords):
            tags.append("outdoor")

        # 医院
        hospital_keywords = ["医院", "挂号", "候诊", "门诊", "急诊", "科室", "取号机"]
        if any(k.lower() in all_text for k in hospital_keywords):
            tags.append("hospital")

        # 商场 / 超市
        mall_keywords = ["商场", "购物中心", "超市", "收银", "收银台", "收款台"]
        if any(k.lower() in all_text for k in mall_keywords):
            tags.append("mall")

        # 地铁 / 站台
        metro_keywords = ["地铁", "站台", "railway", "platform", "xx线", "号线"]
        if any(k.lower() in all_text for k in metro_keywords):
            tags.append("metro")

        # 洗手间
        wc_keywords = ["厕所", "卫生间", "洗手间", "restroom", "toilet", "wc"]
        if any(k.lower() in all_text for k in wc_keywords):
            tags.append("restroom")

        # 走廊（结合结构类词）
        corridor_keywords = ["走廊", "通道", "corridor"]
        if any(k.lower() in all_text for k in corridor_keywords):
            tags.append("corridor")

        # 大厅
        hall_keywords = ["大厅", "大厅服务台", "服务台", "大厅入口"]
        if any(k.lower() in all_text for k in hall_keywords):
            tags.append("hall")

        # 危险相关
        if result.get("hazards"):
            tags.append("hazard_present")
        if result.get("step"):
            tags.append("step_present")
        if result.get("crowd"):
            tags.append("crowded")

        # 去重
        tags = list(dict.fromkeys(tags))
        return tags

    def _build_quick_summary(self, result: Dict[str, Any], tags: List[str]) -> str:
        """规则拼接一个一句话描述，用于前端快速展示"""
        if not tags:
            return "当前场景信息有限，我会尽量帮你描述周围环境。"

        parts: List[str] = []

        # 场景主体
        if "hospital" in tags:
            parts.append("你现在大概率在医院环境附近")
        elif "mall" in tags:
            parts.append("你现在大概率在商场或超市附近")
        elif "metro" in tags:
            parts.append("你现在大概率在地铁相关区域")
        elif "restroom" in tags:
            parts.append("你附近应该有洗手间")
        elif "corridor" in tags:
            parts.append("你可能在一条走廊或通道里")
        elif "hall" in tags:
            parts.append("你可能在一个大厅区域")

        # 室内/室外
        if "indoor" in tags and "outdoor" not in tags:
            parts.append("整体环境更像室内")
        elif "outdoor" in tags and "indoor" not in tags:
            parts.append("整体环境更像室外")

        # 危险 / 台阶 / 人群
        if "hazard_present" in tags:
            parts.append("画面中检测到一些需要注意的风险")
        if "step_present" in tags:
            parts.append("前方可能存在台阶或高度落差")
        if "crowded" in tags:
            parts.append("人比较多，环境有点拥挤")

        if not parts:
            return "我已经识别了当前画面，可以随时帮你描述更具体的内容。"

        return "，".join(parts) + "。"

    # ===== 兼容旧接口 =====
    def describe(self, image_np, nav_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """兼容旧接口，调用 analyze_scene"""
        return self.analyze_scene(image_np)
