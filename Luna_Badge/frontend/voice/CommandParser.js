// frontend/voice/CommandParser.js
// 精简版：适用于 Luna Badge v1.1.0 的最小可用语音交互

(function () {
  'use strict';

  if (window.CommandParser) return;

  function speak(text) {
    if (typeof window.speakText === 'function') {
      window.speakText(text, { source: 'CommandParser' });
    }
    window.LastTTSText = text;
  }

  function clean(text) {
    return text.replace(/\s+/g, '').toLowerCase();
  }

  function getTimeText() {
    const d = new Date();
    return `现在是${d.getHours()}点${d.getMinutes()}分`;
  }

  window.CommandParser = {
    handleASR(raw) {
      if (!raw) return;
      const t = clean(raw);

      //------------------------------------------------
      // 1）基础唤醒
      //------------------------------------------------
      if (t.includes('你在吗') || t.includes('luna')) {
        return speak('我在的，你说。');
      }

      if (t.includes('你好') || t.includes('您好')) {
        return speak('你好呀，我在这里。');
      }

      //------------------------------------------------
      // 2）时间查询
      //------------------------------------------------
      if (t.includes('几点') || t.includes('时间')) {
        return speak(getTimeText());
      }

      //------------------------------------------------
      // 3）导航控制（极简）
      //------------------------------------------------
      if (t.includes('开始导航')) {
        if (window.NavigationFSM?.startNavigation) {
          window.NavigationFSM.startNavigation();
        }
        return speak('好的，开始导航。');
      }

      if (t.includes('停止导航') || t.includes('结束导航')) {
        if (window.NavigationFSM?.stop) {
          window.NavigationFSM.stop();
        }
        return speak('导航已停止。');
      }

      //------------------------------------------------
      // 4）场景问询类（v2.0新增）
      //------------------------------------------------
      if (t.includes('看到什么') || t.includes('现在是什么地方') || t.includes('环境怎么样')) {
        if (window.describeCurrentScene && typeof window.describeCurrentScene === "function") {
          window.describeCurrentScene(true); // 自动播报
          return speak('正在观察周围环境，请稍等。');
        }
        return speak('场景描述功能暂时不可用。');
      }
      if (t.includes('有没有人') || t.includes('附近有人吗')) {
        // TODO: 调用场景问答接口
        return speak('场景问答功能开发中。');
      }
      if (t.includes('有没有楼梯') || t.includes('前面是不是楼梯')) {
        // TODO: 调用场景问答接口
        return speak('场景问答功能开发中。');
      }
      if (t.includes('有没有洗手间') || t.includes('厕所')) {
        // TODO: 调用场景问答接口
        return speak('场景问答功能开发中。');
      }

      //------------------------------------------------
      // 5）重复上一句
      //------------------------------------------------
      if (t.includes('再说一次') || t.includes('重复')) {
        if (window.LastTTSText) return speak(window.LastTTSText);
        return speak('我刚才没有说话。');
      }

      //------------------------------------------------
      // 6）简单回应
      //------------------------------------------------
      if (t.includes('谢谢')) {
        return speak('不客气。');
      }

      if (t.includes('你还好吗')) {
        return speak('我很好。');
      }

      // 其他均不处理
      console.log('[CommandParser] 未匹配指令:', raw);
      return null;
    }
  };

  console.log('✅ 精简版 CommandParser 已加载');
})();
