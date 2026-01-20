"""
Image Corrector Config (v1.3.0)

图像补正配置

所有子模块可通过配置开关控制是否启用
"""

# ========== 模块开关 ==========

# 是否启用各子模块
ENABLE_RETINEX = True
ENABLE_HIGHLIGHT_COMPRESSION = True
ENABLE_DENOISE = True
ENABLE_SHARPEN = True
ENABLE_AI_RESTORER = False  # 1.3.0 默认关闭，1.4 可开启并加载模型

# ========== Retinex-Lite 参数 ==========

RETINEX_SIGMA = 60           # 高斯核 sigma
RETINEX_WEIGHT = 0.6         # 原图与 Retinex 融合权重

# ========== Highlight 压缩参数 ==========

HIGHLIGHT_THRESHOLD = 220    # 亮度超过此值视为高光
HIGHLIGHT_COMPRESSION_STRENGTH = 0.7  # 压缩强度（0-1）

# ========== 去噪参数（Fast Denoise）==========

DENOISE_H = 5                # h 参数（强度）
DENOISE_TEMPLATE_SIZE = 7    # 模板窗口大小
DENOISE_SEARCH_SIZE = 21     # 搜索窗口大小

# ========== 锐化参数 ==========

SHARPEN_STRENGTH = 0.7       # 锐化强度（0-1）

# ========== AI 修复（未来用）==========

AI_MODEL_PATH = ""           # 1.4 版本可填具体模型路径
AI_MAX_RESOLUTION = (640, 480)  # 超过则按比例缩放后送入模型

# ========== 调试 ==========

DEBUG_CORRECTOR = False
























