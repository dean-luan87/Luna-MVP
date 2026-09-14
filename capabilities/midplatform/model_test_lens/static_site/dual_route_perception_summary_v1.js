/**
 * Dual route perception — compact metrics summary line.
 */
(function (global) {
  "use strict";

  function summaryLine(dualRoutePkg) {
    if (!dualRoutePkg || !dualRoutePkg.dual_route_comparison_candidate) return "";
    var cmp = dualRoutePkg.dual_route_comparison_candidate;
    return "dual_route: " + (cmp.agreement_level || "—") +
      " · next: " + (cmp.recommended_followup_route || "—") +
      " · candidate_only";
  }

  global.DualRoutePerceptionSummary = {
    version: "dual_route_perception_summary_v1",
    summaryLine: summaryLine
  };
})(typeof window !== "undefined" ? window : this);
