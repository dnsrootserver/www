"""Skill Loader — discovers and loads skills from various sources."""

import os
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional

from agentforge.core.engine import Skill


class SkillLoader:
    """Discovers and loads skills from directories, URLs, or packages."""
    
    @staticmethod
    def load_from_file(path: str) -> Optional[Skill]:
        """Load a single skill from a YAML file."""
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
            if data and isinstance(data, dict) and "steps" in data:
                return Skill(data, base_dir=str(Path(path).parent))
        except Exception as e:
            print(f"[ERROR] Failed to load {path}: {e}")
        return None
    
    @staticmethod
    def load_from_dir(directory: str) -> List[Skill]:
        """Load all skills from a directory."""
        skills = []
        dirpath = Path(directory)
        for ext in ["*.yaml", "*.yml"]:
            for path in sorted(dirpath.rglob(ext)):
                skill = SkillLoader.load_from_file(str(path))
                if skill:
                    skills.append(skill)
        return skills
    
    @staticmethod
    def load_from_url(url: str) -> Optional[Skill]:
        """Load a skill from a URL."""
        import requests
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = yaml.safe_load(resp.text)
            if data and isinstance(data, dict) and "steps" in data:
                return Skill(data)
        except Exception as e:
            print(f"[ERROR] Failed to load from {url}: {e}")
        return None
    
    @staticmethod
    def load_builtin() -> List[Skill]:
        """Load built-in skills from the package."""
        builtin_dir = Path(__file__).parent.parent / "skills"
        if builtin_dir.exists():
            return SkillLoader.load_from_dir(str(builtin_dir))
        return []
    
    @staticmethod
    def discover(search_paths: Optional[List[str]] = None) -> List[Skill]:
        """Discover skills from multiple locations."""
        skills = []
        
        # Built-in skills
        skills.extend(SkillLoader.load_builtin())
        
        # Search paths
        for path in (search_paths or []):
            if os.path.isdir(path):
                skills.extend(SkillLoader.load_from_dir(path))
            elif os.path.isfile(path):
                skill = SkillLoader.load_from_file(path)
                if skill:
                    skills.append(skill)
        
        # Current directory
        if os.path.isdir("skills"):
            skills.extend(SkillLoader.load_from_dir("skills"))
        
        # User home directory
        home_skills = Path.home() / ".agentforge" / "skills"
        if home_skills.exists():
            skills.extend(SkillLoader.load_from_dir(str(home_skills)))
        
        # Deduplicate by name
        seen = set()
        unique = []
        for s in skills:
            if s.name not in seen:
                seen.add(s.name)
                unique.append(s)
        
        return unique
