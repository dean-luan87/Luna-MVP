"""
Hazard Detector Config (v1.3.0)

危险因素检测配置

参数化配置，支持未来扩展到任意 N×M 网格
"""

# 网格大小（与 grid_slicer 保持一致）
TILE_ROWS = 3
TILE_COLS = 5

# 阈值参数
EDGE_DENSITY_THRESHOLD = 0.15        # 边缘密度阈值
TEXTURE_JUMP_THRESHOLD = 40          # 纹理跳跃阈值
SHAPE_ABNORMAL_THRESHOLD = 0.12      # 形状异常阈值

# 风险权重（L2 融合）
W_EDGE = 0.35                        # 边缘密度权重
W_TEXTURE = 0.30                     # 纹理跳跃权重
W_SHAPE = 0.35                       # 形状异常权重

# 边缘检测参数
SOBEL_KSIZE = 3                      # Sobel 核大小
EDGE_MAG_THRESHOLD = 50              # 边缘幅值阈值

# 纹理分析参数
LBP_POINTS = 8                       # LBP 采样点数
LBP_RADIUS = 1                       # LBP 采样半径

# 形状分析参数
MIN_CONTOUR_AREA = 10                # 最小轮廓面积













