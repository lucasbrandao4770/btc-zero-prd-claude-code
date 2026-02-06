"""Logs Page - View execution history.

This page provides:
- List of LOG files (chronologically)
- Execution summary cards
- Date range filter
- Search within log content
"""

from __future__ import annotations

from datetime import datetime, timedelta

import streamlit as st

from ui.components.file_browser import get_file_info, list_log_files
from ui.components.markdown_viewer import render_log_viewer
from ui.parser import parse_log_file
from ui.state import get_selected_file, init_session_state, set_selected_file

# Initialize session state
init_session_state()

# Page config
st.set_page_config(page_title="Logs - Dev Loop UI", page_icon="memo", layout="wide")


# =============================================================================
# Sidebar - File Browser and Filters
# =============================================================================

with st.sidebar:
    st.header("LOG Files")

    # Refresh button
    if st.button("Refresh", key="refresh_logs", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.divider()

    # Search
    search_query = st.text_input(
        "Search logs",
        placeholder="Search in content...",
        key="log_search",
    )

    # Date filter
    with st.expander("Date Filter"):
        date_options = ["All time", "Last 7 days", "Last 30 days", "Custom"]
        date_filter = st.selectbox("Period", date_options, key="log_date_filter")

        if date_filter == "Custom":
            col1, col2 = st.columns([1, 1])
            with col1:
                start_date = st.date_input("From", key="log_start_date")
            with col2:
                end_date = st.date_input("To", key="log_end_date")

    st.divider()

    # File list
    log_files = list_log_files()

    if not log_files:
        st.info("No LOG files found.")
        st.markdown("Execution logs are created when Dev Loop sessions complete.")
    else:
        # Sort by modification time (newest first)
        log_files = sorted(
            log_files,
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

        # Apply date filter
        if date_filter == "Last 7 days":
            cutoff = datetime.now() - timedelta(days=7)
            log_files = [f for f in log_files if datetime.fromtimestamp(f.stat().st_mtime) > cutoff]
        elif date_filter == "Last 30 days":
            cutoff = datetime.now() - timedelta(days=30)
            log_files = [f for f in log_files if datetime.fromtimestamp(f.stat().st_mtime) > cutoff]

        # Apply search filter
        if search_query:
            filtered_logs = []
            for lf in log_files:
                try:
                    content = lf.read_text(encoding="utf-8")
                    if search_query.lower() in content.lower():
                        filtered_logs.append(lf)
                except Exception:
                    pass
            log_files = filtered_logs

        st.caption(f"Showing {len(log_files)} log files")

        if log_files:
            # File selection
            options = [lf.stem for lf in log_files]
            path_map = {lf.stem: lf for lf in log_files}

            current = get_selected_file()
            current_name = current.stem if current and "LOG" in str(current) else None
            default_idx = options.index(current_name) if current_name in options else 0

            selected_name = st.selectbox(
                "Select LOG",
                options=options,
                index=default_idx,
                key="log_selector",
                label_visibility="collapsed",
            )

            if selected_name:
                selected_path = path_map[selected_name]
                set_selected_file(selected_path, "log")

                # Show file info
                info = get_file_info(selected_path)
                st.caption(f"Modified: {info['modified'].strftime('%Y-%m-%d %H:%M')}")
        else:
            st.warning("No logs match your filters.")


# =============================================================================
# Main Content - Selected LOG
# =============================================================================

st.title("Execution Logs")

selected_file = get_selected_file()
log_files = list_log_files()

if selected_file and selected_file.exists() and "LOG" in selected_file.name:
    # Parse the selected file
    result = parse_log_file(selected_file)

    if result.is_success:
        log = result.value

        # Render the log viewer
        render_log_viewer(log)

        st.divider()

        # Key decisions
        if log.key_decisions:
            st.markdown("## Key Decisions")
            for decision in log.key_decisions:
                st.markdown(f"- {decision}")

        # Files changed
        if log.files_changed:
            st.markdown("## Files Changed")
            for file in log.files_changed:
                st.markdown(f"- `{file}`")

        # Raw content expander
        with st.expander("Show Raw Markdown"):
            st.code(log.raw_content, language="markdown")

    else:
        # Show error with fallback
        st.error(f"Failed to parse LOG: {result.error}")
        try:
            raw = selected_file.read_text(encoding="utf-8")
            with st.expander("Show Raw Content", expanded=True):
                st.code(raw, language="markdown")
        except Exception as e:
            st.error(f"Could not read file: {e}")

elif not log_files:
    # Empty state
    st.info("No execution logs yet.")
    st.markdown("""
    Log files are created when Dev Loop sessions complete (successfully or otherwise).

    Each log contains:
    - Execution summary (duration, outcome, task count)
    - Task execution details
    - Key decisions made
    - Files created/modified

    Complete a Dev Loop session to see logs here.
    """)

else:
    st.info("Select a LOG file from the sidebar to view execution details.")
