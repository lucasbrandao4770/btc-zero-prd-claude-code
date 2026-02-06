"""Markdown viewer component for Dev Loop UI.

This module provides components for rendering PROMPT, PROGRESS, and LOG
files with proper formatting and syntax highlighting.
"""

from __future__ import annotations

from ui.components.status_badges import (
    render_completion_badge,
    render_priority_badge,
    render_status_badge,
)
from ui.models import (
    LogFile,
    ParseResult,
    ProgressFile,
    PromptFile,
    Task,
    TaskPriority,
)

# Try to import streamlit
try:
    import streamlit as st

    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

    class DummySt:
        @staticmethod
        def markdown(text: str, unsafe_allow_html: bool = False) -> None:
            print(text)

        @staticmethod
        def write(text: str) -> None:
            print(text)

        @staticmethod
        def error(text: str) -> None:
            print(f"ERROR: {text}")

        @staticmethod
        def warning(text: str) -> None:
            print(f"WARNING: {text}")

        @staticmethod
        def info(text: str) -> None:
            print(f"INFO: {text}")

        @staticmethod
        def success(text: str) -> None:
            print(f"SUCCESS: {text}")

        @staticmethod
        def code(text: str, language: str = "markdown") -> None:
            print(f"```{language}\n{text}\n```")

        @staticmethod
        def expander(label: str, expanded: bool = False):
            class DummyExpander:
                def __enter__(self):
                    return self

                def __exit__(self, *args):
                    pass

                def markdown(self, text: str, **kwargs):
                    print(text)

            return DummyExpander()

        @staticmethod
        def columns(sizes: list[int]):
            class DummyCol:
                def __enter__(self):
                    return self

                def __exit__(self, *args):
                    pass

                def metric(self, label: str, value: str, **kwargs):
                    print(f"{label}: {value}")

            return [DummyCol() for _ in sizes]

        @staticmethod
        def progress(value: float, text: str = "") -> None:
            print(f"Progress: {value:.1%} {text}")

        @staticmethod
        def metric(label: str, value: str, delta: str | None = None) -> None:
            print(f"{label}: {value}")

        @staticmethod
        def divider() -> None:
            print("-" * 40)

    st = DummySt()


# =============================================================================
# PROMPT Viewer
# =============================================================================


def render_prompt_header(prompt: PromptFile) -> None:
    """Render the header section of a PROMPT file.

    Args:
        prompt: Parsed PromptFile object
    """
    if not HAS_STREAMLIT:
        print(f"# {prompt.name}")
        print(f"Status: {prompt.status.value}")
        return

    # Title row
    st.markdown(f"# {prompt.name}")

    # Status and tier badges
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        st.markdown(render_status_badge(prompt.status.value), unsafe_allow_html=True)

    with col2:
        st.markdown(f"**Tier:** {prompt.quality_tier.value}")

    with col3:
        st.markdown(
            render_completion_badge(prompt.completed_count, prompt.task_count),
            unsafe_allow_html=True,
        )


def render_prompt_goal(prompt: PromptFile) -> None:
    """Render the goal section of a PROMPT file.

    Args:
        prompt: Parsed PromptFile object
    """
    if not HAS_STREAMLIT:
        print(f"\nGoal: {prompt.goal}")
        return

    st.markdown("## Goal")
    st.markdown(prompt.goal)


def render_task_list(tasks: list[Task], priority: TaskPriority | None = None) -> None:
    """Render a list of tasks.

    Args:
        tasks: List of Task objects
        priority: Filter by priority (None = all tasks)
    """
    filtered = tasks if priority is None else [t for t in tasks if t.priority == priority]

    if not filtered:
        return

    if not HAS_STREAMLIT:
        for task in filtered:
            checkbox = "[x]" if task.completed else "[ ]"
            agent = f"@{task.agent_ref}: " if task.agent_ref else ""
            print(f"  - {checkbox} {agent}{task.description}")
        return

    for task in filtered:
        checkbox = ":white_check_mark:" if task.completed else ":white_large_square:"
        agent_text = f"`@{task.agent_ref}` " if task.agent_ref else ""
        st.markdown(f"{checkbox} {agent_text}{task.description}")


def render_prompt_tasks(prompt: PromptFile) -> None:
    """Render all tasks grouped by priority.

    Args:
        prompt: Parsed PromptFile object
    """
    if not HAS_STREAMLIT:
        print("\n## Tasks")
        for priority in [TaskPriority.RISKY, TaskPriority.CORE, TaskPriority.POLISH]:
            print(f"\n### {priority.value}")
            render_task_list(prompt.tasks, priority)
        return

    st.markdown("## Tasks")

    # RISKY tasks
    if prompt.risky_tasks:
        st.markdown(
            f"### {render_priority_badge('RISKY')} RISKY ({len(prompt.risky_tasks)})",
            unsafe_allow_html=True,
        )
        render_task_list(prompt.risky_tasks)

    # CORE tasks
    if prompt.core_tasks:
        st.markdown(
            f"### {render_priority_badge('CORE')} CORE ({len(prompt.core_tasks)})",
            unsafe_allow_html=True,
        )
        render_task_list(prompt.core_tasks)

    # POLISH tasks
    if prompt.polish_tasks:
        st.markdown(
            f"### {render_priority_badge('POLISH')} POLISH ({len(prompt.polish_tasks)})",
            unsafe_allow_html=True,
        )
        render_task_list(prompt.polish_tasks)


def render_prompt_progress_bar(prompt: PromptFile) -> None:
    """Render a progress bar for task completion.

    Args:
        prompt: Parsed PromptFile object
    """
    if not HAS_STREAMLIT:
        print(f"\nProgress: {prompt.completion_percentage:.1f}%")
        return

    pct = prompt.completion_percentage
    st.progress(
        pct / 100,
        text=f"{prompt.completed_count}/{prompt.task_count} tasks ({pct:.1f}%)",
    )


def render_prompt_viewer(prompt: PromptFile) -> None:
    """Render a full PROMPT file viewer.

    This is the main entry point for displaying PROMPT content.

    Args:
        prompt: Parsed PromptFile object
    """
    render_prompt_header(prompt)
    render_prompt_progress_bar(prompt)
    st.divider() if HAS_STREAMLIT else print("-" * 40)
    render_prompt_goal(prompt)
    st.divider() if HAS_STREAMLIT else print("-" * 40)
    render_prompt_tasks(prompt)


def render_prompt_with_fallback(result: ParseResult[PromptFile], raw_content: str = "") -> None:
    """Render a PROMPT file with fallback for parse errors.

    Args:
        result: ParseResult from parse_prompt_file
        raw_content: Raw markdown content for fallback display
    """
    if result.is_success:
        render_prompt_viewer(result.value)
    else:
        if HAS_STREAMLIT:
            st.error(f"Failed to parse PROMPT: {result.error}")
            with st.expander("Show raw content", expanded=True):
                st.code(raw_content or "No content available", language="markdown")
        else:
            print(f"ERROR: {result.error}")
            print(raw_content)


# =============================================================================
# PROGRESS Viewer
# =============================================================================


def render_progress_header(progress: ProgressFile) -> None:
    """Render the header section of a PROGRESS file.

    Args:
        progress: Parsed ProgressFile object
    """
    if not HAS_STREAMLIT:
        print(f"# {progress.name}")
        return

    st.markdown(f"# {progress.name}")

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        st.metric("Status", progress.status.value)

    with col2:
        st.metric("Tasks", f"{progress.tasks_completed}/{progress.total_tasks}")

    with col3:
        st.metric("Iteration", progress.current_iteration)

    with col4:
        st.metric("Completion", f"{progress.completion_percentage:.1f}%")


def render_progress_iteration_log(progress: ProgressFile) -> None:
    """Render the iteration log of a PROGRESS file.

    Args:
        progress: Parsed ProgressFile object
    """
    if not HAS_STREAMLIT:
        print("\n## Iteration Log")
        for entry in progress.iteration_log:
            print(f"  {entry.iteration}: {entry.task} - {entry.status}")
        return

    st.markdown("## Iteration Log")

    if not progress.iteration_log:
        st.info("No iterations logged yet.")
        return

    for entry in progress.iteration_log:
        with st.expander(f"Iteration {entry.iteration}: {entry.task[:50]}...", expanded=False):
            st.markdown(f"**Status:** {entry.status}")
            if entry.agent:
                st.markdown(f"**Agent:** {entry.agent}")
            if entry.key_decisions:
                st.markdown("**Key Decisions:**")
                for decision in entry.key_decisions:
                    st.markdown(f"- {decision}")
            if entry.files_changed:
                st.markdown("**Files Changed:**")
                for file in entry.files_changed:
                    st.markdown(f"- `{file}`")


def render_progress_blockers(progress: ProgressFile) -> None:
    """Render blockers section of a PROGRESS file.

    Args:
        progress: Parsed ProgressFile object
    """
    if not HAS_STREAMLIT:
        print("\n## Blockers")
        for blocker in progress.blockers:
            status = "Resolved" if blocker.is_resolved else "Active"
            print(f"  - [{status}] {blocker.description}")
        return

    st.markdown("## Blockers")

    if not progress.blockers:
        st.success("No blockers!")
        return

    for blocker in progress.blockers:
        if blocker.is_resolved:
            st.markdown(f":white_check_mark: ~~{blocker.description}~~ - {blocker.resolution}")
        else:
            st.markdown(f":warning: **{blocker.description}**")


def render_progress_viewer(progress: ProgressFile) -> None:
    """Render a full PROGRESS file viewer.

    Args:
        progress: Parsed ProgressFile object
    """
    render_progress_header(progress)
    st.divider() if HAS_STREAMLIT else print("-" * 40)
    render_progress_iteration_log(progress)
    st.divider() if HAS_STREAMLIT else print("-" * 40)
    render_progress_blockers(progress)


# =============================================================================
# LOG Viewer
# =============================================================================


def render_log_header(log: LogFile) -> None:
    """Render the header section of a LOG file.

    Args:
        log: Parsed LogFile object
    """
    if not HAS_STREAMLIT:
        print(f"# {log.name}")
        return

    st.markdown(f"# {log.name}")

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        st.metric("Exit Reason", log.exit_reason)

    with col2:
        st.metric("Tasks", str(log.statistics.total_tasks))

    with col3:
        st.metric("Pass Rate", f"{log.statistics.pass_rate:.1f}%")

    with col4:
        st.metric("Duration", log.statistics.duration_formatted)


def render_log_statistics(log: LogFile) -> None:
    """Render statistics section of a LOG file.

    Args:
        log: Parsed LogFile object
    """
    if not HAS_STREAMLIT:
        print("\n## Statistics")
        print(f"  Total: {log.statistics.total_tasks}")
        print(f"  Passed: {log.statistics.passed}")
        print(f"  Failed: {log.statistics.failed}")
        print(f"  Skipped: {log.statistics.skipped}")
        return

    st.markdown("## Statistics")

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        st.metric("Total", log.statistics.total_tasks)

    with col2:
        st.metric("Passed", log.statistics.passed, delta=None)

    with col3:
        st.metric("Failed", log.statistics.failed)

    with col4:
        st.metric("Skipped", log.statistics.skipped)


def render_log_viewer(log: LogFile) -> None:
    """Render a full LOG file viewer.

    Args:
        log: Parsed LogFile object
    """
    render_log_header(log)
    st.divider() if HAS_STREAMLIT else print("-" * 40)
    render_log_statistics(log)


# =============================================================================
# Raw Content Viewer
# =============================================================================


def render_raw_content(content: str, language: str = "markdown") -> None:
    """Render raw content in a code block.

    Args:
        content: Raw text content
        language: Syntax highlighting language
    """
    if HAS_STREAMLIT:
        st.code(content, language=language)
    else:
        print(f"```{language}")
        print(content)
        print("```")
