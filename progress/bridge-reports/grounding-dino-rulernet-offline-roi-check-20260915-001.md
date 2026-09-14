seq65 已实际完成离线实验，结论是**自动流程未通过**：

- 两张清晰尺图定位弱通过，自动裁图覆盖冻结参考尺面 100%。
- 1 秒含尺帧漏检，下游按规则跳过。
- 0 秒木块被误报为 `tape`，RulerNet 随后产生 11 个非尺面候选。
- 与 seq61 共同参考范围比较：ruler_01 匹配保持 7→7；ruler_02 为 4→8，仍有 3 个未匹配。候选不能当作真刻度。

实际调用 Grounding DINO **4 次**、RulerNet **3 次**，全部 forward 完成，无重试、下载或安装。182 个选定旧文件 hash 未变，两把锁已释放，保守计时约 18 分钟。单位仍未知。

证据：[完整报告](C:/Users/MSI/Desktop/AI/QuantiPhy-Practice/active-physical-measurement/runs/grounding_dino_rulernet_seq65_20260915_001/final_report.md) · [总览图](C:/Users/MSI/Desktop/AI/QuantiPhy-Practice/active-physical-measurement/runs/grounding_dino_rulernet_seq65_20260915_001/overview.png) · [核验记录](C:/Users/MSI/Desktop/AI/QuantiPhy-Practice/active-physical-measurement/runs/grounding_dino_rulernet_seq65_20260915_001/verification.json)

下一步主要瓶颈是区分模糊细尺与木块边缘。已停止，未启动 seq66；既有桥文字接口不可调用，未发布任何文件。