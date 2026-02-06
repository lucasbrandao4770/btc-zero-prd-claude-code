"""Status badges component for Dev Loop UI.

This module provides styled badge components for displaying status,
priority, and completion indicators.

All badges return HTML strings that can be rendered with st.markdown(unsafe_allow_html=True).
"""

from __future__ import annotations

# =============================================================================
# Color Constants
# =============================================================================

# Status colors
STATUS_COLORS = {
    "NOT_STARTED": {"bg": "#6c757d", "text": "#ffffff"},  # Gray
    "IN_PROGRESS": {"bg": "#0d6efd", "text": "#ffffff"},  # Blue
    "BLOCKED": {"bg": "#dc3545", "text": "#ffffff"},      # Red
    "COMPLETE": {"bg": "#198754", "text": "#ffffff"},     # Green
}

# Priority colors
PRIORITY_COLORS = {
    "RISKY": {"bg": "#dc3545", "text": "#ffffff"},    # Red
    "CORE": {"bg": "#ffc107", "text": "#212529"},     # Yellow
    "POLISH": {"bg": "#198754", "text": "#ffffff"},   # Green
}

# Default badge style (single line to avoid rendering issues)
DEFAULT_BADGE_STYLE = "display: inline-block; padding: 0.25em 0.6em; font-size: 0.85em; font-weight: 600; line-height: 1; text-align: center; white-space: nowrap; vertical-align: baseline; border-radius: 0.375rem;"


# =============================================================================
# Badge Generators
# =============================================================================


def render_status_badge(status: str) -> str:
    """Render a status badge as HTML.

    Args:
        status: Status value (NOT_STARTED, IN_PROGRESS, BLOCKED, COMPLETE)

    Returns:
        HTML string for the badge
    """
    status_upper = status.upper().replace(" ", "_")
    colors = STATUS_COLORS.get(status_upper, STATUS_COLORS["NOT_STARTED"])

    style = f"{DEFAULT_BADGE_STYLE} background-color: {colors['bg']}; color: {colors['text']};"
    return f'<span style="{style}">{status_upper.replace("_", " ")}</span>'


def render_priority_badge(priority: str) -> str:
    """Render a priority badge as HTML.

    Args:
        priority: Priority value (RISKY, CORE, POLISH)

    Returns:
        HTML string for the badge
    """
    priority_upper = priority.upper()
    colors = PRIORITY_COLORS.get(priority_upper, PRIORITY_COLORS["CORE"])

    # Add emoji prefix
    emoji = {
        "RISKY": "&#128308;",   # Red circle
        "CORE": "&#128993;",    # Yellow circle
        "POLISH": "&#128994;",  # Green circle
    }.get(priority_upper, "")

    style = f"{DEFAULT_BADGE_STYLE} background-color: {colors['bg']}; color: {colors['text']};"
    return f'<span style="{style}">{emoji} {priority_upper}</span>'


def render_completion_badge(completed: int, total: int) -> str:
    """Render a completion badge with progress indicator.

    Args:
        completed: Number of completed items
        total: Total number of items

    Returns:
        HTML string for the badge with progress
    """
    percentage = 0 if total == 0 else (completed / total) * 100

    # Determine color based on percentage
    if percentage >= 100:
        bg_color = "#198754"  # Green
    elif percentage >= 50:
        bg_color = "#0d6efd"  # Blue
    elif percentage > 0:
        bg_color = "#ffc107"  # Yellow
        text_color = "#212529"
    else:
        bg_color = "#6c757d"  # Gray
        text_color = "#ffffff"

    text_color = "#ffffff" if percentage >= 50 or percentage == 0 else "#212529"

    style = f"{DEFAULT_BADGE_STYLE} background-color: {bg_color}; color: {text_color};"
    return f'<span style="{style}">{completed}/{total} ({percentage:.0f}%)</span>'


def render_tier_badge(tier: str) -> str:
    """Render a quality tier badge.

    Args:
        tier: Quality tier (prototype, production, library)

    Returns:
        HTML string for the badge
    """
    tier_lower = tier.lower()

    tier_config = {
        "prototype": {"bg": "#ffc107", "text": "#212529", "icon": "&#9889;"},  # Lightning
        "production": {"bg": "#0d6efd", "text": "#ffffff", "icon": "&#9881;"},  # Gear
        "library": {"bg": "#6f42c1", "text": "#ffffff", "icon": "&#128218;"},  # Book
    }

    config = tier_config.get(tier_lower, tier_config["production"])

    style = f"{DEFAULT_BADGE_STYLE} background-color: {config['bg']}; color: {config['text']};"
    return f'<span style="{style}">{config["icon"]} {tier.upper()}</span>'


# =============================================================================
# Markdown-Compatible Badges (No HTML)
# =============================================================================


def render_status_emoji(status: str) -> str:
    """Render a status indicator using emoji (no HTML).

    Args:
        status: Status value

    Returns:
        Emoji string
    """
    emoji_map = {
        "NOT_STARTED": ":white_circle:",
        "IN_PROGRESS": ":large_blue_circle:",
        "BLOCKED": ":red_circle:",
        "COMPLETE": ":white_check_mark:",
    }
    return emoji_map.get(status.upper(), ":white_circle:")


def render_priority_emoji(priority: str) -> str:
    """Render a priority indicator using emoji (no HTML).

    Args:
        priority: Priority value

    Returns:
        Emoji string
    """
    emoji_map = {
        "RISKY": ":red_circle:",
        "CORE": ":yellow_circle:",
        "POLISH": ":green_circle:",
    }
    return emoji_map.get(priority.upper(), ":white_circle:")


# =============================================================================
# Plain Text Badges (For CLI/Logging)
# =============================================================================


def render_status_text(status: str) -> str:
    """Render a status indicator as plain text.

    Args:
        status: Status value

    Returns:
        Formatted text string
    """
    return f"[{status.upper().replace('_', ' ')}]"


def render_priority_text(priority: str) -> str:
    """Render a priority indicator as plain text.

    Args:
        priority: Priority value

    Returns:
        Formatted text string
    """
    return f"[{priority.upper()}]"


def render_completion_text(completed: int, total: int) -> str:
    """Render completion as plain text.

    Args:
        completed: Number of completed items
        total: Total number of items

    Returns:
        Formatted text string
    """
    if total == 0:
        return "[0/0 (0%)]"
    percentage = (completed / total) * 100
    return f"[{completed}/{total} ({percentage:.0f}%)]"
