# 🤖 AgentForge

**Declarative AI Agent Skill Framework** — Build agent skills with YAML, not code.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/dnsrootserver/www)](https://github.com/dnsrootserver/www)

---

## What is AgentForge?

AgentForge lets you build AI agent skills using **simple YAML files** instead of writing Python code.

**Before AgentForge** — building a skill required:
```python
import requests
import json
# ... 200 lines of boilerplate code ...
```

**With AgentForge** — just write YAML:
```yaml
name: web-search
triggers: ["search", "find"]
steps:
  - tool: shell
    params:
      command: 'curl -s "https://r.jina.ai/https://google.com/search?q={{ input }}"'
  - tool: output
    params:
      message: "{{ stdout }}"
      format: markdown
```

---

## 🚀 Quick Start

### Install

```bash
pip install agentforge
```

### Create your first skill

```bash
agentforge init my-skill
```

### Run a skill

```bash
agentforge run my-skill/skill.yaml
```

### Interactive mode

```bash
agentforge chat
```

---

## 📦 Built-in Skills

AgentForge comes with **7 ready-to-use skills**:

| Skill | Description | Trigger |
|-------|-------------|---------|
| `web-search` | Search the web with Jina | "search ..." |
| `url-reader` | Read any webpage | any URL |
| `system-info` | System diagnostics | "system info" |
| `code-review` | Analyze code quality | "review code.py" |
| `github-repo-info` | GitHub repo details | "github.com/user/repo" |
| `weather` | Weather for any city | "weather in Tokyo" |
| `crypto-price` | Crypto prices | "bitcoin price" |

---

## 🛠️ Available Tools

Skills can use these built-in tools:

| Tool | Description |
|------|-------------|
| `shell` | Execute shell commands |
| `http` | Make HTTP requests |
| `read_file` | Read files |
| `write_file` | Write files |
| `set_variable` | Set variables |
| `prompt` | Ask user for input |
| `log` | Log messages |
| `transform` | Transform data with Python |
| `condition` | Conditional execution |
| `output` | Display formatted output |

---

## 📝 Skill YAML Format

```yaml
name: my-skill
version: "1.0.0"
description: "What this skill does"
author: your-name

triggers:
  - "keyword"
  - type: regex
    pattern: "match (.+) pattern"

variables:
  my_var: "default_value"

config:
  timeout: 30

steps:
  - tool: shell
    params:
      command: "echo Hello {{ input }}"
    output: greeting
    
  - tool: log
    params:
      message: "{{ greeting.stdout }}"
      level: info
      
  - tool: output
    params:
      message: "Done! Result: {{ greeting.stdout }}"
      format: text
```

---

## 💰 Premium Skill Packs

### 🔥 DevOps Pack ($29)
- Docker management
- Kubernetes operations
- Server monitoring
- Log analysis
- Deployment automation

### 🔥 Data Pack ($29)
- CSV/Excel processing
- API data extraction
- Web scraping
- Data visualization

### 🔥 Social Media Pack ($19)
- Twitter/X monitoring
- Reddit search
- RSS feed aggregation

### 🔥 All Access ($79)
- All current and future premium packs
- Priority support
- Custom skill development

---

## 🏗️ Architecture

```
agentforge/
├── __init__.py          # Package init
├── cli.py               # CLI interface
├── core/
│   ├── engine.py        # Core execution engine
│   └── loader.py        # Skill discovery/loading
└── skills/              # Built-in skills
    ├── web-search.yaml
    ├── url-reader.yaml
    ├── system-info.yaml
    ├── code-review.yaml
    ├── github-repo-info.yaml
    ├── weather.yaml
    └── crypto-price.yaml
```

---

## 🔧 Development

```bash
# Clone
git clone https://github.com/dnsrootserver/www.git
cd www

# Install in dev mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Check system
agentforge doctor
```

---

## 🌟 Why AgentForge?

| Feature | AgentForge | LangChain | Custom Code |
|---------|-----------|-----------|-------------|
| Learning curve | ⭐ Easy | ⭐⭐⭐ Hard | ⭐⭐⭐⭐ Very Hard |
| Time to build | ⚡ Minutes | 🕐 Hours | 🕐🕐 Days |
| No code required | ✅ | ❌ | ❌ |
| YAML-based | ✅ | ❌ | ❌ |
| Built-in tools | ✅ 10+ | ✅ Many | DIY |
| Skill marketplace | ✅ | ❌ | ❌ |

---

## 📄 License

MIT License — Free for personal and commercial use.

---

## 🔗 Links

- **GitHub**: https://github.com/dnsrootserver/www
- **Documentation**: See `/docs` directory
- **Premium Skills**: Coming soon on Gumroad

---

*Built with ❤️ for the AI agent community*
