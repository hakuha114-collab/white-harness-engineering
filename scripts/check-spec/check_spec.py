#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_spec.py — SPEC 完整性校验（Harness Engineering 门禁脚本）

用法:
    python check_spec.py <spec_doc.md> [--json]

判定:
    PASS  所有 MUST 与 SHOULD 项通过        -> exit 0
    WARN  所有 MUST 通过，有 SHOULD 未通过   -> exit 2
    FAIL  有 MUST 项未通过                  -> exit 1

校验项与级别定义见同目录 README.md（唯一事实源）。
仅依赖 Python 标准库，Windows / macOS / Linux 通用。
"""

import json
import re
import sys
import io

# Windows 控制台默认 GBK，强制 UTF-8 输出避免中文乱码
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ---- 校验规则配置（与 README.md 校验项表保持一致） ----

# MUST: 必需章节（按标题关键字模糊匹配，命中其一即可）
REQUIRED_SECTIONS = {
    "需求概述/背景": ["需求概述", "背景"],
    "核心目标": ["核心目标", "目标"],
    "成功指标": ["成功指标", "验收指标"],
    "功能规格/功能列表": ["功能规格", "功能列表", "功能需求"],
    "验收标准": ["验收标准"],
    "风险与假设": ["风险与假设", "风险", "假设"],
}

# 歧义表述（出现即 WARN，附命中位置）
AMBIGUOUS_PATTERNS = ["可能", "大概", "也许", "尽量", "适当", "等相关", "等等"]

# 可量化验收标准的特征词（验收标准章节需至少命中若干）
QUANTIFIABLE_HINTS = ["%", "ms", "秒", "分钟", "次", "条", "个", "≥", "≤", ">", "<",
                      "不低于", "不超过", "至少", "至多", "以内", "以上", "以下"]


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        return f.read()


def extract_headings(text: str):
    return [line.strip() for line in text.splitlines() if line.strip().startswith("#")]


def has_section(headings, keywords):
    return any(kw in h for h in headings for kw in keywords)


def section_body(text: str, keywords):
    """提取命中关键字的章节正文（到下一个同级或更高级标题为止）。"""
    lines = text.splitlines()
    capture, level, buf = False, 0, []
    for line in lines:
        m = re.match(r"^(#{1,6})\s+(.*)$", line.strip())
        if m:
            if capture and len(m.group(1)) <= level:
                break
            if any(kw in m.group(2) for kw in keywords):
                capture, level = True, len(m.group(1))
                continue
        if capture:
            buf.append(line)
    return "\n".join(buf).strip()


def check_spec(path: str):
    text = read_text(path)
    headings = extract_headings(text)
    checks = []  # (status, item, message)

    # 1-2. 必需章节（MUST）
    for name, keywords in REQUIRED_SECTIONS.items():
        if has_section(headings, keywords):
            checks.append(("PASS", f"必需章节: {name}", "已存在"))
        else:
            checks.append(("FAIL", f"必需章节: {name}", f"缺少必需章节（关键字: {'/'.join(keywords)}）"))

    # 3. 验收标准可量化（MUST）：验收标准章节需含量化特征
    body = section_body(text, ["验收标准"])
    if body:
        hits = [h for h in QUANTIFIABLE_HINTS if h in body]
        if len(hits) >= 1:
            checks.append(("PASS", "验收标准可量化", f"命中量化特征: {', '.join(hits[:5])}"))
        else:
            checks.append(("FAIL", "验收标准可量化", "验收标准章节未发现可量化指标（如 %/ms/次/≥/至少 等）"))

    # 4. 优先级标注（SHOULD）：功能清单中应出现 P0/P1/P2 或 高/中/低
    func_body = section_body(text, ["功能规格", "功能列表", "功能需求"])
    if func_body:
        if re.search(r"\bP[0-3]\b|优先级|高|中|低", func_body):
            checks.append(("PASS", "功能优先级标注", "已标注"))
        else:
            checks.append(("WARN", "功能优先级标注", "功能列表缺少优先级标注（P0/P1/P2 或 高/中/低）"))

    # 5. 歧义表述（SHOULD→WARN）
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        for p in AMBIGUOUS_PATTERNS:
            if p in line:
                hits.append(f"L{i}: …{line.strip()[:40]}…（命中「{p}」）")
    if hits:
        checks.append(("WARN", "无歧义表述", "发现可能歧义的表述:\n    " + "\n    ".join(hits[:10])))
    else:
        checks.append(("PASS", "无歧义表述", "未发现歧义词"))

    # 6. 判定
    statuses = [c[0] for c in checks]
    if "FAIL" in statuses:
        verdict = "FAIL"
    elif "WARN" in statuses:
        verdict = "WARN"
    else:
        verdict = "PASS"
    return verdict, checks


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(64)
    path = sys.argv[1]
    as_json = "--json" in sys.argv

    verdict, checks = check_spec(path)

    if as_json:
        print(json.dumps({
            "gate": "check-spec",
            "target": path,
            "status": verdict,
            "checks": [{"name": n, "status": s, "message": m} for s, n, m in checks],
        }, ensure_ascii=False, indent=2))
    else:
        print(f"[check-spec] 目标: {path}")
        for s, n, m in checks:
            icon = {"PASS": "✓", "WARN": "⚠", "FAIL": "✗"}[s]
            print(f"  {icon} [{s:4}] {n}: {m}")
        print(f"[check-spec] 判定: {verdict}")

    sys.exit({"PASS": 0, "WARN": 2, "FAIL": 1}[verdict])


if __name__ == "__main__":
    main()
