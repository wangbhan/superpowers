# 测试反模式

**何时参考本文：** 编写或修改测试、添加模拟对象，或者想在生产代码中添加仅用于测试的方法时。

## 概述

测试必须验证真实的行为，而非模拟行为。模拟对象只是用于隔离的手段，而非被测试的对象本身。

**核心原则：**测试代码的行为，而非模拟对象的行为。

**严格遵循 TDD 可避免这些反模式。**

## 铁律

```
1. NEVER test mock behavior
2. NEVER add test-only methods to production classes
3. NEVER mock without understanding dependencies
```

## 反模式 1：测试模拟对象的行为

**违规示例：**
```typescript
// ❌ BAD: Testing that the mock exists
test('renders sidebar', () => {
  render(<Page />);
  expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
});
```

**为何这是错误的：**
- 你验证的是模拟对象是否正常工作，而非组件是否正常工作
- 存在模拟对象时测试通过，不存在时测试失败
- 无法反映真实行为

**你的搭档的纠正：** “我们是在测试模拟对象的行为吗？”

**修正方案：**
```typescript
// ✅ GOOD: Test real component or don't mock it
test('renders sidebar', () => {
  render(<Page />);  // Don't mock sidebar
  expect(screen.getByRole('navigation')).toBeInTheDocument();
});

// OR if sidebar must be mocked for isolation:
// Don't assert on the mock - test Page's behavior with sidebar present
```

### 门控函数

```
BEFORE asserting on any mock element:
  Ask: "Am I testing real component behavior or just mock existence?"

  IF testing mock existence:
    STOP - Delete the assertion or unmock the component

  Test real behavior instead
```

## 反模式 2：生产环境中存在仅用于测试的方法

**违规情况：**
```typescript
// ❌ BAD: destroy() only used in tests
class Session {
  async destroy() {  // Looks like production API!
    await this._workspaceManager?.destroyWorkspace(this.id);
    // ... cleanup
  }
}

// In tests
afterEach(() => session.destroy());
```

**为何错误：**
- 生产环境类被仅用于测试的代码污染
- 若在生产环境中意外调用则十分危险
- 违反 YAGNI 原则和关注点分离原则
- 将对象生命周期与实体生命周期混为一谈

**修正方案：**
```typescript
// ✅ GOOD: Test utilities handle test cleanup
// Session has no destroy() - it's stateless in production

// In test-utils/
export async function cleanupSession(session: Session) {
  const workspace = session.getWorkspaceInfo();
  if (workspace) {
    await workspaceManager.destroyWorkspace(workspace.id);
  }
}

// In tests
afterEach(() => cleanupSession(session));
```

### 门控函数

```
BEFORE adding any method to production class:
  Ask: "Is this only used by tests?"

  IF yes:
    STOP - Don't add it
    Put it in test utilities instead

  Ask: "Does this class own this resource's lifecycle?"

  IF no:
    STOP - Wrong class for this method
```

## 反模式 3：不理解就进行模拟

**违规情况：**
```typescript
// ❌ BAD: Mock breaks test logic
test('detects duplicate server', () => {
  // Mock prevents config write that test depends on!
  vi.mock('ToolCatalog', () => ({
    discoverAndCacheTools: vi.fn().mockResolvedValue(undefined)
  }));

  await addServer(config);
  await addServer(config);  // Should throw - but won't!
});
```

**为何错误：**
- 被模拟的方法存在测试所依赖的副作用（写入配置）
- 为“保险起见”而过度模拟，反而破坏了实际行为
- 测试因错误原因通过，或莫名其妙地失败

**修复方案：**
```typescript
// ✅ GOOD: Mock at correct level
test('detects duplicate server', () => {
  // Mock the slow part, preserve behavior test needs
  vi.mock('MCPServerManager'); // Just mock slow server startup

  await addServer(config);  // Config written
  await addServer(config);  // Duplicate detected ✓
});
```

### 门控函数

```
BEFORE mocking any method:
  STOP - Don't mock yet

  1. Ask: "What side effects does the real method have?"
  2. Ask: "Does this test depend on any of those side effects?"
  3. Ask: "Do I fully understand what this test needs?"

  IF depends on side effects:
    Mock at lower level (the actual slow/external operation)
    OR use test doubles that preserve necessary behavior
    NOT the high-level method the test depends on

  IF unsure what test depends on:
    Run test with real implementation FIRST
    Observe what actually needs to happen
    THEN add minimal mocking at the right level

  Red flags:
    - "I'll mock this to be safe"
    - "This might be slow, better mock it"
    - Mocking without understanding the dependency chain
```

## 反模式 4：不完整的模拟

**违规示例：**
```typescript
// ❌ BAD: Partial mock - only fields you think you need
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' }
  // Missing: metadata that downstream code uses
};

// Later: breaks when code accesses response.metadata.requestId
```

**为何错误：**
- **部分模拟会隐藏结构性假设** - 你只模拟了已知的字段
- **下游代码可能依赖于你未包含的字段** - 导致无声失败
- **测试通过但集成测试失败** - 模拟不完整，真实 API 完整
- **虚假信心** - 测试无法验证真实行为

**铁律：** 模拟现实中存在的完整数据结构，而不仅仅是当前测试所使用的字段。

**解决方法：**
```typescript
// ✅ GOOD: Mirror real API completeness
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' },
  metadata: { requestId: 'req-789', timestamp: 1234567890 }
  // All fields real API returns
};
```

### 门控函数

```
BEFORE creating mock responses:
  Check: "What fields does the real API response contain?"

  Actions:
    1. Examine actual API response from docs/examples
    2. Include ALL fields system might consume downstream
    3. Verify mock matches real response schema completely

  Critical:
    If you're creating a mock, you must understand the ENTIRE structure
    Partial mocks fail silently when code depends on omitted fields

  If uncertain: Include all documented fields
```

## 反模式 5：将集成测试视为事后补救

**违规情况：**
```
✅ Implementation complete
❌ No tests written
"Ready for testing"
```

**为何错误：**
- 测试是实现过程的一部分，而非可选的后续步骤
- TDD本应能发现此问题
- 没有测试就不能声称完整

**解决方案：**
```
TDD cycle:
1. Write failing test
2. Implement to pass
3. Refactor
4. THEN claim complete
```

## 当模拟对象变得过于复杂时

**预警信号：**
- 模拟对象的初始化代码比测试逻辑还长
- 为让测试通过而对所有内容都进行模拟
- 模拟对象缺少真实组件拥有的方法
- 模拟对象发生变化时测试会失败

**你的合作伙伴会问：** “这里真的需要使用模拟对象吗？”

**考虑：** 使用真实组件的集成测试通常比复杂的模拟更简单

## TDD 可防止这些反模式

**TDD 为何有帮助：**
1. **先写测试** → 迫使你思考自己究竟在测试什么
2. **观察测试失败** → 确认测试针对的是真实行为，而非模拟对象
3. **最小化实现** → 避免出现仅用于测试的方法
4. **真实依赖关系** → 在进行模拟前，你能清楚测试实际需要什么

**如果你测试的是模拟行为，那就违反了 TDD**——你添加模拟对象之前，没有先观察测试在真实代码上失败的情况。

## 快速参考

| 反模式 | 解决方案 |
|--------------|-----|
| 对模拟元素进行断言 | 测试真实组件或取消模拟 |
| 生产环境中存在仅用于测试的方法 | 移至测试工具类 |
| 未理解就进行模拟 | 先理解依赖关系，最小化模拟 |
| 不完整的模拟 | 完全映射真实 API |
| 测试作为事后补救 | TDD——先写测试 |
| 过度复杂的模拟 | 考虑使用集成测试 |

## 危险信号

- 断言检查 `*-mock` 测试 ID
- 仅在测试文件中调用的方法
- 模拟设置占测试代码的 50% 以上
- 移除模拟后测试失败
- 无法解释为何需要模拟
- “为了保险起见”而进行模拟

## 核心要点

**模拟是用于隔离的工具，而非测试对象。**

如果 TDD 揭示出你正在测试模拟行为，那就说明你走错了方向。

解决方法：测试真实行为，或者质疑为何要进行模拟。
