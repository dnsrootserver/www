# ⚡ SkillSnap

**用 YAML 构建 AI Agent 技能 — 咔嚓，搞定！** | **Build AI Agent Skills with YAML — Snap, Done!**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.1.0-brightgreen.svg)]()
[![Skills](https://img.shields.io/badge/skills-73-blue.svg)]()

---

> 🚀 **3行YAML = 1个AI Agent技能**
> 
> 不需要Python。不需要JavaScript。只需要写YAML。

---

[🇺🇸 English](#-english) | [🇨🇳 中文](#-中文)

---

## 🇨🇳 中文

### 为什么选择 SkillSnap？

**写一个AI Agent技能，传统方式：**
```python
import requests, json, os, sys
# 200行样板代码...
# 处理错误...
# 配置参数...
# 格式化输出...
# 终于写完了，但别人看不懂
```

**用 SkillSnap：**
```yaml
name: 天气查询
triggers: ["天气"]
steps:
  - tool: shell
    params: {command: "curl -s 'wttr.in/?format=3'"}
  - tool: output
    params: {message: "{{ stdout }}"}
```

**3行核心代码。零学习成本。即刻运行。**

### 🎯 核心优势

| 优势 | 说明 |
|------|------|
| ⚡ **快** | 5分钟创建一个技能，不是5小时 |
| 🎯 **简单** | 写YAML，不写代码 |
| 🌍 **双语** | 完整中英文支持 |
| 🔧 **18工具** | Shell/HTTP/文件/正则/通知/下载... |
| 💎 **73技能** | 开箱即用，覆盖常见场景 |
| 🔌 **可扩展** | 随时添加新技能，一个YAML文件搞定 |

### 🚀 30秒开始

```bash
# 安装
pip install skillsnap

# 查看所有技能
skillsnap list

# 运行一个技能
skillsnap run weather

# 交互模式
skillsnap chat
```

### 📦 73个技能一览

#### 🆓 免费技能（28个）

| 类别 | 技能 |
|------|------|
| 🌐 网络 | web-search, url-reader, url-shortener, ip-lookup, dns-lookup, ping-test, port-check, whois-lookup, ssl-check |
| 💻 开发 | code-review, json-formatter, uuid-generator, base64-encode, hash-generator, regex |
| 🌤️ 生活 | weather, crypto-price, github-repo-info |
| 🛠️ 工具 | system-info, password-gen, cron-helper, text-stats, lorem-ipsum, color-picker, qr-generator, ascii-art, morse-code, pig-latin, word-counter |

#### 💎 付费技能（45个）

| 包 | 技能数 | 价格 | 包含 |
|----|--------|------|------|
| 🔧 DevOps | 15 | $29 | Docker, K8s, 服务器监控, 日志分析, 部署, SSL, 端口扫描, 备份, CI/CD, 安全审计, Nginx, MySQL, Redis, 磁盘, 进程 |
| 📊 Data | 15 | $29 | CSV, Excel, JSON, API, 爬虫, 可视化, SQL, 清洗, 合并, 转换, 正则, 验证, 模拟器, Schema, 采样 |
| 📱 Social | 15 | $19 | Twitter, Reddit, RSS, HN, GitHub, arXiv, PH, YouTube, LinkedIn, Medium, Dev.to, SO, 新闻, 博客, 分析 |
| 🎯 全家桶 | 45 | $59 | **全部付费包 + 终身免费更新** |

### 🛠️ 18个内置工具

| 工具 | 功能 | 工具 | 功能 |
|------|------|------|------|
| shell | 执行命令 | http | HTTP请求 |
| read_file | 读文件 | write_file | 写文件 |
| set_variable | 设变量 | prompt | 用户输入 |
| log | 日志 | transform | 数据转换 |
| condition | 条件判断 | output | 格式输出 |
| regex_extract | 正则提取 | json_parse | JSON解析 |
| loop | 循环 | schedule | 定时任务 |
| retry | 重试 | notify | 通知 |
| download | 下载 | compress | 压缩 |

### 💰 为什么开发者选我们？

| | SkillSnap | LangChain | 自己写代码 |
|--|-----------|-----------|-----------|
| 上手时间 | ⚡ 5分钟 | 🕐 5小时 | 🕐🕐 5天 |
| 需要写代码 | ❌ 不用 | ✅ 要 | ✅ 必须 |
| YAML驱动 | ✅ | ❌ | ❌ |
| 中文支持 | ✅ | ❌ | - |
| 内置技能 | ✅ 73个 | ❌ | ❌ |
| 价格 | 免费起 | 免费 | 时间成本 |

---

## 🇺🇸 English

### ⚡ SkillSnap — Build AI Agent Skills with YAML

**3 lines of YAML = 1 AI Agent skill.**

No Python. No JavaScript. Just YAML.

### Quick Start

```bash
pip install skillsnap
skillsnap list
skillsnap run weather
skillsnap chat
```

### 73 Skills, 18 Tools, Bilingual

- **28 Free Skills**: web search, weather, crypto, GitHub, code review, system info, hashing, JSON, UUID, Base64, URL shortener, IP lookup, DNS, ping, port check, whois, SSL, cron, password, text stats, lorem ipsum, color picker, QR code, ASCII art, Morse code, Pig Latin, word counter
- **15 DevOps Skills** ($29): Docker, K8s, server monitor, log analysis, deployment, SSL checker, port scanner, backup, CI/CD debug, infra audit, Nginx, MySQL, Redis, disk analyzer, process manager
- **15 Data Skills** ($29): CSV, Excel, JSON, API extractor, web scraper, data viz, SQL, data cleaning, merge, format converter, regex builder, data validator, API mocker, schema generator, data sampler
- **15 Social Skills** ($19): Twitter, Reddit, RSS, Hacker News, GitHub trending, arXiv, Product Hunt, YouTube, LinkedIn, Medium, Dev.to, Stack Overflow, news aggregator, blog monitor, social analytics

### Why SkillSnap?

| Feature | SkillSnap | LangChain | Custom Code |
|---------|-----------|-----------|-------------|
| Time to build | ⚡ 5 min | 🕐 5 hours | 🕐🕐 5 days |
| Code required | ❌ No | ✅ Yes | ✅ Must |
| YAML-based | ✅ | ❌ | ❌ |
| Built-in skills | ✅ 73 | ❌ | ❌ |
| Price | Free | Free | Time cost |

---

## 📄 License

MIT — Free for personal and commercial use.

## 🔗 Links

- **GitHub**: https://github.com/dnsrootserver/www
- **Docs**: `/docs`
- **Premium**: Coming soon on Gumroad

---

⚡ **SkillSnap — 用 YAML 构建 AI Agent 技能，快、简单、强大**
