"""
AgentForge Core Engine
Runs skills defined in YAML format.
"""

import os
import json
import subprocess
import re
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
        self.author = skill_data.get("author", "unknown")
        self.triggers = skill_data.get("triggers", [])
        self.steps = skill_data.get("steps", [])
        self.tools = skill_data.get("tools", {})
        self.config = skill_data.get("config", {})
        self.variables = skill_data.get("variables", {})
    
    def matches_trigger(self, user_input: str) -> bool:
        """Check if user input matches any trigger pattern."""
        user_lower = user_input.lower().strip()
        for trigger in self.triggers:
            if isinstance(trigger, str):
                if trigger.lower() in user_lower:
                    return True
            elif isinstance(trigger, dict):
                pattern = trigger.get("pattern", "")
                if trigger.get("type") == "regex":
                    if re.search(pattern, user_input, re.IGNORECASE):
                        return True
                elif trigger.get("type") == "exact":
                    if user_lower == pattern.lower():
                        return True
                elif trigger.get("type") == "startswith":
                    if user_lower.startswith(pattern.lower()):
                        return True
        return False
    
    def render_template(self, template_str: str, context: Dict[str, Any]) -> str:
        """Render a Jinja2 template string."""
        tmpl = Template(template_str)
        return tmpl.render(**context)
    
    def to_dict(self) -> Dict[str, Any]:
        return self.data


class ToolExecutor:
    """Executes tool calls defined in skill steps."""
    
    TOOL_REGISTRY = {}
    
    @classmethod
    def register(cls, name: str):
        """Decorator to register a tool."""
        def decorator(func):
            cls.TOOL_REGISTRY[name] = func
            return func
        return decorator
    
    @classmethod
    def execute(cls, tool_name: str, params: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Execute a registered tool."""
        if tool_name in cls.TOOL_REGISTRY:
            return cls.TOOL_REGISTRY[tool_name](params, context)
        else:
            return {"error": f"Unknown tool: {tool_name}", "available": list(cls.TOOL_REGISTRY.keys())}


# ============ Built-in Tools ============

@ToolExecutor.register("shell")
def _tool_shell(params: Dict, context: Dict) -> Dict:
    """Execute a shell command."""
    cmd = params.get("command", "")
    if not cmd:
        return {"error": "No command specified"}
    
    cmd = Template(cmd).render(**context)
    timeout = params.get("timeout", 30)
    
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "success": result.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        return {"error": f"Command timed out after {timeout}s"}
    except Exception as e:
        return {"error": str(e)}


@ToolExecutor.register("http")
def _tool_http(params: Dict, context: Dict) -> Dict:
    """Make an HTTP request."""
    import requests as req
    
    url = Template(params.get("url", "")).render(**context)
    method = params.get("method", "GET").upper()
    headers = params.get("headers", {})
    body = params.get("body")
    
    if body and isinstance(body, str):
        body = Template(body).render(**context)
    
    try:
        resp = req.request(method, url, headers=headers, json=body if isinstance(body, dict) else None,
                          data=body if isinstance(body, str) else None, timeout=30)
        return {
            "status": resp.status_code,
            "headers": dict(resp.headers),
            "body": resp.text[:5000],
            "success": resp.status_code < 400,
        }
    except Exception as e:
        return {"error": str(e)}


@ToolExecutor.register("read_file")
def _tool_read_file(params: Dict, context: Dict) -> Dict:
    """Read a file."""
    path = Template(params.get("path", "")).render(**context)
    try:
        with open(path, "r", encoding=params.get("encoding", "utf-8")) as f:
            content = f.read()
        return {"content": content, "success": True}
    except Exception as e:
        return {"error": str(e)}


@ToolExecutor.register("write_file")
def _tool_write_file(params: Dict, context: Dict) -> Dict:
    """Write content to a file."""
    path = Template(params.get("path", "")).render(**context)
    content = Template(params.get("content", "")).render(**context)
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding=params.get("encoding", "utf-8")) as f:
            f.write(content)
        return {"path": path, "success": True}
    except Exception as e:
        return {"error": str(e)}


@ToolExecutor.register("set_variable")
def _tool_set_variable(params: Dict, context: Dict) -> Dict:
    """Set a variable in context."""
    name = params.get("name", "")
    value = Template(str(params.get("value", ""))).render(**context)
    context[name] = value
    return {"name": name, "value": value, "success": True}


@ToolExecutor.register("prompt")
def _tool_prompt(params: Dict, context: Dict) -> Dict:
    """Ask user for input."""
    message = Template(params.get("message", "Enter value:")).render(**context)
    default = params.get("default", "")
    var_name = params.get("var", "input")
    
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


@ToolExecutor.register("log")
def _tool_log(params: Dict, context: Dict) -> Dict:
    """Log a message."""
    message = Template(params.get("message", "")).render(**context)
    level = params.get("level", "info")
    
    try:
        from rich.console import Console
        console = Console()
        colors = {"info": "blue", "success": "green", "warn": "yellow", "error": "red"}
        color = colors.get(level, "white")
        console.print(f"[{color}]{message}[/{color}]")
    except:
        print(f"[{level.upper()}] {message}")
    
    return {"message": message, "level": level, "success": True}


@ToolExecutor.register("transform")
def _tool_transform(params: Dict, context: Dict) -> Dict:
    """Transform data using Python expression."""
    expr = params.get("expr", "")
    var_name = params.get("var", "result")
    
    try:
        safe_globals = {"__builtins__": {}, "json": json, "len": len, "str": str,
                       "int": int, "float": float, "list": list, "dict": dict,
                       "sorted": sorted, "filter": filter, "map": map, "sum": sum,
                       "max": max, "min": min, "abs": abs, "round": round}
        result = eval(expr, safe_globals, context)
        context[var_name] = result
        return {"name": var_name, "value": str(result)[:1000], "success": True}
    except Exception as e:
        return {"error": f"Transform error: {e}"}


@ToolExecutor.register("condition")
def _tool_condition(params: Dict, context: Dict) -> Dict:
    """Evaluate a condition."""
    expr = params.get("if", "True")
    try:
        safe_globals = {"__builtins__": {}}
        result = bool(eval(expr, safe_globals, context))
        return {"result": result, "success": True}
    except Exception as e:
        return {"error": str(e), "result": False}


@ToolExecutor.register("loop")
def _tool_loop(params: Dict, context: Dict) -> Dict:
    """Loop over items."""
    items_expr = params.get("items", "[]")
    var_name = params.get("var", "item")
    
    try:
        items = eval(items_expr, {"__builtins__": {}}, context)
        return {"items": list(items), "count": len(list(items)), "success": True,
                "var": var_name}
    except Exception as e:
        return {"error": str(e)}


@ToolExecutor.register("output")
def _tool_output(params: Dict, context: Dict) -> Dict:
    """Output result to user."""
    message = Template(params.get("message", "")).render(**context)
    format_type = params.get("format", "text")
    
    try:
        from rich.console import Console
        from rich.markdown import Markdown
        from rich.panel import Panel
        from rich.table import Table
        from rich import print as rprint
        
        console = Console()
        
        if format_type == "markdown":
            console.print(Panel(Markdown(message), title=params.get("title", "Result")))
        elif format_type == "json":
            data = json.loads(message)
            console.print_json(json.dumps(data))
        elif format_type == "table":
            # message should be JSON array of objects
            data = json.loads(message)
            if data and isinstance(data, list):
                table = Table(title=params.get("title", ""))
                for key in data[0].keys():
                    table.add_column(str(key), style="cyan")
                for row in data:
                    table.add_row(*[str(v) for v in row.values()])
                console.print(table)
        else:
            console.print(message)
    except:
        print(message)
    
    return {"output": message, "success": True}


class AgentEngine:
    """Main engine that loads and runs skills."""
    
    def __init__(self, skills_dir: str = ".", config: Optional[Dict] = None):
        self.skills_dir = Path(skills_dir)
        self.config = config or {}
        self.skills: List[Skill] = []
        self.context: Dict[str, Any] = {}
    
    def load_skills(self) -> int:
        """Load all .yaml/.yml skills from directory."""
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
                except Exception as e:
                    print(f"[WARN] Failed to load {path}: {e}")
        return count
    
    def find_skill(self, user_input: str) -> Optional[Skill]:
        """Find a skill that matches user input."""
        for skill in self.skills:
            if skill.matches_trigger(user_input):
                return skill
        return None
    
    def run_skill(self, skill: Skill, user_input: str = "") -> Dict[str, Any]:
        """Execute a skill's steps."""
        context = {
            "input": user_input,
            "user_input": user_input,
            "config": self.config,
            "variables": skill.variables.copy(),
            **skill.variables,
        }
        
        results = []
        
        for i, step in enumerate(skill.steps):
            tool_name = step.get("tool", "")
            params = step.get("params", {})
            
            # Add step index to context
            context["step"] = i + 1
            
            # Check condition
            if "if" in step:
                cond_result = ToolExecutor.execute("condition", {"if": step["if"]}, context)
                if not cond_result.get("result", False):
                    continue
            
            # Execute tool
            result = ToolExecutor.execute(tool_name, params, context)
            results.append({"step": i + 1, "tool": tool_name, "result": result})
            
            # Update context with output variable
            if "output" in step:
                context[step["output"]] = result
            
            # Break on error if configured
            if not result.get("success", True) and step.get("stop_on_error", False):
                break
        
        return {
            "skill": skill.name,
            "success": all(r["result"].get("success", True) for r in results),
            "steps_executed": len(results),
            "results": results,
            "context": {k: v for k, v in context.items() 
                       if not k.startswith("_") and not callable(v)},
        }
    
    def run_interactive(self):
        """Run in interactive mode."""
        try:
            from rich.console import Console
            from rich.panel import Panel
            from rich.table import Table
            
            console = Console()
            console.print(Panel(
                f"[bold green]AgentForge v1.0.0[/bold green]\n"
                f"Loaded [cyan]{len(self.skills)}[/cyan] skills\n"
                f"Type a command or [dim]help[/dim] to see available skills",
                title="🤖 AgentForge"
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
                    table = Table(title="Available Skills")
                    table.add_column("Skill", style="cyan")
                    table.add_column("Description", style="white")
                    table.add_column("Triggers", style="dim")
                    for s in self.skills:
                        triggers = ", ".join(str(t) for t in s.triggers[:3])
                        table.add_row(s.name, s.description[:50], triggers)
                    console.print(table)
                    continue
                
                if user_input.strip().lower() == "skills":
                    for s in self.skills:
                        console.print(f"  [cyan]{s.name}[/cyan]: {s.description}")
                    continue
                
                skill = self.find_skill(user_input)
                if skill:
                    console.print(f"[dim]Running skill: {skill.name}[/dim]")
                    result = self.run_skill(skill, user_input)
                    if result["success"]:
                        console.print(f"[green]✓ Skill completed ({result['steps_executed']} steps)[/green]")
                    else:
                        console.print(f"[yellow]⚠ Skill completed with issues[/yellow]")
                else:
                    console.print(f"[red]No skill matched: {user_input}[/red]")
                    console.print("[dim]Type 'help' to see available skills[/dim]")
        
        except ImportError:
            print("AgentForge v1.0.0 — Interactive mode requires 'rich'")
            print("Install: pip install rich")
