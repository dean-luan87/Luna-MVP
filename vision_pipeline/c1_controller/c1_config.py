"""
C1 Controller Configuration (Phase C1 - Parameter Freeze v0.1)

⚠️ 重要约束：
- This config is frozen for Phase C1.
- Any adaptive logic must be implemented in Phase C2+.
- DO NOT MODIFY AT RUNTIME
- 禁止任何 runtime 修改（setattr, reload, deepcopy 后修改）
- 不允许 import torch / numpy / cv2
- 只能是常量 + dataclass（可选）
"""

from dataclasses import dataclass

# =========================
# Frame Sampling Control
# =========================

MIN_FPS = 1
MAX_FPS = 5

FPS_CHANGE_COOLDOWN_SEC = 2.0
MAX_FPS_DELTA_PER_STEP = 1

# =========================
# Motion / Stability Guard
# =========================

MOTION_SCORE_THRESHOLD = 0.7
MOTION_SUSTAIN_TIME_SEC = 0.5

RECOVERY_MOTION_THRESHOLD = 0.3
RECOVERY_STABLE_TIME_SEC = 1.0

# =========================
# Flicker / Malicious Guard
# =========================

FRAME_DIFF_LOW_THRESHOLD = 0.05
STATIC_DIFF_THRESHOLD = 0.05  # 静态遮挡阈值（与 FRAME_DIFF_LOW_THRESHOLD 相同）
STATIC_FRAMES_THRESHOLD = 10  # 连续低 diff 帧数阈值

FRAME_DIFF_HIGH_FREQ_COUNT = 5   # 频闪检测：高频跳变次数
FLICKER_COUNT_THRESHOLD = 5  # 频闪检测阈值（与 FRAME_DIFF_HIGH_FREQ_COUNT 相同）

PROTECTION_MODE_DURATION_SEC = 3.0

# =========================
# Observation Priority (Frozen)
# =========================

PRIORITY_SAFETY = 1.0
PRIORITY_NAVIGATION = 0.7
PRIORITY_ENVIRONMENT = 0.3

# =========================
# Scene Privacy Policy
# =========================

CLASS_A_PUBLIC = "allow_camera"
CLASS_B_SEMI_PRIVATE = "allow_with_user_consent"
CLASS_C_PRIVATE = "force_camera_off"

# =========================
# Execution Mode
# =========================

# Phase C1 Active Mode v0.1: 仅控制 ModelingExecutor 执行
# - Shadow Mode: False（已升级为 Active Mode）
# - 控制范围：仅 ModelingExecutor（LV4.2）
# - 不允许控制：fps、抽帧频率、路由
C1_MODE_SHADOW_ONLY = False

# =========================
# Logging Control
# =========================

LOG_INTERVAL_SEC = 0.5

# =========================
# Decision Rhythm Control
# =========================

# C1 决策产出间隔（秒）
# 这是节律闸门：不是每帧都产生 decision，而是到了节律点或强制事件才产出
DECISION_INTERVAL_SEC = 0.5

# C1 心跳间隔（秒）
# 即使没有状态变化，也需要定期输出决策以保持系统活跃度
HEARTBEAT_INTERVAL_SEC = 2.0

