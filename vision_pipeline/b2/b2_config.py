"""
B2 v0.1 Configuration

参数先定死，后面 v0.2 再开放调参
"""

# B2 v0.1 启用开关
B2_V01_ENABLED = True

# 触发：世界变化阈值（0~1），越小越敏感
B2_DIGEST_DELTA_THRESHOLD = 0.25

# 触发：最长沉默（秒），即使世界不变也避免"永不输出"
B2_MAX_SILENCE_SEC = 12.0

# 未来缓存窗口（秒）
B2_HORIZON_SEC_DEFAULT = 6.0

# FutureBuffer TTL（秒）
B2_BUFFER_TTL_SEC = 6.0

# 日志
B2_LOG_INTERVAL_SEC = 2.0  # B2 输出事件记录的最小间隔（避免刷屏）

