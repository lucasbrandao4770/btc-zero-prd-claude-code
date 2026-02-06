"""Dev Loop UI - Streamlit-based interface for managing Dev Loop artifacts.

This package provides a web interface for browsing, creating, and tracking
Dev Loop PROMPT/PROGRESS/LOG files through a local Streamlit application.

Usage:
    from ui.config import get_devloop_path
    from ui.models import PromptFile, ParseResult
    from ui.parser import parse_prompt_file
    from ui.state import init_session_state
"""

__version__ = "0.1.0"

__all__ = [
    "__version__",
]
