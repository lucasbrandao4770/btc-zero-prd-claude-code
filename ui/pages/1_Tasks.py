"""Tasks Page - Browse and view PROMPT files.

This page provides:
- File browser for PROMPT files in sidebar
- Search and filter functionality
- Selected PROMPT details with task list
- Progress bar showing completion
"""

from __future__ import annotations

import streamlit as st

from ui.components.export import render_prompt_export
from ui.components.file_browser import (
    filter_files,
    get_prompt_info,
    list_progress_files,
    list_prompt_files,
    sort_files,
)
from ui.components.markdown_viewer import render_prompt_viewer
from ui.components.status_badges import render_status_badge
from ui.config import QUALITY_TIERS, STATUSES
from ui.models import TaskStatus
from ui.parser import parse_prompt_file
from ui.state import (
    get_filter_status,
    get_filter_tier,
    get_search_query,
    get_selected_file,
    get_sort_by,
    get_sort_order,
    has_active_filters,
    init_session_state,
    reset_filters,
    set_filter_status,
    set_filter_tier,
    set_search_query,
    set_selected_file,
    set_sort_by,
    set_sort_order,
)

# Initialize session state
init_session_state()

# Page config
st.set_page_config(page_title="Tasks - Dev Loop UI", page_icon="clipboard", layout="wide")


# =============================================================================
# Sidebar - File Browser and Filters
# =============================================================================

with st.sidebar:
    st.header("PROMPT Files")

    # Refresh button
    if st.button("Refresh", key="refresh_tasks", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.divider()

    # Search
    search = st.text_input(
        "Search",
        value=get_search_query(),
        placeholder="Search by name or goal...",
        key="search_input",
    )
    if search != get_search_query():
        set_search_query(search)

    # Filters
    with st.expander("Filters", expanded=has_active_filters()):
        # Status filter
        status_options = STATUSES
        current_status = get_filter_status()
        selected_status = st.multiselect(
            "Status",
            options=status_options,
            default=current_status,
            key="status_filter",
        )
        if selected_status != current_status:
            set_filter_status(selected_status)

        # Tier filter
        tier_options = QUALITY_TIERS
        current_tier = get_filter_tier()
        selected_tier = st.multiselect(
            "Quality Tier",
            options=tier_options,
            default=current_tier,
            key="tier_filter",
        )
        if selected_tier != current_tier:
            set_filter_tier(selected_tier)

        # Sort options
        col1, col2 = st.columns([1, 1])
        with col1:
            sort_by = st.selectbox(
                "Sort by",
                options=["name", "date", "status", "completion"],
                index=["name", "date", "status", "completion"].index(get_sort_by()),
                key="sort_by",
            )
            if sort_by != get_sort_by():
                set_sort_by(sort_by)

        with col2:
            sort_order = st.selectbox(
                "Order",
                options=["asc", "desc"],
                index=0 if get_sort_order() == "asc" else 1,
                key="sort_order",
            )
            if sort_order != get_sort_order():
                set_sort_order(sort_order)

        # Clear filters button
        if st.button("Clear Filters", use_container_width=True):
            reset_filters()
            st.rerun()

    st.divider()

    # File list
    prompt_files = list_prompt_files()

    if not prompt_files:
        st.info("No PROMPT files found.")
        st.markdown("Create your first PROMPT using the **Create** page.")
    else:
        # Get file info for all files
        file_infos = [get_prompt_info(pf) for pf in prompt_files]

        # Apply filters
        file_infos = filter_files(
            file_infos,
            status_filter=get_filter_status(),
            tier_filter=get_filter_tier(),
            search_query=get_search_query(),
        )

        # Sort
        file_infos = sort_files(
            file_infos,
            sort_by=get_sort_by(),
            ascending=get_sort_order() == "asc",
        )

        # Show count
        st.caption(f"Showing {len(file_infos)} of {len(prompt_files)} files")

        # File selection
        if file_infos:
            options = [f["name"] for f in file_infos]
            path_map = {f["name"]: f["path"] for f in file_infos}

            current = get_selected_file()
            current_name = current.stem if current else None
            default_idx = options.index(current_name) if current_name in options else 0

            selected_name = st.selectbox(
                "Select PROMPT",
                options=options,
                index=default_idx,
                key="prompt_selector",
                label_visibility="collapsed",
            )

            if selected_name:
                selected_path = path_map[selected_name]
                set_selected_file(selected_path, "prompt")

                # Show file info
                info = next((f for f in file_infos if f["name"] == selected_name), None)
                if info:
                    st.markdown(
                        render_status_badge(str(info.get("status", TaskStatus.NOT_STARTED).value)),
                        unsafe_allow_html=True,
                    )
                    st.caption(
                        f"{info.get('completed_count', 0)}/{info.get('task_count', 0)} tasks"
                    )
        else:
            st.warning("No files match your filters.")


# =============================================================================
# Main Content - Selected PROMPT
# =============================================================================

st.title("Tasks")

selected_file = get_selected_file()

if selected_file and selected_file.exists():
    # Parse the selected file
    result = parse_prompt_file(selected_file)

    if result.is_success:
        prompt = result.value

        # Render the prompt viewer
        render_prompt_viewer(prompt)

        st.divider()

        # Check for associated PROGRESS file
        progress_files = list_progress_files()
        associated_progress = None
        for pf in progress_files:
            if prompt.name in pf.name:
                associated_progress = pf
                break

        if associated_progress:
            st.markdown(f"**Associated Progress:** `{associated_progress.name}`")
            if st.button("View Progress"):
                set_selected_file(associated_progress, "progress")
                st.switch_page("pages/2_Progress.py")

        # Export options
        st.markdown("### Export")
        render_prompt_export(prompt.raw_content, prompt.name)

        # Raw content expander
        with st.expander("Show Raw Markdown"):
            st.code(prompt.raw_content, language="markdown")

    else:
        # Show error with fallback
        st.error(f"Failed to parse PROMPT: {result.error}")
        try:
            raw = selected_file.read_text(encoding="utf-8")
            with st.expander("Show Raw Content", expanded=True):
                st.code(raw, language="markdown")
        except Exception as e:
            st.error(f"Could not read file: {e}")

elif not prompt_files:
    # Empty state
    st.info("No PROMPT files found.")
    st.markdown("""
    Get started by creating your first PROMPT:
    1. Navigate to the **Create** page in the sidebar
    2. Fill in the form with your task details
    3. Click **Save** to create the PROMPT file

    Or manually create a file in `.claude/dev/tasks/PROMPT_YOUR_NAME.md`
    """)

else:
    st.info("Select a PROMPT file from the sidebar to view its details.")
