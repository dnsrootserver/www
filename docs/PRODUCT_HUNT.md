# Product Hunt Launch Post

## Title
AgentForge — Build AI Agent Skills with YAML, not Code 🤖

## Tagline
73 ready-to-use skills. 18 tools. YAML-based. No code required.

## Description

### What is AgentForge?

AgentForge is a declarative framework for building AI agent skills. Instead of writing Python code, you define skills in simple YAML files.

### Why AgentForge?

**Before AgentForge:**
```python
import requests
import json
# 200+ lines of boilerplate code...
```

**With AgentForge:**
```yaml
name: my-skill
triggers: ["do something"]
steps:
  - tool: shell
    params:
      command: "echo hello world"
  - tool: output
    params:
      message: "{{ stdout }}"
```

### Features

- 🎯 **73 ready-to-use skills** — web search, weather, crypto, code review, system info, and more
- 🔧 **18 built-in tools** — shell, HTTP, file ops, regex, JSON, notifications, and more
- 🌍 **Bilingual** — Full English and Chinese support
- 💎 **Premium skill packs** — DevOps, Data, and Social Media
- 🚀 **5-minute setup** — `pip install agentforge` and go

### Who is it for?

- Developers who want to automate tasks without writing code
- DevOps engineers who need quick monitoring and diagnostic tools
- Content creators who want to aggregate social media data
- Anyone who wants to build AI agent skills quickly

### Pricing

- **Free**: 28 skills + 18 tools
- **DevOps Pack**: $29 (15 skills)
- **Data Pack**: $29 (15 skills)
- **Social Pack**: $19 (15 skills)
- **All Access**: $59 (all 73 skills + future updates)

### Links

- GitHub: https://github.com/dnsrootserver/www
- Documentation: Included in repo
- Premium: Coming soon on Gumroad

## Maker Comment

Hey Product Hunt! 👋

I built AgentForge because I was tired of writing the same boilerplate code every time I wanted to create an AI agent skill.

The idea is simple: define skills in YAML, not code. The framework handles all the plumbing — HTTP requests, file operations, shell commands, regex matching, notifications — so you can focus on what your skill actually does.

Version 1.1.0 includes:
- 73 skills across 4 categories
- 18 built-in tools
- Full bilingual support (EN/ZH)
- Interactive CLI mode
- Jinja2 template support

Would love your feedback! What skills would you like to see added?

## Topics
ai, developer-tools, productivity, automation, open-source
