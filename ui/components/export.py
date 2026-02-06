"""Export component for Dev Loop UI.

This module provides export functionality for PROMPT, PROGRESS, and LOG files.
Supports downloading as markdown and copying to clipboard.
"""

from __future__ import annotations

from pathlib import Path

# Try to import streamlit
try:
    import streamlit as st

    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

    class DummySt:
        @staticmethod
        def download_button(**kwargs) -> bool:
            return False

        @staticmethod
        def button(**kwargs) -> bool:
            return False

        @staticmethod
        def success(text: str) -> None:
            print(f"SUCCESS: {text}")

        @staticmethod
        def error(text: str) -> None:
            print(f"ERROR: {text}")

        @staticmethod
        def columns(sizes):
            class DummyCol:
                def __enter__(self):
                    return self

                def __exit__(self, *args):
                    pass

            return [DummyCol() for _ in sizes]

    st = DummySt()


# =============================================================================
# Export Functions
# =============================================================================


def render_download_button(
    content: str,
    filename: str,
    label: str = "Download",
    mime: str = "text/markdown",
    key: str | None = None,
) -> bool:
    """Render a download button for content.

    Args:
        content: The text content to download
        filename: The suggested filename
        label: Button label
        mime: MIME type for the download
        key: Unique key for the button

    Returns:
        True if button was clicked
    """
    if not HAS_STREAMLIT:
        return False

    return st.download_button(
        label=label,
        data=content,
        file_name=filename,
        mime=mime,
        key=key,
        use_container_width=True,
    )


def render_copy_button(content: str, key: str = "copy_btn") -> bool:
    """Render a copy to clipboard button.

    Note: This uses JavaScript injection to copy to clipboard.
    Streamlit doesn't have native clipboard support.

    Args:
        content: The text to copy
        key: Unique key for the button

    Returns:
        True if button was clicked
    """
    if not HAS_STREAMLIT:
        return False

    # JavaScript for clipboard copy
    copy_js = f"""
    <script>
    function copyToClipboard_{key}() {{
        const text = `{content.replace('`', '\\`').replace('${', '\\${')[:5000]}`;
        navigator.clipboard.writeText(text).then(function() {{
            // Success - handled by Streamlit
        }}, function(err) {{
            console.error('Could not copy text: ', err);
        }});
    }}
    </script>
    """

    # Note: Due to Streamlit limitations, this approach has limitations.
    # For a more robust solution, use streamlit-clipboard component.
    if st.button("Copy to Clipboard", key=key, use_container_width=True):
        # Inject JavaScript
        st.markdown(copy_js, unsafe_allow_html=True)
        st.success("Content ready to copy. Use Ctrl+C or Cmd+C on selected text.")
        return True

    return False


def render_export_buttons(
    content: str,
    filename: str,
    file_type: str = "prompt",
) -> None:
    """Render export buttons (download and copy).

    Args:
        content: The content to export
        filename: The filename for download
        file_type: Type of file (prompt, progress, log)
    """
    if not HAS_STREAMLIT:
        return

    col1, col2 = st.columns(2)

    with col1:
        render_download_button(
            content=content,
            filename=filename,
            label="Download .md",
            key=f"download_{file_type}",
        )

    with col2:
        # For clipboard, we'll show raw content that can be selected
        if st.button("Show for Copy", key=f"copy_{file_type}", use_container_width=True):
            st.code(content, language="markdown")
            st.caption("Select all (Ctrl+A) and copy (Ctrl+C)")


def render_prompt_export(content: str, name: str) -> None:
    """Render export options for a PROMPT file.

    Args:
        content: Raw PROMPT content
        name: PROMPT name
    """
    render_export_buttons(
        content=content,
        filename=f"PROMPT_{name}.md",
        file_type="prompt",
    )


def render_progress_export(content: str, name: str) -> None:
    """Render export options for a PROGRESS file.

    Args:
        content: Raw PROGRESS content
        name: PROGRESS name
    """
    render_export_buttons(
        content=content,
        filename=f"PROGRESS_{name}.md",
        file_type="progress",
    )


def render_log_export(content: str, name: str) -> None:
    """Render export options for a LOG file.

    Args:
        content: Raw LOG content
        name: LOG name
    """
    render_export_buttons(
        content=content,
        filename=f"LOG_{name}.md",
        file_type="log",
    )
