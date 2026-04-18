# ⚡ AgentBolt — Product Hunt Launch

## Title
AgentBolt — 3 Lines of YAML = 1 AI Agent Skill ⚡

## Tagline
73 skills. 18 tools. YAML-only. No code. Just fast.

## Maker Comment

Hey Product Hunt! 👋

I was frustrated. Every time I wanted to build an AI agent skill, I had to:
1. Write 200 lines of Python boilerplate
2. Handle errors, configs, output formatting
3. Spend hours on plumbing instead of the actual skill

So I built AgentBolt — a framework where you define AI agent skills in simple YAML files.

**3 lines of YAML = a working skill.**

```yaml
name: weather
triggers: ["weather"]
steps:
  - tool: shell
    params: {command: "curl -s 'wttr.in/?format=3'"}
  - tool: output
    params: {message: "{{ stdout }}"}
```

### What you get:

- **73 ready-to-use skills** — web search, weather, crypto, code review, system diagnostics, and more
- **18 built-in tools** — shell, HTTP, file ops, regex, JSON, notifications, downloads, compression
- **Full bilingual support** — English and Chinese
- **Premium packs** — DevOps ($29), Data ($29), Social ($19), All Access ($59)
- **5-minute setup** — `pip install agentbolt` and you're ready

### Who it's for:

- Developers who want to automate tasks without boilerplate
- DevOps engineers who need quick monitoring tools
- Content creators who want social media aggregation
- Anyone who thinks "there should be a YAML for that"

### What's different:

| | AgentBolt | LangChain | Custom Code |
|--|-----------|-----------|-------------|
| Setup time | 5 min | 5 hours | 5 days |
| Code needed | No | Yes | Must |
| YAML-based | ✅ | ❌ | ❌ |
| Built-in skills | 73 | 0 | 0 |

### Pricing:

- **Free**: 28 skills + 18 tools
- **DevOps Pack**: $29 (15 skills)
- **Data Pack**: $29 (15 skills)
- **Social Pack**: $19 (15 skills)
- **All Access**: $59 (all 45 premium + lifetime updates)

### What's next:

- More skills every month
- MCP (Model Context Protocol) integration
- Cloud-hosted version
- Skill marketplace

Would love your feedback! What skills should I add next? 🚀

## Description

AgentBolt is a declarative framework for building AI agent skills. Define skills in YAML, not code. Includes 73 ready-to-use skills across web search, DevOps, data processing, and social media.

## Topics
ai, developer-tools, productivity, automation, open-source, yaml, no-code, agent

## Links
- GitHub: https://github.com/dnsrootserver/www
- Twitter: @agentbolt (coming)
