seq37 已完成合格部分：6 张照片无文件缺失、无重复 hash；视觉上为 6 张不同照片，采集来源独立性未核实。合格 **4 张：尺子 2、木纹 1、横线纸 1**。树皮类别不符、另一纸图失焦，未调用，因此清晰木纹和横线纸各缺 1 张。

程序确认：真实调用 **4 次**，零重试、格式错误 0、uncertain 0。CPU 核验 1.306 秒，推理预检 5.410 秒，模型加载 3.320 秒，生成及保存合计 7.752 秒。实际 processor 图已打开，生成输入张量与审核记录一致。

以下标签均为**执行器视觉审核，非用户已确认**：

- **img_01：尺子短刻线，拟定 present → present**  
  完整 basis：“在刻度尺的刻度线之间，有一排重复排列的深色短刻线，位于3和4之间，从3到4的刻度线之间，这些短刻线与主刻度线平行。”  
  视觉复核：位置基本对应；不采纳数值读数。
- **img_02：树皮，拟定 absent → 未调用**，不符合目标重复木纹。
- **img_03：连续木纹，拟定 absent → present**  
  完整 basis：“在框内，可以观察到一条细长的深色矩形区域，其内部有重复排列的短刻线，这些刻线与木纹方向一致，位于图像的中上部。”  
  视觉复核：所称短刻线排不对应图像，**暂定误报**。
- **img_04：尺子短刻线，拟定 present → present**  
  完整 basis：“在尺子的刻度线上，有一排重复排列的深色短刻线，从左到右依次可见。这些刻线位于刻度线的下方，与尺子的刻度线平行。”  
  视觉复核：存在性对应，“下方”指代不清。
- **img_05：横线纸及纵向表格线，拟定 absent → present**  
  完整 basis：“框内可见多排深色短刻线，排列整齐，位于左侧区域，与右侧的水平线形成网格状结构。”  
  视觉复核：左侧网格位置对应，但把连续线误认作短刻线，**暂定误报**。
- **img_06：失焦横线纸，拟定 absent → 未调用**。

清晰尺子暂定漏报 **0/2**；木纹、横线纸暂定误报各 **1/1**。这只是小样本诊断，不是旧木块同帧 C 对照，不能证明清晰度因果或统计泛化。

本地证据精确路径：

- [human_review.png](C:/Users/MSI/Desktop/AI/QuantiPhy-Practice/active-physical-measurement/runs/qwen3_vl_clear_ruler_texture_diagnostic_20260911_001/human_review.png)
- [condition_review.png（第1页）](C:/Users/MSI/Desktop/AI/QuantiPhy-Practice/active-physical-measurement/runs/qwen3_vl_clear_ruler_texture_diagnostic_20260911_001/condition_review.png)、同目录 `condition_review_page2.png`、`condition_review_page3.png`
- [完整报告 final_report.md](C:/Users/MSI/Desktop/AI/QuantiPhy-Practice/active-physical-measurement/runs/qwen3_vl_clear_ruler_texture_diagnostic_20260911_001/final_report.md)

全部展示页已打开确认无截断，图片仅本地保存。曾遇木纹图显示传输错误，已完成本地解码与局部核验；无权限、认证、显存或预算阻断。原图及冻结文件 hash 未变。桥文字稿已保存为同目录 `bridge_report.txt`，远端送达未确认，未修改桥控制。

下一步是人工复核两次暂定误报及补图缺项；未自动启动 seq38。