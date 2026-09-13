seq61 完成：**3 次新 forward，全部成功，每图一次；未启动 seq62。**

按冻结的 **10 原生像素、一对一线段匹配**规则：

- 视频：候选 **1→12**，全部不确定，不能确认改善。
- ruler_02：候选 **0→11**，匹配 **0→4**，新未匹配 **7**；这些点靠近主线顶端，不能直接判为误报。
- ruler_01：候选 **7→7**，匹配 **7→7**。未改写 seq59 的历史零匹配记录。

官方流程：RGB、LongestMaxSize 768、居中黑边、CenterCrop 768²、CHW float32 `/255`，模型内归一化；实际尺面为 **768×53、768×80、768×120**。`always_apply/value` 忽略警告已记录，实际 `p=1/fill=0` 验证通过，未改参数。

依赖：albumentations **2.0.8**、numpy **2.4.6**、cv2 **5.0.0**、torch **2.6.0+cu124**、timm **1.0.15**、SMP **0.4.0**。旧输入复算完全一致，但用户安装后的 OpenCV 二进制差异仍是环境混杂，**不能完全归因于预处理**。

首次工作进程发生一次 forward 前路径错误，已保留证据并修正；共4次进程启动、3次forward，无重复推理。123个旧文件、146个依赖文件核验不变，两锁已释放。

证据目录：`C:\Users\MSI\Desktop\AI\QuantiPhy-Practice\active-physical-measurement\runs\rulernet_official_preprocessing_seq61_20260913_001\`

其中包含 [final_report.md](C:/Users/MSI/Desktop/AI/QuantiPhy-Practice/active-physical-measurement/runs/rulernet_official_preprocessing_seq61_20260913_001/final_report.md)、`results.csv`、`point_comparison.csv`、`execution_result.json`、`verification.json`及已打开核验的全部复核图。

下一步仍应先独立确认 ruler_02 参考端点与点语义。既有桥文字接口未暴露，未发布或上传任何文件。