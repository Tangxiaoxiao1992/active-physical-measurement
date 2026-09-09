当前 `write_enabled` 仍未开启，因此按要求停止在只读核查阶段；没有尝试写文件、修改 bridge controls、运行会生成记录的测试或调用付费 API。

核查结论：

- 仓库内未发现 `AGENTS.md`。
- 未读取凭据文件、评分真值或隐藏标签。
- 未修改或覆盖任何历史实验记录。
- 实际修改文件：无。
- 新生成证据：无。
- 测试：未运行，因为当前 permission profile 仅允许读取。

现有缺口已由代码确认：

- `schemas/measurement_plan.schema.json` 缺少明确的端点配对、参考刻度方向、公式和计划置信度结构。
- `apm/core.py:281` 已校验 schema、bbox 范围和目标维度，但未完整校验 candidate point 边界、端点数量/方向与 length/width/thickness 的一致性。
- `apm/runner.py:63` 规划器只调用一次；现有 retry 是网络重试，不是把校验错误反馈给规划器的最多两次纠错。
- `apm/core.py:457` 的叠加图仅提供基础 bbox、点和部分工具线段，缺少完整的点/端点/刻度标签、参考连线和复算标注。
- `apm/core.py:436` 的木块端点工具只选最长 Hough 线，未提供高分辨率关键帧裁剪接口或维度方向约束。
- `configs/experiment.json` 将 `ruler_tick_calibration` 标记为 unavailable；`apm/core.py:495` 和 `apm/core.py:566` 仍直接返回模块不可用。

现有失败证据：

- `runs/apm_dev_round1_v1_full/attempts/B/Q015/repeat_01/validation.json`：两个无效 bbox，并含 schema 外字段。
- `runs/apm_dev_round1_v1_full/attempts/B/Q015/repeat_03/validation.json`：两个无效 bbox。
- `runs/apm_dev_round1_v1_full/attempts/B/Q017/repeat_03/validation.json`：五个无效 bbox，并含非法 `$schema` 字段。
- `runs/apm_dev_round1_v1_full/attempts/B/Q001/repeat_01/validation.json`：尺子标定工具不可用。
- 第一轮汇总见 `runs/apm_dev_round1_v1_full/report.md`：B 组规划有效并成功输出标量为 2/12，≤10% 为 2/12；Q001/Q002 的六次木块尝试均未成功，Q015 三次均无标量，Q017 两次成功、一次因计划无效失败。

恢复工作的必要配置：

- 在本地会话或 bridge 的 workspace permission profile 中为本仓库启用写权限，即将 `write_enabled` 打开（通常对应 `sandbox_mode = workspace-write` 或等价的 workspace read/write 设置）。
- 不需要开放凭据、答案文件或 scoring truth 给开发 runner。

写权限开启后建议先执行：

```powershell
cd active-physical-measurement
python -B -m unittest discover -s tests -v
```

然后实现 schema、两次规划纠错、可核查叠加图、高分辨率裁剪和最小 ruler tick calibration，再以新的唯一 run ID 对缓存样本运行本地验证；不要复用或覆盖 `apm_dev_round1_v1_full`。