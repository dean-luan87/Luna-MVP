// frontend/sound_pack.js
// 简易声音包：根据严重程度播放不同 beep
// 在严重等级时，不只说话，还带一声"滴"或警报音

(function () {
  "use strict";
  if (window.SoundPack) return;

  function playBeep({ duration = 0.15, frequency = 1000, volume = 0.3 } = {}) {
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (!AudioContext) {
        console.warn("[SoundPack] Web Audio API 不可用");
        return;
      }

      const context = new AudioContext();
      const oscillator = context.createOscillator();
      const gainNode = context.createGain();

      oscillator.type = "sine";
      oscillator.frequency.value = frequency;
      gainNode.gain.value = volume;

      oscillator.connect(gainNode);
      gainNode.connect(context.destination);

      oscillator.start();

      setTimeout(function () {
        oscillator.stop();
        context.close();
      }, duration * 1000);
    } catch (e) {
      console.warn("[SoundPack] 播放 beep 失败:", e);
    }
  }

  const SoundPack = {
    /**
     * 播放声音
     * @param {string} severity - 严重程度: critical/warning/info/success
     */
    play(severity) {
      if (severity === "critical") {
        // 连续两声快速 beep（警报音）
        playBeep({ frequency: 1600, duration: 0.1, volume: 0.4 });
        setTimeout(function () {
          playBeep({ frequency: 1600, duration: 0.1, volume: 0.4 });
        }, 180);
      } else if (severity === "warning") {
        // 单声略低频（警告音）
        playBeep({ frequency: 1200, duration: 0.12, volume: 0.3 });
      } else if (severity === "info") {
        // 比较轻微，可以选择不提示
        // playBeep({ frequency: 800, duration: 0.1, volume: 0.2 });
      } else if (severity === "success") {
        // 成功提示音（可选）
        playBeep({ frequency: 1000, duration: 0.08, volume: 0.25 });
      }
    },

    /**
     * 播放自定义beep
     * @param {Object} options - 选项
     * @param {number} options.frequency - 频率（Hz）
     * @param {number} options.duration - 持续时间（秒）
     * @param {number} options.volume - 音量（0-1）
     */
    playCustom(options) {
      playBeep(options);
    },
  };

  window.SoundPack = SoundPack;

  // 自动集成到EventDispatcher（如果存在）
  if (window.EventDispatcher && typeof window.EventDispatcher.subscribe === "function") {
    window.EventDispatcher.subscribe(function (event) {
      if (event.type === "NAV_GUIDANCE" && event.severity) {
        SoundPack.play(event.severity);
      }
    });
  }

  // 自动集成到Hooks.onHazard（如果存在）
  if (window.Hooks && window.Hooks.onHazard && Array.isArray(window.Hooks.onHazard)) {
    window.Hooks.onHazard.push(function (data) {
      const severity = data.level === "critical" ? "critical" : 
                       data.level === "high" ? "warning" : "info";
      SoundPack.play(severity);
    });
  }

  console.log("[SoundPack] 声音包已加载");
})();



