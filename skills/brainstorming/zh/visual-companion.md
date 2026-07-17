# 可视化辅助指南

基于浏览器的可视化头脑风暴辅助工具，用于展示原型、图表和选项。

## 何时使用

应针对每个问题单独决定，而非按每次测试环节决定。判断标准是：**用户通过查看这些内容是否比阅读文字更能理解？**

当内容本身具有视觉性时，**请使用浏览器**：

- **UI 原型图** —— 线框图、版式、导航结构、组件设计
- **架构图** —— 系统组件、数据流、关系图
- **并排视觉对比** —— 比较两种布局、两种配色方案、两种设计方向
- **设计优化** —— 当问题涉及外观与感觉、间距、视觉层次时
- **空间关系** —— 状态机、流程图、以图表形式呈现的实体关系

当内容为文本或表格时，**请使用终端**：

- **需求和范围相关问题** ——“X 是什么意思？”、“哪些功能在范围之内？”
- **概念性 A/B/C 选项** ——在文字描述的方案之间进行选择
- **权衡列表** —— 优缺点、对比表
- **技术决策** —— API 设计、数据建模、架构方案选择
- **澄清性问题** —— 任何答案以文字形式呈现、而非视觉偏好的问题

一个*关于* UI 主题的问题并不一定就是视觉问题。 “你想要什么样的向导？”是概念性的——请使用终端。“这些向导布局中哪一个感觉最合适？”是视觉性的——请使用浏览器。

## 工作原理

服务器监听某个目录中的 HTML 文件，并将最新的一份提供给浏览器。 您将 HTML 内容写入 `screen_dir`，用户在浏览器中看到该内容并可点击选择选项。选项会被记录到 `state_dir/events` 中，供您在下个轮次读取。

**内容片段与完整文档：** 如果您的 HTML 文件以 `<!DOCTYPE` 或 `<html` 开头，服务器将原样提供该文件（仅注入辅助脚本）。否则，服务器会自动将您的内容封装到框架模板中——添加页眉、CSS 主题、连接状态以及所有交互式基础设施。 **默认情况下请编写内容片段。** 仅当您需要完全控制页面时，才编写完整文档。

## 启动会话

```bash
# Start AFTER the user approves the companion. --open auto-opens their browser on
# the first screen; --project-dir persists mockups and enables same-port restart.
scripts/start-server.sh --project-dir /path/to/project --open

# Returns: {"type":"server-started","port":52341,
#           "url":"http://localhost:52341/?key=ab12…",
#           "screen_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/content",
#           "state_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/state"}
```

从响应中保存 `screen_dir` 和 `state_dir`。 有了 `--open`，当您推送第一个屏幕时，浏览器会自动打开——您无需要求用户手动打开，但仍应分享该 URL 作为备用方案（无头/远程环境不会自动打开）。

**该 URL 包含一个会话密钥（`?key=…`）。** 服务器会拒绝任何
缺少该密钥的请求，因此请务必向用户提供来自 `url` 字段的 **完整** URL ——
切勿删除查询字符串，也切勿仅提供裸露的 `http://host:port`。 该
密钥用于控制 HTTP 和 WebSocket 访问，因此闲置的浏览器标签页或网络中的
其他设备无法读取屏幕内容或注入事件。首次加载后，
浏览器会通过 Cookie 记住该密钥，因此刷新页面和 `/files/*` 资源时
无需重复提供该密钥。

**查找连接信息：** 服务器会将其启动时的 JSON 写入 `$STATE_DIR/server-info`。如果你在后台启动了服务器且未捕获标准输出，请读取该文件以获取 URL 和端口。使用 `--project-dir` 时，请检查 `<project>/.superpowers/brainstorm/` 以获取会话目录。

**注意：**将项目根目录作为 `--project-dir` 传递，这样原型文件才会保存在 `.superpowers/brainstorm/` 中，并在服务器重启后保留。如果不这样做，文件会被保存到 `/tmp` 并被清理。 请提醒用户，如果 `.superpowers/` 尚未存在于 `.gitignore` 中，请将其添加进去。

**按平台启动服务器：**

**Claude 代码：**
```bash
# Default mode works — the script backgrounds the server itself.
scripts/start-server.sh --project-dir /path/to/project --open
```

在 Windows 上，脚本会自动检测并切换到前台模式（这会阻塞工具调用）。在 Bash 工具调用中使用 `run_in_background: true`，以便服务器在对话轮次间保持运行，然后在下一轮次读取 `$STATE_DIR/server-info` 以获取 URL 和端口。

**Codex：**
```bash
# Codex reaps background processes. The script auto-detects CODEX_CI and
# switches to foreground mode. Run it normally — no extra flags needed.
scripts/start-server.sh --project-dir /path/to/project --open
```

**Copilot CLI：**
```bash
# Use --foreground and start the server via the bash tool with mode: "async"
# so the process survives across turns. Capture the returned shellId for
# read_bash / stop_bash if you need to interact with it later.
scripts/start-server.sh --project-dir /path/to/project --open --foreground
```

**其他环境：** 服务器必须在对话轮次之间持续在后台运行。 如果您的环境会回收脱离进程，请使用 `--foreground`，并通过您平台的后台执行机制启动该命令。

如果无法通过浏览器访问该 URL（在远程/容器化环境中很常见），请绑定一个非回环主机：

```bash
scripts/start-server.sh \
  --project-dir /path/to/project \
  --host 0.0.0.0 \
  --url-host localhost
```

使用 `--url-host` 控制返回的 URL JSON 中显示的主机名。

## 循环流程

1. **检查服务器是否运行**，然后将 **HTML 内容** 写入 `screen_dir` 中的新文件：
   - **必做：在引用 URL 或推送屏幕之前，必须确认服务器处于运行状态。** 检查 `$STATE_DIR/server-info` 是否存在，而 `$STATE_DIR/server-stopped` 是否不存在。如果服务器已关闭，请使用 `start-server.sh` 并采用 **相同的 `--project-dir`** ——它将复用同一端口，因此用户已打开的标签页会自动重新连接（服务器停机期间会显示“暂停”覆盖层），且无需发送新 URL。 服务器在空闲 4 小时后会自动退出（可通过 `--idle-timeout-minutes` 配置）。
   - 使用语义化文件名：`platform.html`、`visual-style.html`、`layout.html`
   - **切勿重复使用文件名** —— 每个屏幕都应使用新文件
   - 使用文件创建工具 —— **切勿使用 cat/heredoc**（会向终端输出冗余信息）
   - 服务器会自动提供最新文件

2. **告知用户预期内容并结束当前轮次：**
   - 提醒用户 URL（每个步骤都要提醒，不仅限于第一步）
   - 简要文字概述屏幕内容（例如：“正在显示 3 种首页布局选项”）
   - 请用户在终端中回复：“请查看并告诉我您的想法。如果愿意，请点击选择一个选项。”

3. **在你的下一个回合** —— 用户在终端中响应后：
   - 若存在 `$STATE_DIR/events` 文件，请读取该文件 —— 其中包含用户浏览器交互记录（点击、选择）以 JSON 行形式呈现
   - 将其与用户的终端文本合并，以获取完整情况
   - 终端消息是主要反馈；`state_dir/events` 提供结构化的交互数据

4. **迭代或推进** —— 如果反馈导致当前屏幕发生变化，则写入新文件（例如 `layout-v2.html`）。 仅在当前步骤通过验证后才转到下一个问题。

5. **返回终端时清空** —— 当下一步无需使用浏览器时（例如，澄清性问题、权衡讨论），推送一个等待屏幕以清除过时内容：

   ```html
   <!-- filename: waiting.html (or waiting-2.html, etc.) -->
   <div style="display:flex;align-items:center;justify-content:center;min-height:60vh">
     <p class="subtitle">Continuing in terminal...</p>
   </div>
   ```

   这可防止用户在对话已进入下一阶段时，仍盯着已解决的选择项发呆。当下一个可视化问题出现时，照常推送新的内容文件。

6. 重复此过程直至完成。

## 编写内容片段

只需编写页面内部的内容即可。服务器会自动将其封装到框架模板中（包括页眉、主题 CSS、连接状态以及所有交互基础设施）。

**最简示例：**

```html
<h2>Which layout works better?</h2>
<p class="subtitle">Consider readability and visual hierarchy</p>

<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Single Column</h3>
      <p>Clean, focused reading experience</p>
    </div>
  </div>
  <div class="option" data-choice="b" onclick="toggleSelect(this)">
    <div class="letter">B</div>
    <div class="content">
      <h3>Two Column</h3>
      <p>Sidebar navigation with main content</p>
    </div>
  </div>
</div>
```

就这样。无需 `<html>`、CSS 或 `<script>` 标签。服务器会自动提供所有这些内容。

## 可用 CSS 类

框架模板为您的内容提供了以下 CSS 类：

### 选项（A/B/C 选项）

```html
<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Title</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

**多选：** 在容器中添加 `data-multiselect`，允许用户选择多个选项。每次点击都会切换该选项的选中样式。

```html
<div class="options" data-multiselect>
  <!-- same option markup — users can select/deselect multiple -->
</div>
```

### 卡片（视觉设计）

```html
<div class="cards">
  <div class="card" data-choice="design1" onclick="toggleSelect(this)">
    <div class="card-image"><!-- mockup content --></div>
    <div class="card-body">
      <h3>Name</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

### 原型容器

```html
<div class="mockup">
  <div class="mockup-header">Preview: Dashboard Layout</div>
  <div class="mockup-body"><!-- your mockup HTML --></div>
</div>
```

### 分屏视图（并排显示）

```html
<div class="split">
  <div class="mockup"><!-- left --></div>
  <div class="mockup"><!-- right --></div>
</div>
```

### 优缺点

```html
<div class="pros-cons">
  <div class="pros"><h4>Pros</h4><ul><li>Benefit</li></ul></div>
  <div class="cons"><h4>Cons</h4><ul><li>Drawback</li></ul></div>
</div>
```

### 原型元素（线框图构建模块）

```html
<div class="mock-nav">Logo | Home | About | Contact</div>
<div style="display: flex;">
  <div class="mock-sidebar">Navigation</div>
  <div class="mock-content">Main content area</div>
</div>
<button class="mock-button">Action Button</button>
<input class="mock-input" placeholder="Input field">
<div class="placeholder">Placeholder area</div>
```

### 排版与版块

- `h2` — 页面标题
- `h3` — 版块标题
- `.subtitle` — 标题下方的次要文本
- `.section` — 带有底部边距的内容块
- `.label` — 小型大写标签文本

## 浏览器事件格式

当用户在浏览器中点击选项时，其交互操作会被记录到 `$STATE_DIR/events` 中（每行一个 JSON 对象）。当您推送新屏幕时，该文件会自动清空。

```jsonl
{"type":"click","choice":"a","text":"Option A - Simple Layout","timestamp":1706000101}
{"type":"click","choice":"c","text":"Option C - Complex Grid","timestamp":1706000108}
{"type":"click","choice":"b","text":"Option B - Hybrid","timestamp":1706000115}
```

完整的事件流展示了用户的探索路径——他们在做出决定前可能会点击多个选项。最后一个 `choice` 事件通常代表最终选择，但点击模式可能揭示出值得进一步询问的犹豫或偏好。

如果不存在 `$STATE_DIR/events`，则表示用户未与浏览器进行交互——此时仅使用终端文本。

## 设计建议

- **根据问题调整设计保真度** —— 布局问题使用线框图，细节问题使用精细设计稿
- **在每页说明问题** —— 例如“哪种布局看起来更专业？”，而非仅仅“选一个”
- **推进前先迭代** —— 如果反馈导致当前屏幕内容发生变化，请撰写新版本
- **每屏选项最多 2-4 个**
- **关键处使用真实内容** —— 对于摄影作品集，请使用真实图片（Unsplash）。占位内容会掩盖设计问题。
- **保持原型简洁** —— 专注于布局和结构，而非像素级精准设计

## 文件命名

- 使用语义化命名：`platform.html`、`visual-style.html`、`layout.html`
- 切勿重复使用文件名——每个界面必须是一个新文件
- 迭代时：在文件名后添加版本后缀，如 `layout-v2.html`、`layout-v3.html`
- 服务器根据修改时间提供最新文件

## 清理

```bash
scripts/stop-server.sh $SESSION_DIR
```

如果该会话使用了 `--project-dir`，原型文件将保留在 `.superpowers/brainstorm/` 中以供日后参考。只有 `/tmp` 会话在停止时才会被删除。

## 参考

- 帧模板（CSS 参考）：`scripts/frame-template.html`
- 辅助脚本（客户端）：`scripts/helper.js`
