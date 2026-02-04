// frontend/speech_policy.js
// 统一文案策略（SpeechPolicy）

(function () {
  "use strict";
  if (window.SpeechPolicy) return;

  window.SpeechPolicy = {
    getHazardMessage(type) {
      const map = {
        obstacle: "前方有障碍物，请注意安全。",
        person: "前方有人接近，请注意避让。",
        vehicle: "前方有车辆经过，请特别小心。",
        stepDown: "前方是下台阶，请注意脚下落差。",
        stepUp: "前方是上台阶，请抬脚注意高度。",
        stairs: "前方有楼梯，请注意台阶。",
        door: "前方有门，请注意。",
        elevator: "前方有电梯，请注意。",
        crowd: "前方人群较多，请放慢速度。",
        narrow: "前方通道较窄，请小心通过。",
      };
      return map[type] || "请注意前方情况。";
    },

    getNavigationMessage(action, direction, distance) {
      if (action === "turn") {
        return `前方${distance || ""}米${direction === "left" ? "左" : "右"}转`;
      } else if (action === "straight") {
        return `请直行${distance ? distance + "米" : ""}`;
      } else if (action === "stop") {
        return "已到达目的地";
      }
      return "请跟随导航指引";
    },

    getStepMessage(direction, distance) {
      if (direction === "up") {
        return `前方${distance || ""}米有上台阶，请抬脚注意高度。`;
      } else if (direction === "down") {
        return `前方${distance || ""}米有下台阶，请注意脚下落差。`;
      }
      return `前方${distance || ""}米有台阶，请注意。`;
    },

    /**
     * v1.1.1 新增：根据方向 + 距离 + 类型生成更拟人的提示语句
     * @param {Object} params - {type, direction, distance}
     * @param {string} params.type - 危险类型 (obstacle/person/vehicle/stepUp/stepDown)
     * @param {string} params.direction - 方向 (leftFront/front/rightFront)
     * @param {number|null} params.distance - 距离（米）
     * @returns {string} 拟人化提示语句
     */
    getHazardSentence({ type, direction, distance }) {
      const dirMap = {
        leftFront: "左前方",
        front: "正前方",
        rightFront: "右前方",
      };

      const dirText = dirMap[direction] || "前方";

      const distText = distance
        ? distance < 0.5
          ? "半米内"
          : distance < 1.0
          ? "1米内"
          : `${distance.toFixed(1)}米处`
        : "前方";

      const typeMap = {
        obstacle: "有障碍物",
        person: "有人接近",
        vehicle: "有车辆经过",
        stepUp: "是上台阶",
        stepDown: "是下台阶",
        stairs: "有楼梯",
        door: "有门",
        elevator: "有电梯",
        crowd: "人群较多",
        narrow: "通道较窄",
      };

      const t = typeMap[type] || "情况不明";

      return `${dirText}${distText}${t}，请注意。`;
    },
  };

  console.log("[SpeechPolicy] 统一文案策略已加载");
})();

