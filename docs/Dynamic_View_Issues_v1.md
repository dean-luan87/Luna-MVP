## Dynamic View v1 工作清单（Issue / Checklist）

### 🅰️ Dynamic View v1（必须完成）

A1. 建立模块骨架  
- 新建 dynamic_view/ 目录  
- 放入 types.py / entity.py / state_machine.py / engine.py / scheduler.py  
- 能被 import，不报错

A2. 状态机正确性  
- 覆盖状态流转：  
  - NOT_SEEN → APPEARED  
  - APPEARED → STABLE  
  - STABLE → INVISIBLE  
  - INVISIBLE → RECOVERED  
  - INVISIBLE → DISAPPEARED（TTL）  
- 禁止 STABLE → DISAPPEARED 直跳

A3. Observation Scheduler v1  
- 支持 request / revoke  
- priority / ttl 字段齐全  
- 不读取任何证据

A4. Observer 插件示例  
- BaseObserver 抽象类  
- ElevatorObserver（stub，返回假 evidence）  
- TrafficLightObserver（stub）

A5. Engine 对外接口  
- stable_world_state() 可被 C 读取  
- 不返回 INVISIBLE / APPEARED  
- 不直接触发任何动作

---

### 🅱️ 对接准备（不立即做，但要留口）
- C 模块改为只读 stable_world_state  
- Task Engine 未来订阅状态变化事件  
- Debug / RA-View 可读取全量状态
