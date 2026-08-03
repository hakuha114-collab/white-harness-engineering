# 蓝湖原型对接（Lanhu MCP）

## 对接说明
通过社区版 [lanhu-mcp](https://github.com/dsphper/lanhu-mcp)（Python/fastmcp 实现）打通蓝湖（lanhuapp.com）设计协作平台，让 AI 在需求分析、UI 还原、切图导出等环节直接读取蓝湖里的 Axure 原型、UI 设计稿、需求文档与切图资源，避免在「设计稿 ↔ 代码」之间靠人肉搬运。

典型场景：
- 需求拆解：读取 Axure 原型 + AI 分析需求 → 产出 SPEC（`skills/create-spec`）。
- UI 还原：读取设计稿精确参数（尺寸/间距/颜色/字体）→ 生成 HTML+CSS 参考。
- 资源导出：批量下载语义化命名的切图/图标。

## 前置条件
- Python >= 3.10（建议用 venv 隔离，避免污染系统环境）
- Git
- 一个蓝湖账号，并能从浏览器开发者工具复制登录 Cookie（`LANHU_COOKIE`）

## 安装步骤

```bash
# 1. 拉取源码到统一托管目录
git clone https://github.com/dsphper/lanhu-mcp.git ~/.workbuddy/mcp-servers/lanhu-mcp
cd ~/.workbuddy/mcp-servers/lanhu-mcp

# 2. 建虚拟环境并装依赖
python -m venv venv
# Windows 激活：
venv\Scripts\activate
# macOS / Linux：
source venv/bin/activate

pip install -r requirements.txt
# 依赖：fastmcp httpx beautifulsoup4 playwright lxml python-dotenv htmlmin2
# playwright 还需下载浏览器内核：
playwright install
```

## 准备 .env（鉴权）
在 server 目录放 `.env`，**不要把 Cookie 写进 mcp.json**：

```dotenv
# ~/.workbuddy/mcp-servers/lanhu-mcp/.env
LANHU_COOKIE=你的蓝湖登录Cookie（从 lanhuapp.com 浏览器开发者工具复制请求头 Cookie）
LANHU_USER_NAME=你的蓝湖昵称（建议英文，用于协作 @提醒）
LANHU_USER_ROLE=Developer
```

> `LANHU_COOKIE` 获取方式见仓库 `GET-COOKIE-TUTORIAL.md`。Cookie 有时效，过期后需重新复制。

## mcp.json 配置（stdio，已验证可用）

WorkBuddy 读取的是 **`~/.workbuddy/mcp.json`**（无前导点！写错成 `.mcp.json` 不会被加载）。在该文件 `mcpServers` 中追加：

```json
{
  "mcpServers": {
    "lanhu": {
      "type": "stdio",
      "command": "<HOME>/.workbuddy/mcp-servers/lanhu-mcp/venv/Scripts/python.exe",
      "args": [
        "<HOME>/.workbuddy/mcp-servers/lanhu-mcp/lanhu_mcp_server.py"
      ],
      "cwd": "<HOME>/.workbuddy/mcp-servers/lanhu-mcp",
      "timeout": 120000,
      "env": {
        "MCP_TRANSPORT": "stdio",
        "LANHU_USER_NAME": "你的蓝湖昵称",
        "LANHU_USER_ROLE": "Developer"
      },
      "description": "蓝湖 Lanhu MCP Server (第三方社区版, 读取蓝湖设计稿/需求文档/切图)"
    }
  }
}
```

- `<HOME>`：Windows 为 `C:/Users/你的用户名`，macOS/Linux 为 `~`。
- `command` 必须用 **venv 里的 python**，不要直接用系统 `python`，否则可能缺依赖或版本不符。
- `cwd` **必须指向 server 目录**，server 启动时会读取同目录 `.env` 里的 `LANHU_COOKIE`；这也避免把敏感串写进可被 git 跟踪的 `mcp.json`。
- `env` 里只放非敏感的传输方式与身份标识；鉴权 Cookie 一律走 `.env`。

配置后在 WorkBuddy「连接器 → MCP 服务管理」界面点击「信任」启用该 server。

## ⚠️ 接入避坑（血泪经验）
1. **文件名是 `mcp.json` 不是 `.mcp.json`**：两者完全不同，写错位置配置不会被加载。
2. **cwd 指到 server 目录**：让它读同目录 `.env` 的密钥/cookie，别把敏感串硬编码进 `mcp.json`（会被 git 跟踪泄露）。
3. **Python 用 venv**：系统 python 可能版本不对或缺少 fastmcp 等依赖。
4. **playwright 内核**：`pip install` 后还要 `playwright install` 下载浏览器，否则启动报缺浏览器。
5. **Cookie 过期**：蓝湖 Cookie 有时效，AI 调不通时优先检查 `.env` 里的 Cookie 是否失效。

## 能力清单（Tools）

| 工具 | 功能 |
|------|------|
| `lanhu_resolve_invite_link` | 解析蓝湖邀请链接 |
| `lanhu_get_pages` | 获取 Axure 原型页面列表（需求分析前必调） |
| `lanhu_get_ai_analyze_page_result` | AI 分析原型页面，提取需求细节（开发/测试/探索三模式） |
| `lanhu_get_designs` | 获取 UI 设计图列表 |
| `lanhu_get_ai_analyze_design_result` | 分析设计稿，返回预览、精确参数、HTML+CSS 参考 |
| `lanhu_get_design_slices` | 获取并下载切图/图标（语义化命名） |
| `lanhu_say` / `lanhu_say_list` / `lanhu_say_detail` / `lanhu_say_edit` / `lanhu_say_delete` | 团队留言板：发布/查看/编辑/删除协作消息，支持 @提醒 |
| `lanhu_get_members` | 查看项目协作者及访问记录 |

## 在 Harness 流程中的用法
- **需求分析阶段**：先 `lanhu_get_pages` + `lanhu_get_ai_analyze_page_result` 读懂原型，再走 `skills/create-spec` 产出 SPEC，避免需求靠人肉转述。
- **UI 开发阶段**：`lanhu_get_ai_analyze_design_result` 拿到精确尺寸/间距/颜色/字体与 HTML+CSS 参考，对照 `rules/coding-standards.md` 落地。
- **资源交付阶段**：`lanhu_get_design_slices` 批量导出切图，按 `assets/` 资产化沉淀。

## 验证方法
1. 启动 server 检查能正常进入 MCP 握手（stdio 模式会等待 JSON-RPC）：
   ```bash
   cd <HOME>/.workbuddy/mcp-servers/lanhu-mcp
   venv/Scripts/python.exe lanhu_mcp_server.py
   ```
   无 `ImportError` / 无 "cookie not found" 即基础可用。
2. 在 WorkBuddy 连接器里启用 lanhu 后，用 `lanhu_get_pages` 实际拉一次蓝湖项目页面，能返回数据即端到端打通。
