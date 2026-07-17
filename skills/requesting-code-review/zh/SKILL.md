---
name: requesting-code-review
description: 在完成任务、实现主要功能或合并之前使用，以验证工作是否符合要求
---

# 请求代码审查

派遣一名代码审查员子代理，在问题连锁反应发生前及时发现并处理。审查员将获得经过精确设计的评估上下文——绝不会包含您的会话历史记录。这能让审查员专注于工作成果本身，而非您的思维过程，同时保留您自身的上下文以便继续工作。

**核心原则：** 尽早审查，频繁审查。

## 何时请求审查

**强制要求：**
- 在子代理驱动开发中的每项任务完成后
- 完成主要功能后
- 合并到主分支之前

**可选但有益：**
- 遇到瓶颈时（获取新视角）
- 重构前（基线检查）
- 修复复杂 bug 后

## 如何请求

**1. 获取 git SHA：**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. 调度代码评审子代理：**

派遣 `general-purpose` 子代理，并填写 [code-reviewer.md](code-reviewer.md) 中的模板

**占位符：**
- `{DESCRIPTION}` - 您所构建内容的简要概述
- `{PLAN_OR_REQUIREMENTS}` - 该功能应实现的功能
- `{BASE_SHA}` - 起始提交
- `{HEAD_SHA}` - 结束提交

**3. 处理反馈：**
- 立即修复关键问题
- 在继续之前修复重要问题
- 记录次要问题以备后用
- 若评审者有误，请提出异议（并说明理由）

## 示例

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch code reviewer subagent]
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types
  PLAN_OR_REQUIREMENTS: Task 2 from docs/superpowers/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## 与工作流的集成

**子代理驱动开发：**
- 每完成一项任务后进行审查
- 在问题恶化前及时发现
- 修复问题后再进行下一项任务

**执行计划：**
- 每完成一项任务或在自然的检查点进行审查
- 获取反馈、落实改进、继续推进

**临时开发：**
- 合并前进行审查
- 遇到瓶颈时进行审查

## 红旗警示

**切勿：**
- 以“很简单”为由跳过审查
- 忽视严重问题
- 在重要问题未解决的情况下继续推进
- 与合理的技术反馈争论

**如果评审者有误：**
- 基于技术理由提出异议
- 展示证明代码/测试可正常运行的证据
- 请求澄清

参见模板：[code-reviewer.md](code-reviewer.md)
