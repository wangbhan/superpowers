---
name: writing-plans
description: 当您针对多步骤任务制定了规格说明或需求时，请在着手编写代码之前使用此方法
---

# 计划编写

## 概述

在假设工程师对我们的代码库一无所知且品味堪忧的前提下，编写全面的实施方案。将他们需要了解的一切都记录下来：每项任务需要修改哪些文件、可能需要查阅的代码、测试用例和文档，以及如何进行测试。 将整个计划分解为易于消化的任务。遵循 DRY 原则。遵循 YAGNI 原则。采用 TDD。频繁提交。

假设他们是技术娴熟的开发者，但几乎不了解我们的工具集或问题领域。假设他们对良好的测试设计了解不多。

**开始时宣布：** “我正在使用‘编写计划’技能来创建实施计划。”

**背景：** 若在隔离的工作树中工作，该工作树应在执行时通过 `superpowers:using-git-worktrees` 技能创建。

**将计划保存至：** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- （用户对计划位置的偏好设置将覆盖此默认值）

## 范围检查

如果规格说明书涵盖多个独立的子系统，则应在头脑风暴阶段将其拆分为子项目规格说明书。若未拆分，建议将其拆分为独立的计划——每个子系统一个计划。每个计划都应能够独立产出可运行且可测试的软件。

## 文件结构

在定义任务之前，应规划好将创建或修改哪些文件，以及每个文件负责什么。这是确定分解方案的关键环节。

- 设计具有清晰边界和明确接口的单元。每个文件应只承担一项明确的职责。
- 只有将代码置于完整上下文中，才能进行最佳推理；当文件职责专注时，修改也更可靠。应优先选择规模较小、职责明确的文件，而非功能过于繁杂的大型文件。
- 需要协同变更的文件应集中放置。按职责划分，而非按技术层级划分。
- 在现有代码库中，应遵循既定模式。 如果代码库使用的是大型文件，不要单方面进行重构——但如果正在修改的文件已经变得难以管理，将拆分纳入计划是合理的。

这种结构指导着任务分解。每个任务应产生自包含的变更，这些变更独立存在时也应有意义。

## 任务规模优化

任务是具有独立测试周期且值得由
新审阅者进行审核的最小单元。在划定任务边界时：将准备、
配置、框架搭建和文档编写步骤纳入到
需要这些步骤的任务中；仅在审阅者可能有充分理由
拒绝一个任务而批准其相邻任务的情况下才进行拆分。 每个任务应以一个
可独立测试的交付物作为结束。

## 适度细分的任务粒度

**每个步骤即为一项操作（2-5分钟）：**
- “编写失败的测试” - 步骤
- “运行测试以确保其失败” - 步骤
- “实现使测试通过的最小代码” - 步骤
- “运行测试并确保其通过” - 步骤
- “提交” - 步骤

## 计划文档标题

**每个计划必须以以下标题开头：**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

## Global Constraints

[The spec's project-wide requirements — version floors, dependency limits,
naming and copy rules, platform requirements — one line each, with exact
values copied verbatim from the spec. Every task's requirements implicitly
include this section.]

---
```

## 任务结构

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**
- Consumes: [what this task uses from earlier tasks — exact signatures]
- Produces: [what later tasks rely on — exact function names, parameter
  and return types. A task's implementer sees only their own task; this
  block is how they learn the names and types neighboring tasks use.]

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: 添加特定功能"
```
````

## 禁止使用占位符

每个步骤都必须包含工程师实际需要的内容。以下属于**计划失败**——切勿写入：
- “待定”（TBD）、“待办”（TODO）、“稍后实现”、“补充细节”
- “添加适当的错误处理” / “添加验证” / “处理边界情况”
- “为上述内容编写测试”（未提供实际测试代码）
- “类似于任务 N”（重复代码——工程师可能按非顺序阅读任务）
- 仅描述“做什么”而未说明“如何做”的步骤（代码步骤必须包含代码块）
- 引用任何任务中未定义的类型、函数或方法

## 请记住
- 始终注明确切的文件路径
- 每个步骤都要包含完整的代码——如果某一步会修改代码，请展示代码
- 确切的命令及其预期输出
- 遵循 DRY、YAGNI、TDD 原则，并频繁提交

## 自我审查

完成计划撰写后，以全新的视角审视规格说明书，并对照其检查计划。这是一份由你自行执行的检查清单——而非分派给子代理的任务。

**1. 规格说明书覆盖率：** 浏览规格说明书中的每个部分/需求。你能指出哪个任务实现了该需求吗？列出任何遗漏之处。

**2. 占位符扫描：** 在计划中搜索红旗——即上文“无占位符”部分中提到的任何模式。予以修正。

**3. 类型一致性：** 你在后续任务中使用的类型、方法签名和属性名称是否与早期任务中定义的一致？例如，某个函数在任务 3 中名为 `clearLayers()`，但在任务 7 中却名为 `clearFullLayers()`，这便是一个错误。

若发现问题，请直接在代码中修复。无需重新审查——修复后即可继续。若发现某项规格要求未对应任何任务，请添加相应任务。

## 执行交接

保存计划后，提供执行选项：

**“计划已完成并保存至 `docs/superpowers/plans/<filename>.md`。 两种执行选项：**

**1. 子代理驱动（推荐）** - 我为每个任务调度一个新的子代理，在任务之间进行审查，快速迭代

**2. 内联执行** - 使用 executing-plans 在本次会话中执行任务，通过检查点进行批量执行

**选择哪种方式？”**

**若选择“子代理驱动”：**
- **必备子技能：** 使用超能力：subagent-driven-development
- 每个任务分配一个新的子代理 + 两阶段审查

**若选择“内联执行”：**
- **必备子技能：** 使用超能力：executing-plans
- 采用带检查点的批量执行，以便进行审查
