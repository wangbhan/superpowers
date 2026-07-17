## 子代理调度需要多代理支持

在您的 Codex 配置（`~/.codex/config.toml`）中添加：

```toml
[features]
multi_agent = true
```

这将为 `spawn_agent`、`wait_agent` 和 `close_agent` 等技能启用 `dispatching-parallel-agents` 和 `subagent-driven-development`。在使用子代理驱动开发时，当实施者和审阅者子代理完成所有工作后，应始终关闭它们。

## 环境检测

创建工作树或完成分支的技能应在继续操作前，
通过只读 git 命令检测其
环境：

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

- `GIT_DIR != GIT_COMMON` → 已处于关联的工作树中（跳过创建）
- `BRANCH` 为空 → 脱离 HEAD（无法从沙盒进行分支/推送/PR）

有关各技能如何使用这些信号，请参阅 `using-git-worktrees` 第 0 步和 `finishing-a-development-branch`
第 1 步。

## Codex 应用收尾

当沙盒阻止分支/推送操作时（在
外部管理的工作树中处于脱离 HEAD 状态），代理会提交所有工作，并通知
用户使用应用的原生控制功能：

- **“创建分支”** — 命名分支，然后通过应用 UI 进行提交/推送/创建拉取请求
- **“移交至本地”** — 将工作转移至用户的本地检出

代理仍可运行测试、准备文件，并输出建议的分支
名称、提交信息和拉取请求描述，供用户复制。
