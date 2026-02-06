"""Progress Page - Track session progress.

This page provides:
- List of PROGRESS files
- Iteration history timeline
- Blockers display
- Key decisions from iteration log
"""

from __future__ import annotations

import streamlit as st

from ui.components.file_browser import list_progress_files, list_prompt_files
from ui.components.markdown_viewer import render_progress_viewer
from ui.parser import parse_progress_file
from ui.state import get_selected_file, init_session_state, set_selected_file

# Initialize session state
init_session_state()

# Page config
st.set_page_config(
    page_title="Progress - Dev Loop UI",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)


# =============================================================================
# Sidebar - File Browser
# =============================================================================

with st.sidebar:
    st.header("PROGRESS Files")

    # Refresh button
    if st.button("Refresh", key="refresh_progress", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.divider()

    # File list
    progress_files = list_progress_files()

    if not progress_files:
        st.info("No PROGRESS files found.")
        st.markdown("Start a Dev Loop session to see progress here.")
    else:
        # Sort by modification time (newest first)
        progress_files = sorted(
            progress_files,
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

        # File selection
        options = [pf.stem for pf in progress_files]
        path_map = {pf.stem: pf for pf in progress_files}

        current = get_selected_file()
        current_name = current.stem if current and current.suffix == ".md" else None
        default_idx = options.index(current_name) if current_name in options else 0

        selected_name = st.selectbox(
            "Select PROGRESS",
            options=options,
            index=default_idx,
            key="progress_selector",
            label_visibility="collapsed",
        )

        if selected_name:
            selected_path = path_map[selected_name]
            set_selected_file(selected_path, "progress")


# =============================================================================
# Main Content - Selected PROGRESS
# =============================================================================

st.title("Progress Tracking")

selected_file = get_selected_file()
progress_files = list_progress_files()

if selected_file and selected_file.exists() and "PROGRESS" in selected_file.name:
    # Parse the selected file
    result = parse_progress_file(selected_file)

    if result.is_success:
        progress = result.value

        # Render the progress viewer
        render_progress_viewer(progress)

        st.divider()

        # Link to source PROMPT
        prompt_files = list_prompt_files()
        associated_prompt = None
        for pf in prompt_files:
            if progress.name in pf.name:
                associated_prompt = pf
                break

        if associated_prompt:
            st.markdown(f"**Source PROMPT:** `{associated_prompt.name}`")
            if st.button("View PROMPT"):
                set_selected_file(associated_prompt, "prompt")
                st.switch_page("pages/1_Tasks.py")

        # Raw content expander
        with st.expander("Show Raw Markdown"):
            st.code(progress.raw_content, language="markdown")

    else:
        # Show error with fallback
        st.error(f"Failed to parse PROGRESS: {result.error}")
        try:
            raw = selected_file.read_text(encoding="utf-8")
            with st.expander("Show Raw Content", expanded=True):
                st.code(raw, language="markdown")
        except Exception as e:
            st.error(f"Could not read file: {e}")

elif not progress_files:
    # Empty state
    st.info("No active sessions.")
    st.markdown("""
    Progress files are created when you start a Dev Loop session.

    To start a session:
    1. Create a PROMPT file (or use an existing one)
    2. Run the Dev Loop: `/dev tasks/PROMPT_YOUR_NAME.md`
    3. Progress will be tracked automatically

    Check back here once you've started iterating!
    """)

else:
    st.info("Select a PROGRESS file from the sidebar to view session details.")
