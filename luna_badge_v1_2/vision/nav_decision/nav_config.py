"""
Navigation Decision Config (v1.3.0)

导航决策配置
"""

# 阈值参数
FORWARD_THRESHOLD = 0.5      # 向前直行的阈值
NARROW_THRESHOLD = 0.4       # 窄道检测阈值
RISK_BLOCK_THRESHOLD = 0.6   # 高风险阻挡阈值
STOP_THRESHOLD = 0.2         # 整体阻挡阈值（列平均分）

# 决策平滑
EMA_ALPHA = 0.6              # 决策平滑系数（0-1），越大越平滑

# 偏移阈值（用于判断 SLIGHT vs HARD）
SLIGHT_OFFSET_THRESHOLD = 1.2  # 偏移超过此值认为是 HARD

# 网格中心列索引（5列的中心是2）
CENTER_COLUMN = 2









