只读诊断完成：**未证实路径基准错误；seq19 是否开始或完成推理仍为未知。**

所有路径均相对于配置工作区 `.`。为缩短引用，下文：
- `P` = `active-physical-measurement`
- `E18` = `P/runs/qwen3_vl_anchor_integer_1000_resume_20260910_002`
- `E20` = `P/runs/qwen3_vl_anchor_crop_recovery_20260910_002`

当前目录就是配置工作区；`git rev-parse` 返回非 Git 仓库，`P/.git` 也不存在。`README.md` 标识 QuantiPhy 验证集，`P/README.md` 标识主动物理测量子项目。`runs/` 与 `P/runs/` 均存在。工作区内未找到 `AGENTS.md`；检查的可选 `.agents/AGENTS.md`、`.codex/AGENTS.md`、`.cursor/rules` 也不存在，未向工作区外查找。

证据存在情况：

| 序列 | 结果 | 相对证据路径 |
|---|---|---|
| 18 | 有推理完成证据：记录一次生成、未修复，并有原始响应 | `E18/generation_started.json`、`E18/inference.json`、`E18/raw_response.txt` |
| 19 | 有脚本及内嵌 prompt；未找到可归属的裁剪图、独立 prompt、原始／修复响应、阶段记录或报告 | `P/scripts/run_qwen3_vl_anchor_crop_localization.py`；`E20/source_snapshots/02_run_qwen3_vl_anchor_crop_localization.py` |
| 20 | 有停止报告；记录证据缺失、新调用数为零、未加载模型 | `E20/report.md`、`E20/failure.json`、`E20/runtime.json` |

枚举涵盖隐藏及 gitignore 排除文件，跳过模型、虚拟环境等依赖目录及链接；同时检查了其他裁剪／定位命名和 prompt 特征。两个布局下均未找到 `qwen3_vl_anchor_crop_localization_20260910_001`。这仅说明当前搜索范围内证据缺失，不能推出“未推理”。

相关文件元数据（修改时间为本地时间）：

| 相对路径 | 字节 | 修改时间 |
|---|---:|---|
| `P/scripts/run_qwen3_vl_anchor_crop_localization.py` | 10707 | 2026-09-10 12:21:23 |
| `E20/source_snapshots/02_run_qwen3_vl_anchor_crop_localization.py` | 10707 | 2026-09-10 12:35:10 |
| `P/scripts/record_crop_recovery_stop.py` | 7847 | 2026-09-10 12:35:03 |
| `E20/report.md` | 3221 | 2026-09-10 12:35:10 |
| `E20/failure.json` | 663 | 2026-09-10 12:35:10 |
| `E20/source_manifest.json` | 1698 | 2026-09-10 12:35:10 |

seq19 当前脚本与 seq20 快照的 SHA256 相同。脚本指定源图 `P/runs/apm_dev_round1_v1_full/shared_frames/internet_0004/f003_t003000ms.jpg`，该文件存在（30895 字节，2026-09-09 11:49:21）。计划裁剪 `[0,144,683,288]` 后放大两倍；这些是输入计划，不能证明执行过。依据：上述脚本、`E20/source_verification.json`。

**路径判断：**`P/scripts/record_crop_recovery_stop.py` 用 `root/runs/...` 查 seq19，并检查 `root.parent/runs/...`；`source_manifest.json` 的路径则相对于 `root.parent` 输出，因此带 `active-physical-measurement/` 前缀有合理解释。历史调用的 `root` 实参未见直接执行记录，但现有代码、清单及当前目录检查均不支持已证实路径错误。

**锁范围：**静态代码确定 seq18/19 共用 `P/runs/qwen3_vl_inference.lock`，锁定首字节。seq18 锁覆盖 `run_locked()`；seq19 覆盖源图处理、模型加载、生成及响应写入，但目录创建和测试在锁外。只约束遵守相同协议的执行者，不能据锁文件判断当前进程状态。依据：`P/scripts/run_qwen3_vl_anchor_integer_1000.py`、seq19 脚本。

本次未运行推理、测试或恢复脚本，未写文件或发布；无权限、认证或预算阻断。历史失败为 seq20 的 `stopped_evidence_missing`，已完成缺失诊断。

**建议下一步：**由本地提供 seq19 启动命令、当时工作目录及中断前最后阶段的脱敏执行记录，再决定是否恢复。桥执行记录若在工作区外：**当前任务范围不可读取，需要本地提供脱敏执行记录**。