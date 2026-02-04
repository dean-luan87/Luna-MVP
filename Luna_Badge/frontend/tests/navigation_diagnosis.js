// frontend/tests/navigation_diagnosis.js
// 导航 & 语音链路诊断脚本
// 使用方式：在控制台执行 runNavDiagnosis() 或 runNavigationDiagnosis()

(function () {
  'use strict';

  function log(msg, extra) {
    console.log('[NavDiagnosis] ' + msg, extra || {});
  }

  function safeGet(name) {
    try {
      return window[name];
    } catch (e) {
      return undefined;
    }
  }

  function testTTS() {
    const PriorityTTSQueue = safeGet('PriorityTTSQueue') || safeGet('priorityTTSQueue');
    const AudioPipeline = safeGet('AudioPipeline');
    const speakText = safeGet('speakText');

    log('开始测试 TTS 播报链路');

    // 优先使用统一入口
    if (typeof speakText === 'function') {
      speakText('这是导航诊断测试播报，如果你能听到，说明语音通路正常。', {
        source: 'NavDiagnosis',
        priority: 'test'
      });
      return 'used_speakText';
    }

    // 其次直接压入队列
    if (PriorityTTSQueue && typeof PriorityTTSQueue.enqueue === 'function') {
      PriorityTTSQueue.enqueue({
        type: 'TTS',
        text: '这是导航诊断测试播报，通过 TTS 队列发送。',
        meta: { source: 'NavDiagnosis', priority: 'test' }
      });
      // 如果 AudioPipeline 有 _drain 方法，手动触发一次
      if (AudioPipeline && typeof AudioPipeline._drain === 'function') {
        AudioPipeline._drain();
      }
      return 'used_PriorityTTSQueue';
    }

    log('⚠️ 未找到可用的 TTS 入口，请检查 AudioPipeline / PriorityTTSQueue / speakText 是否加载');
    return 'no_tts_entry';
  }

  function runNavigationDiagnosis() {
    log('=== 导航 & 语音自检开始 ===');

    const NavigationFSM = safeGet('NavigationFSM');
    const NavigationHook = safeGet('NavigationHook');
    const EventFlow = safeGet('EventFlow');
    const EventFlowPro = safeGet('EventFlowPro');
    const VisionBridge = safeGet('VisionBridge');
    const AutoRecovery = safeGet('AutoRecovery');
    const PriorityTTSQueue = safeGet('PriorityTTSQueue') || safeGet('priorityTTSQueue');
    const AudioPipeline = safeGet('AudioPipeline');
    const speakText = safeGet('speakText');

    const report = {
      nav: {
        hasNavigationFSM: !!NavigationFSM,
        hasHandleEvent:
          !!NavigationFSM && typeof NavigationFSM.handleEvent === 'function',
        hasNavigationHook: !!NavigationHook
      },
      eventFlow: {
        hasEventFlow: !!EventFlow,
        hasEventFlowPro: !!EventFlowPro
      },
      vision: {
        hasVisionBridge: !!VisionBridge
      },
      tts: {
        hasPriorityTTSQueue: !!PriorityTTSQueue,
        hasAudioPipeline: !!AudioPipeline,
        hasSpeakText: typeof speakText === 'function'
      },
      recovery: {
        hasAutoRecovery: !!AutoRecovery
      }
    };

    log('模块存在性检查结果：', report);

    // 1) 简单检查 NavigationFSM.handleEvent 是否存在
    if (!report.nav.hasNavigationFSM) {
      log('❌ NavigationFSM 未加载');
    } else if (!report.nav.hasHandleEvent) {
      log('❌ NavigationFSM.handleEvent 不存在，请确认 de_navigation_audio.js 是否为最新版本');
    } else {
      log('✅ NavigationFSM.handleEvent 存在');
    }

    // 2) 模拟发送一个 space_update_enhanced 事件
    if (NavigationFSM && typeof NavigationFSM.handleEvent === 'function') {
      const fakeSpaceUpdate = {
        type: 'space_update_enhanced',
        spaceState: {
          scene_type: 'corridor',
          overall_risk: 'low',
          nav_info: {
            goal_id: 'test_goal',
            distance_to_goal_m: 8,
            at_goal: false,
            reached_waypoint: true
          }
        }
      };
      try {
        NavigationFSM.handleEvent(fakeSpaceUpdate);
        log('✅ 已向 NavigationFSM 发送模拟 space_update_enhanced 事件');
      } catch (e) {
        log('❌ NavigationFSM.handleEvent 处理事件时异常', e);
      }
    }

    // 3) 测试 TTS 通路
    const ttsResult = testTTS();
    report.tts.testResult = ttsResult;

    log('=== 导航 & 语音自检结束 ===', report);

    return report;
  }

  // 挂到 window，提供两个名字
  window.runNavigationDiagnosis = runNavigationDiagnosis;
  window.runNavDiagnosis = runNavigationDiagnosis;

  log('诊断脚本已挂载，控制台可调用 runNavDiagnosis()');
})();
