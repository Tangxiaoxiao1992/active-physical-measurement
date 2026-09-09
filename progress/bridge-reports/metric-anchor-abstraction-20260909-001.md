已完成 metric anchor 泛化改造，未读取或修改评分真值，未调用付费 API，未改 bridge、既有实验记录或交互式台球流程，也未执行 git push。

主要修改：

- `active-physical-measurement/schemas/measurement_plan.schema.json`
  - 升级至 schema v3。
  - 新增完整 `metric_anchor`：物理先验、视觉 primitive、support region、锚点、方向、平面/深度关系、适用条件和置信度。
  - 新增规范化 `measurement_equation`。
- `active-physical-measurement/apm/metric_anchors.py`
  - 新建按 `visual_primitive` 注册和路由的后端接口。
  - 实现 `periodic_ticks` 与 `known_segment`。
  - 其余四种 primitive 明确返回 `unsupported_visual_primitive`。
- `active-physical-measurement/apm/core.py`
  - 核心流程不再依赖 ruler 名称或 ruler 专用工具。
  - 验证单位、方向和平行度、共面、深度、透视适用性、目标维度适用性及方程操作数绑定。
  - 程序根据 `metric_scale_ratio` 执行最终计算。
- `active-physical-measurement/prompts/measurement_planner_zh.txt`
  - 改为先抽取题目物理先验，再寻找对应视觉结构。
- `active-physical-measurement/configs/experiment.json`
  - 注册通用 `metric_anchor_measure` 工具和相关配置。
- `active-physical-measurement/scripts/offline_e2e_demo.py`
  - 离线演示迁移至 v3 通用锚点接口。
- `active-physical-measurement/tests/test_core.py`
  - 新增尺子周期刻度、非尺子周期标记、已知线段、unsupported primitive 和几何验证负例。
- `active-physical-measurement/docs/metric_anchor_v3.md`
  - 记录接口、后端扩展和兼容性规则。
- `active-physical-measurement/README.md`
  - 更新 v3 使用与迁移说明。

验证结果：

```text
python -m unittest discover -s tests -v
Ran 13 tests in 0.762s
OK
```

三种表面形式均归一化为包含 `known_quantity`、`observed_quantity`、`metric_scale`、`backend` 和 `confidence` 的相同接口；尺子名称和非尺子名称调用相同周期检测后端。已知线段也通过同一方程完成离线端到端木块计算。

兼容性影响：v2 的 `reference`、`ruler_tick_calibration`、`ruler_calibrated_dimension` 和 `geometry.formula` 计划需要迁移；既有 `runs/` 记录未改写。历史评分兼容逻辑保留。

尚未实现：`known_object_extent`、`grid_or_lattice`、`depth_reference`、`temporal_interval`。它们目前只能显式报告 unsupported。

下一步木块实验：为真实开发集木块帧制作不含答案和硬编码坐标的 v3 可审计计划，优先验证锚点与目标边的共面、同深度和平行证据；随后仅运行离线视觉后端与程序方程，并将真实失败案例作为新实验记录保存。