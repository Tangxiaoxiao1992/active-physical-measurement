修复与零模型调用重放已完成，成功判据全部满足。

- 首次响应：SHA-256 `326a2b993139d2dda77a69c35ffd8ab5b0529a394363e9dec317937d98fb8c72`；围栏 JSON；已剥离；JSON/schema 有效；bbox `[214,440,789,680]`
- 修复响应：SHA-256 `74b908a3a551a00fb0e1709fdd4cb5266fbb106aa43744b3720fa77de55f3373`；围栏 JSON；已剥离；JSON/schema 有效；bbox `[212,440,788,688]`
- 选中首次响应：原推理无需修复，仅需确定性去围栏
- 归一化 bbox：`[214,440,789,680]`
- 854×480 半开像素 bbox：`[183,211,674,326]`
- 数值未改变；未夹取、调整、重排或猜测
- Overlay：`active-physical-measurement/runs/qwen3_vl_normalized_json_fence_replay_20260909_001/overlay.png`
- 测试：修改前 33/33、专项 7/7、最终全量 36/36 通过
- 新失败：无；历史失败仅为 Markdown 围栏导致严格 JSON 入口解析失败
- 模型调用：0

完整证据位于：

`active-physical-measurement/runs/qwen3_vl_normalized_json_fence_replay_20260909_001/`

其中包含 `replay_validation.json`、`source_references.json`、`selected_response.json`、`bbox_px.json`、`test_results.json`、`report.md` 和 `bridge_status.json`。

程序仅确认格式去围栏、schema、坐标换算和 overlay 管线可执行；目标面语义正确性仍等待人工查看 overlay。未修改 prompt、原始证据、评分真值、metric_anchor 或桥接控制。