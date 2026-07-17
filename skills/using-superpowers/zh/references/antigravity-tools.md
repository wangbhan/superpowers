# Antigravity CLI (`agy`) 工具映射

技能通过操作来实现（例如“派遣子代理”、“创建待办事项”、“读取文件”）。在 Antigravity CLI (`agy`) 中，这些操作对应于以下工具。

| 操作技能请求 | Antigravity CLI 对应项 |
|----------------------|----------------------|
| 派遣子代理 (`Subagent (general-purpose):` 模板) | 带内置 `TypeName` 的 `invoke_subagent` — 用于全功能操作的 `self`，用于只读操作的 `research`（参见 [子代理支持](#subagent-support)) |
| 任务跟踪（“创建待办事项”、“标记为已完成”） | 一个 **任务工件** — 包含 `IsArtifact: true` 和 `ArtifactType: "task"` 的 `write_to_file`（参见 [任务跟踪](#task-tracking)）。 **不是** `manage_task`，后者用于管理后台进程。 |

## 任务跟踪

Antigravity **没有待办事项工具**（`manage_task` 管理后台
进程 — `list`/`kill`/`status`/`send_input` — 它*不是*待办清单）。 当某项
技能要求创建待办事项列表或跟踪任务时，请维护一个**任务文档**：一个
使用 `write_to_file`（`IsArtifact: true`、
`ArtifactMetadata.ArtifactType: "task"`）保存、通过 `replace_file_content` /
`multi_replace_file_content` 进行编辑。

在任何多步骤任务开始时，创建任务文档，列出计划的
每个步骤。随着每个步骤的完成，编辑该文档以标记为已完成（`- [x]`）。
如果计划发生变化，请更新检查清单。保持其内容最新——这是你了解
剩余工作的权威依据；一旦讨论内容变长，在开始
每个步骤之前请重新阅读它。
