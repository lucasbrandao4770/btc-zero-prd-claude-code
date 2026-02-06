"""File browser component for Dev Loop UI.

This module provides file listing and selection components for browsing
PROMPT, PROGRESS, and LOG files.

All file listing functions use @st.cache_data for performance.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from ui.config import (
    CACHE_TTL_SECONDS,
    LOG_PATTERN,
    PROGRESS_PATTERN,
    PROMPT_PATTERN,
    get_logs_path,
    get_progress_path,
    get_tasks_path,
)
from ui.models import TaskStatus
from ui.parser import parse_prompt_file
from ui.state import get_selected_file, get_sort_by, get_sort_order, set_selected_file

# Try to import streamlit for caching
try:
    import streamlit as st

    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

    def cache_data(ttl: int | None = None, show_spinner: bool = False):
        def decorator(func):
            return func
        return decorator

    class DummySt:
        @staticmethod
        def cache_data(ttl: int | None = None, show_spinner: bool = False):
            return cache_data(ttl, show_spinner)

        @staticmethod
        def write(text: str) -> None:
            print(text)

        @staticmethod
        def info(text: str) -> None:
            print(f"INFO: {text}")

        @staticmethod
        def selectbox(label: str, options: list, **kwargs) -> str | None:
            return options[0] if options else None

    st = DummySt()


# =============================================================================
# File Listing Functions (with caching)
# =============================================================================


def _get_dir_mtime(path: Path) -> float:
    """Get directory modification time for cache invalidation."""
    try:
        if path.exists():
            return path.stat().st_mtime
        return 0.0
    except OSError:
        return 0.0


@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def _list_files_cached(directory: str, pattern: str, mtime: float) -> list[str]:
    """List files matching pattern in directory (cached).

    Args:
        directory: Directory path as string
        pattern: Glob pattern to match
        mtime: Directory modification time for cache invalidation

    Returns:
        List of file paths as strings
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        return []
    return [str(p) for p in dir_path.glob(pattern)]


def list_prompt_files() -> list[Path]:
    """List all PROMPT files in the tasks directory.

    Uses @st.cache_data with TTL for performance.

    Returns:
        List of Path objects for PROMPT files
    """
    tasks_path = get_tasks_path()
    mtime = _get_dir_mtime(tasks_path)
    file_strs = _list_files_cached(str(tasks_path), PROMPT_PATTERN, mtime)
    return [Path(f) for f in file_strs]


def list_progress_files() -> list[Path]:
    """List all PROGRESS files in the progress directory.

    Returns:
        List of Path objects for PROGRESS files
    """
    progress_path = get_progress_path()
    mtime = _get_dir_mtime(progress_path)
    file_strs = _list_files_cached(str(progress_path), PROGRESS_PATTERN, mtime)
    return [Path(f) for f in file_strs]


def list_log_files() -> list[Path]:
    """List all LOG files in the logs directory.

    Returns:
        List of Path objects for LOG files
    """
    logs_path = get_logs_path()
    mtime = _get_dir_mtime(logs_path)
    file_strs = _list_files_cached(str(logs_path), LOG_PATTERN, mtime)
    return [Path(f) for f in file_strs]


# =============================================================================
# File Metadata
# =============================================================================


def get_file_info(path: Path) -> dict:
    """Get metadata for a file.

    Args:
        path: Path to the file

    Returns:
        Dictionary with file metadata
    """
    stat = path.stat()
    return {
        "name": path.stem,
        "path": path,
        "size": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime),
        "modified_ts": stat.st_mtime,
    }


def get_prompt_info(path: Path) -> dict:
    """Get metadata for a PROMPT file including parsed data.

    Args:
        path: Path to the PROMPT file

    Returns:
        Dictionary with file and parsed metadata
    """
    info = get_file_info(path)
    result = parse_prompt_file(path)

    if result.is_success:
        prompt = result.value
        info.update({
            "status": prompt.status,
            "quality_tier": prompt.quality_tier,
            "task_count": prompt.task_count,
            "completed_count": prompt.completed_count,
            "completion_pct": prompt.completion_percentage,
            "goal": prompt.goal[:100] + "..." if len(prompt.goal) > 100 else prompt.goal,
            "parse_success": True,
        })
    else:
        info.update({
            "status": TaskStatus.NOT_STARTED,
            "quality_tier": None,
            "task_count": 0,
            "completed_count": 0,
            "completion_pct": 0.0,
            "goal": "",
            "parse_success": False,
            "parse_error": result.error,
        })

    return info


# =============================================================================
# Sorting
# =============================================================================


def sort_files(files: list[dict], sort_by: str = "date", ascending: bool = False) -> list[dict]:
    """Sort file info dictionaries.

    Args:
        files: List of file info dictionaries
        sort_by: Field to sort by (name, date, status, completion)
        ascending: Whether to sort ascending

    Returns:
        Sorted list of file info dictionaries
    """
    sort_keys = {
        "name": lambda x: x.get("name", "").lower(),
        "date": lambda x: x.get("modified_ts", 0),
        "status": lambda x: x.get("status", TaskStatus.NOT_STARTED).value,
        "completion": lambda x: x.get("completion_pct", 0),
    }

    key_func = sort_keys.get(sort_by, sort_keys["date"])
    return sorted(files, key=key_func, reverse=not ascending)


# =============================================================================
# Filtering
# =============================================================================


def filter_files(
    files: list[dict],
    status_filter: list[str] | None = None,
    tier_filter: list[str] | None = None,
    search_query: str = "",
) -> list[dict]:
    """Filter file info dictionaries.

    Args:
        files: List of file info dictionaries
        status_filter: List of status values to include (empty = all)
        tier_filter: List of tier values to include (empty = all)
        search_query: Text to search for in name/goal

    Returns:
        Filtered list of file info dictionaries
    """
    result = files

    # Filter by status
    if status_filter:
        result = [
            f for f in result
            if str(f.get("status", "")).upper() in [s.upper() for s in status_filter]
        ]

    # Filter by tier
    if tier_filter:
        result = [
            f for f in result
            if f.get("quality_tier") and str(f["quality_tier"].value).lower() in [
                t.lower() for t in tier_filter
            ]
        ]

    # Filter by search query
    if search_query:
        query = search_query.lower()
        result = [
            f for f in result
            if query in f.get("name", "").lower() or query in f.get("goal", "").lower()
        ]

    return result


# =============================================================================
# Streamlit Components
# =============================================================================


def render_file_list(
    files: list[Path],
    file_type: str = "prompt",
    on_select: Callable[[Path], None] | None = None,
) -> Path | None:
    """Render a list of files as a selectable list.

    Args:
        files: List of file paths to display
        file_type: Type of files (prompt, progress, log)
        on_select: Callback when file is selected

    Returns:
        Selected file path or None
    """
    if not HAS_STREAMLIT:
        return files[0] if files else None

    if not files:
        st.info(f"No {file_type.upper()} files found.")
        return None

    # Get file info for display
    file_infos = []
    for path in files:
        info = get_prompt_info(path) if file_type == "prompt" else get_file_info(path)
        file_infos.append(info)

    # Sort files
    sort_by = get_sort_by()
    ascending = get_sort_order() == "asc"
    file_infos = sort_files(file_infos, sort_by, ascending)

    # Create selectbox options
    options = [f["name"] for f in file_infos]
    path_map = {f["name"]: f["path"] for f in file_infos}

    # Get current selection
    current = get_selected_file()
    current_name = current.stem if current else None
    default_index = options.index(current_name) if current_name in options else 0

    # Render selectbox
    selected_name = st.selectbox(
        f"Select {file_type.title()}",
        options,
        index=default_index,
        key=f"file_browser_{file_type}",
    )

    if selected_name:
        selected_path = path_map[selected_name]
        set_selected_file(selected_path, file_type)

        if on_select:
            on_select(selected_path)

        return selected_path

    return None


def render_file_browser(
    files: list[Path],
    on_select: Callable[[Path], None] | None = None,
) -> Path | None:
    """Render the main file browser component.

    This is a convenience wrapper around render_file_list for PROMPT files.

    Args:
        files: List of PROMPT file paths
        on_select: Callback when file is selected

    Returns:
        Selected file path or None
    """
    return render_file_list(files, file_type="prompt", on_select=on_select)


def render_empty_state(file_type: str = "prompt") -> None:
    """Render a friendly empty state message.

    Args:
        file_type: Type of files (prompt, progress, log)
    """
    if not HAS_STREAMLIT:
        print(f"No {file_type} files found.")
        return

    messages = {
        "prompt": "No PROMPT files found. Create your first one!",
        "progress": "No active sessions. Start a Dev Loop to see progress here.",
        "log": "No execution logs yet.",
    }

    st.info(messages.get(file_type, f"No {file_type} files found."))
