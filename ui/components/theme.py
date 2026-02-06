"""Theme component for Dev Loop UI.

This module provides theme toggle functionality for the Streamlit application.
It uses custom CSS injection to provide visual theme adjustments.

Note: Full Streamlit theming requires .streamlit/config.toml. This module
provides complementary CSS adjustments and preference persistence.

Limitations:
- Cannot fully override Streamlit's base theme
- Best used with Streamlit's built-in dark mode setting
- CSS adjustments are applied on top of existing theme
"""

from __future__ import annotations

from ui.state import get_theme, set_theme, toggle_theme

# Try to import streamlit
try:
    import streamlit as st

    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

    class DummySt:
        @staticmethod
        def markdown(text: str, unsafe_allow_html: bool = False) -> None:
            pass

        @staticmethod
        def toggle(label: str, value: bool = False, **kwargs) -> bool:
            return value

    st = DummySt()


# =============================================================================
# Theme CSS
# =============================================================================

DARK_THEME_CSS = """
<style>
/* Dark theme adjustments */
.stApp {
    background-color: #0e1117;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #1a1a2e;
}

/* Cards and containers */
.stMarkdown, .stText {
    color: #fafafa;
}

/* Status badges - ensure visibility in dark mode */
.status-badge {
    box-shadow: 0 1px 3px rgba(255,255,255,0.1);
}

/* Tables */
table {
    background-color: #1e1e2e;
}

th {
    background-color: #2d2d44;
    color: #fafafa;
}

td {
    color: #e0e0e0;
}

/* Code blocks */
code {
    background-color: #2d2d44;
    color: #e0e0e0;
}

/* Inputs */
.stTextInput input, .stSelectbox select, .stTextArea textarea {
    background-color: #2d2d44;
    color: #fafafa;
    border-color: #444;
}

/* Expanders */
.streamlit-expanderHeader {
    background-color: #1e1e2e;
    color: #fafafa;
}

/* Metrics */
[data-testid="stMetricValue"] {
    color: #fafafa;
}

/* Progress bar */
.stProgress > div > div {
    background-color: #0d6efd;
}
</style>
"""

LIGHT_THEME_CSS = """
<style>
/* Light theme adjustments */
.stApp {
    background-color: #ffffff;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #f8f9fa;
}

/* Cards and containers */
.stMarkdown, .stText {
    color: #212529;
}

/* Status badges */
.status-badge {
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* Tables */
table {
    background-color: #ffffff;
}

th {
    background-color: #f8f9fa;
    color: #212529;
}

td {
    color: #495057;
}

/* Code blocks */
code {
    background-color: #f8f9fa;
    color: #212529;
}

/* Inputs */
.stTextInput input, .stSelectbox select, .stTextArea textarea {
    background-color: #ffffff;
    color: #212529;
    border-color: #ced4da;
}

/* Expanders */
.streamlit-expanderHeader {
    background-color: #f8f9fa;
    color: #212529;
}

/* Metrics */
[data-testid="stMetricValue"] {
    color: #212529;
}
</style>
"""


# =============================================================================
# Theme Functions
# =============================================================================


def apply_theme_css() -> None:
    """Apply CSS based on current theme preference.

    Call this early in your app to inject theme-specific styles.
    """
    if not HAS_STREAMLIT:
        return

    current_theme = get_theme()
    css = DARK_THEME_CSS if current_theme == "dark" else LIGHT_THEME_CSS
    st.markdown(css, unsafe_allow_html=True)


def render_theme_toggle() -> None:
    """Render a theme toggle switch in the sidebar.

    This creates a toggle that switches between light and dark themes.
    The preference is persisted in session state.
    """
    if not HAS_STREAMLIT:
        return

    current_theme = get_theme()
    is_dark = current_theme == "dark"

    # Use a toggle with moon/sun icons
    new_value = st.toggle(
        "Dark Mode",
        value=is_dark,
        key="theme_toggle",
        help="Toggle between light and dark theme",
    )

    # Update theme if changed
    if new_value != is_dark:
        set_theme("dark" if new_value else "light")
        st.rerun()


def render_theme_selector() -> None:
    """Render a theme selector dropdown.

    Alternative to toggle for more explicit selection.
    """
    if not HAS_STREAMLIT:
        return

    current_theme = get_theme()

    selected = st.selectbox(
        "Theme",
        options=["light", "dark"],
        index=0 if current_theme == "light" else 1,
        key="theme_selector",
        help="Select your preferred color theme",
    )

    if selected != current_theme:
        set_theme(selected)
        st.rerun()


def get_theme_icon() -> str:
    """Get an icon representing the current theme.

    Returns:
        Moon icon for dark theme, sun icon for light theme
    """
    return "moon" if get_theme() == "dark" else "sun"


def get_theme_colors() -> dict[str, str]:
    """Get color values for the current theme.

    Returns:
        Dictionary with color keys and hex values
    """
    if get_theme() == "dark":
        return {
            "background": "#0e1117",
            "secondary_background": "#1a1a2e",
            "text": "#fafafa",
            "secondary_text": "#b0b0b0",
            "primary": "#0d6efd",
            "success": "#198754",
            "warning": "#ffc107",
            "error": "#dc3545",
            "border": "#444444",
        }
    else:
        return {
            "background": "#ffffff",
            "secondary_background": "#f8f9fa",
            "text": "#212529",
            "secondary_text": "#6c757d",
            "primary": "#0d6efd",
            "success": "#198754",
            "warning": "#ffc107",
            "error": "#dc3545",
            "border": "#ced4da",
        }
