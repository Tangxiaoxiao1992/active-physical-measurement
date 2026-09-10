已按停止条件结束恢复，未重新推理。

- 指定 seq19 原目录不存在，读取失败为 `FileNotFoundError / WinError 3`。旧轮响应、调用状态和修复预算无法确定。
- 同一项目独占锁已取得，覆盖全部恢复证据操作后释放。
- 原图 SHA256 与 seq18 一致；相关测试 **19/19 通过**。
- 新推理 **0 次**、新修复 **0 次**；旧轮调用总数未知。无新框、指标或 overlay；推理耗时及显存不可得。记录与测试耗时 **0.175 秒**。

报告及证据位于：
`active-physical-measurement/runs/qwen3_vl_anchor_crop_recovery_20260910_002/`

其中 `report.md` 为最终报告，`failure.json` 记录阻断原因，`source_manifest.json` 和 `test_results.json` 提供来源及测试证据。

下一步需找回 seq19 原证据目录及执行记录，再持同一锁核验。未发布文件、修改桥控制或覆盖旧记录；未认定尺子定位成功。