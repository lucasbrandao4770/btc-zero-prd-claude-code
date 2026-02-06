"""Configuration module for Dev Loop UI.

This module provides configuration settings and path handling for the
Dev Loop UI application. All paths use pathlib.Path for cross-platform
compatibility.

Environment Variables:
    DEVLOOP_PATH: Override the default Dev Loop base path
    DEVLOOP_LOG_LEVEL: Set logging level (DEBUG, INFO, WARNING, ERROR)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Final

# =============================================================================
# Path Configuration
# =============================================================================

def get_app_root() -> Path:
    """Get the root directory of the UI application.

    Returns the directory containing this config.py file.
    """
    return Path(__file__).parent.resolve()


def get_devloop_path() -> Path:
    """Get the Dev Loop base path.

    Priority:
        1. DEVLOOP_PATH environment variable (if set)
        2. Default: .claude/dev relative to project root

    Returns:
        Path to the Dev Loop directory containing tasks/, progress/, logs/
    """
    env_path = os.environ.get("DEVLOOP_PATH")
    if env_path:
        return Path(env_path).resolve()

    # Default: navigate up from ui/ to project root, then to .claude/dev
    project_root = get_app_root().parent
    return project_root / ".claude" / "dev"


def get_tasks_path() -> Path:
    """Get the path to the tasks directory (PROMPT files)."""
    return get_devloop_path() / "tasks"


def get_progress_path() -> Path:
    """Get the path to the progress directory (PROGRESS files)."""
    return get_devloop_path() / "progress"


def get_logs_path() -> Path:
    """Get the path to the logs directory (LOG files)."""
    return get_devloop_path() / "logs"


def get_templates_path() -> Path:
    """Get the path to the templates directory."""
    return get_devloop_path() / "templates"


def get_ui_logs_path() -> Path:
    """Get the path to the UI application logs directory."""
    logs_dir = get_app_root() / "logs"
    logs_dir.mkdir(exist_ok=True)
    return logs_dir


# =============================================================================
# Application Constants
# =============================================================================

# Quality tiers for PROMPT files
QUALITY_TIERS: Final[list[str]] = ["prototype", "production", "library"]
DEFAULT_QUALITY_TIER: Final[str] = "production"

# Status values for PROMPT/PROGRESS files
STATUSES: Final[list[str]] = ["NOT_STARTED", "IN_PROGRESS", "BLOCKED", "COMPLETE"]

# Priority levels
PRIORITIES: Final[list[str]] = ["RISKY", "CORE", "POLISH"]

# Date/time format for display and parsing
DATE_FORMAT: Final[str] = "%Y-%m-%d"
DATETIME_FORMAT: Final[str] = "%Y-%m-%dT%H:%M:%SZ"
DISPLAY_DATETIME_FORMAT: Final[str] = "%Y-%m-%d %H:%M"

# =============================================================================
# Caching Configuration
# =============================================================================

# Time-to-live for cached file reads (in seconds)
CACHE_TTL_SECONDS: Final[int] = 60

# Maximum number of files to cache
CACHE_MAX_ENTRIES: Final[int] = 100

# =============================================================================
# UI Configuration
# =============================================================================

# Page configuration
PAGE_TITLE: Final[str] = "Dev Loop UI"
PAGE_ICON: Final[str] = "loop"
PAGE_LAYOUT: Final[str] = "wide"

# Sidebar width (in pixels, approximate)
SIDEBAR_WIDTH: Final[int] = 300

# Maximum content preview length
MAX_PREVIEW_LENGTH: Final[int] = 500

# =============================================================================
# File Patterns
# =============================================================================

# File naming patterns
PROMPT_PREFIX: Final[str] = "PROMPT_"
PROGRESS_PREFIX: Final[str] = "PROGRESS_"
LOG_PREFIX: Final[str] = "LOG_"

PROMPT_PATTERN: Final[str] = "PROMPT_*.md"
PROGRESS_PATTERN: Final[str] = "PROGRESS_*.md"
LOG_PATTERN: Final[str] = "LOG_*.md"

# =============================================================================
# Regex Patterns
# =============================================================================

# Pattern for extracting task name from PROMPT filename
# e.g., PROMPT_DEVLOOP_UI.md -> DEVLOOP_UI
PROMPT_NAME_PATTERN: Final[str] = r"PROMPT_(.+)\.md$"

# Pattern for checkbox items: - [ ] or - [x]
CHECKBOX_PATTERN: Final[str] = r"^(\s*)-\s*\[([ xX])\]\s*(.+)$"

# Pattern for agent references: @agent-name:
AGENT_REF_PATTERN: Final[str] = r"@([\w-]+):"

# Priority section headers (both emoji and plain text)
PRIORITY_HEADERS: Final[dict[str, str]] = {
    "RISKY": r"###\s*(?:🔴\s*)?RISKY",
    "CORE": r"###\s*(?:🟡\s*)?CORE",
    "POLISH": r"###\s*(?:🟢\s*)?POLISH",
}

# =============================================================================
# Logging Configuration
# =============================================================================

LOG_LEVEL: Final[str] = os.environ.get("DEVLOOP_LOG_LEVEL", "INFO")
LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE: Final[str] = "devloop_ui.log"


# =============================================================================
# Validation
# =============================================================================

def validate_paths() -> dict[str, bool]:
    """Validate that all required paths exist.

    Returns:
        Dictionary mapping path names to existence status
    """
    return {
        "devloop_base": get_devloop_path().exists(),
        "tasks": get_tasks_path().exists(),
        "progress": get_progress_path().exists(),
        "logs": get_logs_path().exists(),
        "templates": get_templates_path().exists(),
    }


def ensure_paths() -> None:
    """Ensure all required directories exist, creating them if necessary."""
    for path_fn in [get_tasks_path, get_progress_path, get_logs_path, get_ui_logs_path]:
        path = path_fn()
        path.mkdir(parents=True, exist_ok=True)
