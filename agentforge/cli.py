"""
AgentBolt CLI — Command line interface for the AgentBolt framework.
"""

import os
import sys
import json
import yaml
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich import print as rprint

from agentbolt import __version__
from agentbolt.core.engine import AgentEngine, Skill
from agentbolt.core.loader import SkillLoader

console = Console()


@click.group()
@click.version_option(__version__, prog_name="agentbolt")
def main():
    """🤖 AgentBolt — Build AI Agent Skills with YAML — Fast, Simple, Powerful
    
    Build AI Agent Skills with YAML — Fast, Simple, Powerful.
    """
    pass


@main.command()
@click.argument("name")
@click.option("--dir", "-d", default=".", help="Directory to create skill in")
def init(name, dir):
    """Create a new skill from template."""
    skill_dir = Path(dir) / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    skill_file = skill_dir / "skill.yaml"
    
    template = {
        "name": name,
        "version": "1.0.0",
        "description": f"A skill that {name.replace('-', ' ')}",
        "author": "your-name",
        "triggers": [name, f"run {name}"],
        "variables": {
            "example_var": "default_value",
        },
        "steps": [
            {
                "tool": "log",
                "params": {
                    "message": f"Running {name} skill...",
                    "level": "info",
                },
            },
            # Add your steps here
            {
                "tool": "output",
                "params": {
                    "message": f"✅ {name} completed!",
                    "format": "text",
                },
            },
        ],
    }
    
    with open(skill_file, "w") as f:
        yaml.dump(template, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    console.print(Panel(
        f"[green]✓[/green] Created skill: [cyan]{name}[/cyan]\n"
        f"  File: {skill_file}\n\n"
        f"[dim]Edit the YAML file to define your skill's behavior.\n"
        f"Run with: agentbolt run {skill_file}[/dim]",
        title="New Skill"
    ))


@main.command()
@click.argument("skill_path")
@click.option("--input", "-i", "user_input", default="", help="User input text")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON")
def run(skill_path, user_input, json_output):
    """Run a skill from a YAML file or directory."""
    
    # Load skill(s)
    if os.path.isdir(skill_path):
        skills = SkillLoader.load_from_dir(skill_path)
        if not skills:
            console.print(f"[red]No skills found in {skill_path}[/red]")
            return
        engine = AgentEngine(skills_dir=skill_path)
        engine.skills = skills
    elif os.path.isfile(skill_path):
        skill = SkillLoader.load_from_file(skill_path)
        if not skill:
            console.print(f"[red]Failed to load skill: {skill_path}[/red]")
            return
        engine = AgentEngine()
        engine.skills = [skill]
    else:
        console.print(f"[red]Not found: {skill_path}[/red]")
        return
    
    # Find matching skill
    if user_input:
        matched = engine.find_skill(user_input)
    else:
        matched = engine.skills[0] if engine.skills else None
        user_input = skill_path
    
    if not matched:
        console.print(f"[yellow]No skill matched input: {user_input}[/yellow]")
        return
    
    # Run
    console.print(f"[dim]Running: {matched.name}[/dim]")
    result = engine.run_skill(matched, user_input)
    
    if json_output:
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        if result["success"]:
            console.print(f"[green]✓ Completed in {result['steps_executed']} steps[/green]")
        else:
            console.print(f"[yellow]⚠ Completed with issues[/yellow]")


@main.command()
@click.option("--dir", "-d", default=".", help="Skills directory")
@click.option("--input", "-i", "user_input", default=None, help="Process single input")
def chat(dir, user_input):
    """Interactive chat mode or single input processing."""
    engine = AgentEngine(skills_dir=dir)
    count = engine.load_skills()
    
    if count == 0:
        console.print("[yellow]No skills found. Create one with: agentbolt init <name>[/yellow]")
        return
    
    if user_input:
        skill = engine.find_skill(user_input)
        if skill:
            result = engine.run_skill(skill, user_input)
            console.print_json(json.dumps(result, default=str))
        else:
            console.print(f"[red]No skill matched: {user_input}[/red]")
    else:
        engine.run_interactive()


@main.command()
@click.option("--dir", "-d", default=".", help="Skills directory")
def list(dir):
    """List all available skills."""
    skills = SkillLoader.load_from_dir(dir)
    
    if not skills:
        # Also check built-in
        skills = SkillLoader.load_builtin()
    
    if not skills:
        console.print("[yellow]No skills found.[/yellow]")
        console.print("[dim]Create one with: agentbolt init <name>[/dim]")
        return
    
    table = Table(title=f"Available Skills ({len(skills)})")
    table.add_column("Name", style="cyan", min_width=20)
    table.add_column("Version", style="dim")
    table.add_column("Description", style="white")
    table.add_column("Triggers", style="green")
    
    for skill in skills:
        triggers = ", ".join(str(t)[:20] for t in skill.triggers[:3])
        table.add_row(
            skill.name,
            skill.version,
            skill.description[:50],
            triggers,
        )
    
    console.print(table)


@main.command()
@click.argument("skill_path")
def validate(skill_path):
    """Validate a skill YAML file."""
    skill = SkillLoader.load_from_file(skill_path)
    
    if not skill:
        console.print(f"[red]✗ Invalid: {skill_path}[/red]")
        return
    
    errors = []
    warnings = []
    
    if not skill.name:
        errors.append("Missing 'name' field")
    if not skill.steps:
        errors.append("No 'steps' defined")
    if not skill.triggers:
        warnings.append("No 'triggers' defined — skill won't auto-match")
    if not skill.description:
        warnings.append("No 'description' field")
    
    for i, step in enumerate(skill.steps):
        if "tool" not in step:
            errors.append(f"Step {i+1}: Missing 'tool' field")
    
    if errors:
        console.print(f"[red]✗ {len(errors)} error(s):[/red]")
        for e in errors:
            console.print(f"  [red]• {e}[/red]")
    else:
        console.print(f"[green]✓ Valid skill: {skill.name}[/green]")
    
    if warnings:
        for w in warnings:
            console.print(f"  [yellow]⚠ {w}[/yellow]")


@main.command()
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON")
def doctor(json_output):
    """Check system and dependencies."""
    checks = []
    
    # Python version
    py_ver = sys.version.split()[0]
    checks.append({"name": "Python", "status": "ok", "detail": py_ver})
    
    # Required packages
    for pkg in ["yaml", "requests", "rich", "click", "jinja2"]:
        try:
            __import__(pkg)
            checks.append({"name": pkg, "status": "ok", "detail": "installed"})
        except ImportError:
            checks.append({"name": pkg, "status": "missing", "detail": "pip install " + pkg})
    
    # Optional packages
    for pkg in ["openai", "anthropic", "feedparser"]:
        try:
            __import__(pkg)
            checks.append({"name": pkg + " (optional)", "status": "ok", "detail": "installed"})
        except ImportError:
            checks.append({"name": pkg + " (optional)", "status": "optional", "detail": "not installed"})
    
    if json_output:
        click.echo(json.dumps(checks, indent=2))
    else:
        table = Table(title="System Check")
        table.add_column("Package", style="cyan")
        table.add_column("Status")
        table.add_column("Detail", style="dim")
        
        for c in checks:
            status = {"ok": "[green]✓[/green]", "missing": "[red]✗[/red]",
                     "optional": "[yellow]○[/yellow]"}[c["status"]]
            table.add_row(c["name"], status, c["detail"])
        
        console.print(table)


@main.command()
def examples():
    """Show example skills."""
    examples_dir = Path(__file__).parent.parent / "skills"
    if examples_dir.exists():
        for f in sorted(examples_dir.glob("*.yaml")):
            console.print(f"\n[bold cyan]{'='*50}[/bold cyan]")
            console.print(f"[bold]{f.name}[/bold]")
            console.print(f"[bold cyan]{'='*50}[/bold cyan]")
            with open(f) as fh:
                content = fh.read()
            console.print(Syntax(content, "yaml", theme="monokai"))
    else:
        console.print("[yellow]No examples found.[/yellow]")


if __name__ == "__main__":
    main()
