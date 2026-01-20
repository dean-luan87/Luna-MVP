# -*- coding: utf-8 -*-
"""
Luna 实体徽章 MVP 配置文件
"""

import os

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 模型路径配置
MODEL_PATHS = {
    'yolo': {
        'model_path': os.path.join(PROJECT_ROOT, 'models', 'yolov8n.pt'),
        'confidence_threshold': 0.5,
        'classes': ['person', 'car', 'truck', 'bus', 'bicycle', 'motorcycle', 'stop sign', 'traffic light']
    },
    'paddleocr': {
        'use_angle_cls': True,
        'lang': 'ch',
        'use_gpu': False
    },
    'qwen2_vl': {
        'api_key': 'your_api_key_here',  # 需要替换为实际的API密钥
        'api_url': 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation',
        'model_name': 'qwen2-vl-plus'
    },
    'whisper': {
        'model_size': 'base',
        'language': 'zh'
    },
    'tts': {
        'engine': 'pyttsx3',  # 可选: pyttsx3, edge-tts
        'language': 'zh',
        'rate': 150
    }
}

# 摄像头配置
CAMERA_CONFIG = {
    'camera_index': 0,  # 默认摄像头索引
    'width': 640,
    'height': 480,
    'fps': 30
}

# 日志配置
LOG_CONFIG = {
    'log_dir': os.path.join(PROJECT_ROOT, 'logs'),
    'log_file': 'luna_recognition.log',
    'json_log_file': 'luna_recognition.json',
    'max_log_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# 处理配置
PROCESSING_CONFIG = {
    'process_interval': 2.0,  # 处理间隔（秒）
    'max_detection_objects': 10,  # 最大检测物体数量
    'max_ocr_text_length': 100,  # 最大OCR文本长度
    'description_max_length': 200  # 最大描述长度
}

# 调试配置（v1.8.4: Risk Debug Snapshot）
DEBUG_CONFIG = {
    "enable_risk_debug": True,  # 是否启用 Risk 调试快照日志输出（测试时启用）
    "enable_risk_console": False,  # 是否启用 Risk 调试控制台输出（P0.5，暂不实现）
    # "enable_risk_overlay": False,  # 是否启用 Risk 调试 Overlay（P1，v1.8.5+，暂不实现）
}

# Shadow Mode 配置（v1.8.4: 真实模型接入第一阶段）
# Shadow Mode = 只打日志，不播报
# 正确顺序：模型输出 → RiskAdvisoryService → RiskDebugSnapshot（日志） → 人工/离线验证 → 确认稳定后开启播报
RISK_SHADOW_MODE = False  # True = 只打日志，不播报；False = 正常播报

# 输出配置
OUTPUT_CONFIG = {
    'print_results': True,
    'play_audio': True,
    'save_json': True,
    'show_camera_feed': True
}



# Global log level (default INFO; override via env LOG_LEVEL)
LOG_LEVEL = __import__('os').environ.get('LOG_LEVEL', 'INFO')

# V1.8.1: Observer Mode 配置
# 可以通过环境变量 OBSERVER_MODE_ENABLED 覆盖
OBSERVER_MODE_ENABLED = os.environ.get('OBSERVER_MODE_ENABLED', 'false').lower() == 'true'
