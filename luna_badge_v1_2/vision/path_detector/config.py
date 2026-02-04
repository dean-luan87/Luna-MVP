"""
Path Detector Config (v1.3.0)

可走路径识别配置
"""

# 网格大小（与 grid_slicer 保持一致）
TILE_ROWS = 3
TILE_COLS = 5

# 权重参数
COLOR_WEIGHT = 0.40       # 颜色相似度权重
TEXTURE_WEIGHT = 0.30     # 纹理相似度权重
EDGE_WEIGHT = 0.20        # 边缘权重
SHAPE_WEIGHT = 0.10       # 形状权重

# 阈值参数
COLOR_THRESHOLD = 0.55    # 颜色相似度阈值
TEXTURE_THRESHOLD = 0.50  # 纹理相似度阈值
WALKABLE_THRESHOLD = 0.55  # 最终可走性阈值

# F4 风险排除阈值
RISK_REJECT_THRESHOLD = 0.35  # 风险超过此值则不可走

# 多帧平滑
SMOOTH_ALPHA = 0.4        # 平滑系数（0-1）

# 底部区域提取（用于建立地面模型）
BOTTOM_RATIO = 0.25       # 底部 25% 区域用于建立地面模型

# 边缘检测参数
EDGE_MAG_THRESHOLD = 40   # 边缘幅值阈值

# KMeans 聚类参数
KMEANS_N_CLUSTERS = 2     # 颜色聚类数量
KMEANS_BATCH_SIZE = 2048  # 批处理大小

# LBP 直方图参数
LBP_HIST_BINS = 32        # LBP 直方图 bin 数量
























