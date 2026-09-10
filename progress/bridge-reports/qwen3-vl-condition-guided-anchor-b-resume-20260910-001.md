已完成并停止。兼容入口解除A缺 `status` 的阻断，但B仍框整张裁剪图，未达到紧贴参照、排除相邻物体的目标。

A首次原文及原严格失败结果逐字节保留。适配决策为 `pending_verification_candidate`，未补造 `candidate_found`；显式 `uncertain/none` 不升级。“1厘米”为 `given_condition`，刻度线及位置为 `unverified_model_claim`。

B原始回答全文：

~~~~text
```json
{
  "bbox_1000_int": [0, 0, 1000, 1000],
  "brief_visual_basis": "尺子的标定间隔为1厘米，尺子放置在木块上方，与木块边缘对齐"
}
```
~~~~

- 调用：A **0次**，B **1次**，修复 **0次**。
- 程序坐标事实：归一化 `[0,0,1000,1000]`；原图 `[0,144,683,288]`。直接映射，无调整，范围及非退化检查通过。
- 与seq22比较：面积均为 **98,352 px²**，面积比 **1.0**，四边变化均为 **0**。这些不证明语义正确。
- 测试 **11/11通过**；加载 **4.608秒**，推理 **2.431秒**，执行 **14.447秒**；峰值显存 allocated **4417.451 MiB**、reserved **4452 MiB**。
- 输入哈希、尺寸及处理器核对通过。无预算、权限、认证或锁忙阻断。`git status`失败：工作区不是Git仓库；未执行Git写操作。

证据目录（相对工作区）：
`active-physical-measurement/runs/qwen3_vl_condition_guided_anchor_b_resume_20260910_001/`

其中保存完整提示、原答、适配决策、校验、配置、性能、来源及产物哈希、`final_report.md`。准确图片路径：

- `active-physical-measurement/runs/qwen3_vl_condition_guided_anchor_b_resume_20260910_001/crop_overlay.png`
- `active-physical-measurement/runs/qwen3_vl_condition_guided_anchor_b_resume_20260910_001/original_overlay.png`

两图已查看；蓝框与旧橙框重合。B依据复述已知条件，位置与对齐仍是模型主张。下一步仅人工核验参照结构及边界。本轮未读取标签或凭据、改桥控制、发布或追加推理。