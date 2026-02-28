"""
测试路由 (Test Routes) v1.2.0
提供功能测试、场景模拟、性能监控等测试接口
"""

from flask import Blueprint, request, jsonify
from core.response import ok, error
from config.error_codes import ERR
from services.runtime import rt
import time
import logging
import json

logger = logging.getLogger(__name__)

test_bp = Blueprint("test", __name__, url_prefix="/api/test")


# ==================== ① 实时视觉调试 ====================

@test_bp.route('/vision/debug', methods=['POST'])
def vision_debug():
    """
    视觉调试接口
    返回：原始画面 + YOLO检测框 + OCR结果 + 场景描述
    """
    try:
        # 获取图像
        if 'image' in request.files:
            file = request.files['image']
            image_bytes = file.read()
        elif request.is_json:
            data = request.get_json() or {}
            from utils.image_utils import decode_base64_image
            image_b64 = data.get('image')
            if not image_b64:
                return error(ERR.NAV_IO_001, "缺少image参数")
            image_bytes = decode_base64_image(image_b64)
            if image_bytes is None:
                return error(ERR.NAV_IO_002, "图片解码失败")
        else:
            return error(ERR.NAV_IO_001, "缺少图片数据")

        import numpy as np
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(image_bytes))
        image_np = np.array(img)
        if len(image_np.shape) == 3 and image_np.shape[2] == 4:
            image_np = image_np[:, :, :3]

        start_time = time.time()
        results = {}

        # 1. YOLO检测
        yolo_start = time.time()
        detections = []
        if hasattr(rt, 'vision_engine') and rt.vision_engine:
            try:
                v_res = rt.vision_engine.detect_and_recognize(image_np)
                detections = v_res.get('detections', [])
                results['ocr_results'] = v_res.get('ocr_results', [])
            except Exception as e:
                logger.warning(f"YOLO检测失败: {e}")
                results['yolo_error'] = str(e)
        yolo_time = (time.time() - yolo_start) * 1000
        results['yolo'] = {
            'detections': detections,
            'count': len(detections),
            'latency_ms': round(yolo_time, 2)
        }

        # 2. 危险检测
        hazards = []
        if hasattr(rt, 'hazard_detector') and rt.hazard_detector:
            try:
                hazards_raw = rt.hazard_detector.detect_hazards(image_np, detected_objects=detections)
                hazards = [h.to_dict() if hasattr(h, 'to_dict') else h for h in hazards_raw] if hazards_raw else []
            except Exception as e:
                logger.warning(f"危险检测失败: {e}")
        results['hazards'] = hazards

        # 3. 台阶检测
        step_result = None
        if hasattr(rt, 'step_detector') and rt.step_detector:
            try:
                step_result = rt.step_detector.detect_step(image_np)
            except Exception as e:
                logger.warning(f"台阶检测失败: {e}")
        results['step'] = step_result

        # 4. 标识牌检测
        signboards = []
        if hasattr(rt, 'signboard_detector') and rt.signboard_detector:
            try:
                signboards_raw = rt.signboard_detector.detect_signboards(image_np)
                signboards = [s.to_dict() if hasattr(s, 'to_dict') else s for s in signboards_raw] if signboards_raw else []
            except Exception as e:
                logger.warning(f"标识牌检测失败: {e}")
        results['signboards'] = signboards

        # 5. 场景描述
        scene_description = None
        try:
            from modules.scene_description.description_engine import SceneDescriptionEngine
            scene_engine = SceneDescriptionEngine()
            scene_description = scene_engine.describe(
                objects=detections,
                texts=results.get('ocr_results', []),
                hazards=hazards,
                facilities=[],
                env_features={}
            )
        except Exception as e:
            logger.warning(f"场景描述失败: {e}")

        total_time = (time.time() - start_time) * 1000

        return ok({
            'total_latency_ms': round(total_time, 2),
            'yolo': results['yolo'],
            'ocr': results.get('ocr_results', []),
            'hazards': hazards,
            'step': step_result,
            'signboards': signboards,
            'scene_description': scene_description,
            'performance': {
                'yolo_ms': round(yolo_time, 2),
                'total_ms': round(total_time, 2),
                'fps': round(1000 / total_time, 2) if total_time > 0 else 0
            }
        })
    except Exception as e:
        logger.exception(f"视觉调试接口异常: {e}")
        return error(ERR.NAV_VIS_001, f"视觉调试失败: {str(e)}")


# ==================== ② 功能测试台 ====================

@test_bp.route('/feature/yolo', methods=['POST'])
def test_yolo():
    """YOLO目标检测测试"""
    try:
        if 'image' not in request.files:
            return error(ERR.NAV_IO_001, "缺少image文件")
        
        file = request.files['image']
        image_bytes = file.read()
        
        import numpy as np
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(image_bytes))
        image_np = np.array(img)
        if len(image_np.shape) == 3 and image_np.shape[2] == 4:
            image_np = image_np[:, :, :3]

        start = time.time()
        if hasattr(rt, 'vision_engine') and rt.vision_engine:
            result = rt.vision_engine.detect_and_recognize(image_np)
            latency = (time.time() - start) * 1000
            
            return ok({
                'detections': result.get('detections', []),
                'count': len(result.get('detections', [])),
                'latency_ms': round(latency, 2),
                'request_body': {'image': 'multipart/form-data'},
                'response_format': 'standard'
            })
        else:
            return error(ERR.VISION_NOT_READY, "视觉引擎未初始化")
    except Exception as e:
        logger.exception(f"YOLO测试失败: {e}")
        return error(ERR.NAV_VIS_001, f"YOLO测试失败: {str(e)}")


@test_bp.route('/feature/ocr', methods=['POST'])
def test_ocr():
    """OCR文字识别测试"""
    try:
        if 'image' not in request.files:
            return error(ERR.NAV_IO_001, "缺少image文件")
        
        file = request.files['image']
        image_bytes = file.read()
        
        import numpy as np
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(image_bytes))
        image_np = np.array(img)
        if len(image_np.shape) == 3 and image_np.shape[2] == 4:
            image_np = image_np[:, :, :3]

        start = time.time()
        if hasattr(rt, 'vision_engine') and rt.vision_engine:
            result = rt.vision_engine.detect_and_recognize(image_np)
            ocr_results = result.get('ocr_results', [])
            latency = (time.time() - start) * 1000
            
            return ok({
                'ocr_results': ocr_results,
                'texts': [r.get('text', '') for r in ocr_results],
                'count': len(ocr_results),
                'latency_ms': round(latency, 2)
            })
        else:
            return error(ERR.VISION_NOT_READY, "视觉引擎未初始化")
    except Exception as e:
        logger.exception(f"OCR测试失败: {e}")
        return error(ERR.NAV_VIS_002, f"OCR测试失败: {str(e)}")


@test_bp.route('/feature/hazard', methods=['POST'])
def test_hazard():
    """危险检测测试"""
    try:
        if 'image' not in request.files:
            return error(ERR.NAV_IO_001, "缺少image文件")
        
        file = request.files['image']
        image_bytes = file.read()
        
        import numpy as np
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(image_bytes))
        image_np = np.array(img)
        if len(image_np.shape) == 3 and image_np.shape[2] == 4:
            image_np = image_np[:, :, :3]

        start = time.time()
        if hasattr(rt, 'hazard_detector') and rt.hazard_detector:
            # 先获取检测结果
            detections = []
            if hasattr(rt, 'vision_engine') and rt.vision_engine:
                try:
                    v_res = rt.vision_engine.detect_and_recognize(image_np)
                    detections = v_res.get('detections', [])
                except:
                    pass
            
            hazards_raw = rt.hazard_detector.detect_hazards(image_np, detected_objects=detections)
            hazards = [h.to_dict() if hasattr(h, 'to_dict') else h for h in hazards_raw] if hazards_raw else []
            latency = (time.time() - start) * 1000
            
            return ok({
                'hazards': hazards,
                'count': len(hazards),
                'latency_ms': round(latency, 2),
                'severity_summary': {
                    'critical': sum(1 for h in hazards if h.get('severity') == 'critical'),
                    'warning': sum(1 for h in hazards if h.get('severity') == 'warning'),
                    'info': sum(1 for h in hazards if h.get('severity') == 'info')
                }
            })
        else:
            return error(ERR.NAV_ENV_003, "危险检测器未初始化")
    except Exception as e:
        logger.exception(f"危险检测测试失败: {e}")
        return error(ERR.NAV_ENV_003, f"危险检测测试失败: {str(e)}")


@test_bp.route('/feature/step', methods=['POST'])
def test_step():
    """台阶检测测试"""
    try:
        if 'image' not in request.files:
            return error(ERR.NAV_IO_001, "缺少image文件")
        
        file = request.files['image']
        image_bytes = file.read()
        
        import numpy as np
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(image_bytes))
        image_np = np.array(img)
        if len(image_np.shape) == 3 and image_np.shape[2] == 4:
            image_np = image_np[:, :, :3]

        start = time.time()
        if hasattr(rt, 'step_detector') and rt.step_detector:
            result = rt.step_detector.detect_step(image_np)
            latency = (time.time() - start) * 1000
            
            return ok({
                'step_detection': result,
                'detected': bool(result),
                'latency_ms': round(latency, 2)
            })
        else:
            return error(ERR.NAV_ENV_001, "台阶检测器未初始化")
    except Exception as e:
        logger.exception(f"台阶检测测试失败: {e}")
        return error(ERR.NAV_ENV_001, f"台阶检测测试失败: {str(e)}")


@test_bp.route('/feature/navigation', methods=['POST'])
def test_navigation():
    """导航功能测试"""
    try:
        data = request.get_json() or {}
        action = data.get('action', 'status')
        
        if not hasattr(rt, 'navigation_manager') or rt.navigation_manager is None:
            return error(ERR.NAV_NOT_READY, "导航管理器未初始化")
        
        nav = rt.navigation_manager
        
        if action == 'status':
            status = nav.get_status()
            return ok({
                'status': status,
                'is_idle': nav.is_idle() if hasattr(nav, 'is_idle') else True
            })
        elif action == 'start':
            destination = data.get('destination', '测试目的地')
            route_segments = data.get('route_segments', [])
            success = nav.start_navigation(destination, route_segments) if hasattr(nav, 'start_navigation') else False
            return ok({
                'success': success,
                'status': nav.get_status()
            })
        elif action == 'stop':
            nav.cancel('测试停止') if hasattr(nav, 'cancel') else None
            return ok({'status': nav.get_status()})
        else:
            return error(ERR.NAV_GENERAL_001, f"未知action: {action}")
    except Exception as e:
        logger.exception(f"导航测试失败: {e}")
        return error(ERR.NAV_ENGINE_ERROR, f"导航测试失败: {str(e)}")


@test_bp.route('/feature/tts', methods=['POST'])
def test_tts():
    """TTS语音合成测试"""
    try:
        data = request.get_json() or {}
        text = data.get('text', '这是一次TTS测试。')
        voice = data.get('voice', 'zh-CN-XiaoxiaoNeural')
        rate = data.get('rate', '+0%')
        
        if hasattr(rt, 'tts_manager') and rt.tts_manager:
            start = time.time()
            audio_b64 = rt.tts_manager.synthesize(text, voice, rate)
            latency = (time.time() - start) * 1000
            
            return ok({
                'audio': audio_b64,
                'text_length': len(text),
                'latency_ms': round(latency, 2),
                'voice': voice,
                'rate': rate
            })
        else:
            return error(ERR.TTS_ENGINE_ERROR, "TTS引擎未初始化")
    except Exception as e:
        logger.exception(f"TTS测试失败: {e}")
        return error(ERR.TTS_SYNTH_FAIL, f"TTS测试失败: {str(e)}")


# ==================== ③ 联动场景模拟 ====================

@test_bp.route('/scenario/street_navigation', methods=['POST'])
def scenario_street_navigation():
    """
    场景A：街道路况导航
    模拟：启动导航 → 逐帧更新 → 检测危险 → 转弯 → 偏航纠正
    """
    try:
        data = request.get_json() or {}
        frames = data.get('frames', [])  # 多帧图像数据（base64数组）
        
        if not frames:
            return error(ERR.NAV_GENERAL_001, "缺少frames参数")
        
        results = []
        nav_started = False
        
        for i, frame_b64 in enumerate(frames):
            frame_result = {
                'frame_index': i,
                'timestamp': time.time()
            }
            
            # 解码图像
            from utils.image_utils import decode_base64_image
            image_np = decode_base64_image(frame_b64)
            if image_np is None:
                frame_result['error'] = '图片解码失败'
                results.append(frame_result)
                continue
            
            # 第一帧：启动导航
            if i == 0 and not nav_started:
                if hasattr(rt, 'navigation_manager') and rt.navigation_manager:
                    rt.navigation_manager.start_navigation('测试目的地', [])
                    nav_started = True
                    frame_result['action'] = 'navigation_started'
            
            # 视觉检测
            detections = []
            hazards = []
            if hasattr(rt, 'vision_engine') and rt.vision_engine:
                try:
                    v_res = rt.vision_engine.detect_and_recognize(image_np)
                    detections = v_res.get('detections', [])
                except:
                    pass
            
            if hasattr(rt, 'hazard_detector') and rt.hazard_detector:
                try:
                    hazards_raw = rt.hazard_detector.detect_hazards(image_np, detected_objects=detections)
                    hazards = [h.to_dict() if hasattr(h, 'to_dict') else h for h in hazards_raw] if hazards_raw else []
                except:
                    pass
            
            frame_result['detections'] = len(detections)
            frame_result['hazards'] = len(hazards)
            
            # 导航更新
            if nav_started and hasattr(rt, 'navigation_manager'):
                try:
                    nav_status = rt.navigation_manager.get_status()
                    frame_result['nav_status'] = nav_status.get('state', 'unknown')
                except:
                    pass
            
            results.append(frame_result)
        
        return ok({
            'scenario': 'street_navigation',
            'total_frames': len(frames),
            'frames': results,
            'summary': {
                'navigation_started': nav_started,
                'total_detections': sum(r.get('detections', 0) for r in results),
                'total_hazards': sum(r.get('hazards', 0) for r in results)
            }
        })
    except Exception as e:
        logger.exception(f"街道路况导航场景测试失败: {e}")
        return error(ERR.NAV_STRAT_001, f"场景测试失败: {str(e)}")


@test_bp.route('/scenario/indoor_navigation', methods=['POST'])
def scenario_indoor_navigation():
    """
    场景B：室内导航（医院/商场/地铁）
    模拟：OCR提取信息 → 识别导视牌 → 构建拓扑图
    """
    try:
        data = request.get_json() or {}
        frames = data.get('frames', [])
        scene_type = data.get('scene_type', 'hospital')  # hospital / mall / subway
        
        if not frames:
            return error(ERR.NAV_GENERAL_001, "缺少frames参数")
        
        results = []
        ocr_texts = []
        signboards = []
        
        for i, frame_b64 in enumerate(frames):
            from utils.image_utils import decode_base64_image
            image_np = decode_base64_image(frame_b64)
            if image_np is None:
                continue
            
            frame_result = {'frame_index': i}
            
            # OCR识别
            if hasattr(rt, 'vision_engine') and rt.vision_engine:
                try:
                    v_res = rt.vision_engine.detect_and_recognize(image_np)
                    ocr_results = v_res.get('ocr_results', [])
                    texts = [r.get('text', '') for r in ocr_results]
                    ocr_texts.extend(texts)
                    frame_result['ocr_texts'] = texts
                except:
                    pass
            
            # 标识牌识别
            if hasattr(rt, 'signboard_detector') and rt.signboard_detector:
                try:
                    signs_raw = rt.signboard_detector.detect_signboards(image_np)
                    signs = [s.to_dict() if hasattr(s, 'to_dict') else s for s in signs_raw] if signs_raw else []
                    signboards.extend(signs)
                    frame_result['signboards'] = signs
                except:
                    pass
            
            results.append(frame_result)
        
        # 场景描述
        scene_desc = None
        try:
            from modules.scene_description.description_engine import SceneDescriptionEngine
            scene_engine = SceneDescriptionEngine()
            scene_desc = scene_engine.describe(
                objects=[],
                texts=[{'text': t} for t in ocr_texts],
                hazards=[],
                facilities=[],
                env_features={}
            )
        except:
            pass
        
        return ok({
            'scenario': 'indoor_navigation',
            'scene_type': scene_type,
            'total_frames': len(frames),
            'ocr_texts': list(set(ocr_texts)),  # 去重
            'signboards': signboards,
            'scene_description': scene_desc,
            'frames': results
        })
    except Exception as e:
        logger.exception(f"室内导航场景测试失败: {e}")
        return error(ERR.NAV_STRAT_001, f"场景测试失败: {str(e)}")


@test_bp.route('/scenario/life_scenarios', methods=['POST'])
def scenario_life_scenarios():
    """
    场景C：生活场景
    模拟：找服务台、找洗手间、找电梯等
    """
    try:
        data = request.get_json() or {}
        scenario = data.get('scenario', 'find_service_desk')  # find_service_desk / find_restroom / find_elevator
        frame_b64 = data.get('image')
        
        if not frame_b64:
            return error(ERR.NAV_IO_001, "缺少image参数")
        
        from utils.image_utils import decode_base64_image
        image_np = decode_base64_image(frame_b64)
        if image_np is None:
            return error(ERR.NAV_IO_002, "图片解码失败")
        
        result = {
            'scenario': scenario,
            'found': False,
            'details': {}
        }
        
        # OCR识别
        ocr_texts = []
        if hasattr(rt, 'vision_engine') and rt.vision_engine:
            try:
                v_res = rt.vision_engine.detect_and_recognize(image_np)
                ocr_results = v_res.get('ocr_results', [])
                ocr_texts = [r.get('text', '') for r in ocr_results]
            except:
                pass
        
        # 根据场景类型判断
        if scenario == 'find_service_desk':
            keywords = ['服务台', '咨询', 'service', 'desk']
            found_texts = [t for t in ocr_texts if any(kw in t for kw in keywords)]
            result['found'] = len(found_texts) > 0
            result['details'] = {'matched_texts': found_texts}
        
        elif scenario == 'find_restroom':
            keywords = ['洗手间', '卫生间', '厕所', 'toilet', 'restroom']
            found_texts = [t for t in ocr_texts if any(kw in t for kw in keywords)]
            result['found'] = len(found_texts) > 0
            result['details'] = {'matched_texts': found_texts}
        
        elif scenario == 'find_elevator':
            keywords = ['电梯', 'elevator', 'lift']
            found_texts = [t for t in ocr_texts if any(kw in t for kw in keywords)]
            result['found'] = len(found_texts) > 0
            result['details'] = {'matched_texts': found_texts}
        
        return ok(result)
    except Exception as e:
        logger.exception(f"生活场景测试失败: {e}")
        return error(ERR.NAV_STRAT_001, f"场景测试失败: {str(e)}")


@test_bp.route('/scenario/task_chain', methods=['POST'])
def scenario_task_chain():
    """
    场景D：多任务链联动
    模拟：导航 → 上厕所 → 恢复导航
    """
    try:
        data = request.get_json() or {}
        tasks = data.get('tasks', [])  # 任务序列
        
        if not tasks:
            return error(ERR.NAV_GENERAL_001, "缺少tasks参数")
        
        results = []
        current_task = None
        
        for i, task in enumerate(tasks):
            task_result = {
                'task_index': i,
                'task_type': task.get('type'),
                'status': 'pending'
            }
            
            if task.get('type') == 'navigation':
                # 导航任务
                if hasattr(rt, 'navigation_manager') and rt.navigation_manager:
                    destination = task.get('destination', '测试目的地')
                    rt.navigation_manager.start_navigation(destination, [])
                    task_result['status'] = 'running'
                    current_task = 'navigation'
            
            elif task.get('type') == 'find_restroom':
                # 找洗手间（中断导航）
                if current_task == 'navigation':
                    if hasattr(rt, 'navigation_manager'):
                        rt.navigation_manager.pause('找洗手间')
                    task_result['status'] = 'running'
                    current_task = 'find_restroom'
            
            elif task.get('type') == 'resume_navigation':
                # 恢复导航
                if current_task == 'find_restroom':
                    if hasattr(rt, 'navigation_manager'):
                        rt.navigation_manager.resume()
                    task_result['status'] = 'running'
                    current_task = 'navigation'
            
            results.append(task_result)
        
        return ok({
            'scenario': 'task_chain',
            'tasks': results,
            'current_task': current_task,
            'summary': {
                'total_tasks': len(tasks),
                'completed': sum(1 for r in results if r['status'] == 'completed')
            }
        })
    except Exception as e:
        logger.exception(f"任务链场景测试失败: {e}")
        return error(ERR.NAV_STRAT_001, f"场景测试失败: {str(e)}")


# ==================== ④ 实时日志 + 性能监控 ====================

@test_bp.route('/performance/metrics', methods=['GET'])
def performance_metrics():
    """性能指标获取"""
    try:
        metrics = {
            'timestamp': time.time(),
            'modules': {}
        }
        
        # 视觉引擎性能
        if hasattr(rt, 'vision_engine') and rt.vision_engine:
            metrics['modules']['vision'] = {
                'ready': True,
                'model_loaded': hasattr(rt.vision_engine, 'model') and rt.vision_engine.model is not None
            }
        
        # 导航管理器性能
        if hasattr(rt, 'navigation_manager') and rt.navigation_manager:
            metrics['modules']['navigation'] = {
                'ready': True,
                'is_idle': rt.navigation_manager.is_idle() if hasattr(rt.navigation_manager, 'is_idle') else True
            }
        
        # TTS引擎性能
        if hasattr(rt, 'tts_manager') and rt.tts_manager:
            metrics['modules']['tts'] = {
                'ready': True
            }
        
        # 系统性能
        try:
            import psutil
            process = psutil.Process()
            metrics['system'] = {
                'memory_mb': round(process.memory_info().rss / 1024 / 1024, 2),
                'cpu_percent': process.cpu_percent(interval=0.1)
            }
        except:
            metrics['system'] = {'error': 'psutil不可用'}
        
        return ok(metrics)
    except Exception as e:
        logger.exception(f"性能指标获取失败: {e}")
        return error(ERR.SYSTEM_METRIC_FAIL, f"性能指标获取失败: {str(e)}")


@test_bp.route('/logs/recent', methods=['GET'])
def recent_logs():
    """获取最近的日志"""
    try:
        log_path = "logs/system.log"
        import os
        if not os.path.exists(log_path):
            return ok({'logs': [], 'count': 0})
        
        lines = []
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()[-100:]  # 最近100条
        
        logs = []
        for line in lines:
            try:
                log_entry = json.loads(line.strip())
                logs.append(log_entry)
            except:
                # 如果不是JSON格式，直接添加原始文本
                logs.append({'raw': line.strip()})
        
        return ok({
            'logs': logs,
            'count': len(logs),
            'source': log_path
        })
    except Exception as e:
        logger.exception(f"日志获取失败: {e}")
        return error(ERR.NAV_SYS_003, f"日志获取失败: {str(e)}")


@test_bp.route('/logs/errors', methods=['GET'])
def error_logs():
    """获取错误日志"""
    try:
        log_path = "logs/errors.log"
        import os
        if not os.path.exists(log_path):
            return ok({'errors': [], 'count': 0})
        
        lines = []
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()[-50:]  # 最近50条错误
        
        errors = []
        for line in lines:
            try:
                error_entry = json.loads(line.strip())
                errors.append(error_entry)
            except:
                errors.append({'raw': line.strip()})
        
        return ok({
            'errors': errors,
            'count': len(errors),
            'source': log_path
        })
    except Exception as e:
        logger.exception(f"错误日志获取失败: {e}")
        return error(ERR.NAV_SYS_003, f"错误日志获取失败: {str(e)}")


# ==================== 导航模拟测试 ====================

@test_bp.route('/navigation/simulate_step', methods=['POST'])
def simulate_navigation_step():
    """模拟导航步骤（用于测试）"""
    try:
        data = request.get_json() or {}
        step = data.get('step', 'go_straight')
        
        if not hasattr(rt, 'navigation_manager') or rt.navigation_manager is None:
            return error(ERR.NAV_NOT_READY, "导航管理器未初始化")
        
        nav = rt.navigation_manager
        
        # 模拟步骤处理
        step_actions = {
            'turn_left': {'action': 'turn_left', 'angle': -90, 'message': '左转'},
            'turn_right': {'action': 'turn_right', 'angle': 90, 'message': '右转'},
            'go_straight': {'action': 'go_straight', 'distance': 10, 'message': '直行'},
            'turn_around': {'action': 'turn_around', 'angle': 180, 'message': '掉头'}
        }
        
        step_info = step_actions.get(step, {'action': step, 'message': '未知步骤'})
        
        # 获取当前状态
        status = nav.get_status()
        
        return ok({
            'step': step,
            'step_info': step_info,
            'current_status': status,
            'simulated': True,
            'message': f'模拟执行: {step_info["message"]}'
        })
    except Exception as e:
        logger.exception(f"导航步骤模拟失败: {e}")
        return error(ERR.NAV_ENGINE_ERROR, f"模拟失败: {str(e)}")


# ==================== 音频测试 ====================

@test_bp.route('/audio/test_wakeup', methods=['POST'])
def test_wakeup():
    """测试唤醒词识别"""
    try:
        data = request.get_json() or {}
        text = data.get('text', 'Luna你在吗')
        
        # 检查前端CommandParser是否可用
        # 这里只是返回测试结果，实际处理在前端
        wakeup_keywords = ['luna', '你在吗', '在不在', '在吗']
        detected = any(kw in text.lower() for kw in wakeup_keywords)
        
        return ok({
            'text': text,
            'detected': detected,
            'wakeup_keywords': wakeup_keywords,
            'message': '唤醒词测试（实际处理在前端CommandParser）'
        })
    except Exception as e:
        logger.exception(f"唤醒词测试失败: {e}")
        return error(ERR.NAV_GENERAL_001, f"测试失败: {str(e)}")

