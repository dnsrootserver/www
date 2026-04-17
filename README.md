# 🤖 AgentForge

**用 YAML 构建 AI Agent 技能，无需写代码。** | **Build AI Agent Skills with YAML, not Code.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.1.0-brightgreen.svg)]()
[![Skills](https://img.shields.io/badge/skills-73-blue.svg)]()

---

[🇺🇸 English](#english) | [🇨🇳 中文](#中文)

---

## 中文

### 什么是 AgentForge？

AgentForge 是一个**声明式 AI Agent 技能框架**。你只需要写一个 YAML 文件，就能创建一个完整的 AI Agent 技能——不需要 Python，不需要 JavaScript，不需要任何编程语言。

**传统方式** — 写一个 Agent 技能需要：
```python
import requests
import json
import os
# ... 200+ 行样板代码 ...
```

**AgentForge 方式** — 只需要写 YAML：
```yaml
name: 天气查询
triggers: ["天气"]
triggers_zh: ["天气", "查天气"]
steps:
  - tool: shell
    params:
      command: "curl -s 'wttr.in/?format=3'"
  - tool: output
    params:
      message: "{{ stdout }}"
```

### 🚀 快速开始

```bash
# 安装
pip install agentforge

# 创建新技能
agentforge init 我的技能

# 运行技能
agentforge run 我的技能/skill.yaml

# 交互模式
agentforge chat
```

### 📦 内置技能（28个免费 + 45个付费）

#### 免费技能（28个）

| 技能 | 说明 | 触发词 |
|------|------|--------|
| web-search | 网页搜索 | search, 搜索 |
| url-reader | 网页内容提取 | read url, 读取网页 |
| weather | 天气查询 | weather, 天气 |
| crypto-price | 加密货币行情 | bitcoin, 比特币 |
| github-repo-info | GitHub仓库分析 | github.com |
| code-review | 代码审查 | review code, 代码审查 |
| system-info | 系统诊断 | system info, 系统信息 |
| hash-generator | 哈希生成 | hash, 哈希 |
| json-formatter | JSON格式化 | json, 格式化json |
| uuid-generator | UUID生成 | uuid, 生成uuid |
| base64-encode | Base64编解码 | base64, 编码 |
| url-shortener | 短链接生成 | short url, 短链接 |
| ip-lookup | IP查询 | ip lookup, IP查询 |
| dns-lookup | DNS查询 | dns, DNS查询 |
| ping-test | Ping测试 | ping |
| port-check | 端口检查 | port check, 端口检查 |
| whois-lookup | Whois查询 | whois |
| ssl-check | SSL证书检查 | ssl, SSL检查 |
| cron-helper | Cron表达式 | cron |
| password-gen | 密码生成 | password, 密码 |
| text-stats | 文本统计 | text stats, 字数统计 |
| lorem-ipsum | Lorem文本 | lorem |
| color-picker | 颜色生成 | color, 颜色 |
| qr-generator | 二维码生成 | qr, 二维码 |
| ascii-art | ASCII艺术字 | ascii |
| morse-code | 摩斯电码 | morse |
| pig-latin | Pig Latin | pig latin |
| word-counter | 词频分析 | word count, 词频 |

#### 💎 付费技能包

| 包 | 技能数 | 价格 | 说明 |
|----|--------|------|------|
| 🔧 DevOps Pack | 15 | $29 | Docker, K8s, 服务器监控, 日志分析等 |
| 📊 Data Pack | 15 | $29 | CSV/Excel处理, API提取, 数据可视化等 |
| 📱 Social Pack | 15 | $19 | Twitter, Reddit, RSS, GitHub趋势等 |
| 🎯 All Access | 45 | $59 | 全部付费包 + 未来更新 |

### 🛠️ 18个内置工具

| 工具 | 说明 |
|------|------|
| shell | 执行Shell命令 |
| http | HTTP请求 |
| read_file | 读取文件 |
| write_file | 写入文件 |
| set_variable | 设置变量 |
| prompt | 用户输入 |
| log | 日志输出 |
| transform | Python表达式转换 |
| condition | 条件判断 |
| output | 格式化输出 |
| regex_extract | 正则提取 |
| json_parse | JSON解析 |
| loop | 循环 |
| schedule | 定时任务 |
| retry | 重试 |
| notify | 通知 |
| download | 下载文件 |
| compress | 压缩/解压 |

### 💰 为什么选择 AgentForge？

| 对比 | AgentForge | LangChain | 自己写代码 |
|------|-----------|-----------|-----------|
| 学习曲线 | ⭐ 简单 | ⭐⭐⭐ 困难 | ⭐⭐⭐⭐ 很难 |
| 构建时间 | ⚡ 几分钟 | 🕐 几小时 | 🕐🕐 几天 |
| 需要写代码 | ✅ 不需要 | ❌ 需要 | ❌ 必须 |
| YAML驱动 | ✅ | ❌ | ❌ |
| 内置工具 | ✅ 18个 | ✅ 多 | DIY |
| 中文支持 | ✅ | ❌ | - |
| 技能市场 | ✅ | ❌ | ❌ |

---

## English

### What is AgentForge?

AgentForge is a **declarative AI agent skill framework**. Write a YAML file to create a complete AI agent skill — no Python, no JavaScript, no code required.

### Quick Start

```bash
pip install agentforge
agentforge init my-skill
agentforge run my-skill/skill.yaml
agentforge chat
```

### 73 Skills Included

- **28 Free Skills**: web search, weather, crypto, GitHub, code review, system info, hashing, JSON, UUID, Base64, URL shortener, IP lookup, DNS, ping, port check, whois, SSL, cron, password, text stats, lorem ipsum, color picker, QR code, ASCII art, Morse code, Pig Latin, word counter
- **15 DevOps Skills** ($29): Docker, K8s, server monitor, log analysis, deployment, SSL checker, port scanner, backup, CI/CD debug, infra audit, Nginx, MySQL, Redis, disk analyzer, process manager
- **15 Data Skills** ($29): CSV, Excel, JSON, API extractor, web scraper, data viz, SQL, data cleaning, merge, format converter, regex builder, data validator, API mocker, schema generator, data sampler
- **15 Social Skills** ($19): Twitter, Reddit, RSS, Hacker News, GitHub trending, arXiv, Product Hunt, YouTube, LinkedIn, Medium, Dev.to, Stack Overflow, news aggregator, blog monitor, social analytics

### 18 Built-in Tools

shell, http, read_file, write_file, set_variable, prompt, log, transform, condition, output, regex_extract, json_parse, loop, schedule, retry, notify, download, compress

---

## 📄 License

MIT License — Free for personal and commercial use.

## 🔗 Links

- **GitHub**: https://github.com/dnsrootserver/www
- **Documentation**: See `/docs`
- **Premium Skills**: https://gumroad.com/agentforge (coming soon)

---

*Built with ❤️ for the AI agent community*
