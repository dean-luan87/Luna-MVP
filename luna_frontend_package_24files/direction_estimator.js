// frontend/direction_estimator.js
// 方向估计：根据 bbox 横向位置判断 leftFront / front / rightFront

(function () {
  "use strict";
  if (window.calcDirection) return;

  /**
   * 根据 bbox 横向位置判断方向
   * @param {Object} bbox - 边界框 {x1, y1, x2, y2}，坐标范围 0~1
   * @returns {string} "leftFront" | "front" | "rightFront"
   */
  window.calcDirection = function (bbox) {
    if (!bbox || typeof bbox.x1 !== "number" || typeof bbox.x2 !== "number") {
      console.warn("[DirectionEstimator] Invalid bbox:", bbox);
      return "front"; // 默认值
    }

    const center = (bbox.x1 + bbox.x2) / 2; // 0~1 屏幕相对坐标

    if (center < 0.33) return "leftFront";
    if (center < 0.66) return "front";
    return "rightFront";
  };

  console.log("[DirectionEstimator] 方向估计算法已加载");
})();

