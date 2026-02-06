"""Dev Loop UI - Main Application Entry Point.

This is the main Streamlit application for the Dev Loop UI.
Run with: streamlit run ui/app.py

The application provides:
- Dashboard with overview statistics
- Multi-page navigation via pages/ folder
- Session state management
- Logging configuration
"""

from __future__ import annotations

import logging

import streamlit as st

from ui.components.file_browser import (
    get_prompt_info,
    list_log_files,
    list_progress_files,
    list_prompt_files,
)
from ui.components.status_badges import render_status_badge
from ui.components.theme import apply_theme_css, render_theme_toggle
from ui.config import (
    LOG_FORMAT,
    LOG_LEVEL,
    PAGE_ICON,
    PAGE_LAYOUT,
    PAGE_TITLE,
    get_ui_logs_path,
)
from ui.models import TaskStatus
from ui.state import init_session_state

# =============================================================================
# Logging Configuration
# =============================================================================


def setup_logging() -> None:
    """Configure application logging."""
    log_path = get_ui_logs_path() / "devloop_ui.log"

    # Create handler for file logging
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Configure root logger
    logger = logging.getLogger("devloop_ui")
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
    logger.addHandler(file_handler)


# =============================================================================
# Page Configuration
# =============================================================================

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/your-repo/devloop-ui",
        "Report a bug": "https://github.com/your-repo/devloop-ui/issues",
        "About": "Dev Loop UI - A Streamlit application for managing Dev Loop artifacts.",
    },
)


# =============================================================================
# Initialize Application
# =============================================================================

# Setup logging
setup_logging()

# Initialize session state
init_session_state()

# Get logger
logger = logging.getLogger("devloop_ui")
logger.info("Application started")


# =============================================================================
# Dashboard - Home Page
# =============================================================================


def render_dashboard() -> None:
    """Render the main dashboard with overview statistics."""
    st.title("Dev Loop Dashboard")
    st.markdown("Welcome to the Dev Loop UI. Use the sidebar to navigate between pages.")

    # Load file lists
    prompt_files = list_prompt_files()
    progress_files = list_progress_files()
    log_files = list_log_files()

    # Overview metrics
    st.markdown("## Overview")

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        st.metric("PROMPT Files", len(prompt_files))

    with col2:
        st.metric("PROGRESS Files", len(progress_files))

    with col3:
        st.metric("LOG Files", len(log_files))

    # Calculate active sessions
    active_count = 0
    for pf in prompt_files:
        info = get_prompt_info(pf)
        if info.get("status") == TaskStatus.IN_PROGRESS:
            active_count += 1

    with col4:
        st.metric("Active Sessions", active_count)

    st.divider()

    # Status breakdown
    if prompt_files:
        st.markdown("## Status Breakdown")

        status_counts = {
            "NOT_STARTED": 0,
            "IN_PROGRESS": 0,
            "BLOCKED": 0,
            "COMPLETE": 0,
        }

        for pf in prompt_files:
            info = get_prompt_info(pf)
            status = str(info.get("status", TaskStatus.NOT_STARTED).value)
            if status in status_counts:
                status_counts[status] += 1

        cols = st.columns([1, 1, 1, 1])
        for i, (status, count) in enumerate(status_counts.items()):
            with cols[i]:
                st.markdown(
                    f"{render_status_badge(status)} **{count}**",
                    unsafe_allow_html=True,
                )

        st.divider()

    # Recent activity
    st.markdown("## Recent Activity")

    if prompt_files:
        # Sort by modification time
        recent_files = sorted(
            prompt_files,
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )[:5]

        for pf in recent_files:
            info = get_prompt_info(pf)
            status = info.get("status", TaskStatus.NOT_STARTED)
            status_badge = render_status_badge(str(status.value))
            completion = f"{info.get('completed_count', 0)}/{info.get('task_count', 0)}"

            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**{info['name']}**")
            with col2:
                st.markdown(status_badge, unsafe_allow_html=True)
            with col3:
                st.markdown(completion)
    else:
        st.info("No PROMPT files found. Create your first one using the Create page!")

    # Footer
    st.divider()
    st.markdown(
        """
        <div style="text-align: center; color: #888; font-size: 0.8em;">
            Dev Loop UI v0.1.0 |
            <a href="https://docs.streamlit.io" target="_blank">Streamlit Docs</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# Sidebar
# =============================================================================


def render_sidebar() -> None:
    """Render the sidebar with navigation hints."""
    with st.sidebar:
        st.markdown("## Navigation")
        st.markdown("""
        Use the pages in the sidebar to:
        - **Tasks**: Browse and view PROMPT files
        - **Progress**: Track session progress
        - **Logs**: View execution history
        - **Create**: Create new PROMPT files
        """)

        st.divider()

        # Quick stats
        st.markdown("## Quick Stats")
        prompt_count = len(list_prompt_files())
        progress_count = len(list_progress_files())
        log_count = len(list_log_files())

        st.markdown(f"- {prompt_count} PROMPT files")
        st.markdown(f"- {progress_count} PROGRESS files")
        st.markdown(f"- {log_count} LOG files")

        # Refresh button
        st.divider()
        if st.button("Refresh All", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

        # Theme toggle
        st.divider()
        st.markdown("## Settings")
        render_theme_toggle()


# =============================================================================
# Main
# =============================================================================


def main() -> None:
    """Main application entry point."""
    # Apply theme CSS
    apply_theme_css()

    render_sidebar()
    render_dashboard()


if __name__ == "__main__":
    main()
