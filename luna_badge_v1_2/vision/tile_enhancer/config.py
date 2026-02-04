"""
Tile Enhancer Config (v1.3.0)

局部关键区增强配置

参数化配置，支持未来扩展到任意 N×M 网格
"""

# 网格大小（可扩展到 3×7、5×9 等）
TILE_ROWS = 3
TILE_COLS = 5

# 阈值参数
BRIGHTNESS_THRESHOLD = 60      # 低光阈值
CONTRAST_THRESHOLD = 25        # 低对比度阈值
NOISE_THRESHOLD = 12           # 噪声阈值

# 增强开关
ENABLE_CLAHE = True            # 启用 CLAHE 对比度增强
ENABLE_GAMMA = True            # 启用 Gamma 校正
ENABLE_BILATERAL = True        # 启用双边滤波去噪

# Gamma 校正参数
GAMMA_VALUE = 1.4              # Gamma 值（>1 提亮）

# CLAHE 参数
CLAHE_CLIP_LIMIT = 2.0         # CLAHE clip limit
CLAHE_TILE_GRID_SIZE = (8, 8)  # CLAHE tile grid size

# Bilateral Filter 参数
BILATERAL_D = 3                # 滤波直径
BILATERAL_SIGMA_COLOR = 15     # 颜色空间标准差
BILATERAL_SIGMA_SPACE = 15     # 坐标空间标准差
























