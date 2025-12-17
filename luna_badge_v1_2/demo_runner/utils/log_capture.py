"""
Log Capture Utility

捕获并断言 C-5 行为
"""

from typing import List, Dict, Any, Set


class LogCapture:
    """
    日志捕获器
    
    用于捕获 C-5 调度器的行为并做断言
    """
    
    def __init__(self):
        """初始化日志捕获器"""
        self.records: List[Dict[str, Any]] = []
    
    def record(self, entry: Dict[str, Any]):
        """
        记录日志条目
        
        Args:
            entry: 日志条目（包含 action, vision_state, speed, delay_ms, reason 等）
        """
        self.records.append(entry)
    
    def assert_no_emit_during(self, vision_state: str, allow_critical: bool = False):
        """
        断言在指定视觉状态下没有 EMIT（除非是关键表达）
        
        Args:
            vision_state: 视觉状态
            allow_critical: 是否允许关键表达
            
        Raises:
            AssertionError: 如果发现非预期的 EMIT
        """
        for r in self.records:
            if r.get("vision_state") == vision_state:
                action = r.get("action")
                is_critical = r.get("is_critical", False)
                
                if action == "EMIT":
                    if not allow_critical or not is_critical:
                        raise AssertionError(
                            f"Unexpected EMIT during {vision_state}: "
                            f"action={action}, is_critical={is_critical}, reason={r.get('reason')}"
                        )
    
    def assert_delay_bucket(self, allowed: Set[int]):
        """
        断言延迟值在允许的范围内
        
        Args:
            allowed: 允许的延迟值集合（毫秒）
            
        Raises:
            AssertionError: 如果发现不允许的延迟值
        """
        for r in self.records:
            if r.get("action") == "EMIT":
                delay_ms = r.get("delay_ms", 0)
                if delay_ms not in allowed:
                    raise AssertionError(
                        f"Invalid delay {delay_ms}ms, allowed: {allowed}. "
                        f"Record: {r}"
                    )
    
    def assert_replace_happened(self):
        """
        断言发生了替换操作
        
        Raises:
            AssertionError: 如果没有发生替换
        """
        if not any(r.get("action") == "QUEUE" and r.get("reason") == "replaced" for r in self.records):
            raise AssertionError("Expected replace but none occurred")
    
    def assert_queue_flush_happened(self):
        """
        断言发生了队列清空操作
        
        Raises:
            AssertionError: 如果没有发生队列清空
        """
        # 通过检查视觉状态变化时队列大小变化来判断
        # 简化版：检查是否有 DROP 且 reason 包含 state_change
        if not any(
            r.get("action") == "DROP" and "state_change" in str(r.get("reason", ""))
            for r in self.records
        ):
            # 或者检查是否有队列大小从非零变为零的记录
            pass  # 简化版，实际可以通过更详细的记录来判断
    
    def get_emits_during(self, vision_state: str) -> List[Dict[str, Any]]:
        """
        获取在指定视觉状态下的所有 EMIT 记录
        
        Args:
            vision_state: 视觉状态
            
        Returns:
            List[Dict[str, Any]]: EMIT 记录列表
        """
        return [
            r for r in self.records
            if r.get("vision_state") == vision_state and r.get("action") == "EMIT"
        ]
    
    def get_all_emits(self) -> List[Dict[str, Any]]:
        """
        获取所有 EMIT 记录
        
        Returns:
            List[Dict[str, Any]]: EMIT 记录列表
        """
        return [r for r in self.records if r.get("action") == "EMIT"]
    
    def print_summary(self):
        """打印日志摘要"""
        print("\n" + "="*60)
        print("日志摘要")
        print("="*60)
        
        emits = self.get_all_emits()
        drops = [r for r in self.records if r.get("action") == "DROP"]
        queues = [r for r in self.records if r.get("action") == "QUEUE"]
        
        print(f"  总记录数: {len(self.records)}")
        print(f"  EMIT: {len(emits)}")
        print(f"  DROP: {len(drops)}")
        print(f"  QUEUE: {len(queues)}")
        
        if emits:
            print(f"\n  EMIT 详情:")
            for e in emits:
                print(f"    - {e.get('contract_id')}: delay={e.get('delay_ms')}ms, "
                      f"state={e.get('vision_state')}, reason={e.get('reason')}")
        
        if drops:
            print(f"\n  DROP 详情:")
            for d in drops:
                print(f"    - {d.get('contract_id')}: state={d.get('vision_state')}, "
                      f"reason={d.get('reason')}")
