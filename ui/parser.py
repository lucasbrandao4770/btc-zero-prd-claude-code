"""Markdown parser for Dev Loop files with caching.

This module provides parsing functions for PROMPT, PROGRESS, and LOG files.
All functions return ParseResult[T] for error handling instead of raising
exceptions.

Caching Strategy:
- All file reading functions use @st.cache_data with TTL from config
- Cache invalidation happens on explicit refresh or TTL expiry
- File modification time (mtime) is checked to detect changes

Example:
    result = parse_prompt_file(path)
    if result.is_success:
        prompt = result.value
    else:
        st.error(result.error)
"""

from __future__ import annotations

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import frontmatter

# Configure logger
logger = logging.getLogger("devloop_ui.parser")

from ui.config import (
    AGENT_REF_PATTERN,
    CACHE_TTL_SECONDS,
    CHECKBOX_PATTERN,
    PROMPT_NAME_PATTERN,
)
from ui.models import (
    Blocker,
    ExecutionStatistics,
    ExitCriterion,
    IterationLogEntry,
    LogFile,
    ParseResult,
    ProgressFile,
    PromptConfig,
    PromptFile,
    QualityTier,
    Task,
    TaskPriority,
    TaskStatus,
)

if TYPE_CHECKING:
    pass

# Try to import streamlit for caching, but make module work without it for testing
try:
    import streamlit as st

    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    # Create a dummy cache_data decorator for testing
    def cache_data(ttl: int | None = None, show_spinner: bool = False):
        def decorator(func):
            return func
        return decorator
    # Create a dummy st module
    class DummySt:
        @staticmethod
        def cache_data(ttl: int | None = None, show_spinner: bool = False):
            return cache_data(ttl, show_spinner)
    st = DummySt()


# =============================================================================
# File Reading with Caching
# =============================================================================


def _get_file_mtime(path: Path) -> float:
    """Get file modification time for cache invalidation."""
    try:
        return path.stat().st_mtime
    except OSError:
        return 0.0


@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def _read_file_cached(path_str: str, mtime: float) -> str:
    """Read file content with caching.

    Args:
        path_str: String path (for cache key serialization)
        mtime: File modification time (for cache invalidation)

    Returns:
        File content as string
    """
    path = Path(path_str)
    return path.read_text(encoding="utf-8")


def read_file(path: Path) -> ParseResult[str]:
    """Read a file with caching and error handling.

    Args:
        path: Path to the file

    Returns:
        ParseResult containing file content or error
    """
    try:
        logger.debug(f"Reading file: {path}")
        if not path.exists():
            logger.warning(f"File not found: {path}")
            return ParseResult.failure(f"File not found: {path}")
        if not path.is_file():
            logger.warning(f"Path is not a file: {path}")
            return ParseResult.failure(f"Not a file: {path}")

        mtime = _get_file_mtime(path)
        content = _read_file_cached(str(path), mtime)
        logger.debug(f"Successfully read {len(content)} bytes from {path.name}")
        return ParseResult.success(content)
    except PermissionError:
        return ParseResult.failure(f"Permission denied: {path}")
    except UnicodeDecodeError as e:
        return ParseResult.failure(f"Failed to decode file {path}: {e}")
    except Exception as e:
        return ParseResult.failure(f"Failed to read file {path}: {e}")


# =============================================================================
# Frontmatter Parsing
# =============================================================================


def _parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content.

    Args:
        content: Raw markdown content

    Returns:
        Tuple of (metadata dict, content without frontmatter)
    """
    try:
        post = frontmatter.loads(content)
        return dict(post.metadata), post.content
    except Exception:
        # No frontmatter or invalid - return empty metadata
        return {}, content


# =============================================================================
# Section Extraction
# =============================================================================


def _extract_section(content: str, header: str, level: int = 2) -> str | None:
    """Extract content of a markdown section.

    Args:
        content: Markdown content
        header: Section header text (without #)
        level: Header level (default 2 for ##)

    Returns:
        Section content or None if not found
    """
    prefix = "#" * level
    pattern = rf"^{prefix}\s+{re.escape(header)}\s*$"
    lines = content.split("\n")

    start_idx = None
    for i, line in enumerate(lines):
        if re.match(pattern, line, re.IGNORECASE):
            start_idx = i + 1
            break

    if start_idx is None:
        return None

    # Find the end of the section (next header of same or higher level)
    end_idx = len(lines)
    for i in range(start_idx, len(lines)):
        if re.match(rf"^#{{{1},{level}}}\s+", lines[i]):
            end_idx = i
            break

    return "\n".join(lines[start_idx:end_idx]).strip()


def _extract_table_rows(content: str) -> list[dict[str, str]]:
    """Extract rows from a markdown table.

    Args:
        content: Content containing a markdown table

    Returns:
        List of dicts mapping header names to cell values
    """
    lines = [line.strip() for line in content.split("\n") if line.strip()]

    # Find table start (line with |)
    table_lines = [ln for ln in lines if "|" in ln]
    if len(table_lines) < 3:  # Need header, separator, at least one row
        return []

    # Parse header
    header_line = table_lines[0]
    headers = [h.strip() for h in header_line.split("|") if h.strip()]

    # Skip separator line and parse data rows
    rows = []
    for line in table_lines[2:]:
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if len(cells) >= len(headers):
            row = {headers[i]: cells[i] for i in range(len(headers))}
            rows.append(row)

    return rows


# =============================================================================
# Task Parsing
# =============================================================================


def _parse_tasks(content: str) -> list[Task]:
    """Parse tasks from markdown content.

    Supports both emoji and plain text priority headers:
    - ### RISKY or ### RISKY (Do First)
    - ### CORE
    - ### POLISH or ### POLISH (Do Last)

    Args:
        content: Markdown content containing task sections

    Returns:
        List of Task objects
    """
    tasks = []
    current_priority: TaskPriority | None = None
    checkbox_re = re.compile(CHECKBOX_PATTERN, re.MULTILINE)
    agent_re = re.compile(AGENT_REF_PATTERN)

    lines = content.split("\n")
    for line_num, line in enumerate(lines, 1):
        # Check for priority headers
        line_lower = line.lower()
        if "###" in line:
            if "risky" in line_lower:
                current_priority = TaskPriority.RISKY
                continue
            elif "core" in line_lower:
                current_priority = TaskPriority.CORE
                continue
            elif "polish" in line_lower:
                current_priority = TaskPriority.POLISH
                continue

        # Parse checkbox items
        match = checkbox_re.match(line)
        if match and current_priority:
            checkbox_mark = match.group(2).lower()
            completed = checkbox_mark == "x"
            description = match.group(3).strip()

            # Extract agent reference
            agent_ref = None
            agent_match = agent_re.search(description)
            if agent_match:
                agent_ref = agent_match.group(1)
                # Remove agent ref from description
                description = agent_re.sub("", description).strip()

            # Clean up description (remove leading ** for bold)
            description = re.sub(r"^\*\*(.+?)\*\*", r"\1", description)

            tasks.append(
                Task(
                    description=description,
                    priority=current_priority,
                    completed=completed,
                    agent_ref=agent_ref,
                    line_number=line_num,
                )
            )

    return tasks


# =============================================================================
# PROMPT File Parsing
# =============================================================================


@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def _parse_prompt_content(content: str, path_str: str, _mtime: float) -> dict:
    """Parse PROMPT file content (cached internal function).

    Args:
        content: Raw file content
        path_str: File path as string (for cache key)
        mtime: Modification time (for cache invalidation)

    Returns:
        Dictionary with parsed data
    """
    path = Path(path_str)
    _metadata, body = _parse_frontmatter(content)

    # Extract name from filename or markdown title
    name_match = re.search(PROMPT_NAME_PATTERN, path.name)
    if name_match:
        name = name_match.group(1)
    else:
        # Try to extract from markdown title: # PROMPT: NAME
        title_match = re.search(r"#\s*PROMPT:\s*(\w+)", content)
        name = title_match.group(1) if title_match else path.stem

    # Parse goal
    goal_section = _extract_section(body, "Goal")
    goal = goal_section.strip() if goal_section else ""

    # Parse quality tier - check for explicit **Tier:** marker first
    tier_section = _extract_section(body, "Quality Tier")
    quality_tier = QualityTier.PRODUCTION
    if tier_section:
        # Look for explicit tier declaration: **Tier:** production
        tier_match = re.search(r"\*\*Tier:\*\*\s*(\w+)", tier_section)
        if tier_match:
            tier_value = tier_match.group(1).lower()
            if tier_value == "prototype":
                quality_tier = QualityTier.PROTOTYPE
            elif tier_value == "library":
                quality_tier = QualityTier.LIBRARY
            elif tier_value == "production":
                quality_tier = QualityTier.PRODUCTION

    # Parse tasks from Tasks section
    tasks_section = _extract_section(body, "Tasks") or _extract_section(body, "Tasks (Prioritized)")
    tasks = _parse_tasks(tasks_section) if tasks_section else []

    # Parse exit criteria
    exit_section = _extract_section(body, "Exit Criteria")
    exit_criteria = []
    if exit_section:
        for line in exit_section.split("\n"):
            match = re.match(r"^\s*-\s*\[([ xX])\]\s*(.+)$", line)
            if match:
                met = match.group(1).lower() == "x"
                description = match.group(2).strip()
                exit_criteria.append(ExitCriterion(description=description, met=met))

    # Parse status from Progress section
    progress_section = _extract_section(body, "Progress")
    status = TaskStatus.NOT_STARTED
    if progress_section:
        status_match = re.search(r"\*\*Status:\*\*\s*(\w+)", progress_section)
        if status_match:
            status_str = status_match.group(1).upper()
            try:
                status = TaskStatus(status_str)
            except ValueError:
                pass

    # Parse config
    config_section = _extract_section(body, "Config")
    config = PromptConfig()
    if config_section:
        # Extract YAML-like values
        mode_match = re.search(r"mode:\s*(\w+)", config_section)
        if mode_match:
            config = PromptConfig(mode=mode_match.group(1))

        max_iter_match = re.search(r"max_iterations:\s*(\d+)", config_section)
        if max_iter_match:
            config.max_iterations = int(max_iter_match.group(1))

    return {
        "name": name,
        "goal": goal,
        "quality_tier": quality_tier,
        "tasks": [t.model_dump() for t in tasks],
        "exit_criteria": [e.model_dump() for e in exit_criteria],
        "status": status,
        "config": config.model_dump(),
        "raw_content": content,
    }


def parse_prompt_file(path: Path) -> ParseResult[PromptFile]:
    """Parse a PROMPT_*.md file.

    This function uses @st.cache_data for caching with TTL from config.
    Cache is invalidated when file modification time changes.

    Args:
        path: Path to the PROMPT file

    Returns:
        ParseResult containing PromptFile or error message
    """
    try:
        logger.info(f"Parsing PROMPT file: {path.name}")
        # Read file with caching
        read_result = read_file(path)
        if read_result.is_failure:
            logger.error(f"Failed to read PROMPT file: {read_result.error}")
            return ParseResult.failure(read_result.error)

        content = read_result.value
        mtime = _get_file_mtime(path)

        # Parse content (cached)
        data = _parse_prompt_content(content, str(path), mtime)

        # Reconstruct tasks from dicts
        tasks = [Task(**t) for t in data["tasks"]]
        exit_criteria = [ExitCriterion(**e) for e in data["exit_criteria"]]
        config = PromptConfig(**data["config"])

        prompt = PromptFile(
            name=data["name"],
            file_path=path,
            goal=data["goal"],
            quality_tier=data["quality_tier"],
            tasks=tasks,
            exit_criteria=exit_criteria,
            status=data["status"],
            config=config,
            raw_content=data["raw_content"],
        )

        logger.info(f"Successfully parsed PROMPT: {prompt.name} ({len(tasks)} tasks)")
        return ParseResult.success(prompt)

    except Exception as e:
        logger.exception(f"Failed to parse PROMPT file {path.name}")
        return ParseResult.failure(f"Failed to parse PROMPT file {path.name}: {e}")


# =============================================================================
# PROGRESS File Parsing
# =============================================================================


@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def _parse_progress_content(content: str, path_str: str, _mtime: float) -> dict:
    """Parse PROGRESS file content (cached internal function)."""
    path = Path(path_str)
    _metadata, body = _parse_frontmatter(content)

    # Extract name from filename or markdown title
    name_match = re.search(r"PROGRESS_(.+)\.md$", path.name)
    if name_match:
        name = name_match.group(1)
    else:
        # Try to extract from markdown title: # PROGRESS: NAME
        title_match = re.search(r"#\s*PROGRESS:\s*(\w+)", content)
        name = title_match.group(1) if title_match else path.stem

    # Parse summary table
    summary_section = _extract_section(body, "Summary")
    tasks_completed = 0
    total_tasks = 0
    current_iteration = 0
    status = TaskStatus.NOT_STARTED
    started = None
    last_updated = None

    if summary_section:
        rows = _extract_table_rows(summary_section)
        for row in rows:
            metric = row.get("Metric", row.get("**Metric**", "")).replace("**", "")
            value = row.get("Value", row.get("**Value**", "")).replace("**", "")

            if "Status" in metric:
                try:
                    status = TaskStatus(value)
                except ValueError:
                    pass
            elif "Tasks Completed" in metric:
                match = re.match(r"(\d+)\s*/\s*(\d+)", value)
                if match:
                    tasks_completed = int(match.group(1))
                    total_tasks = int(match.group(2))
            elif "Current Iteration" in metric:
                try:
                    current_iteration = int(value)
                except ValueError:
                    pass
            elif "Started" in metric:
                try:
                    started = datetime.fromisoformat(value.replace("Z", "+00:00"))
                except ValueError:
                    pass
            elif "Last Updated" in metric:
                try:
                    last_updated = datetime.fromisoformat(value.replace("Z", "+00:00"))
                except ValueError:
                    pass

    # Parse iteration log
    iteration_log = []
    log_section = _extract_section(body, "Iteration Log")
    if log_section:
        # Split by ### Iteration headers
        iteration_blocks = re.split(r"###\s+Iteration\s+(\d+)", log_section)
        for i in range(1, len(iteration_blocks), 2):
            if i + 1 < len(iteration_blocks):
                iter_num = int(iteration_blocks[i])
                block = iteration_blocks[i + 1]

                entry = IterationLogEntry(iteration=iter_num)

                # Parse fields
                task_match = re.search(r"\*\*Task:\*\*\s*(.+)", block)
                if task_match:
                    entry.task = task_match.group(1).strip()

                status_match = re.search(r"\*\*Status:\*\*\s*(\w+)", block)
                if status_match:
                    entry.status = status_match.group(1).strip()

                iteration_log.append(entry)

    # Parse blockers
    blockers = []
    blocker_section = _extract_section(body, "Blockers")
    if blocker_section:
        rows = _extract_table_rows(blocker_section)
        for row in rows:
            desc = row.get("Blocker", "")
            if desc and desc != "-":
                iter_str = row.get("Iteration", "")
                resolution = row.get("Resolution", "")
                try:
                    iter_num = int(iter_str) if iter_str and iter_str != "-" else None
                except ValueError:
                    iter_num = None
                blockers.append(
                    Blocker(
                        description=desc,
                        iteration=iter_num,
                        resolution=resolution if resolution != "-" else None,
                    )
                )

    return {
        "name": name,
        "status": status,
        "tasks_completed": tasks_completed,
        "total_tasks": total_tasks,
        "current_iteration": current_iteration,
        "started": started.isoformat() if started else None,
        "last_updated": last_updated.isoformat() if last_updated else None,
        "iteration_log": [e.model_dump() for e in iteration_log],
        "blockers": [b.model_dump() for b in blockers],
        "raw_content": content,
    }


def parse_progress_file(path: Path) -> ParseResult[ProgressFile]:
    """Parse a PROGRESS_*.md file.

    This function uses @st.cache_data for caching with TTL from config.

    Args:
        path: Path to the PROGRESS file

    Returns:
        ParseResult containing ProgressFile or error message
    """
    try:
        read_result = read_file(path)
        if read_result.is_failure:
            return ParseResult.failure(read_result.error)

        content = read_result.value
        mtime = _get_file_mtime(path)

        data = _parse_progress_content(content, str(path), mtime)

        # Reconstruct objects
        iteration_log = [IterationLogEntry(**e) for e in data["iteration_log"]]
        blockers = [Blocker(**b) for b in data["blockers"]]

        started = datetime.fromisoformat(data["started"]) if data["started"] else None
        last_updated = (
            datetime.fromisoformat(data["last_updated"]) if data["last_updated"] else None
        )

        progress = ProgressFile(
            name=data["name"],
            file_path=path,
            status=data["status"],
            tasks_completed=data["tasks_completed"],
            total_tasks=data["total_tasks"],
            current_iteration=data["current_iteration"],
            started=started,
            last_updated=last_updated,
            iteration_log=iteration_log,
            blockers=blockers,
            raw_content=data["raw_content"],
        )

        return ParseResult.success(progress)

    except Exception as e:
        return ParseResult.failure(f"Failed to parse PROGRESS file {path.name}: {e}")


# =============================================================================
# LOG File Parsing
# =============================================================================


@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def _parse_log_content(content: str, path_str: str, _mtime: float) -> dict:
    """Parse LOG file content (cached internal function)."""
    path = Path(path_str)
    _metadata, body = _parse_frontmatter(content)

    # Extract name from filename
    name_match = re.search(r"LOG_(.+?)_\d{8}", path.name)
    name = name_match.group(1) if name_match else path.stem

    # Parse execution summary
    summary_section = _extract_section(body, "Execution Summary")
    prompt_name = ""
    started = None
    completed = None
    exit_reason = ""
    mode = "hitl"
    quality_tier = QualityTier.PRODUCTION

    if summary_section:
        rows = _extract_table_rows(summary_section)
        for row in rows:
            metric = row.get("Metric", "").replace("**", "")
            value = row.get("Value", "").replace("**", "")

            if "PROMPT" in metric:
                prompt_match = re.search(r"PROMPT_(\w+)", value)
                if prompt_match:
                    prompt_name = prompt_match.group(1)
            elif "Started" in metric:
                try:
                    started = datetime.fromisoformat(value.replace("Z", "+00:00"))
                except ValueError:
                    pass
            elif "Completed" in metric:
                try:
                    completed = datetime.fromisoformat(value.replace("Z", "+00:00"))
                except ValueError:
                    pass
            elif "Exit Reason" in metric:
                exit_reason = value
            elif "Mode" in metric:
                mode = value.lower()
            elif "Quality Tier" in metric:
                try:
                    quality_tier = QualityTier(value.lower())
                except ValueError:
                    pass

    # Parse statistics
    stats_section = _extract_section(body, "Statistics")
    statistics = ExecutionStatistics()
    if stats_section:
        total_match = re.search(r"Total Tasks:\s*(\d+)", stats_section)
        passed_match = re.search(r"Passed:\s*(\d+)", stats_section)
        failed_match = re.search(r"Failed:\s*(\d+)", stats_section)
        skipped_match = re.search(r"Skipped:\s*(\d+)", stats_section)
        iterations_match = re.search(r"Total Iterations:\s*(\d+)", stats_section)

        statistics = ExecutionStatistics(
            total_tasks=int(total_match.group(1)) if total_match else 0,
            passed=int(passed_match.group(1)) if passed_match else 0,
            failed=int(failed_match.group(1)) if failed_match else 0,
            skipped=int(skipped_match.group(1)) if skipped_match else 0,
            total_iterations=int(iterations_match.group(1)) if iterations_match else 0,
        )

    # Parse key decisions (list items under ## Key Decisions)
    key_decisions: list[str] = []
    decisions_section = _extract_section(body, "Key Decisions")
    if decisions_section:
        for line in decisions_section.split("\n"):
            # Match markdown list items: - item or * item
            match = re.match(r"^\s*[-*]\s+(.+)$", line)
            if match:
                key_decisions.append(match.group(1).strip())

    # Parse files changed (list items under ## Files Changed or ## Files Created/Modified)
    files_changed: list[str] = []
    files_section = _extract_section(body, "Files Changed") or _extract_section(
        body, "Files Created/Modified"
    )
    if files_section:
        for line in files_section.split("\n"):
            # Match markdown list items, often with backticks: - `path/to/file.py`
            match = re.match(r"^\s*[-*]\s+`?([^`]+)`?$", line)
            if match:
                files_changed.append(match.group(1).strip())

    return {
        "name": name,
        "prompt_name": prompt_name,
        "started": started.isoformat() if started else None,
        "completed": completed.isoformat() if completed else None,
        "exit_reason": exit_reason,
        "mode": mode,
        "quality_tier": quality_tier,
        "statistics": statistics.model_dump(),
        "key_decisions": key_decisions,
        "files_changed": files_changed,
        "raw_content": content,
    }


def parse_log_file(path: Path) -> ParseResult[LogFile]:
    """Parse a LOG_*.md file.

    This function uses @st.cache_data for caching with TTL from config.

    Args:
        path: Path to the LOG file

    Returns:
        ParseResult containing LogFile or error message
    """
    try:
        read_result = read_file(path)
        if read_result.is_failure:
            return ParseResult.failure(read_result.error)

        content = read_result.value
        mtime = _get_file_mtime(path)

        data = _parse_log_content(content, str(path), mtime)

        started = datetime.fromisoformat(data["started"]) if data["started"] else None
        completed = datetime.fromisoformat(data["completed"]) if data["completed"] else None
        statistics = ExecutionStatistics(**data["statistics"])

        log = LogFile(
            name=data["name"],
            file_path=path,
            prompt_name=data["prompt_name"],
            started=started,
            completed=completed,
            exit_reason=data["exit_reason"],
            mode=data["mode"],
            quality_tier=data["quality_tier"],
            statistics=statistics,
            key_decisions=data["key_decisions"],
            files_changed=data["files_changed"],
            raw_content=data["raw_content"],
        )

        return ParseResult.success(log)

    except Exception as e:
        return ParseResult.failure(f"Failed to parse LOG file {path.name}: {e}")


# =============================================================================
# Utility Functions
# =============================================================================


def clear_parser_cache() -> None:
    """Clear all parser caches.

    Call this when files have been modified externally and need to be re-read.
    """
    if HAS_STREAMLIT:
        # Access the clear method on the actual streamlit cache_data decorator
        import streamlit
        streamlit.cache_data.clear()
