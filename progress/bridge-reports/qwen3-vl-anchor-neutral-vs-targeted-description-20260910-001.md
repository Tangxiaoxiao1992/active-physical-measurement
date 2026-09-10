seq31 已完成并停止：固定调用 **4/4**，全部完成，无异常、重试或格式失败。未启动 seq32，未发布文件。

中性问题全文：
> 描述图中实际可见的表面和线条特征，不推测被遮挡或看不清的内容。

附加要求：只用一句简短的自然语言描述。

针对性问题全文：
> 当前图片中，是否能辨认出白色尺身上一排重复排列的深色短刻线？只判断当前图片实际可见的内容；木纹、长边缘和阴影不算。无法辨认时回答uncertain。

沿用 seq30 完整输出要求：
> 只输出JSON对象 {"presence":"present|absent|uncertain","brief_visual_basis":"一句当前图中可见的依据"}，presence取三个枚举之一。

四份原答全文：

- **Region2 中性／case_1**：完成，自然语言格式通过，1.226s。
  > 一张被手或物体部分遮挡的白色纸张，上面有模糊的黑色文字和一条水平的黑色线条。

- **Region2 针对性／case_2**：完成，JSON 格式通过，0.760s。
  ```json
  {"presence":"present","brief_visual_basis":"图像中可见白色尺子上有一排深色短刻线"}
  ```

- **Region4 中性／case_3**：完成，自然语言格式通过，0.322s。
  > 一张带有水平纹理的浅色纸张表面。

- **Region4 针对性／case_4**：完成，JSON 格式通过，0.855s。
  ```json
  {"presence":"present","brief_visual_basis":"图像中可见白色尺身上有一排重复排列的深色短刻线"}
  ```

语义审核：两份中性回答均为“没有提及刻线”，两份针对性回答均为“明确声称有刻线”；没有明确否认或不确定回答。针对性原答均与 seq30 逐字一致。按暂定人工预期，Region4 针对性为误报；这一差异与提示诱导假设一致，但中性遗漏不能证明因果，也不能当作正确识别。问题和输出形式同时变化，不计算跨任务准确率或推断泛化、容量。

直接复用 seq30 两张裁图，哈希及像素一致。四例均为 **1376×96、129 视觉 tokens**；同图两问 tensor 完全一致。沿用 Qwen3-VL-2B-Instruct、既有 venv、bfloat16、sdpa、确定性生成及384 token上限，中性 system 无变更。四套输入、编码和 processor 检查均在模型加载前通过。执行耗时11.059s，其中加载2.811s。

无权限、认证、预算或锁阻断。仅出现确定性生成下采样参数可能被忽略的库警告，未更改配置。

产物相对 **P=active-physical-measurement**：
`runs/qwen3_vl_anchor_neutral_vs_targeted_description_20260910_001/`

其中保存 `final_report.md`、`comparison.md`、`case_1_raw_response.txt` 至 `case_4_raw_response.txt`、完整消息、manifest/config/processor 检查及 `stages.jsonl`。`review.png` 已检查排版与原图像素，**仅在本地，未远端提供**。

下一步仅人工核验 `review.png` 中 Region4 的断言及中性描述依据。旧证据保留，未修改 scoring truth、桥控制或读取凭据、held-out 标签。