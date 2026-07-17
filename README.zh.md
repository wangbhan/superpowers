# Superpowers

Superpowers 是一套面向编程代理的完整软件开发方法论，它基于一组可组合的技能以及一些初始指令构建而成，这些指令可确保您的代理正确使用这些技能。

## 招聘启事！

我们正在招聘一名全职人员，协助处理 Superpowers 社区事务及代码开发工作。 
您可以在 https://primeradiant.com/jobs/superpowers-community-engineer/ 查看职位详情。
如果您认识合适的人选，请务必推荐给我们。

## 快速入门

为您的智能代理赋予“超能力”： [Claude Code](#claude-code)、[Antigravity](#antigravity)、[Codex App](#codex-app)、[Codex CLI](#codex-cli)、[Cursor](#cursor)、 [Factory Droid](#factory-droid)、[GitHub Copilot CLI](#github-copilot-cli)、[Kimi Code](#kimi-code)、[OpenCode](#opencode)、[Pi](#pi)。

## 工作原理

一切始于你启动编程助手的那一刻。一旦它察觉到你在构建某个项目，它*不会*立即跳入代码编写环节。相反，它会退后一步，询问你真正想要实现什么。 

一旦它从对话中梳理出需求规格说明，就会将其拆分成足够短的段落展示给你，让你能够真正阅读并消化。 

在你确认设计方案后，你的代理会制定一份实施计划，其清晰度足以让一位热情高涨但品味欠佳、缺乏判断力、不了解项目背景且厌恶测试的初级工程师也能轻松遵循。该计划强调真正的红/绿 TDD、YAGNI（你不会需要它）和 DRY 原则。 

接下来，一旦你发出“开始”指令，它便会启动一个*子代理驱动开发*流程，让代理们逐一处理每个工程任务，检查并审查自己的工作，然后继续推进。你的代理一次自主工作几个小时而不偏离你制定的计划，这种情况并不罕见。

虽然还有许多其他功能，但这便是系统的核心。而且由于技能会自动触发，您无需进行任何特殊操作。您的编码代理天生就拥有“超能力”。

## 商业服务

如果您在企业环境中使用 Superpowers，并希望获得商业支持、额外工具或支出管理服务，请随时通过 sales@primeradiant.com 与我们联系。

## 安装

安装方式因框架而异。如果您使用多个框架，请为每个框架分别安装 Superpowers。

### Claude Code

您可通过 [Claude 官方插件市场](https://claude.com/plugins/superpowers) 获取 Superpowers

#### 官方市场

- 从 Anthropic 官方市场安装插件：

  ```bash
  /plugin install superpowers@claude-plugins-official
  ```

#### Superpowers 插件市场

Superpowers 插件市场为 Claude Code 提供 Superpowers 及其他相关插件。

- 注册该插件市场：

  ```bash
  /plugin marketplace add obra/superpowers-marketplace
  ```

- 从该市场安装插件：

  ```bash
  /plugin install superpowers@superpowers-marketplace
  ```

### Antigravity

从该仓库将 Superpowers 作为插件安装：

```bash
agy plugin install https://github.com/obra/superpowers
```

Antigravity 会触发该插件的 session-start 钩子，因此 Superpowers 从
第一条消息开始即处于激活状态。使用相同的命令重新安装即可更新。

### Codex 应用

您可通过 [官方 Codex 插件市场](https://github.com/openai/plugins) 获取 Superpowers。

- 在 Codex 应用中，点击侧边栏中的“插件”。
- 您应在“编程”部分看到 `Superpowers`。
- 点击 Superpowers 旁边的 `+`，并按照提示操作。

### Codex CLI

您可通过 [官方 Codex 插件市场](https://github.com/openai/plugins) 获取 Superpowers。

- 打开插件搜索界面：

  ```bash
  /plugins
  ```

- 搜索“Superpowers”：

  ```bash
  superpowers
  ```

- 选择 `Install Plugin`。

### Cursor

- 在 Cursor Agent 聊天界面中，从市场安装：

  ```text
  /add-plugin superpowers
  ```

- 或者在插件市场中搜索“superpowers”。

### Factory Droid

- 注册插件市场：

  ```bash
  droid plugin marketplace add https://github.com/obra/superpowers
  ```

- 安装插件：

  ```bash
  droid plugin install superpowers@superpowers
  ```

### GitHub Copilot CLI

- 注册市场：

  ```bash
  copilot plugin marketplace add obra/superpowers-marketplace
  ```

- 安装插件：

  ```bash
  copilot plugin install superpowers@superpowers-marketplace
  ```

### Kimi Code

“Superpowers” 可在 Kimi Code 的插件市场中找到。

- 打开 Kimi Code 的插件管理器：

  ```text
  /plugins
  ```

- 前往 `Marketplace` > `Superpowers` 并安装。

- 或直接从该仓库安装：

  ```text
  /plugins install https://github.com/obra/superpowers
  ```

- 详细文档：[docs/README.kimi.md](docs/README.kimi.md)

### OpenCode

OpenCode 使用其专有的插件安装机制；即使您
已在其他框架中使用过 Superpowers，也需单独安装。

- 告知 OpenCode：

  ```
  Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md
  ```

- 详细文档：[docs/README.opencode.md](docs/README.opencode.md)

### Pi

从该仓库将 Superpowers 作为 Pi 包安装：

```bash
pi install git:github.com/obra/superpowers
```

进行本地开发时，请将此代码检出并作为临时包加载，然后运行 Pi：

```bash
pi -e /path/to/superpowers
```

该 Pi 包会加载 Superpowers 技能以及一个小型扩展，该扩展会在会话启动时以及压缩后再次注入 `using-superpowers` 引导程序。 Pi 具备原生技能，因此无需兼容性工具 `Skill`。子代理和任务列表工具仍作为可选的 Pi 配套包。

## 基本工作流程

1. **头脑风暴** - 在编写代码前启动。 通过提问完善粗略构想，探索替代方案，分段呈现设计以供验证。保存设计文档。

2. **使用 Git 工作树** - 设计获批后启动。在新分支上创建隔离的工作区，运行项目配置，验证干净的测试基线。

3. **编写计划** - 在设计获得批准后启动。将工作分解为易于处理的任务（每个任务耗时 2-5 分钟）。每个任务都包含精确的文件路径、完整的代码以及验证步骤。

4. **子代理驱动开发** 或 **执行计划** - 随计划启动。针对每个任务派遣新的子代理，并进行两阶段审查（先检查规范符合性，再检查代码质量），或以批量方式执行并由人工进行检查点审核。

5. **测试驱动开发** - 在实现阶段启动。 强制执行“红-绿-重构”原则：编写会失败的测试，观察其失败，编写最简代码，观察其通过，提交代码。删除测试编写前的代码。

6. **请求代码审查** - 在任务之间触发。根据计划进行审查，按严重程度报告问题。关键问题将阻塞进度。

7. **完成开发分支** - 在任务完成时触发。验证测试，提供选项（合并/提交拉取请求/保留/弃用），清理工作树。

**代理会在任何任务开始前检查相关技能。** 这些是强制性工作流，而非建议。

## 内容简介

### 技能库

**测试**
- **测试驱动开发** - RED-GREEN-REFACTOR 循环（包含测试反模式参考）

**调试**
- **系统化调试** - 四阶段根本原因排查流程（包含根本原因追踪、深度防御、基于条件的等待技术）
- **完成前验证** - 确保问题已真正修复

**协作** 
- **头脑风暴** - 苏格拉底式设计优化
- **制定计划** - 详细的实施计划
- **执行计划** - 带检查点的批量执行
- **调度并行代理** - 并发子代理工作流
- **请求代码审查** - 预审查检查清单
- **接收代码审查** - 回应反馈
- **使用 Git 工作树** - 并行开发分支
- **完成开发分支** - 合并/PR决策工作流
- **子代理驱动开发** - 通过两阶段审查实现快速迭代（先检查规范符合性，再检查代码质量）

**元层面**
- **写作技能** - 遵循最佳实践创建新技能（包括测试方法论）
- **使用超级技能** - 技能系统简介

## 理念

- **测试驱动开发** - 始终先编写测试
- **系统化胜于临时应付** - 流程重于猜测
- **降低复杂度** - 以简洁为首要目标
- **证据优先于主张** - 验证后再宣布成功

请阅读 [原始发布公告](https://blog.fsck.com/2025/10/09/superpowers/)。

## 贡献

Superpowers 的一般贡献流程如下。请注意，我们通常不接受新技能的贡献，且对技能的任何更新都必须在我们支持的所有编码代理上都能正常运行。

1. 分叉代码库
2. 切换到 'dev' 分支
3. 为您的开发工作创建一个分支
4. 参考 `writing-skills` 技能的实现方式来创建和测试新技能或修改后的技能
5. 提交拉取请求（PR），请务必填写拉取请求模板。

技能行为测试使用来自 [superpowers-evals](https://github.com/prime-radiant-inc/superpowers-evals/) 的 drill eval 测试框架，该框架已克隆到 `evals/` 中——有关设置方法，请参阅 `evals/README.md`。 插件基础设施测试位于 `tests/`，并通过相应的 `run-*.sh` 或 `npm test` 运行。

完整指南请参见 `skills/writing-skills/SKILL.md`。

## 更新

Superpowers 的更新在一定程度上取决于编码代理，但通常是自动进行的。

## 许可协议

MIT 许可协议——详情请参阅 LICENSE 文件

## 可视化伴侣遥测

由于技能和插件不会向创作者提供任何反馈，我们无从得知有多少用户正在使用 Superpowers。默认情况下，头脑风暴功能中可选的可视化伴侣功能所显示的 Prime Radiant 徽标是从我们的网站加载的。该徽标包含当前使用的 Superpowers 版本信息。 该徽标不包含任何关于您的项目、提示词或编码代理的详细信息。我们无法看到您的点击操作，也无法获知您正在构建的内容。这有助于我们大致了解有多少人正在使用 Superpowers 以及他们使用的是哪个版本。 此功能完全可选。若要禁用，请将环境变量 `SUPERPOWERS_DISABLE_TELEMETRY` 设置为任意真值。Superpowers 同时也支持 Claude Code 的 `DISABLE_TELEMETRY` 和 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 退出选项。

## 社区

Superpowers 由 [Jesse Vincent](https://blog.fsck.com) 以及 [Prime Radiant](https://primeradiant.com) 的其他成员共同开发。

- **Discord**：[加入我们](https://discord.gg/35wsABTejz)，获取社区支持、提出问题，并分享您使用 Superpowers 开发的作品
- **问题跟踪**：https://github.com/obra/superpowers/issues
- **版本发布公告**：[订阅](https://primeradiant.com/superpowers/) 以获取新版本通知
