// frontend/errors/ErrorCode.js
// 前端错误码体系

(function () {
  "use strict";
  if (window.ErrorCode) return;

  window.ErrorCode = {
    // 视觉相关
    YOLO_TIMEOUT: "E_VISION_TIMEOUT",
    YOLO_EMPTY: "E_VISION_EMPTY",
    YOLO_LOW_CONF: "E_VISION_LOW_CONF",

    // 场景图相关
    SCENE_NODE_FAIL: "E_SCENE_NODE_FAIL",
    SCENE_UPDATE_FAIL: "E_SCENE_UPDATE_FAIL",

    // 导航相关
    NAV_NO_ROUTE: "E_NAV_NO_ROUTE",
    NAV_STUCK: "E_NAV_STUCK",
    NAV_REROUTE_FAIL: "E_NAV_REROUTE_FAIL",

    // 任务链相关
    TASK_STEP_ERROR: "E_TASK_STEP_ERROR",
    TASK_ABORT: "E_TASK_ABORT",
    TASK_RECOVERY_FAIL: "E_TASK_RECOVERY_FAIL",

    // 系统错误
    SYS_MODULE_CRASH: "E_SYS_CRASH",
    SYS_RESTART: "E_SYS_RESTART",
    SYS_FORCE_RECOVER: "E_SYS_FORCE_RECOVER",
  };

  console.log("[ErrorCode] 前端错误码体系已加载");
})();

