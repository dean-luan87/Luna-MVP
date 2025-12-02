// frontend/distance_estimator.js
// 距离估计（简单版）：根据 bbox 高度推测粗略距离

(function () {
  "use strict";
  if (window.calcDistance) return;

  /**
   * 根据 bbox 高度推测粗略距离
   * @param {Object} bbox - 边界框 {x1, y1, x2, y2}，坐标范围 0~1
   * @returns {number|null} 距离（米），如果太远则返回 null
   */
  window.calcDistance = function (bbox) {
    if (!bbox || typeof bbox.y1 !== "number" || typeof bbox.y2 !== "number") {
      console.warn("[DistanceEstimator] Invalid bbox:", bbox);
      return null;
    }

    const h = bbox.y2 - bbox.y1; // 0~1

    if (h > 0.45) return 0.3; // 30cm 以内
    if (h > 0.20) return 0.8; // 80cm 左右
    if (h > 0.10) return 1.2; // 1.2m+

    return null; // 太远，不报具体距离
  };

  console.log("[DistanceEstimator] 距离估计算法已加载");
})();



