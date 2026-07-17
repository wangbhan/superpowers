---
name: verification-before-completion
description: 在声称工作已完成、已修复或通过之前使用，即在提交代码或创建拉取请求之前——在做出任何成功声明之前，必须先运行验证命令并确认输出结果；在做出断言之前，务必提供证据
---

# 完成前的验证

## 概述

未经验证就声称工作已完成，这是不诚实，而非高效。

**核心原则：** 先有证据，后有声明，永远如此。

**违反这条规则的字面规定，就是违反了这条规则的精神。**

## 铁律

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

若未执行本消息中的验证命令，则不得声称其通过。

## 门控函数

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## 常见失败情况

| 声明 | 要求 | 不足 |
|-------|----------|----------------|
| 测试通过 | 测试命令输出：0 个失败 | 上一轮运行结果为“应通过” |
| 代码检查器无误 | 代码检查器输出：0 个错误 | 部分检查，推断 |
| 构建成功 | 构建命令：exit 0 | 代码检查通过，日志正常 |
| 错误修复 | 测试原始症状：通过 | 代码已修改，推定已修复 |
| 回归测试正常 | 红绿循环已验证 | 测试仅通过一次 |
| 代理完成 | 版本控制系统差异显示有改动 | 代理报告“成功” |
| 满足要求 | 逐行检查清单 | 测试通过 |

## 红旗警告 - 停止

- 使用“应该”、“可能”、“似乎”等词
- 在验证前表达满意（“太棒了！”、“完美！”、“搞定！”等）
- 未经验证就准备提交/推送/创建PR
- 轻信代理的成功报告
- 依赖部分验证
- 抱有“就这一次”的想法
- 疲惫不堪，只想尽快结束工作
- **任何在未运行验证的情况下暗示成功的措辞**

## 防止自我合理化

| 借口 | 现实 |
|--------|---------|
| “现在应该能行了” | 运行验证 |
| “我很确定” | 确定性 ≠ 证据 |
| “就这一次” | 绝无例外 |
| “静态分析工具通过了” | 静态分析工具 ≠ 编译器 |
| “代理报告成功” | 独立验证 |
| “我累了” | 疲惫 ≠ 借口 |
| “部分检查就够了” | 部分检查无法证明任何事情 |
| “用词不同，所以规则不适用” | 重精神，轻条文 |

## 关键模式

**测试：**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**回归测试（TDD 红-绿）：**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**构建：**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**需求：**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**代理授权：**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## 为何这很重要

来自24段失败的回忆：
- 你的合作伙伴说“我不相信你”——信任破裂
- 发布了未定义的函数——会导致崩溃
- 发布了缺失需求——功能不完整
- 因虚假完成而浪费时间 → 重新定位 → 返工
- 违反原则：“诚实是核心价值观。若说谎，将被替换。”

## 何时适用

**务必在以下情况之前：**
- 任何形式的成功/完成声明
- 任何满意度的表达
- 任何关于工作状态的积极表述
- 提交代码、创建PR、完成任务
- 转入下一项任务
- 将任务委派给代理

**规则适用于：**
- 确切措辞
- 改写和同义词
- 暗示成功的表述
- 任何暗示已完成或正确的沟通

## 核心要点

**验证绝无捷径。**

执行命令。阅读输出结果。然后才可确认结果。

这一点绝无商量余地。
