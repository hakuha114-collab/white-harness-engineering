# 代码规范红线

> L1 级强制规则，违反即回退修复

## 1. 命名规范

### 1.1 通用原则

- [ ] 命名必须使用英文，禁止拼音或中英混用
- [ ] 命名必须表达明确语义，禁止无意义缩写（如 `a`, `tmp`, `data2`）
- [ ] 命名长度控制在 2-30 个字符
- [ ] 避免使用保留字和内置函数名

### 1.2 变量命名

- [ ] 变量使用 `camelCase`（JavaScript/TypeScript/Java）
- [ ] 变量使用 `snake_case`（Python）
- [ ] 常量使用 `UPPER_SNAKE_CASE`
- [ ] 布尔变量以 `is`/`has`/`should`/`can` 开头

### 1.3 函数命名

- [ ] 函数使用 `camelCase`（JS/TS/Java）或 `snake_case`（Python）
- [ ] 函数名应为动词或动词短语：`getUserInfo`, `calculateTotal`
- [ ] 私有方法以下划线开头：`_internalProcess`

### 1.4 类/接口命名

- [ ] 类使用 `PascalCase`
- [ ] 接口使用 `PascalCase`，不加 `I` 前缀（TypeScript）
- [ ] 抽象类以 `Abstract` 开头或以 `Base` 结尾

### 1.5 文件/目录命名

- [ ] 文件名使用 `kebab-case`：`user-service.ts`
- [ ] 目录名使用 `kebab-case`：`api-gateway/`
- [ ] 测试文件以 `.test.` 或 `.spec.` 标识：`user-service.test.ts`

## 2. 代码结构

### 2.1 函数规范

- [ ] 单个函数长度不超过 50 行
- [ ] 函数参数不超过 5 个，超过使用对象传参
- [ ] 函数必须有返回类型声明（TypeScript/Java）
- [ ] 函数单一职责，一个函数只做一件事

### 2.2 类规范

- [ ] 单个类长度不超过 300 行
- [ ] 类成员访问修饰符必须明确（public/private/protected）
- [ ] 类的职责单一，符合 SOLID 原则

### 2.3 文件规范

- [ ] 单个文件长度不超过 500 行
- [ ] 每个文件只导出一个主模块/类
- [ ] 文件顶部必须有模块说明注释

### 2.4 目录规范

- [ ] 目录层级不超过 5 层
- [ ] 每个目录必须有 `README.md` 或 `index` 文件
- [ ] 按功能模块组织，不按技术类型组织

## 3. 注释规范

### 3.1 必须注释

- [ ] 公共 API 必须有 JSDoc/DocString
- [ ] 复杂逻辑必须有行内注释
- [ ] 配置项必须有说明
- [ ] TODO 必须附带责任人和预期时间

### 3.2 禁止注释

- [ ] 禁止注释掉的代码（用 Git 管理历史）
- [ ] 禁止无意义的注释（如 `// add 1`）
- [ ] 禁止过度注释，代码应自解释

## 4. 依赖管理

- [ ] 禁止引入不必要的依赖
- [ ] 依赖版本必须锁定（package-lock / requirements.txt）
- [ ] 新增依赖需在 PR 中说明理由
- [ ] 禁止使用已知有安全漏洞的依赖版本

## 5. 版本控制

- [ ] 分支命名：`feature/xxx`, `bugfix/xxx`, `hotfix/xxx`
- [ ] Commit 消息遵循 Conventional Commits
- [ ] 禁止直接 push 到 main/master 分支
- [ ] 每次提交必须通过 Lint 检查

---

**校验脚本**: `scripts/check-code-style/`
**违反处理**: L1 级别，代码审查 Agent 直接打回，必须修复后方可推进
