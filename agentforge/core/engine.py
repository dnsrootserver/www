"""
AgentBolt Core Engine v1.1.0
Supports 18 built-in tools + LLM integration + multi-language
"""

import os
import json
import subprocess
import re
import hashlib
import time
import base64
from typing import Dict, Any, List, Optional
from pathlib import Path

import yaml
from jinja2 import Template


class Skill:
    """Represents a single agent skill loaded from YAML."""
    
    def __init__(self, skill_data: Dict[str, Any], base_dir: str = "."):
        self.data = skill_data
        self.base_dir = base_dir
        self.name = skill_data.get("name", "unnamed")
        self.version = skill_data.get("version", "1.0.0")
        self.description = skill_data.get("description", "")
        self.description_zh = skill_data.get("description_zh", "")
        self.author = skill_data.get("author", "unknown")
        self.category = skill_data.get("category", "general")
        self.triggers = skill_data.get("triggers", [])
        self.triggers_zh = skill_data.get("triggers_zh", [])
        self.steps = skill_data.get("steps", [])
        self.tools = skill_data.get("tools", {})
        self.config = skill_data.get("config", {})
        self.variables = skill_data.get("variables", {})
        self.tags = skill_data.get("tags", [])
        self.premium = skill_data.get("premium", False)
        self.price = skill_data.get("price", None)
    
    def matches_trigger(self, user_input: str) -> bool:
        """Check if user input matches any trigger pattern (EN + ZH)."""
        user_lower = user_input.lower().strip()
        all_triggers = self.triggers + self.triggers_zh
        for trigger in all_triggers:
            if isinstance(trigger, str):
                if trigger.lower() in user_lower:
                    return True
            elif isinstance(trigger, dict):
                pattern = trigger.get("pattern", "")
                t = trigger.get("type", "contains")
                if t == "regex":
                    if re.search(pattern, user_input, re.IGNORECASE):
                        return True
                elif t == "exact":
                    if user_lower == pattern.lower():
                        return True
                elif t == "startswith":
                    if user_lower.startswith(pattern.lower()):
                        return True
                elif t == "contains":
                    if pattern.lower() in user_lower:
                        return True
        return False
    
    def render_template(self, template_str: str, context: Dict[str, Any]) -> str:
        tmpl = Template(template_str)
        return tmpl.render(**context)
    
    def to_dict(self) -> Dict[str, Any]:
        return self.data


class ToolExecutor:
    """Executes tool calls. Supports 18+ built-in tools."""
    
    TOOL_REGISTRY = {}
    
    @classmethod
    def register(cls, name: str):
        def decorator(func):
            cls.TOOL_REGISTRY[name] = func
            return func
        return decorator
    
    @classmethod
    def execute(cls, tool_name: str, params: Dict[str, Any], context: Dict[str, Any]) -> Any:
        if tool_name in cls.TOOL_REGISTRY:
            try:
                return cls.TOOL_REGISTRY[tool_name](params, context)
            except Exception as e:
                return {"error": str(e), "success": False}
        return {"error": f"Unknown tool: {tool_name}", "available": list(cls.TOOL_REGISTRY.keys()), "success": False}
    
    @classmethod
    def list_tools(cls) -> List[str]:
        return list(cls.TOOL_REGISTRY.keys())


# ============ TOOL: shell ============
@ToolExecutor.register("shell")
def _tool_shell(params, context):
    cmd = _render(params.get("command", ""), context)
    if not cmd:
        return {"error": "No command specified", "success": False}
    timeout = params.get("timeout", 30)
    workdir = _render(params.get("workdir", ""), context) or None
    env = {**os.environ}
    for k, v in params.get("env", {}).items():
        env[k] = _render(str(v), context)
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, cwd=workdir, env=env)
        return {"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode, "success": result.returncode == 0}
    except subprocess.TimeoutExpired:
        return {"error": f"Timeout after {timeout}s", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}


# ============ TOOL: http ============
@ToolExecutor.register("http")
def _tool_http(params, context):
    import requests as req
    url = _render(params.get("url", ""), context)
    method = params.get("method", "GET").upper()
    headers = {k: _render(str(v), context) for k, v in params.get("headers", {}).items()}
    body = params.get("body")
    if body and isinstance(body, str):
        body = _render(body, context)
    if body and isinstance(body, dict):
        body = json.loads(_render(json.dumps(body), context))
    try:
        resp = req.request(method, url, headers=headers, json=body if isinstance(body, dict) else None, data=body if isinstance(body, str) else None, timeout=params.get("timeout", 30))
        return {"status": resp.status_code, "headers": dict(resp.headers), "body": resp.text[:10000], "json": resp.json() if resp.headers.get("content-type","").startswith("application/json") else None, "success": resp.status_code < 400}
    except Exception as e:
        return {"error": str(e), "success": False}


# ============ TOOL: read_file ============
@ToolExecutor.register("read_file")
def _tool_read_file(params, context):
    path = _render(params.get("path", ""), context)
    try:
        with open(path, "r", encoding=params.get("encoding", "utf-8")) as f:
            content = f.read()
        lines = content.split("\n")
        return {"content": content, "lines": len(lines), "size": len(content), "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}


# ============ TOOL: write_file ============
@ToolExecutor.register("write_file")
def _tool_write_file(params, context):
    path = _render(params.get("path", ""), context)
    content = _render(params.get("content", ""), context)
    mode = params.get("mode", "w")
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, mode, encoding=params.get("encoding", "utf-8")) as f:
            f.write(content)
        return {"path": path, "size": len(content), "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}


# ============ TOOL: set_variable ============
@ToolExecutor.register("set_variable")
def _tool_set_variable(params, context):
    name = params.get("name", "")
    value = _render(str(params.get("value", "")), context)
    context[name] = value
    return {"name": name, "value": value, "success": True}


# ============ TOOL: prompt ============
@ToolExecutor.register("prompt")
def _tool_prompt(params, context):
    message = _render(params.get("message", "Input:"), context)
    var_name = params.get("var", "input")
    default = params.get("default", "")
    try:
        from rich.console import Console
        console = Console()
        user_input = console.input(f"[bold cyan]{message}[/bold cyan] ")
    except:
        user_input = input(f"{message} ")
    if not user_input and default:
        user_input = default
    context[var_name] = user_input
    return {"name": var_name, "value": user_input, "success": True}


# ============ TOOL: log ============
@ToolExecutor.register("log")
def _tool_log(params, context):
    message = _render(params.get("message", ""), context)
    level = params.get("level", "info")
    try:
        from rich.console import Console
        console = Console()
        colors = {"info": "blue", "success": "green", "warn": "yellow", "error": "red", "debug": "dim"}
        icons = {"info": "ℹ️", "success": "✅", "warn": "⚠️", "error": "❌", "debug": "🔍"}
        color = colors.get(level, "white")
        icon = icons.get(level, "")
        console.print(f"  {icon} [{color}]{message}[/{color}]")
    except:
        print(f"[{level.upper()}] {message}")
    return {"message": message, "level": level, "success": True}


# ============ TOOL: transform ============
@ToolExecutor.register("transform")
def _tool_transform(params, context):
    expr = params.get("expr", "")
    var_name = params.get("var", "result")
    try:
        safe_globals = {"__builtins__": {}, "json": json, "len": len, "str": str, "int": int, "float": float,
                       "list": list, "dict": dict, "sorted": sorted, "filter": filter, "map": map,
                       "sum": sum, "max": max, "min": min, "abs": abs, "round": round, "isinstance": isinstance,
                       "type": type, "range": range, "enumerate": enumerate, "zip": zip, "any": any, "all": all,
                       "hash": hash, "re": re, "os": os, "time": time, "base64": base64, "hashlib": hashlib}
        result = eval(expr, safe_globals, context)
        context[var_name] = result
        return {"name": var_name, "value": str(result)[:5000], "success": True}
    except Exception as e:
        return {"error": f"Transform error: {e}", "success": False}


# ============ TOOL: condition ============
@ToolExecutor.register("condition")
def _tool_condition(params, context):
    expr = params.get("if", "True")
    try:
        result = bool(eval(expr, {"__builtins__": {}}, context))
        return {"result": result, "success": True}
    except Exception as e:
        return {"error": str(e), "result": False, "success": False}


# ============ TOOL: output ============
@ToolExecutor.register("output")
def _tool_output(params, context):
    message = _render(params.get("message", ""), context)
    fmt = params.get("format", "text")
    title = params.get("title", "")
    try:
        from rich.console import Console
        from rich.markdown import Markdown
        from rich.panel import Panel
        from rich.table import Table
        from rich.syntax import Syntax
        console = Console()
        if fmt == "markdown":
            console.print(Panel(Markdown(message), title=title or "Output"))
        elif fmt == "json":
            data = json.loads(message)
            console.print_json(json.dumps(data))
        elif fmt == "table":
            data = json.loads(message)
            if data and isinstance(data, list):
                table = Table(title=title)
                for key in data[0].keys():
                    table.add_column(str(key), style="cyan")
                for row in data:
                    table.add_row(*[str(v) for v in row.values()])
                console.print(table)
        elif fmt == "code":
            lang = params.get("lang", "python")
            console.print(Syntax(message, lang, theme="monokai"))
        elif fmt == "panel":
            console.print(Panel(message, title=title or "Result"))
        else:
            if title:
                console.print(f"\n[bold]{title}[/bold]")
            console.print(message)
    except:
        if title:
            print(f"\n=== {title} ===")
        print(message)
    return {"output": message, "success": True}


# ============ TOOL: regex_extract ============
@ToolExecutor.register("regex_extract")
def _tool_regex_extract(params, context):
    text = _render(params.get("text", ""), context)
    pattern = params.get("pattern", "")
    var_name = params.get("var", "matches")
    group = params.get("group", 0)
    try:
        matches = re.findall(pattern, text)
        if isinstance(group, int) and matches and isinstance(matches[0], tuple):
            matches = [m[group] for m in matches]
        context[var_name] = matches
        return {"matches": matches, "count": len(matches), "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}


# ============ TOOL: json_parse ============
@ToolExecutor.register("json_parse")
def _tool_json_parse(params, context):
    text = _render(params.get("text", ""), context)
    var_name = params.get("var", "data")
    try:
        data = json.loads(text)
        context[var_name] = data
        return {"data": data, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}


# ============ TOOL: loop ============
@ToolExecutor.register("loop")
def _tool_loop(params, context):
    items_expr = params.get("items", "[]")
    var_name = params.get("var", "item")
    steps = params.get("steps", [])
    try:
        items = eval(items_expr, {"__builtins__": {}}, context)
        items = list(items)
        results = []
        for item in items:
            ctx = {**context, var_name: item}
            for step in steps:
                tool = step.get("tool", "")
                p = step.get("params", {})
                r = ToolExecutor.execute(tool, p, ctx)
                results.append(r)
        return {"items_processed": len(items), "results": results, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}


# ============ TOOL: schedule ============
@ToolExecutor.register("schedule")
def _tool_schedule(params, context):
    """Write a cron job or scheduled task."""
    command = _render(params.get("command", ""), context)
    schedule = params.get("schedule", "0 * * * *")
    action = params.get("action", "show")
    
    if action == "show":
        return {"message": f"Would schedule: {command} at {schedule}", "success": True}
    elif action == "add":
        cron_line = f"{schedule} {command}"
        try:
            result = subprocess.run("(crontab -l 2>/dev/null; echo '{}') | crontab -".format(cron_line), shell=True, capture_output=True, text=True)
            return {"message": f"Added cron: {cron_line}", "success": result.returncode == 0}
        except Exception as e:
            return {"error": str(e), "success": False}
    return {"message": "Unknown action", "success": False}


# ============ TOOL: retry ============
@ToolExecutor.register("retry")
def _tool_retry(params, context):
    """Retry a step N times with delay."""
    steps = params.get("steps", [])
    max_attempts = params.get("max_attempts", 3)
    delay = params.get("delay", 1)
    
    for attempt in range(max_attempts):
        for step in steps:
            tool = step.get("tool", "")
            p = step.get("params", {})
            result = ToolExecutor.execute(tool, p, context)
            if result.get("success", True):
                return {"attempts": attempt + 1, "result": result, "success": True}
        if attempt < max_attempts - 1:
            time.sleep(delay)
    
    return {"attempts": max_attempts, "success": False, "error": "All attempts failed"}


# ============ TOOL: notify ============
@ToolExecutor.register("notify")
def _tool_notify(params, context):
    """Send notification (desktop, file, webhook)."""
    message = _render(params.get("message", ""), context)
    method = params.get("method", "desktop")
    title = _render(params.get("title", "AgentBolt"), context)
    
    try:
        if method == "desktop":
            subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'], capture_output=True)
            return {"message": "Desktop notification sent", "success": True}
        elif method == "webhook":
            import requests
            url = _render(params.get("url", ""), context)
            resp = requests.post(url, json={"text": message, "title": title}, timeout=10)
            return {"status": resp.status_code, "success": resp.status_code < 400}
        elif method == "file":
            path = _render(params.get("path", "/tmp/agentbolt-notifications.log"), context)
            with open(path, "a") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {title}: {message}\n")
            return {"path": path, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}


# ============ TOOL: download ============
@ToolExecutor.register("download")
def _tool_download(params, context):
    """Download a file from URL."""
    import requests as req
    url = _render(params.get("url", ""), context)
    dest = _render(params.get("dest", ""), context)
    try:
        resp = req.get(url, timeout=params.get("timeout", 60), stream=True)
        resp.raise_for_status()
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        size = os.path.getsize(dest)
        return {"path": dest, "size": size, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}


# ============ TOOL: compress ============
@ToolExecutor.register("compress")
def _tool_compress(params, context):
    """Compress/decompress files."""
    import zipfile, tarfile
    action = params.get("action", "zip")
    source = _render(params.get("source", ""), context)
    dest = _render(params.get("dest", ""), context)
    
    try:
        if action == "zip":
            with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as zf:
                if os.path.isdir(source):
                    for root, dirs, files in os.walk(source):
                        for f in files:
                            zf.write(os.path.join(root, f), os.path.relpath(os.path.join(root, f), source))
                else:
                    zf.write(source, os.path.basename(source))
        elif action == "unzip":
            with zipfile.ZipFile(source, 'r') as zf:
                zf.extractall(dest)
        return {"path": dest, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}


# ============ TOOL: template ============
@ToolExecutor.register("template")
def _tool_template(params, context):
    """Render a Jinja2 template file."""
    template_path = _render(params.get("template", ""), context)
    output_path = _render(params.get("output", ""), context)
    try:
        with open(template_path, "r") as f:
            tmpl = Template(f.read())
        rendered = tmpl.render(**context)
        if output_path:
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            with open(output_path, "w") as f:
                f.write(rendered)
            return {"path": output_path, "success": True}
        else:
            return {"content": rendered, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}


# ============ Helper ============
def _render(template_str, context):
    """Render a Jinja2 template string safely."""
    if not template_str or "{{" not in template_str:
        return template_str
    try:
        return Template(str(template_str)).render(**context)
    except:
        return template_str


class AgentEngine:
    """Main engine that loads and runs skills."""
    
    def __init__(self, skills_dir: str = ".", config: Optional[Dict] = None):
        self.skills_dir = Path(skills_dir)
        self.config = config or {}
        self.skills: List[Skill] = []
        self.context: Dict[str, Any] = {}
    
    def load_skills(self) -> int:
        count = 0
        for ext in ["*.yaml", "*.yml"]:
            for path in sorted(self.skills_dir.rglob(ext)):
                try:
                    with open(path) as f:
                        data = yaml.safe_load(f)
                    if data and isinstance(data, dict) and "steps" in data:
                        skill = Skill(data, base_dir=str(path.parent))
                        self.skills.append(skill)
                        count += 1
                except:
                    pass
        return count
    
    def find_skill(self, user_input: str) -> Optional[Skill]:
        for skill in self.skills:
            if skill.matches_trigger(user_input):
                return skill
        return None
    
    def run_skill(self, skill: Skill, user_input: str = "") -> Dict[str, Any]:
        context = {
            "input": user_input, "user_input": user_input,
            "config": self.config, "variables": skill.variables.copy(),
            **skill.variables,
        }
        results = []
        for i, step in enumerate(skill.steps):
            context["step"] = i + 1
            if "if" in step:
                cond = ToolExecutor.execute("condition", {"if": step["if"]}, context)
                if not cond.get("result", False):
                    continue
            tool_name = step.get("tool", "")
            params = step.get("params", {})
            result = ToolExecutor.execute(tool_name, params, context)
            results.append({"step": i + 1, "tool": tool_name, "result": result})
            if "output" in step:
                context[step["output"]] = result
            if not result.get("success", True) and step.get("stop_on_error", False):
                break
        return {
            "skill": skill.name, "success": all(r["result"].get("success", True) for r in results),
            "steps_executed": len(results), "results": results,
            "context": {k: v for k, v in context.items() if not k.startswith("_") and not callable(v)},
        }
    
    def run_interactive(self):
        try:
            from rich.console import Console
            from rich.panel import Panel
            from rich.table import Table
            console = Console()
            console.print(Panel(
                f"[bold green]AgentBolt v1.1.0[/bold green]\n"
                f"Loaded [cyan]{len(self.skills)}[/cyan] skills | [cyan]{len(ToolExecutor.list_tools())}[/cyan] tools\n"
                f"Type [bold]help[/bold] for commands, [bold]skills[/bold] to list skills",
                title="🤖 AgentBolt"
            ))
            while True:
                try:
                    user_input = console.input("\n[bold yellow]▶[/bold yellow] ")
                except (EOFError, KeyboardInterrupt):
                    console.print("\n[bold red]Goodbye![/bold red]")
                    break
                if not user_input.strip():
                    continue
                if user_input.strip().lower() in ["quit", "exit", "q"]:
                    console.print("[bold red]Goodbye![/bold red]")
                    break
                if user_input.strip().lower() in ["help", "?"]:
                    table = Table(title="Commands")
                    table.add_column("Command", style="cyan")
                    table.add_column("Description")
                    for cmd, desc in [("help", "Show this help"), ("skills", "List all skills"), ("tools", "List all tools"), ("run <skill>", "Run a skill"), ("quit", "Exit")]:
                        table.add_row(cmd, desc)
                    console.print(table)
                    continue
                if user_input.strip().lower() == "skills":
                    table = Table(title=f"Skills ({len(self.skills)})")
                    table.add_column("Name", style="cyan")
                    table.add_column("Category", style="dim")
                    table.add_column("Description")
                    table.add_column("Premium", style="yellow")
                    for s in self.skills:
                        table.add_row(s.name, s.category, s.description[:40], "💎" if s.premium else "")
                    console.print(table)
                    continue
                if user_input.strip().lower() == "tools":
                    console.print(f"[cyan]Available tools ({len(ToolExecutor.list_tools())}):[/cyan]")
                    for t in ToolExecutor.list_tools():
                        console.print(f"  • {t}")
                    continue
                skill = self.find_skill(user_input)
                if skill:
                    console.print(f"[dim]Running: {skill.name}[/dim]")
                    result = self.run_skill(skill, user_input)
                    if result["success"]:
                        console.print(f"[green]✓ Completed ({result['steps_executed']} steps)[/green]")
                    else:
                        console.print(f"[yellow]⚠ Completed with issues[/yellow]")
                else:
                    console.print(f"[red]No skill matched. Type 'skills' to see available.[/red]")
        except ImportError:
            print("AgentBolt v1.1.0 — Install 'rich' for interactive mode: pip install rich")
