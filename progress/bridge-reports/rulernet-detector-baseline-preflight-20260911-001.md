本轮因网络权限阻塞停止：首次官方 commit 请求返回 **WinError 10013**，未重试或绕过。

- 四张冻结 ROI 的 hash 全部匹配旧记录。
- 未下载源码/权重、未安装依赖，原 Qwen 环境未修改。
- **真实 forward 0 次**，无热图或候选核验图；未启动 seq43。

[完整报告](active-physical-measurement/runs/rulernet_detector_baseline_preflight_20260911_001/final_report.md) 已包含失败证据、环境版本、手动下载的完整 Windows 放置路径及后续检查步骤；同目录有自包含 `bridge_report.txt`，未发布任何文件。