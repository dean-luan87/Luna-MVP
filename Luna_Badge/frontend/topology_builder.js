// frontend/topology_builder.js
/**
 * TopologyBuilder / 拓扑构建器
 * 把结构结果抽象成"拓扑点"
 * 输出：front_open / left_blocked / right_open / corridor_width / turn_hint
 */
(function () {
  'use strict';
  
  if (window.TopologyBuilder) return;

  function logDebug(msg, p) { window.logDebug?.('[TopologyBuilder] ' + msg, p || {}); }
  function logError(msg, p) { window.logError?.('[TopologyBuilder] ' + msg, p || {}); }

  function TopologyBuilderClass() {}

  /**
   * 输入：StructureAnalyzer 结果
   * 输出：拓扑结构（左右阻塞、中间是否开阔、是否走廊、是否转弯）
   */
  TopologyBuilderClass.prototype.build = function (structureInfo) {
    try {
      if (!structureInfo) return null;

      const {
        left_wall,
        right_wall,
        left_distance,
        right_distance,
        is_corridor,
        is_narrow,
        is_wide
      } = structureInfo;

      const frontOpen = !is_narrow || (!left_wall && !right_wall);

      const hint =
        is_corridor
          ? 'corridor'
          : is_wide
          ? 'open_area'
          : is_narrow
          ? 'narrow_passage'
          : 'normal';

      const result = {
        left_blocked: left_distance < 0.4,
        right_blocked: right_distance < 0.4,
        front_open: frontOpen,
        space_type: hint,
        width_m: left_distance + right_distance
      };

      logDebug('build result', result);
      return result;
    } catch (e) {
      logError('build error', e);
      return null;
    }
  };

  window.TopologyBuilder = new TopologyBuilderClass();

  if (window.logInfo) {
    window.logInfo('TopologyBuilder模块加载完成', { module: 'topology_builder' });
  } else {
    console.log('✅ TopologyBuilder模块加载完成', { module: 'topology_builder' });
  }
})();

