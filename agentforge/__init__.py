"""
AgentForge — Declarative AI Agent Skill Framework
Build agent skills with YAML, not code.
"""

__version__ = "1.1.0"
__author__ = "AgentForge Contributors"

from agentforge.core.engine import AgentEngine, Skill
from agentforge.core.loader import SkillLoader

__all__ = ["AgentEngine", "Skill", "SkillLoader"]
