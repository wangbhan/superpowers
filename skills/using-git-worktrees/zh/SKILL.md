---
name: using-git-worktrees
description: 在开始需要与当前工作区隔离的功能开发工作时，或在执行实现计划之前使用此功能——通过原生工具或 Git 工作树回退机制确保存在一个隔离的工作区
---

# 使用 Git 工作树

## 概述

确保工作在隔离的工作区中进行。优先使用平台的原生工作树工具。仅在没有原生工具可用时，才退而求其次使用手动创建的 Git 工作树。

**核心原则：** 首先检测是否已存在隔离环境。然后使用原生工具。最后再退而求其次使用 Git。切勿与系统机制作对。

**开始时声明：** “我正在使用 using-git-worktrees 技能来设置一个隔离的工作区。”

## 第 0 步：检测现有隔离状态

**在创建任何内容之前，请检查您是否已处于隔离的工作区中。**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

**子模块保护：** 在 Git 子模块内部，`GIT_DIR != GIT_COMMON` 同样成立。 在断定“已处于工作树中”之前，请先确认你不在子模块中：

```bash
# If this returns a path, you're in a submodule, not a worktree — treat as normal repo
git rev-parse --show-superproject-working-tree 2>/dev/null
```

**如果为 `GIT_DIR != GIT_COMMON`（且非子模块）：** 你已经处于链接的工作树中。跳至步骤 2（项目设置）。 切勿创建另一个工作树。

报告分支状态：
- 处于分支上：“已位于 `<name>` 分支上的 `<path>` 隔离工作区中。”
- 脱离 HEAD 状态："已位于 `<path>` 的隔离工作区中（脱离 HEAD，由外部管理）。完成后需创建分支。"

**如果当前位置为 `GIT_DIR == GIT_COMMON`（或处于子模块中）：** 您处于普通仓库检出状态。

用户是否已在您的操作指南中指定了工作树偏好？如果未指定，请在创建工作树前征得用户同意：

> “您希望我设置一个隔离的工作树吗？这可以保护您当前分支免受更改影响。”

若用户已声明偏好，请直接遵循，无需再次询问。 如果用户拒绝同意，则直接在原地操作并跳至步骤 2。

## 步骤 1：创建隔离工作区

**您有两种方法。请按以下顺序尝试。**

### 1a. 原生工作树工具（推荐）

用户已请求创建隔离工作区（步骤 0 同意）。您是否已有创建工作树的方法？这可能是名称类似 `EnterWorktree`、`WorktreeCreate` 的工具，`/worktree` 命令，或是 `--worktree` 标志。 如果有，请直接使用并跳至步骤 2。

原生工具会自动处理目录定位、分支创建和清理工作。当已有原生工具时，若仍使用 `git worktree add`，会产生您的测试框架无法识别或管理的“幽灵状态”。

仅当没有可用的原生工作树工具时，才继续执行步骤 1b。

### 1b. Git 工作树备用方案

**仅在步骤 1a 不适用时使用此方法** —— 即没有可用的原生工作树工具。使用 git 手动创建工作树。

#### 目录选择

请遵循以下优先级顺序。用户的显式偏好始终优先于检测到的文件系统状态。

1. **检查说明文档中是否声明了工作树目录偏好。** 如果用户已指定，则直接使用，无需询问。

2. **检查是否存在项目本地工作树目录：**
   ```bash
   ls -d .worktrees 2>/dev/null     # Preferred (hidden)
   ls -d worktrees 2>/dev/null      # Alternative
   ```
   若找到，则使用该目录。若两者均存在，则 `.worktrees` 优先。

3. **如果没有其他指导**，则默认使用项目根目录下的 `.worktrees/`。

#### 安全验证（仅限项目本地目录）

**在创建工作树之前，必须验证该目录已被忽略：**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**若未被忽略：**将其添加到 .gitignore 中，提交该更改，然后继续。

**为何至关重要：**防止意外将工作树内容提交到代码库。

#### 创建工作树

```bash
# Determine path based on chosen location
path="$LOCATION/$BRANCH_NAME"

git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

**沙箱备用方案：**如果 `git worktree add` 因权限错误（沙箱拒绝）而失败，请告知用户沙箱阻止了工作树的创建，并将改在当前目录中进行操作。然后在当前位置运行设置和基线测试。

## 步骤 2：项目设置

自动检测并运行相应的设置：

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

## 步骤 3：验证干净基线

运行测试以确保工作区处于干净状态：

```bash
# Use project-appropriate command
npm test / cargo test / pytest / go test ./...
```

**如果测试失败：** 报告失败情况，询问是否继续或进行排查。

**如果测试通过：** 报告已准备就绪。

### 报告

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## 快速参考

| 情况 | 操作 |
|-----------|--------|
| 已存在于关联的工作树中 | 跳过创建（步骤 0） |
| 位于子模块中 | 视为普通仓库（步骤 0 保护机制） |
| 可用原生工作树工具 | 使用该工具（步骤 1a） |
| 无原生工具 | 回退到 Git 工作树（步骤 1b） |
| 存在 `.worktrees/` | 使用它（验证是否被忽略） |
| 存在 `worktrees/` | 使用它（验证是否被忽略） |
| 两者均存在 | 使用 `.worktrees/` |
| 两者均不存在 | 检查说明文件，然后默认使用 `.worktrees/` |
| 目录未被忽略 | 添加到 .gitignore 并提交 |
| 创建时出现权限错误 | 回退到沙箱，就地操作 |
| 基线测试失败 | 报告失败并咨询 |
| 没有 package.json/Cargo.toml | 跳过依赖项安装 |

## 常见错误

### 与测试框架冲突

- **问题：** 当平台已提供隔离环境时仍使用 `git worktree add`
- **解决方法：** 第 0 步会检测现有的隔离环境。第 1a 步将交由原生工具处理。

### 跳过检测

- **问题：** 在现有工作树内创建嵌套工作树
- **解决方法：** 在创建任何内容之前，务必先运行步骤 0

### 跳过忽略规则验证

- **问题：** 工作树内容被纳入版本控制，污染 `git status` 输出
- **解决方法：** 在创建项目本地工作树前，务必先使用 `git check-ignore`

### 假设目录位置

- **问题：** 导致不一致，违反项目规范
- **解决方法：**遵循优先级：显式指令 > 现有的项目本地目录 > 默认值

### 在测试失败时继续操作

- **问题：**无法区分新出现的错误与原有问题
- **解决方法：**报告失败情况，获得明确许可后再继续

## 红旗警告

**切勿：**
- 当步骤 0 检测到现有隔离环境时创建工作树
- 在拥有原生工作树工具（例如 `EnterWorktree`）的情况下使用 `git worktree add`。这是头号错误——若有该工具，请务必使用。
- 跳过步骤 1a，直接执行步骤 1b 的 git 命令
- 在未验证是否被忽略（项目本地）的情况下创建工作树
- 跳过基线测试验证
- 未经询问就继续执行失败的测试

**始终：**
- 首先运行步骤 0 的检测
- 优先使用原生工具，而非 Git 备用方案
- 遵循目录优先级：显式指令 > 现有的项目本地目录 > 默认设置
- 验证目录是否已被标记为项目本地忽略项
- 自动检测并运行项目设置
- 验证测试基线是否干净
