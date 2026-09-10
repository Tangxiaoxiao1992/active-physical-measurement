本轮完成，坐标表达管线验证成功，已停止。

证据目录：`runs/qwen3_vl_anchor_integer_1000_resume_20260910_002/`

- 真实推理 **1 次**，修复 **0 次**；首次响应通过严格 JSON/schema。原始响应：`raw_response.txt`。
- 整数框：`[0,300,800,600]`。
- 未调整换算的半开像素框：`[0,144,683,288]`，合法、非退化。
- 与 target 的 IoU：`0.325844`；中心距离：`101.100198 px`；不完全相同。
- Overlay：`runs/qwen3_vl_anchor_integer_1000_resume_20260910_002/overlay.png`。
- 测试：基线 **45/45**，最终 **50/50**；证据为目录内 `test_results.json`。
- 实验无失败或权限阻塞；生成参数警告及辅助比较命令返回码已记入 `report.md`。

程序仅确认格式、坐标合法与几何关系。区域是否真正框住尺子：**待人工查看 overlay**。

完整报告：`runs/qwen3_vl_anchor_integer_1000_resume_20260910_002/report.md`。旧记录和桥控制未改，未发布。