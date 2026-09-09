实验已完成并停止，结果为失败。

- 真实推理：是，1 次；`do_sample=false`
- schema 修复：否；首次响应已通过严格 JSON/schema，按约束不得重试
- 图像 SHA-256：`e148b1f84cc6b96fc72beb44c8142d810e7464ebd6197510ec6409ea5c03bdb9`
- anchor 归一化框：`[0.0,0.0,0.99,0.01]`
- 原样转换像素框：`[0,0,1,0]`，xyxy 半开；高度为 0，非法
- target 像素框：`[183,211,674,324]`
- IoU：`0.0`
- 中心距离：`504.717990565028 px`
- 完全相同：否；但因 anchor 非法，程序判定 `legal_and_different=false`
- overlay：`runs/qwen3_vl_anchor_normalized_region_20260909_001/overlay.png` 未生成，避免夹取或伪造合法框
- 测试：基线 41/41；最终 45/45 通过

证据位于：

- `runs/qwen3_vl_anchor_normalized_region_20260909_001/raw_response.txt`
- `runs/qwen3_vl_anchor_normalized_region_20260909_001/inference.json`
- `runs/qwen3_vl_anchor_normalized_region_20260909_001/validation.json`
- `runs/qwen3_vl_anchor_normalized_region_20260909_001/test_results.json`
- `runs/qwen3_vl_anchor_normalized_region_20260909_001/report.md`
- `runs/qwen3_vl_anchor_normalized_region_20260909_001/bridge_status.json`

程序只能确认首次响应格式有效、数值未经修改以及转换失败；本轮未证明区域分离管线成功，也因没有合法 overlay 而无法进行语义人工确认。下一步需要另行授权一个新实验来处理模型把 0–1000 坐标误写成近似 0–1 数值的问题。