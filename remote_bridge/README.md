# 手机发消息 → GitHub 指令 → 本地 Codex

这是可配置的初版控制桥，不是已经连接你电脑的远程服务。桥使用官方 Python Codex SDK，当前会话通过 GitHub 写任务，本地 Python 进程读取并执行。每个任务启动独立 SDK 会话，读取项目文件获得背景；不会接管正在运行的桌面会话。

## 交给电脑上的 Codex

请安装并验证本目录的控制桥，先不运行研究实验：

1. 检查本机 Python 3.10+、Git 和 Codex 登录。先阅读 bridge.py。将控制桥放在研究工作区之外的独立目录；避免桌面 Codex 和 SDK 同时修改同一工作区。
2. 建立独立 Python 虚拟环境并安装 requirements.txt，记录实际 SDK 版本。使用官方支持的登录方式完成本机认证，不复制或上传凭据。SDK 版本差异若需修复，先保留修改记录。
3. 复制 config.example.json 为 config.json，填写已有项目的绝对路径。首次保持 execution_enabled=false、write_enabled=false、publish_report=false。
4. 为 GitHub 仓库配置仅限本仓库 Contents 读写的本地凭据，放在 APM_GITHUB_TOKEN 环境变量中，不写入代码或 git。桥信任指定仓库 main 分支上 control/command.json 的写入者；不要给不可信账号该仓库写权限。
5. 运行单元测试和 --check。--check 只检查 GitHub 读取及本地配置，不调用模型；不验证 GitHub 写权限和 Codex 登录有效性。
6. 启动桥验证状态文件写回 GitHub。然后将 execution_enabled=true，仍保持 write_enabled=false，重启桥。联系当前聊天发送一个有有效期的新只读 smoke 指令，读取项目 README 并汇报，不运行实验。此步有模型用量。
7. 检查超时、停止、重复任务、进程重启行为，特别测试 Windows taskkill 是否终止子进程。验证后再启用 write_enabled，并设置需要的模型和任务时限。不要修改权限策略绕过登录或审批阻断。
8. 当前仓库公开。publish_report=true 会自动发布 Codex 最终文字答复；确认报告仅包含可公开项目内容后启用。代码仅做有限密钥字符串过滤，不能保证自动去除所有敏感内容。原始日志、图片、代码变更不会自动上传。
9. 全部联调完成后，用 Windows 任务计划程序以当前登录用户在登录时启动此虚拟环境的 python.exe 和 bridge.py，工作目录设为控制桥目录。验证进程实际继承凭据环境。保持电脑联网、通电且不睡眠。
10. 把脱敏的联调状态、SDK 版本和遗留问题写入 progress/setup.md 供远端读取。禁止上传环境变量或登录文件。

Windows PowerShell（在控制桥目录执行）：

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item config.example.json config.json
# 手工编辑 config.json 并在本机设置 APM_GITHUB_TOKEN；不要在聊天中粘贴密钥
.\.venv\Scripts\python.exe -m unittest -v
.\.venv\Scripts\python.exe bridge.py --config config.json --check
.\.venv\Scripts\python.exe bridge.py --config config.json
```

## 指令协议

固定仓库 Tangxiaoxiao1992/active-physical-measurement，读取 main 的 control/command.json。修改文件须使用当前 blob SHA 防止覆盖并发修改。整个文件是单槽邮箱，不是队列；一次只提交一个任务，等确认后再提交下一项。后台每约20秒读取；网络请求及发布可能延长延迟。

```json
{
  "seq": 2,
  "action": "run",
  "task_id": "smoke-readme-001",
  "expires_at": "替换为未来的 ISO UTC 时间，例如 2026-09-10T12:00:00Z",
  "prompt": "只读取 README.md，说明当前研究阶段，不修改文件，不调用实验 API。"
}
```

- seq：每次指令严格递增，先读 progress/bridge-status.json 和当前 command.json。
- task_id：run 必须使用全新编号；新会话需要的任务背景写入 prompt 或仓库文档。连续任务要显式要求先读上阶段报告。
- expires_at：过期指令不执行，用来避免长时间离线后执行陈旧任务。
- pause：暂停后续调度，当前任务继续至结束。它不是挂起当前进程。
- stop：task_id 必须匹配当前任务；尝试终止本地工作进程树，不回滚文件，也无法撤销已发送的 API 请求。远端或脱离进程树的作业不保证停止。
- 继续：使用更高 seq 的新 run，明确从哪个检查点继续。不要删除去重状态来重跑任务。

运行记录先落盘，再启动任务。崩溃重启时在途任务标为 interrupted_unknown 并退出，需本地检查遗留进程后重新启动；不会自动重做可能已付费的任务。两个桥同时启动默认被本机端口锁阻止。不支持多台机器并行监听同一邮箱。

## 看结果

- progress/bridge-status.json：状态、任务 ID、更新时间与最后接收的序号，每约60秒上传。必须检查 updated_at；离线的 running 不代表电脑仍在运行。
- progress/bridge-reports/<task_id>.md：启用 publish_report 后上传最终文字报告，失败上传会重试。
- runtime/<task_id>/：完整本地日志与结果；不提交 git。

报告文字是模型报告，不是独立核验。审查标注图或代码需另行明确上传这些项目文件。控制桥不自动 git pull/commit/push 研究工作区，避免覆盖未提交工作。需要发布代码时，作为明确的后续任务提出。

## 限制与成本

- execution_enabled=false 为默认；没有默认付费研究任务。
- max_task_seconds 是运行时限，不是美元费用上限；模型账户额度与实验 API 费用分别计算。收费实验需现有 runner 的预算硬限制，桥本身不能限制任意子程序的 API 开销。
- GitHub 凭据从 worker 环境移除，但这不是完整的凭据隔离边界；同用户进程及本地配置仍需妥善管理。
- 未使用自动审批或 full_access；需要额外权限时可能阻塞直至超时，本机需先验证权限设置。
- 本地模型调用、Windows SDK 和后台任务需要在用户电脑联调；这里的离线测试不能替代端到端测试。
- 当前聊天不会自动醒来：用户在手机发消息后，助手读取报告并提交下一条指令。

SDK 文档：https://learn.chatgpt.com/docs/codex-sdk
