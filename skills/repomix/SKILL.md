# Skill: 代码库打包分析

## 元信息

```yaml
name: repomix
version: 1.0.0
description: 将代码库打包为AI友好的单文件，用于代码结构分析、模式查找、Token统计和AI上下文准备。支持本地目录和远程GitHub仓库。
trigger:
  - "分析仓库"
  - "分析代码库"
  - "打包代码"
  - "repomix"
  - "代码结构"
  - "token统计"
  - "explore repo"
  - "analyze codebase"
inputs:
  - name: target
    type: string
    required: true
    description: 本地目录路径或远程仓库 owner/repo
  - name: include_pattern
    type: string
    required: false
    description: 包含文件模式，如 **/*.ts,**/*.md
  - name: compress
    type: boolean
    required: false
    description: 是否启用Tree-sitter压缩（大仓库推荐，减少约70% token）
outputs:
  - name: packed_file
    type: file
    description: 打包后的AI友好文件（XML/Markdown/Plain/JSON格式）
  - name: metrics
    type: object
    description: 包含文件数、字符数、Token数的统计信息
rules:
  - rules/coding-standards.md
  - rules/security-rules.md
```

## 执行步骤

### Step 1: 确定目标类型

- 本地目录：验证路径存在
- 远程仓库：格式为 owner/repo（如 facebook/react）

### Step 2: 执行打包

```bash
# 远程仓库（输出到临时目录）
npx repomix@latest --remote <owner/repo> --output %TEMP%/<repo-name>-analysis.xml

# 本地目录
npx repomix@latest <directory> --output %TEMP%/<name>-analysis.xml

# 大仓库压缩
npx repomix@latest --remote <owner/repo> --compress --output %TEMP%/<repo-name>-analysis.xml

# 指定文件类型
npx repomix@latest --include "**/*.{ts,tsx,js,jsx}" --output %TEMP%/filtered-analysis.xml
```

### Step 3: 读取输出指标

命令输出包含：
- **处理文件数**
- **总字符数**
- **总Token数**（AI消耗估算）
- **输出文件路径**

### Step 4: 分析输出内容

1. 查看文件树部分（输出文件开头）了解项目结构
2. 使用 grep/search 搜索关键模式：
   - 导出函数和入口点
   - API端点和路由
   - 数据模型和Schema
   - 认证和权限相关代码
3. 对大文件使用 offset/limit 分段读取

### Step 5: 生成分析报告

> **按主 SKILL.md「报告输出规范」输出的 HTML 文件**（`.html`）。保留以下分区：基本指标（文件数/总 Token/输出文件）、项目结构（文件树概览）、关键发现（架构模式/核心模块/潜在问题，用 `.tag` 或色标区分风险）、下一步建议。落盘建议：`reports/codebase-analysis-<日期>.html`，并在对话中预览交付。

## 关键选项

| 选项 | 说明 |
|------|------|
| `--style xml` | 默认格式，结构清晰，推荐 |
| `--style markdown` | 人类可读格式 |
| `--compress` | Tree-sitter压缩，减少约70% token |
| `--include` | 仅包含匹配模式的文件 |
| `--ignore` | 额外忽略模式 |
| `--remote-branch` | 指定分支/标签/提交 |

## 最佳实践

1. 超过10万行的仓库务必使用 `--compress`
2. 先用模式搜索定位，再分段读取详情
3. 输出文件放到临时目录，避免污染工作区
4. 使用 `--include` 聚焦特定模块
5. XML格式默认推荐，文件边界清晰

## 安全

Repomix 自动排除敏感文件（API Key、凭证、.env），信任其安全默认值。
