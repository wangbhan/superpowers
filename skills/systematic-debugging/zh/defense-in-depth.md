# 多层防御验证

## 概述

当修复由无效数据引发的 bug 时，仅在某处添加验证似乎就足够了。但这一单一检查可能会因不同的代码路径、重构或模拟而被绕过。

**核心原则：**在数据流经的每一层都进行验证。从结构上杜绝该缺陷的发生。

## 为何需要多层验证

单层验证：“我们修复了该缺陷”
多层验证：“我们从根本上杜绝了该缺陷”

不同层级可捕获不同的情况：
- 入口验证可捕获大多数缺陷
- 业务逻辑可捕获边界情况
- 环境守护机制可防范特定上下文中的风险
- 当其他层失效时，调试日志可提供帮助

## 四层架构

### 第 1 层：入口点验证
**目的：** 在 API 边界处拒绝明显无效的输入

```typescript
function createProject(name: string, workingDirectory: string) {
  if (!workingDirectory || workingDirectory.trim() === '') {
    throw new Error('workingDirectory cannot be empty');
  }
  if (!existsSync(workingDirectory)) {
    throw new Error(`workingDirectory does not exist: ${workingDirectory}`);
  }
  if (!statSync(workingDirectory).isDirectory()) {
    throw new Error(`workingDirectory is not a directory: ${workingDirectory}`);
  }
  // ... proceed
}
```

### 第 2 层：业务逻辑验证
**目的：** 确保数据对当前操作而言合理

```typescript
function initializeWorkspace(projectDir: string, sessionId: string) {
  if (!projectDir) {
    throw new Error('projectDir required for workspace initialization');
  }
  // ... proceed
}
```

### 第 3 层：环境防护
**目的：** 防止在特定上下文中执行危险操作

```typescript
async function gitInit(directory: string) {
  // In tests, refuse git init outside temp directories
  if (process.env.NODE_ENV === 'test') {
    const normalized = normalize(resolve(directory));
    const tmpDir = normalize(resolve(tmpdir()));

    if (!normalized.startsWith(tmpDir)) {
      throw new Error(
        `Refusing git init outside temp dir during tests: ${directory}`
      );
    }
  }
  // ... proceed
}
```

### 第 4 层：调试仪器
**目的：** 捕获上下文信息以供取证分析

```typescript
async function gitInit(directory: string) {
  const stack = new Error().stack;
  logger.debug('About to git init', {
    directory,
    cwd: process.cwd(),
    stack,
  });
  // ... proceed
}
```

## 应用该模式

当发现 bug 时：

1. **追踪数据流** - 错误值源自何处？在何处被使用？
2. **绘制所有检查点** - 列出数据经过的每个点
3. **在每一层添加验证** - 入口层、业务层、环境层、调试层
4. **测试每一层** - 尝试绕过第 1 层，验证第 2 层能否捕获该异常

## 会议中的示例

错误：空字符串 `projectDir` 导致源代码中的 `git init` 被触发

**数据流：**
1. 测试环境 → 空字符串
2. `Project.create(name, '')`
3. `WorkspaceManager.createWorkspace('')`
4. `git init` 在 `process.cwd()` 中执行

**新增四层：**
- 第 1 层：`Project.create()` 验证非空/存在/可写
- 第 2 层：`WorkspaceManager` 验证 projectDir 不为空
- 第 3 层：`WorktreeManager` 拒绝在测试中于 tmpdir 之外执行 git init
- 第 4 层：在执行 git init 之前记录堆栈跟踪

**结果：** 全部 1847 个测试均通过，无法复现该缺陷

## 关键洞见

这四个层级均不可或缺。在测试过程中，每个层级都捕获了其他层级遗漏的缺陷：
- 不同的代码路径绕过了入口验证
- 模拟对象绕过了业务逻辑检查
- 不同平台上的边界情况需要环境保护机制
- 调试日志识别出了结构性误用

**不要仅停留在一个验证点。** 应在每个层级都添加检查。
