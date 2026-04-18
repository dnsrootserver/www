# AgentBolt Quick Start Guide

## Installation

```bash
pip install agentbolt
```

## Your First Skill (5 minutes)

### 1. Create a skill

```bash
agentbolt init my-first-skill
```

This creates `my-first-skill/skill.yaml`:

```yaml
name: my-first-skill
version: "1.0.0"
description: "A skill that my first skill"
author: your-name
triggers:
  - my-first-skill
  - run my-first-skill
variables:
  example_var: default_value
steps:
  - tool: log
    params:
      message: Running my-first-skill skill...
      level: info
  - tool: output
    params:
      message: "✅ my-first-skill completed!"
      format: text
```

### 2. Edit the skill

Add a real step — fetch weather:

```yaml
name: my-weather
version: "1.0.0"
description: "Get weather for any city"
author: you
triggers:
  - "weather"
  - type: regex
    pattern: "weather (in )?(.+)"
steps:
  - tool: shell
    params:
      command: "curl -s 'wttr.in/?format=3'"
      timeout: 10
    output: weather
  - tool: output
    params:
      message: "{{ weather.stdout }}"
      format: text
```

### 3. Run it

```bash
agentbolt run my-weather/skill.yaml
```

### 4. Interactive mode

```bash
agentbolt chat
```

## Available Tools

| Tool | Description | Key Params |
|------|-------------|------------|
| `shell` | Run shell commands | `command`, `timeout` |
| `http` | HTTP requests | `url`, `method`, `headers` |
| `read_file` | Read files | `path` |
| `write_file` | Write files | `path`, `content` |
| `log` | Print messages | `message`, `level` |
| `output` | Formatted output | `message`, `format` |
| `transform` | Python expressions | `expr`, `var` |
| `prompt` | User input | `message`, `var` |
| `set_variable` | Set variables | `name`, `value` |
| `condition` | If conditions | `if` |

## Template Variables

Use Jinja2 syntax in params:

- `{{ input }}` — User input
- `{{ variable_name }}` — Skill variables
- `{{ step_output.stdout }}` — Previous step output
- `{{ input | urlencode }}` — URL encode
- `{% if condition %}...{% endif %}` — Conditionals

## Publishing Your Skill

1. Write your `skill.yaml`
2. Test with `agentbolt run skill.yaml`
3. Validate with `agentbolt validate skill.yaml`
4. Share the YAML file — it's just one file!

## Monetization

Create premium skill packs and sell on:
- Gumroad
- Your own website
- GitHub Sponsors
