seq40 已完成，仅审计，未修复、未调参，未启动 seq41。

- **width**：逐行汇总 ±18px 内全部 dark 样本，取95%分位数；并非中心连续主体宽度。**side**：从连接点后6px开始，统计侧条带弱像素占比≥.75的行比例。
- img_04 的59个width超限中，**4个仅width失败，55个重叠其它失败**。c19实际采到上方横边，不能把59个提案全当真实刻线。
- c3的side失败来自连接根部附近第6–13px；网格反例的交叉位于多个内部位置。证据揭示方法限制，但尚不足以确定统一连接区边界，因此未冒称实现bug或增大跳过范围。
- 四图旧→重放：img_01保持`present_candidate`；img_03/04/05保持`absent`。img_04未救回；uncertain=0。
- 四图结果精确重放、输入与旧目录哈希检查通过。审计及首版渲染墙钟6.505秒；排版截断和补充渲染`StopIteration`已记录并修正，原记录保留。17页已实际打开核验。

完整报告、机器证据及所有图片Windows路径见：
[final_report.md](C:/Users/MSI/Desktop/AI/QuantiPhy-Practice/active-physical-measurement/runs/anchor_width_crossing_sampling_audit_20260911_001/final_report.md)

代表图：
[c3连接根部](C:/Users/MSI/Desktop/AI/QuantiPhy-Practice/active-physical-measurement/runs/anchor_width_crossing_sampling_audit_20260911_001/sampling_review_page03_reviewed.png)；
[网格内部交叉](C:/Users/MSI/Desktop/AI/QuantiPhy-Practice/active-physical-measurement/runs/anchor_width_crossing_sampling_audit_20260911_001/sampling_review_page11_reviewed.png)。

下一步需要原掩膜拓扑证据，证明统一连接区终止定义不会忽略网格内部交叉。本轮已停止。无权限、认证或预算阻塞；未联网、读取凭据或标签、修改桥控制、发布文件。