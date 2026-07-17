# 技能编写最佳实践

> 了解如何编写有效的技能，以便客服人员能够顺利发现并成功使用。

优秀的技能应简洁明了、结构合理，并经过实际使用测试。本指南提供了实用的编写建议，帮助您编写出客服人员能够顺利发现并有效使用的技能。

有关技能工作原理的概念性背景，请参阅 [技能概述](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)。

## 核心原则

### 简洁是关键

[上下文窗口](https://platform.claude.com/docs/en/build-with-claude/context-windows) 是一项公共资源。您的技能需与智能代理所需了解的其他所有信息共享该上下文窗口，包括：

* 系统提示
* 对话历史记录
* 其他技能的元数据
* 您的实际请求

技能中的并非每个令牌都会立即产生开销。启动时，仅会预加载所有技能的元数据（名称和描述）。 代理仅在技能变得相关时才会读取 SKILL.md，并仅在需要时读取其他文件。不过，SKILL.md 的简洁性依然重要：一旦代理加载该文件，其中的每个令牌都会与对话历史记录及其他上下文信息产生竞争。

**默认假设**：代理已经非常智能

仅添加代理尚未掌握的上下文。对每条信息进行审视：

* “代理真的需要这个解释吗？”
* “能否假设代理已经知道这一点？”
* “这一段内容是否值得消耗这些令牌？”

**良好示例：简洁**（约 50 个令牌）：

````markdown  theme={null}
## 提取 PDF 文本

使用 pdfplumber 进行文本提取：

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

**Bad example: Too verbose** (approximately 150 tokens):

```markdown  theme={null}
## 提取 PDF 文本

PDF（便携式文档格式）文件是一种常见的文件格式，其中包含
文本、图像和其他内容。要从 PDF 中提取文本， 你需要
使用一个库。虽然有许多用于 PDF 处理的库，但我们
推荐 pdfplumber，因为它易于使用且能很好地处理大多数情况。
首先，你需要使用 pip 安装它。然后你可以使用下面的代码……
```

The concise version assumes the agent knows what PDFs are and how libraries work.

### Set appropriate degrees of freedom

Match the level of specificity to the task's fragility and variability.

**High freedom** (text-based instructions):

Use when:

* Multiple approaches are valid
* Decisions depend on context
* Heuristics guide the approach

Example:

```markdown  theme={null}
## 代码审查流程

1. 分析代码结构和组织方式
2. 检查潜在的错误或边界情况
3. 针对可读性和可维护性提出改进建议
4. 验证是否符合项目规范
```

**Medium freedom** (pseudocode or scripts with parameters):

Use when:

* A preferred pattern exists
* Some variation is acceptable
* Configuration affects behavior

Example:

````markdown  theme={null}
## 生成报告

使用此模板并根据需要进行自定义：

```python
def generate_report(data, format="markdown", include_charts=True):
    # Process data
    # Generate output in specified format
    # Optionally include visualizations
```
`ZZZPH5ZZZ`markdown  theme={null}
## 数据库迁移

请精确运行此脚本：

```bash
python scripts/migrate.py --verify --backup
```

请勿修改命令或添加额外参数。
````

**Analogy**: Think of the agent as a robot exploring a path:

* **Narrow bridge with cliffs on both sides**: There's only one safe way forward. Provide specific guardrails and exact instructions (low freedom). Example: database migrations that must run in exact sequence.
* **Open field with no hazards**: Many paths lead to success. Give general direction and trust the agent to find the best route (high freedom). Example: code reviews where context determines the best approach.

### Test with all models you plan to use

Skills act as additions to models, so effectiveness depends on the underlying model. Test your Skill with all the models you plan to use it with.

**Testing considerations by model**:

* **Claude Haiku** (fast, economical): Does the Skill provide enough guidance?
* **Claude Sonnet** (balanced): Is the Skill clear and efficient?
* **Claude Opus** (powerful reasoning): Does the Skill avoid over-explaining?

What works perfectly for Opus might need more detail for Haiku. If you plan to use your Skill across multiple models, aim for instructions that work well with all of them.

## Skill structure

<Note>
  **YAML Frontmatter**: The SKILL.md frontmatter requires two fields:

  * `name` - Human-readable name of the Skill (64 characters maximum)
  * `description` - One-line description of what the Skill does and when to use it (1024 characters maximum)

  For complete Skill structure details, see the [Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#skill-structure).
</Note>

### Naming conventions

Use consistent naming patterns to make Skills easier to reference and discuss. We recommend using **gerund form** (verb + -ing) for Skill names, as this clearly describes the activity or capability the Skill provides.

**Good naming examples (gerund form)**:

* "Processing PDFs"
* "Analyzing spreadsheets"
* "Managing databases"
* "Testing code"
* "Writing documentation"

**Acceptable alternatives**:

* Noun phrases: "PDF Processing", "Spreadsheet Analysis"
* Action-oriented: "Process PDFs", "Analyze Spreadsheets"

**Avoid**:

* Vague names: "Helper", "Utils", "Tools"
* Overly generic: "Documents", "Data", "Files"
* Inconsistent patterns within your skill collection

Consistent naming makes it easier to:

* Reference Skills in documentation and conversations
* Understand what a Skill does at a glance
* Organize and search through multiple Skills
* Maintain a professional, cohesive skill library

### Writing effective descriptions

The `description` field enables Skill discovery and should include both what the Skill does and when to use it.

<Warning>
  **Always write in third person**. The description is injected into the system prompt, and inconsistent point-of-view can cause discovery problems.

  * **Good:** "Processes Excel files and generates reports"
  * **Avoid:** "I can help you process Excel files"
  * **Avoid:** "You can use this to process Excel files"
</Warning>

**Be specific and include key terms**. Include both what the Skill does and specific triggers/contexts for when to use it.

Each Skill has exactly one description field. The description is critical for skill selection: agents use it to choose the right Skill from potentially 100+ available Skills. Your description must provide enough detail for an agent to know when to select this Skill, while the rest of SKILL.md provides the implementation details.

Effective examples:

**PDF Processing skill:**

```yaml  theme={null}
描述：从 PDF 文件中提取文本和表格，填写表单，合并文档。在处理 PDF 文件时，或当用户提及 PDF、表单或文档提取时使用。
```

**Excel Analysis skill:**

```yaml  theme={null}
description: 分析 Excel 电子表格、创建数据透视表、生成图表。在分析 Excel 文件、电子表格、表格数据或 .xlsx 文件时使用。
```

**Git Commit Helper skill:**

```yaml  theme={null}
描述：通过分析 Git 差异生成描述性提交信息。当用户请求帮助编写提交信息或审查已暂存的更改时使用。
```

Avoid vague descriptions like these:

```yaml  theme={null}
description: 协助处理文档
```

```yaml  theme={null}
description: 处理数据
```

```yaml  theme={null}
description: 处理文件相关操作
```

### Progressive disclosure patterns

SKILL.md serves as an overview that points agents to detailed materials as needed, like a table of contents in an onboarding guide. For an explanation of how progressive disclosure works, see [How Skills work](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work) in the overview.

**Practical guidance:**

* Keep SKILL.md body under 500 lines for optimal performance
* Split content into separate files when approaching this limit
* Use the patterns below to organize instructions, code, and resources effectively

#### Visual overview: From simple to complex

A basic Skill starts with just a SKILL.md file containing metadata and instructions:

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=87782ff239b297d9a9e8e1b72ed72db9" alt="Simple SKILL.md file showing YAML frontmatter and markdown body" data-og-width="2048" width="2048" data-og-height="1153" height="1153" data-path="images/agent-skills-simple-file.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=c61cc33b6f5855809907f7fda94cd80e 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=90d2c0c1c76b36e8d485f49e0810dbfd 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=ad17d231ac7b0bea7e5b4d58fb4aeabb 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=f5d0a7a3c668435bb0aee9a3a8f8c329 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=0e927c1af9de5799cfe557d12249f6e6 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=46bbb1a51dd4c8202a470ac8c80a893d 2500w" />

As your Skill grows, you can bundle additional content that agents load only when needed:

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=a5e0aa41e3d53985a7e3e43668a33ea3" alt="Bundling additional reference files like reference.md and forms.md." data-og-width="2048" width="2048" data-og-height="1327" height="1327" data-path="images/agent-skills-bundling-content.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=f8a0e73783e99b4a643d79eac86b70a2 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=dc510a2a9d3f14359416b706f067904a 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=82cd6286c966303f7dd914c28170e385 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=56f3be36c77e4fe4b523df209a6824c6 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=d22b5161b2075656417d56f41a74f3dd 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=3dd4bdd6850ffcc96c6c45fcb0acd6eb 2500w" />

The complete Skill directory structure might look like this:

```
pdf/
├── SKILL.md # 主要说明（触发时加载）
├── FORMS.md # 表单填写指南（按需加载）
├── reference.md # API 参考（按需加载）
├── examples.md # 使用示例（按需加载）
└── scripts/
    ├── analyze_form.py   # 实用脚本（执行，不加载）
    ├── fill_form.py # 表单填写脚本
    └── validate.py # 验证脚本
```

#### Pattern 1: High-level guide with references

````markdown  theme={null}
---
name: PDF 处理
description: 从 PDF 文件中提取文本和表格，填写表单，并合并文档。在处理 PDF 文件时，或当用户提及 PDF、表单或文档提取时使用。
---

# PDF 处理

## 快速入门

使用 pdfplumber 提取文本：
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## 高级功能

**表单填写**：完整指南请参见 [FORMS.md](FORMS.md)
**API 参考**：所有方法请参见 [REFERENCE.md](REFERENCE.md)
**示例**：常见模式请参见 [EXAMPLES.md](EXAMPLES.md)
````

Agents load FORMS.md, REFERENCE.md, or EXAMPLES.md only when needed.

#### Pattern 2: Domain-specific organization

For Skills with multiple domains, organize content by domain to avoid loading irrelevant context. When a user asks about sales metrics, the agent only needs to read sales-related schemas, not finance or marketing data. This keeps token usage low and context focused.

```
bigquery-skill/
├── SKILL.md（概述与导航）
└── reference/
    ├── finance.md（收入、计费指标）
    ├── sales.md（商机、销售漏斗）
    ├── product.md（API 使用、功能）
    └── marketing.md（营销活动、归因）
```

````markdown SKILL.md theme={null}
# BigQuery 数据分析

## 可用数据集

**财务**：收入、ARR、计费 → 参见 [reference/finance.md](reference/finance.md)
**销售**：商机、销售管道、客户 → 参见 [reference/sales.md](reference/sales.md)
**产品**：API 使用情况、功能、采用率 → 参见 [reference/product.md](reference/product.md)
**营销**：营销活动、归因、电子邮件 → 参见 [reference/marketing.md](reference/marketing.md)

## 快速搜索

使用 grep 查找特定指标：

```bash
grep -i "revenue" reference/finance.md
grep -i "pipeline" reference/sales.md
grep -i "api usage" reference/product.md
```
````

#### Pattern 3: Conditional details

Show basic content, link to advanced content:

```markdown  theme={null}
# DOCX 处理

## 创建文档

使用 docx-js 创建新文档。 参见 [DOCX-JS.md](DOCX-JS.md)。

## 编辑文档

对于简单的编辑，请直接修改 XML。

**关于修订标记**：参见 [REDLINING.md](REDLINING.md)
**关于 OOXML 的详细信息**：请参阅 [OOXML.md](OOXML.md)
```

Agents read REDLINING.md or OOXML.md only when the user needs those features.

### Avoid deeply nested references

Agents may partially read files when they're referenced from other referenced files. When encountering nested references, an agent might use commands like `head -100` to preview content rather than reading entire files, resulting in incomplete information.

**Keep references one level deep from SKILL.md**. All reference files should link directly from SKILL.md to ensure agents read complete files when needed.

**Bad example: Too deep**:

```markdown  theme={null}
# SKILL.md
请参阅 [advanced.md](advanced.md)...

# advanced.md
参见 [details.md](details.md)...

# details.md
以下是具体信息...
```

**Good example: One level deep**:

```markdown  theme={null}
# SKILL.md

**基本用法**：[请参阅 SKILL.md 中的说明]
**高级功能**：请参阅 [advanced.md](advanced.md)
**API 参考**：请参阅 [reference.md](reference.md)
**示例**：参见 [examples.md](examples.md)
```

### Structure longer reference files with table of contents

For reference files longer than 100 lines, include a table of contents at the top. This ensures agents can see the full scope of available information even when previewing with partial reads.

**Example**:

```markdown  theme={null}
# API 参考

## 目录
- 身份验证与配置
- 核心方法（创建、读取、更新、删除）
- 高级功能（批量操作、Webhook）
- 错误处理模式
- 代码示例

## 身份验证与配置
...

## 核心方法
...
```

Agents can then read the complete file or jump to specific sections as needed.

For details on how this filesystem-based architecture enables progressive disclosure, see the [Runtime environment](#runtime-environment) section in the Advanced section below.

## Workflows and feedback loops

### Use workflows for complex tasks

Break complex operations into clear, sequential steps. For particularly complex workflows, provide a checklist that the agent can copy into its response and check off as it progresses.

**Example 1: Research synthesis workflow** (for Skills without code):

````markdown  theme={null}
## 研究综述工作流

复制此检查清单并跟踪您的进度：

```
Research Progress:
- [ ] Step 1: Read all source documents
- [ ] Step 2: Identify key themes
- [ ] Step 3: Cross-reference claims
- [ ] Step 4: Create structured summary
- [ ] Step 5: Verify citations
```

**步骤 1：阅读所有源文档**

审阅 `sources/` 目录中的每份文档。记录主要论点及支持证据。

**步骤 2：识别关键主题**

寻找各来源之间的共性。哪些主题反复出现？各来源在哪些方面达成共识或存在分歧？

**步骤 3：交叉核对论点**

针对每个主要论点，核实其是否出现在原始资料中。记录每个论点由哪份来源支持。

**步骤 4：编写结构化摘要**

按主题整理研究结果。内容应包括：
- 主要论点
- 来源中的支持证据
- 冲突观点（如有）

**步骤 5：核对引用**

检查每个论点是否引用了正确的来源文档。如果引用不完整，请返回步骤 3。
`ZZZPH25ZZZ`markdown  theme={null}
## PDF 表单填写工作流

复制此检查清单，并在完成各项任务后勾选：

```
Task Progress:
- [ ] Step 1: Analyze the form (run analyze_form.py)
- [ ] Step 2: Create field mapping (edit fields.json)
- [ ] Step 3: Validate mapping (run validate_fields.py)
- [ ] Step 4: Fill the form (run fill_form.py)
- [ ] Step 5: Verify output (run verify_output.py)
```

**步骤 1：分析表单**

运行：`python scripts/analyze_form.py input.pdf`

这将提取表单字段及其位置，并保存到 `fields.json`。

**步骤 2：创建字段映射**

编辑 `fields.json` 以添加每个字段的值。

**步骤 3：验证映射**

运行：`python scripts/validate_fields.py fields.json`

在继续之前，请修复任何验证错误。

**步骤 4：填写表单**

运行：`python scripts/fill_form.py input.pdf fields.json output.pdf`

**步骤 5：验证输出**

运行：`python scripts/verify_output.py output.pdf`

如果验证失败，请返回步骤 2。
````

Clear steps prevent agents from skipping critical validation. The checklist helps both you and the agent track progress through multi-step workflows.

### Implement feedback loops

**Common pattern**: Run validator → fix errors → repeat

This pattern greatly improves output quality.

**Example 1: Style guide compliance** (for Skills without code):

```markdown  theme={null}
## 内容审核流程

1. 根据 STYLE_GUIDE.md 中的指南起草内容
2. 对照检查清单进行审核：
   - 检查术语的一致性
   - 验证示例是否符合标准格式
   - 确认所有必填部分均已包含
3. 若发现问题：
   - 针对每个问题注明具体章节位置
   - 修改内容
   - 再次核对检查清单
4. 仅在满足所有要求后方可继续
5. 最终定稿并保存文档
```

This shows the validation loop pattern using reference documents instead of scripts. The "validator" is STYLE\_GUIDE.md, and the agent performs the check by reading and comparing.

**Example 2: Document editing process** (for Skills with code):

```markdown  theme={null}
## 文档编辑流程

1. 对 `word/document.xml` 进行编辑
2. **立即验证**：`python ooxml/scripts/validate.py unpacked_dir/`
3. 若验证失败：
   - 仔细查看错误信息
   - 修复 XML 中的问题
   - 重新运行验证
4. **仅在验证通过后才继续**
5. 重新构建：`python ooxml/scripts/pack.py unpacked_dir/ output.docx`
6. 测试生成的文档
```

The validation loop catches errors early.

## Content guidelines

### Avoid time-sensitive information

Don't include information that will become outdated:

**Bad example: Time-sensitive** (will become wrong):

```markdown  theme={null}
若在 2025 年 8 月之前进行此操作，请使用旧版 API。
2025 年 8 月之后，请使用新版 API。
```

**Good example** (use "old patterns" section):

```markdown  theme={null}
## 当前方法

使用 v2 API 端点：`api.example.com/v2/messages`

## 旧模式

<details>
<summary>旧版 v1 API（将于 2025 年 8 月弃用）</summary>

使用的 v1 API：`api.example.com/v1/messages`

该端点已不再受支持。
</details>
```

The old patterns section provides historical context without cluttering the main content.

### Use consistent terminology

Choose one term and use it throughout the Skill:

**Good - Consistent**:

* Always "API endpoint"
* Always "field"
* Always "extract"

**Bad - Inconsistent**:

* Mix "API endpoint", "URL", "API route", "path"
* Mix "field", "box", "element", "control"
* Mix "extract", "pull", "get", "retrieve"

Consistency helps agents understand and follow instructions.

## Common patterns

### Template pattern

Provide templates for output format. Match the level of strictness to your needs.

**For strict requirements** (like API responses or data formats):

````markdown  theme={null}
## 报告结构

请务必始终使用此精确的模板结构：

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```
`ZZZPH33ZZZ`markdown  theme={null}
## 报告结构

以下是一个合理的默认格式，但请根据分析结果自行判断：

```markdown
# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]
```

请根据具体的分析类型调整各部分内容。
`ZZZPH35ZZZ`markdown  theme={null}
## 提交信息格式

请参照以下示例生成提交信息：

**示例 1：**
输入：添加了基于 JWT 令牌的用户身份验证
输出：
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**示例 2：**
输入：修复了报告中日期显示错误的 bug
输出：
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

**示例 3：**
输入：更新了依赖项并重构了错误处理
输出：
```
chore: update dependencies and refactor error handling

- Upgrade lodash to 4.17.21
- Standardize error response format across endpoints
```

请遵循以下格式：类型(范围)：简要描述，随后是详细说明。
````

Examples help agents understand the desired style and level of detail more clearly than descriptions alone.

### Conditional workflow pattern

Guide agents through decision points:

```markdown  theme={null}
## 文档修改工作流

1. 确定修改类型：

   **创建新内容？** → 请遵循下方的“创建工作流”
   **编辑现有内容？** → 请遵循下方的“编辑工作流”

2. 创建工作流：
   - 使用 docx-js 库
   - 从头开始构建文档
   - 导出为 .docx 格式

3. 编辑工作流：
   - 解压现有文档
   - 直接修改 XML
   - 每次修改后进行验证
   - 完成后重新打包
```

<Tip>
  If workflows become large or complicated with many steps, consider pushing them into separate files and tell the agent to read the appropriate file based on the task at hand.
</Tip>

## Evaluation and iteration

### Build evaluations first

**Create evaluations BEFORE writing extensive documentation.** This ensures your Skill solves real problems rather than documenting imagined ones.

**Evaluation-driven development:**

1. **Identify gaps**: Run your agent on representative tasks without a Skill. Document specific failures or missing context
2. **Create evaluations**: Build three scenarios that test these gaps
3. **Establish baseline**: Measure the agent's performance without the Skill
4. **Write minimal instructions**: Create just enough content to address the gaps and pass evaluations
5. **Iterate**: Execute evaluations, compare against baseline, and refine

This approach ensures you're solving actual problems rather than anticipating requirements that may never materialize.

**Evaluation structure**:

```json  theme={null}
{
  "skills": ["pdf-processing"],
  "query": "从该 PDF 文件中提取所有文本并保存到 output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "使用合适的 PDF 处理库或命令行工具成功读取 PDF 文件",
    "从文档的所有页面中提取文本内容，且不遗漏任何页面",
    "将提取的文本以清晰、可读的格式保存到名为 output.txt 的文件中"
  ]
}
```

<Note>
  This example demonstrates a data-driven evaluation with a simple testing rubric. We do not currently provide a built-in way to run these evaluations. Users can create their own evaluation system. Evaluations are your source of truth for measuring Skill effectiveness.
</Note>

### Develop Skills iteratively with the agent

The most effective Skill development process involves the agent itself. Work with one instance ("Agent A") to create a Skill that will be used by other instances ("Agent B"). Agent A helps you design and refine instructions, while Agent B tests them in real tasks. This works because the underlying models understand both how to write effective agent instructions and what information agents need.

**Creating a new Skill:**

1. **Complete a task without a Skill**: Work through a problem with Agent A using normal prompting. As you work, you'll naturally provide context, explain preferences, and share procedural knowledge. Notice what information you repeatedly provide.

2. **Identify the reusable pattern**: After completing the task, identify what context you provided that would be useful for similar future tasks.

   **Example**: If you worked through a BigQuery analysis, you might have provided table names, field definitions, filtering rules (like "always exclude test accounts"), and common query patterns.

3. **Ask Agent A to create a Skill**: "Create a Skill that captures this BigQuery analysis pattern we just used. Include the table schemas, naming conventions, and the rule about filtering test accounts."

   <Tip>
     Modern agents understand the Skill format and structure natively. You don't need special system prompts or a "writing skills" skill to get help creating Skills. Simply ask the agent to create a Skill and it will generate properly structured SKILL.md content with appropriate frontmatter and body content.
   </Tip>

4. **Review for conciseness**: Check that Agent A hasn't added unnecessary explanations. Ask: "Remove the explanation about what win rate means - the agent already knows that."

5. **Improve information architecture**: Ask Agent A to organize the content more effectively. For example: "Organize this so the table schema is in a separate reference file. We might add more tables later."

6. **Test on similar tasks**: Use the Skill with Agent B (a fresh instance with the Skill loaded) on related use cases. Observe whether Agent B finds the right information, applies rules correctly, and handles the task successfully.

7. **Iterate based on observation**: If Agent B struggles or misses something, return to Agent A with specifics: "When the agent used this Skill, it forgot to filter by date for Q4. Should we add a section about date filtering patterns?"

**Iterating on existing Skills:**

The same hierarchical pattern continues when improving Skills. You alternate between:

* **Working with Agent A** (the expert who helps refine the Skill)
* **Testing with Agent B** (the agent using the Skill to perform real work)
* **Observing Agent B's behavior** and bringing insights back to Agent A

1. **Use the Skill in real workflows**: Give Agent B (with the Skill loaded) actual tasks, not test scenarios

2. **Observe Agent B's behavior**: Note where it struggles, succeeds, or makes unexpected choices

   **Example observation**: "When I asked Agent B for a regional sales report, it wrote the query but forgot to filter out test accounts, even though the Skill mentions this rule."

3. **Return to Agent A for improvements**: Share the current SKILL.md and describe what you observed. Ask: "I noticed Agent B forgot to filter test accounts when I asked for a regional report. The Skill mentions filtering, but maybe it's not prominent enough?"

4. **Review Agent A's suggestions**: Agent A might suggest reorganizing to make rules more prominent, using stronger language like "MUST filter" instead of "always filter", or restructuring the workflow section.

5. **Apply and test changes**: Update the Skill with Agent A's refinements, then test again with Agent B on similar requests

6. **Repeat based on usage**: Continue this observe-refine-test cycle as you encounter new scenarios. Each iteration improves the Skill based on real agent behavior, not assumptions.

**Gathering team feedback:**

1. Share Skills with teammates and observe their usage
2. Ask: Does the Skill activate when expected? Are instructions clear? What's missing?
3. Incorporate feedback to address blind spots in your own usage patterns

**Why this approach works**: Agent A understands agent needs, you provide domain expertise, Agent B reveals gaps through real usage, and iterative refinement improves Skills based on observed behavior rather than assumptions.

### Observe how agents navigate Skills

As you iterate on Skills, pay attention to how agents actually use them in practice. Watch for:

* **Unexpected exploration paths**: Does the agent read files in an order you didn't anticipate? This might indicate your structure isn't as intuitive as you thought
* **Missed connections**: Does the agent fail to follow references to important files? Your links might need to be more explicit or prominent
* **Overreliance on certain sections**: If the agent repeatedly reads the same file, consider whether that content should be in the main SKILL.md instead
* **Ignored content**: If the agent never accesses a bundled file, it might be unnecessary or poorly signaled in the main instructions

Iterate based on these observations rather than assumptions. The 'name' and 'description' in your Skill's metadata are particularly critical. Agents use these when deciding whether to trigger the Skill in response to the current task. Make sure they clearly describe what the Skill does and when it should be used.

## Anti-patterns to avoid

### Avoid Windows-style paths

Always use forward slashes in file paths, even on Windows:

* ✓ **Good**: `scripts/helper.py`, `reference/guide.md`
* ✗ **Avoid**: `scripts\helper.py`, `reference\guide.md`

Unix-style paths work across all platforms, while Windows-style paths cause errors on Unix systems.

### Avoid offering too many options

Don't present multiple approaches unless necessary:

````markdown  theme={null}
**错误示例：选项过多**（容易造成混淆）：
"您可以使用 pypdf、pdfplumber、PyMuPDF、pdf2image，或者..."

**正确示例：提供默认选项**（并保留灵活调整空间）：
"使用 pdfplumber 进行文本提取：
```python
import pdfplumber
```

对于需要 OCR 处理的扫描 PDF，请改用结合 pytesseract 的 pdf2image。"
````

## Advanced: Skills with executable code

The sections below focus on Skills that include executable scripts. If your Skill uses only markdown instructions, skip to [Checklist for effective Skills](#checklist-for-effective-skills).

### Solve, don't punt

When writing scripts for Skills, handle error conditions rather than punting to the agent.

**Good example: Handle errors explicitly**:

```python  theme={null}
def process_file(path):
    """处理文件，若文件不存在则创建。"""
    try:
 with open(path) as f:
 return f.read()
    except FileNotFoundError:
 # 创建包含默认内容的文件，而非报错
 print(f"未找到文件 {path}，正在创建默认文件")
        with open(path, 'w') as f:
 f.write('')
 return ''
    except PermissionError:
 # 提供替代方案，而非直接报错
 print(f"无法访问 {path}，使用默认值")
 return ''
```

**Bad example: Punt to the agent**:

```python  theme={null}
def process_file(path):
    # 直接报错，让代理自行处理
    return open(path).read()
```

Configuration parameters should also be justified and documented to avoid "voodoo constants" (Ousterhout's law). If you don't know the right value, how will the agent determine it?

**Good example: Self-documenting**:

```python  theme={null}
# HTTP 请求通常在 30 秒内完成
# 较长的超时时间可应对网速较慢的情况
REQUEST_TIMEOUT = 30

# 三次重试可在可靠性与速度之间取得平衡
# 大多数间歇性故障在第二次重试时即可解决
MAX_RETRIES = 3
```

**Bad example: Magic numbers**:

```python  theme={null}
TIMEOUT = 47  # 为什么是 47？
RETRIES = 5   # 为什么是 5？
```

### Provide utility scripts

Even if your agent could write a script, pre-made scripts offer advantages:

**Benefits of utility scripts**:

* More reliable than generated code
* Save tokens (no need to include code in context)
* Save time (no code generation required)
* Ensure consistency across uses

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=4bbc45f2c2e0bee9f2f0d5da669bad00" alt="Bundling executable scripts alongside instruction files" data-og-width="2048" width="2048" data-og-height="1154" height="1154" data-path="images/agent-skills-executable-scripts.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=9a04e6535a8467bfeea492e517de389f 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=e49333ad90141af17c0d7651cca7216b 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=954265a5df52223d6572b6214168c428 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=2ff7a2d8f2a83ee8af132b29f10150fd 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=48ab96245e04077f4d15e9170e081cfb 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=0301a6c8b3ee879497cc5b5483177c90 2500w" />

The diagram above shows how executable scripts work alongside instruction files. The instruction file (forms.md) references the script, and the agent can execute it without loading its contents into context.

**Important distinction**: Make clear in your instructions whether the agent should:

* **Execute the script** (most common): "Run `analyze_form.py` to extract fields"
* **Read it as reference** (for complex logic): "See `analyze_form.py` for the field extraction algorithm"

For most utility scripts, execution is preferred because it's more reliable and efficient. See the [Runtime environment](#runtime-environment) section below for details on how script execution works.

**Example**:

````markdown  theme={null}
## 实用脚本

**analyze_form.py**：从 PDF 中提取所有表单字段

```bash
python scripts/analyze_form.py input.pdf > fields.json
```

输出格式：
```json
{
  "field_name": {"type": "text", "x": 100, "y": 200},
  "signature": {"type": "sig", "x": 150, "y": 500}
}
```

**validate_boxes.py**：检查边界框是否重叠

```bash
python scripts/validate_boxes.py fields.json
# Returns: "OK" or lists conflicts
```

**fill_form.py**：将字段值填入 PDF

```bash
python scripts/fill_form.py input.pdf fields.json output.pdf
```
`ZZZPH52ZZZ`markdown  theme={null}
## 表单布局分析

1. 将 PDF 转换为图像：
   ```bash
   python scripts/pdf_to_images.py form.pdf
   ```

2. 分析每页图像以识别表单字段
3. 代理可以直观地查看字段的位置和类型
````

<Note>
  In this example, you'd need to write the `pdf_to_images.py` script.
</Note>

Agent vision capabilities help understand layouts and structures.

### Create verifiable intermediate outputs

When agents perform complex, open-ended tasks, they can make mistakes. The "plan-validate-execute" pattern catches errors early by having the agent first create a plan in a structured format, then validate that plan with a script before executing it.

**Example**: Imagine asking the agent to update 50 form fields in a PDF based on a spreadsheet. Without validation, it might reference non-existent fields, create conflicting values, miss required fields, or apply updates incorrectly.

**Solution**: Use the workflow pattern shown above (PDF form filling), but add an intermediate `changes.json` file that gets validated before applying changes. The workflow becomes: analyze → **create plan file** → **validate plan** → execute → verify.

**Why this pattern works:**

* **Catches errors early**: Validation finds problems before changes are applied
* **Machine-verifiable**: Scripts provide objective verification
* **Reversible planning**: The agent can iterate on the plan without touching originals
* **Clear debugging**: Error messages point to specific problems

**When to use**: Batch operations, destructive changes, complex validation rules, high-stakes operations.

**Implementation tip**: Make validation scripts verbose with specific error messages like "Field 'signature\_date' not found. Available fields: customer\_name, order\_total, signature\_date\_signed" to help the agent fix issues.

### Package dependencies

Skills run in the code execution environment with platform-specific limitations:

* **claude.ai**: Can install packages from npm and PyPI and pull from GitHub repositories
* **Anthropic API**: Has no network access and no runtime package installation

List required packages in your SKILL.md and verify they're available in the [code execution tool documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool).

### Runtime environment

Skills run in a code execution environment with filesystem access, bash commands, and code execution capabilities. For the conceptual explanation of this architecture, see [The Skills architecture](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#the-skills-architecture) in the overview.

**How this affects your authoring:**

**How agents access Skills:**

1. **Metadata pre-loaded**: At startup, the name and description from all Skills' YAML frontmatter are loaded into the system prompt
2. **Files read on-demand**: Agents use their file-reading tools to access SKILL.md and other files from the filesystem when needed
3. **Scripts executed efficiently**: Utility scripts can be executed via bash without loading their full contents into context. Only the script's output consumes tokens
4. **No context penalty for large files**: Reference files, data, or documentation don't consume context tokens until actually read

* **File paths matter**: Agents navigate your skill directory like a filesystem. Use forward slashes (`reference/guide.md`), not backslashes
* **Name files descriptively**: Use names that indicate content: `form_validation_rules.md`, not `doc2.md`
* **Organize for discovery**: Structure directories by domain or feature
  * Good: `reference/finance.md`, `reference/sales.md`
  * Bad: `docs/file1.md`, `docs/file2.md`
* **Bundle comprehensive resources**: Include complete API docs, extensive examples, large datasets; no context penalty until accessed
* **Prefer scripts for deterministic operations**: Write `validate_form.py` rather than asking the agent to generate validation code
* **Make execution intent clear**:
  * "Run `analyze_form.py` to extract fields" (execute)
  * "See `analyze_form.py` for the extraction algorithm" (read as reference)
* **Test file access patterns**: Verify the agent can navigate your directory structure by testing with real requests

**Example:**

```
bigquery-skill/
├── SKILL.md（概述，指向参考文件）
└── reference/
    ├── finance.md（收入指标）
    ├── sales.md（销售漏斗数据）
    └── product.md（使用情况分析）
```

When the user asks about revenue, the agent reads SKILL.md, sees the reference to `reference/finance.md`, and invokes bash to read just that file. The sales.md and product.md files remain on the filesystem, consuming zero context tokens until needed. This filesystem-based model is what enables progressive disclosure. Agents can navigate and selectively load exactly what each task requires.

For complete details on the technical architecture, see [How Skills work](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work) in the Skills overview.

### MCP tool references

If your Skill uses MCP (Model Context Protocol) tools, always use fully qualified tool names to avoid "tool not found" errors.

**Format**: `ServerName:tool_name`

**Example**:

```markdown  theme={null}
使用 BigQuery:bigquery_schema 工具检索表结构。
使用 GitHub:create_issue 工具创建问题。
```

Where:

* `BigQuery` and `GitHub` are MCP server names
* `bigquery_schema` and `create_issue` are the tool names within those servers

Without the server prefix, agents may fail to locate the tool, especially when multiple MCP servers are available.

### Avoid assuming tools are installed

Don't assume packages are available:

````markdown  theme={null}
**错误示例：默认已安装**：
“使用 pdf 库处理该文件。”

**正确示例：明确说明依赖项**：
“安装所需包：`pip install pypdf`

然后使用它：
```python
from pypdf import PdfReader
reader = PdfReader("file.pdf")
```”
````

## 技术说明

### YAML 前置信息要求

SKILL.md 的前置信息需要包含 `name`（最多 64 个字符）和 `description` （最多 1024 个字符）字段。完整的结构详情请参阅 [技能概述](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#skill-structure)。

### 配额限制

为获得最佳性能，请将 SKILL.md 正文控制在 500 行以内。如果内容超过此限制，请按照前面描述的渐进式披露模式将其拆分为多个文件。有关架构的详细信息，请参阅 [技能概述](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work)。

## 有效技能的检查清单

在分享技能之前，请确认以下事项：

### 核心质量

* [ ] 描述具体且包含关键术语
* [ ] 描述同时包含技能的功能及其适用场景
* [ ] SKILL.md 正文少于 500 行
* [ ] 附加细节放在单独的文件中（如有需要）
* [ ] 无时效性信息（或已归入“旧模式”部分）
* [ ] 全文术语使用一致
* [ ] 示例具体而非抽象
* [ ] 文件引用仅有一层深度
* [ ] 恰当使用了渐进式披露
* [ ] 工作流步骤清晰

### 代码与脚本

* [ ] 脚本应解决问题，而非将问题推给代理
* [ ] 错误处理明确且有帮助
* [ ] 不存在“神秘常量”（所有值均有依据）
* [ ] 说明中列出了所需包，并已验证其可用性
* [ ] 脚本附有清晰的文档
* [ ] 不使用 Windows 风格的路径（全部使用正斜杠）
* [ ] 关键操作设有验证/核查步骤
* [ ] 质量关键任务包含反馈循环

### 测试

* [ ] 创建了至少三个评估
* [ ] 已使用 Haiku、Sonnet 和 Opus 进行测试
* [ ] 已针对真实使用场景进行测试
* [ ] 已采纳团队反馈（如适用）

## 后续步骤

<CardGroup cols={2}>
  <Card title="开始使用 Agent Skills" icon="rocket" href="https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart">
    创建您的第一个技能
  </Card>

  <Card title="在 Claude Code 中使用技能" icon="terminal" href="https://code.claude.com/docs/en/skills">
    在 Claude Code 中创建和管理技能
  </Card>

  <Card title="通过 API 使用技能" icon="code" href="https://platform.claude.com/docs/en/build-with-claude/skills-guide">
    通过编程方式上传和使用技能
  </Card>
</CardGroup>
