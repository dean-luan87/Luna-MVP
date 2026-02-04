# Bring-Up A-1 ～ A-5 Issue 模板清单（v1）

以下内容为可直接复制进 Cursor 的 Issue 模板。  
格式：Issue 标题 → 目标 → 工作内容 → 交付物 → 验收标准

---

## A-1｜固定系统主循环（System Main Loop）

目标  
系统具备唯一、稳定的运行入口，可在无任何外部输入情况下持续运行。

工作内容  
- 明确系统运行模式（tick 或 event-driven，二选一）
- 实现唯一 main_loop / run() 入口
- 每个循环包含：
  - tick_id
  - timestamp
  - snapshot 生成点
  - trace 写入点

交付物  
- runtime/main_loop.py（或等价文件）
- 固定的 TICK_INTERVAL 或事件驱动说明

验收标准  
- 系统在无任何真实输入下运行 ≥30 分钟不崩
- Trace 中可看到连续 tick 记录
- 不存在多个并行主循环

---

## A-2｜Trace / DebugView 输出骨架（空内容可）

目标  
系统拥有统一、稳定、可扩展的观测输出通道。

工作内容  
- 建立 trace 写入模块（jsonl）
- 每个 tick 写入一条 trace
- Trace 至少包含：
  - timestamp
  - tick_id
  - system_snapshot（可为空结构）

交付物  
- observe/trace_writer.py
- 自动生成的 runs/*.jsonl

验收标准  
- Trace 文件持续增长
- Trace 结构在 30 分钟运行内不发生变化
- 后续模块仅需“填字段”，不需要改 trace 结构

---

## A-3｜system_snapshot P0 结构冻结

目标  
定义并冻结“唯一世界事实来源”，为后续所有模块提供统一读写入口。

工作内容  
- 定义 system_snapshot P0 schema（允许字段为空）
- 明确 snapshot 的创建、更新、读取接口
- 禁止任何模块私有维护“世界状态”

建议 P0 结构  
```
{
  "time": "...",
  "self_state": {},
  "perception_facts": {},
  "navigation_state": {},
  "device_state": {},
  "task_state": {},
  "health": {}
}
```

交付物  
- core/system_snapshot.py
- snapshot lifecycle 接口（create / update）

验收标准  
- 每个 tick 都生成 snapshot
- snapshot 被完整写入 trace
- 后续模块只能通过 snapshot 获取状态

---

## A-4｜Empty Fixtures 运行（无真实世界）

目标  
系统在“空世界”下也能完整运行，支持回放与复现。

工作内容  
- 定义 empty fixtures（无摄像头 / 无 GPS / 无 OCR）
- fixtures 可指定运行时长
- fixtures 可驱动 main loop

交付物  
- tests/fixtures/empty_world.json
- tools/run_from_fixtures.py（如已有则复用）

验收标准  
- 使用 fixtures 可启动系统
- 可生成 trace
- 不依赖任何外部设备或服务

---

## A-5｜Health / Heartbeat（存活监测）

目标  
系统可明确判断“是否仍在运行”，为后续异常处理打基础。

工作内容  
- 每个 tick 更新 health 信息：
  - last_tick_time
  - loop_alive = true
- health 写入 system_snapshot

交付物  
- health/heartbeat.py（或内嵌于 main loop）

验收标准  
- Trace 中可看到 health 字段持续更新
- 停止运行时 health 状态可明确识别

---

## A 部分整体 Gate（Cursor Milestone）

只有当以下 5 条全部满足，才允许进入 B（语言输出）：
- 无任何真实输入可运行 ≥30 分钟
- 每个 tick 都有 trace
- system_snapshot 结构稳定
- fixtures 可复现完整运行
- 新模块只需读写 snapshot 即可接入
