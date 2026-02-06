"""Session state management for Dev Loop UI.

This module provides centralized session state management for the Streamlit
application. All user preferences and UI state are stored in st.session_state
for persistence across reruns.

Usage:
    # At app startup
    init_session_state()

    # Get/set values
    selected = get_state("selected_file")
    set_state("selected_file", "/path/to/file.md")

    # Reset filters
    reset_filters()
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

# Try to import streamlit, but allow module to work without it for testing
try:
    import streamlit as st

    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    # Create a mock session_state for testing
    _mock_session_state: dict[str, Any] = {}

    class MockSessionState(dict[str, Any]):
        """Mock session state that behaves like st.session_state."""

        def __init__(self) -> None:
            super().__init__()
            self.update(_mock_session_state)

        def __getattr__(self, key: str) -> Any:
            return self.get(key)

        def __setattr__(self, key: str, value: Any) -> None:
            self[key] = value
            _mock_session_state[key] = value

    class MockSt:
        session_state: MockSessionState = MockSessionState()

    st = MockSt()  # type: ignore[assignment]


# =============================================================================
# State Keys
# =============================================================================

# File selection
KEY_SELECTED_FILE = "selected_file"
KEY_SELECTED_FILE_TYPE = "selected_file_type"  # prompt, progress, log

# Filtering
KEY_FILTER_STATUS = "filter_status"
KEY_FILTER_TIER = "filter_tier"
KEY_SEARCH_QUERY = "search_query"

# Sorting
KEY_SORT_BY = "sort_by"
KEY_SORT_ORDER = "sort_order"

# UI preferences
KEY_THEME = "theme"
KEY_SIDEBAR_EXPANDED = "sidebar_expanded"
KEY_SHOW_RAW_CONTENT = "show_raw_content"

# Page-specific
KEY_TASKS_PAGE_TAB = "tasks_page_tab"
KEY_PROGRESS_PAGE_TAB = "progress_page_tab"
KEY_LOGS_DATE_RANGE = "logs_date_range"

# Create form state
KEY_CREATE_NAME = "create_name"
KEY_CREATE_GOAL = "create_goal"
KEY_CREATE_TIER = "create_tier"
KEY_CREATE_TASKS = "create_tasks"


# =============================================================================
# Default Values
# =============================================================================

DEFAULTS: dict[str, Any] = {
    # File selection
    KEY_SELECTED_FILE: None,
    KEY_SELECTED_FILE_TYPE: "prompt",
    # Filtering
    KEY_FILTER_STATUS: [],  # Empty list = show all
    KEY_FILTER_TIER: [],  # Empty list = show all
    KEY_SEARCH_QUERY: "",
    # Sorting
    KEY_SORT_BY: "date",  # name, date, status, completion
    KEY_SORT_ORDER: "desc",  # asc, desc
    # UI preferences
    KEY_THEME: "light",  # light, dark
    KEY_SIDEBAR_EXPANDED: True,
    KEY_SHOW_RAW_CONTENT: False,
    # Page-specific
    KEY_TASKS_PAGE_TAB: "overview",
    KEY_PROGRESS_PAGE_TAB: "timeline",
    KEY_LOGS_DATE_RANGE: None,
    # Create form
    KEY_CREATE_NAME: "",
    KEY_CREATE_GOAL: "",
    KEY_CREATE_TIER: "production",
    KEY_CREATE_TASKS: [],
}


# =============================================================================
# Initialization
# =============================================================================


def init_session_state() -> None:
    """Initialize all session state values with defaults.

    Call this at the start of app.py to ensure all state keys exist.
    Only sets values that don't already exist (preserves existing state).
    """
    for key, default in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default


def reset_session_state() -> None:
    """Reset all session state to default values.

    Use this for a "fresh start" option.
    """
    for key, default in DEFAULTS.items():
        st.session_state[key] = default


# =============================================================================
# Getters and Setters
# =============================================================================


def get_state(key: str, default: Any = None) -> Any:
    """Get a value from session state.

    Args:
        key: The state key to retrieve
        default: Default value if key doesn't exist

    Returns:
        The stored value or default
    """
    if key in DEFAULTS and default is None:
        default = DEFAULTS[key]
    return st.session_state.get(key, default)


def set_state(key: str, value: Any) -> None:
    """Set a value in session state.

    Args:
        key: The state key to set
        value: The value to store
    """
    st.session_state[key] = value


def has_state(key: str) -> bool:
    """Check if a key exists in session state.

    Args:
        key: The state key to check

    Returns:
        True if the key exists
    """
    return key in st.session_state


# =============================================================================
# File Selection
# =============================================================================


def get_selected_file() -> Path | None:
    """Get the currently selected file path."""
    path_str = get_state(KEY_SELECTED_FILE)
    return Path(path_str) if path_str else None


def set_selected_file(path: Path | None, file_type: str = "prompt") -> None:
    """Set the currently selected file.

    Args:
        path: Path to the selected file, or None to clear
        file_type: Type of file (prompt, progress, log)
    """
    set_state(KEY_SELECTED_FILE, str(path) if path else None)
    set_state(KEY_SELECTED_FILE_TYPE, file_type)


def clear_selected_file() -> None:
    """Clear the file selection."""
    set_state(KEY_SELECTED_FILE, None)
    set_state(KEY_SELECTED_FILE_TYPE, "prompt")


# =============================================================================
# Filtering
# =============================================================================


def get_filter_status() -> list[str]:
    """Get the current status filter list."""
    return get_state(KEY_FILTER_STATUS, [])


def set_filter_status(statuses: list[str]) -> None:
    """Set the status filter.

    Args:
        statuses: List of status values to show (empty = all)
    """
    set_state(KEY_FILTER_STATUS, statuses)


def get_filter_tier() -> list[str]:
    """Get the current quality tier filter list."""
    return get_state(KEY_FILTER_TIER, [])


def set_filter_tier(tiers: list[str]) -> None:
    """Set the quality tier filter.

    Args:
        tiers: List of tier values to show (empty = all)
    """
    set_state(KEY_FILTER_TIER, tiers)


def get_search_query() -> str:
    """Get the current search query."""
    return get_state(KEY_SEARCH_QUERY, "")


def set_search_query(query: str) -> None:
    """Set the search query.

    Args:
        query: Search text to filter by
    """
    set_state(KEY_SEARCH_QUERY, query)


def reset_filters() -> None:
    """Reset all filters to their default values."""
    set_state(KEY_FILTER_STATUS, [])
    set_state(KEY_FILTER_TIER, [])
    set_state(KEY_SEARCH_QUERY, "")
    set_state(KEY_SORT_BY, "date")
    set_state(KEY_SORT_ORDER, "desc")


def has_active_filters() -> bool:
    """Check if any filters are currently active."""
    return bool(
        get_filter_status()
        or get_filter_tier()
        or get_search_query()
    )


# =============================================================================
# Sorting
# =============================================================================


def get_sort_by() -> str:
    """Get the current sort field."""
    return get_state(KEY_SORT_BY, "date")


def set_sort_by(field: str) -> None:
    """Set the sort field.

    Args:
        field: Field to sort by (name, date, status, completion)
    """
    valid_fields = ["name", "date", "status", "completion"]
    if field in valid_fields:
        set_state(KEY_SORT_BY, field)


def get_sort_order() -> str:
    """Get the current sort order."""
    return get_state(KEY_SORT_ORDER, "desc")


def set_sort_order(order: str) -> None:
    """Set the sort order.

    Args:
        order: Sort order (asc, desc)
    """
    if order in ["asc", "desc"]:
        set_state(KEY_SORT_ORDER, order)


def toggle_sort_order() -> None:
    """Toggle between ascending and descending sort order."""
    current = get_sort_order()
    set_sort_order("asc" if current == "desc" else "desc")


# =============================================================================
# UI Preferences
# =============================================================================


def get_theme() -> str:
    """Get the current theme preference."""
    return get_state(KEY_THEME, "light")


def set_theme(theme: str) -> None:
    """Set the theme preference.

    Args:
        theme: Theme name (light, dark)
    """
    if theme in ["light", "dark"]:
        set_state(KEY_THEME, theme)


def toggle_theme() -> None:
    """Toggle between light and dark theme."""
    current = get_theme()
    set_theme("dark" if current == "light" else "light")


def is_dark_theme() -> bool:
    """Check if dark theme is active."""
    return get_theme() == "dark"


def get_show_raw_content() -> bool:
    """Check if raw content view is enabled."""
    return get_state(KEY_SHOW_RAW_CONTENT, False)


def set_show_raw_content(show: bool) -> None:
    """Set whether to show raw content view."""
    set_state(KEY_SHOW_RAW_CONTENT, show)


# =============================================================================
# Create Form State
# =============================================================================


def get_create_form_data() -> dict[str, Any]:
    """Get all create form field values."""
    return {
        "name": get_state(KEY_CREATE_NAME, ""),
        "goal": get_state(KEY_CREATE_GOAL, ""),
        "tier": get_state(KEY_CREATE_TIER, "production"),
        "tasks": get_state(KEY_CREATE_TASKS, []),
    }


def set_create_form_data(data: dict[str, Any]) -> None:
    """Set create form field values.

    Args:
        data: Dictionary with name, goal, tier, tasks
    """
    if "name" in data:
        set_state(KEY_CREATE_NAME, data["name"])
    if "goal" in data:
        set_state(KEY_CREATE_GOAL, data["goal"])
    if "tier" in data:
        set_state(KEY_CREATE_TIER, data["tier"])
    if "tasks" in data:
        set_state(KEY_CREATE_TASKS, data["tasks"])


def reset_create_form() -> None:
    """Reset create form to default values."""
    set_state(KEY_CREATE_NAME, "")
    set_state(KEY_CREATE_GOAL, "")
    set_state(KEY_CREATE_TIER, "production")
    set_state(KEY_CREATE_TASKS, [])
