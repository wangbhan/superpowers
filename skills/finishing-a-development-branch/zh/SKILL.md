---
name: finishing-a-development-branch
description: 在实现工作完成、所有测试通过，且需要决定如何整合该工作时使用——通过提供有关合并、PR 或清理的结构化选项，指导开发工作的完成
---

# 完成开发分支

## 概述

通过提供明确的选项并处理所选的工作流，指导开发工作的完成。

**核心原则：** 验证测试 → 检测环境 → 提供选项 → 执行选择 → 清理。

**开始时声明：**“我将使用‘完成开发分支’技能来完成这项工作。”

## 流程

### 步骤 1：验证测试

**在提供选项之前，先验证测试是否通过：**

```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**如果测试失败：**
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

停止。不要继续进行步骤 2。

**如果测试通过：** 继续进行步骤 2。

### 步骤 2：检测环境

**在提供选项前，确定工作区状态：**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```

这将决定显示哪个菜单以及清理方式：

| 状态 | 菜单 | 清理 |
|-------|------|---------|
| `GIT_DIR == GIT_COMMON`（普通仓库） | 标准 4 个选项 | 无工作树需清理 |
| `GIT_DIR != GIT_COMMON`，命名分支 | 标准 4 个选项 | 基于来源（参见步骤 6） |
| `GIT_DIR != GIT_COMMON`，脱离主分支的 HEAD | 精简为 3 个选项（无合并） | 无需清理（由外部管理） |

### 第 3 步：确定基准分支

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

或者询问：“该分支是从 main 分支分出的——这样对吗？”

### 第 4 步：呈现选项

**普通仓库和命名分支的工作树 —— 请精确呈现以下 4 个选项：**

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**脱离主分支的 HEAD —— 请精确呈现以下 3 个选项：**

```
Implementation complete. You're on a detached HEAD (externally managed workspace).

1. Push as new branch and create a Pull Request
2. Keep as-is (I'll handle it later)
3. Discard this work

Which option?
```

**不要添加解释**——保持选项简洁。

### 第 5 步：执行选择

#### 选项 1：本地合并

```bash
# Get main repo root for CWD safety
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

# Merge first — verify success before removing anything
git checkout <base-branch>
git pull
git merge <feature-branch>

# Verify tests on merged result
<test command>

# Only after merge succeeds: cleanup worktree (Step 6), then delete branch
```

随后：清理工作树（步骤 6），然后删除分支：

```bash
git branch -d <feature-branch>
```

#### 选项 2：推送并创建 PR

```bash
# Push branch
git push -u origin <feature-branch>
```

**请勿清理工作树** —— 用户需要保留工作树以便根据 PR 反馈进行迭代。

#### 选项 3：保持原样

报告：“保留分支 <名称>。工作树保存在 <路径>。”

**不要清理工作树。**

#### 选项 4：弃用

**先确认：**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

等待明确确认。

若已确认：
```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
```

然后：清理工作树（步骤 6），随后强制删除分支：
```bash
git branch -D <feature-branch>
```

### 步骤 6：清理工作区

**仅在选项 1 和 4 时执行。**选项 2 和 3 始终保留工作树。

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

**若为 `GIT_DIR == GIT_COMMON`：**普通仓库，无需清理工作树。完成。

**如果工作树路径位于 `.worktrees/` 或 `worktrees/` 之下：** 该工作树由“超级权限”创建——我们负责清理。

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git worktree remove "$WORKTREE_PATH"
git worktree prune  # Self-healing: clean up any stale registrations
```

**否则：** 该工作区由主机环境（测试框架）负责。 请勿将其删除。如果您的平台提供了工作区退出工具，请使用该工具。否则，请保留该工作区。

## 快速参考

| 选项 | 合并 | 推送 | 保留工作树 | 清理分支 |
|--------|-------|------|---------------|----------------|
| 1. 本地合并 | 是 | - | - | 是 |
| 2. 创建 PR | - | 是 | 是 | - |
| 3. 保持原样 | - | - | 是 | - |
| 4. 丢弃 | - | - | - | 是（强制） |

## 常见错误

**跳过测试验证**
- **问题：** 合并有问题的代码，创建会失败的 PR
- **解决方法：** 在提供选项前务必验证测试

**开放式问题**
- **问题：** “我接下来该做什么？” 表述含糊
- **解决方法：** 提供恰好 4 个结构化的选项（如果是脱离 HEAD 的分支，则提供 3 个）

**为选项 2 清理工作树**
- **问题：** 移除用户在 PR 迭代过程中需要的工作树
- **解决方法：** 仅针对选项 1 和 4 进行清理

**在移除工作树前删除分支**
- **问题：** `git branch -d` 失败，因为工作树仍引用该分支
- **解决方案：** 先合并，再移除工作树，最后删除分支

**在工作树内部运行 git worktree remove**
- **问题：**当当前工作目录位于待删除的工作树内时，命令会无提示失败
- **解决方案：**在执行 `git worktree remove` 之前，始终先通过 `cd` 切换到主仓库根目录

**清理由测试框架拥有的工作树**
- **问题：** 删除测试框架创建的工作树会导致“幽灵状态”
- **解决方法：** 仅清理位于 `.worktrees/` 或 `worktrees/` 下的工作树

**丢弃操作无需确认**
- **问题：** 意外删除工作
- **修复：** 要求手动输入“discard”进行确认

## 红旗警告

**切勿：**
- 在测试失败时继续操作
- 未验证合并结果的测试就进行合并
- 未经确认就删除工作树
- 未经明确请求就强制推送
- 在确认合并成功前删除工作树
- 清理非自己创建的工作树（溯源检查）
- 在工作树内部运行 `git worktree remove`

**必须：**
- 提供选项前验证测试
- 显示菜单前检测环境
- 精确提供 4 个选项 （若为脱离主分支的 HEAD，则为 3 个）
- 选项 4 需获取键入确认
- 仅在选择选项 1 和 4 时清理工作树
- 在移除工作树前，将 `cd` 推送到主仓库根目录
- 移除后运行 `git worktree prune`
