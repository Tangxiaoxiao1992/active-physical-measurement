seq43 已完成可离线工作，**forward=0/4**，耗时约 444 秒；未启动 seq44、未发布文件。

- 两个 ZIP 完整性与 SHA256 已核验并安全解压；源码 commit 仅有档案注释证据，权重远端 hash 未独立核实。
- checkpoint 受限读取成功；完整网络严格加载因 SMP/timm 缺失尚未执行。
- 首次 PyPI 请求触发 **WinError 10013**，立即停止，未重试或绕过。
- 四图 hash、旧目录 hash、原环境包清单均未变；输入映射和检查页已保存、实际查看。无热图或检测结论。

下一步：将 `segmentation_models_pytorch-0.4.0-py3-none-any.whl`、`timm-1.0.15-py3-none-any.whl` 放入本轮 `wheelhouse`，先检查元数据和兼容性。

完整证据、下载链接及精确 Windows 路径见 [final_report.md](C:/Users/MSI/Desktop/AI/QuantiPhy-Practice/active-physical-measurement/runs/rulernet_local_archives_detector_baseline_20260912_001/final_report.md)。