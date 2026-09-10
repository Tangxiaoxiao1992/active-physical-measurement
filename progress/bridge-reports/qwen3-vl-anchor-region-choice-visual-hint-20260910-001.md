seq27 **实验无效，已停止**。PowerShell 管道将追加中文编码成问号；生成前检查未发现此错误。已保存失败更正报告，原证据全部保留，不重复推理。

实际原始回答全文：

```json
{
  "selected_ids": [1, 2, 3, 4],
  "brief_visual_basis": "所有四个区域都显示了木块的表面，但无法从图像中确定木块的长度和厚度，因为图像中没有提供足够的尺寸参照。"
}
```

批准追加提示全文（**实际未正确送入模型**）：

> 寻找白色长条表面上一排深色、近似平行的短线。它们沿长条方向排列，与木块上不规则的浅色纹理不同。中间可能被手指遮挡，应检查未被遮挡的部分。本轮只找这种视觉特征，不判断能否算出木块尺寸。

程序事实：

- 推理 **1次**，修复 **0次**。选择与seq26相同，均为 `[1,2,3,4]`；不匹配暂定人工集合，但不能据此评价批准提示的效果。
- 图片文件及像素一致，1366×528。SHA256：`1fa1d7c0e148db3252120a0e993988e48e55545c9dece20aba0533eb3d2bbe7e`。
- 同模型、虚拟环境、bfloat16、sdpa、`do_sample=false`、384 token上限。处理器仍为 **1376×512／688视觉tokens**。
- 锁获取、准备、加载、生成、原答保存、回画、落盘均完成。16项解析／映射检查及6项输出检查通过；**批准提示精确一致性审计失败**。
- 加载4.409秒、生成2.590秒、总11.284秒；峰值显存 allocated 4382.173 MiB、reserved 4412 MiB。存在采样参数可能被忽略的警告。

人工审阅：已查看两张回画和原答；全选未区分可见短线与木纹，最终语义待用户核验。本轮原计划属于“**针对本样本的teacher文字辅助**”，不是零样本、泛化验证或训练／蒸馏；实际输入损坏，不能形成有效实验结论。

精确证据路径（相对配置工作区）：

- `active-physical-measurement/runs/qwen3_vl_anchor_region_choice_visual_hint_20260910_001/failure_report.md`
- `active-physical-measurement/runs/qwen3_vl_anchor_region_choice_visual_hint_20260910_001/selection_review.png`
- `active-physical-measurement/runs/qwen3_vl_anchor_region_choice_visual_hint_20260910_001/original_selection_overlay.png`
- `active-physical-measurement/runs/qwen3_vl_anchor_region_choice_visual_hint_20260910_001/stages.jsonl`

失败更正报告优先于原 `report.md`。下一步须由用户决定是否批准新轮次，并先验证UTF-8传递及批准原文逐字符一致。未发布文件、未修改桥控制，不自动启动seq28。