# Dev Loop UI

A Streamlit-based local web interface for managing Dev Loop artifacts (PROMPT, PROGRESS, and LOG files).

## Overview

Dev Loop UI provides a visual interface for:

- **Browsing** PROMPT files with status, progress, and task information
- **Tracking** session progress through PROGRESS files
- **Viewing** execution history in LOG files
- **Creating** new PROMPT files with validation

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Setup

1. Navigate to the ui directory:

```bash
cd ui
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Or install with optional development dependencies:

```bash
pip install -e ".[dev]"
```

## Running the Application

Start the Streamlit server:

```bash
streamlit run ui/app.py
```

The application will open in your default browser at `http://localhost:8501`.

### Command Line Options

```bash
# Run on a specific port
streamlit run ui/app.py --server.port 8502

# Run in headless mode (no browser auto-open)
streamlit run ui/app.py --server.headless true

# Run with a specific theme
streamlit run ui/app.py --theme.base dark
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEVLOOP_PATH` | Base path for Dev Loop files | `../.claude/dev` (relative to ui/) |
| `DEVLOOP_LOG_LEVEL` | Logging level | `INFO` |

### Example

```bash
# Use a custom Dev Loop path
export DEVLOOP_PATH=/path/to/your/.claude/dev
streamlit run ui/app.py
```

## Features

### Dashboard (Home)

- Overview statistics (PROMPT, PROGRESS, LOG counts)
- Status breakdown (NOT_STARTED, IN_PROGRESS, BLOCKED, COMPLETE)
- Recent activity feed

### Tasks Page

- File browser with search and filters
- Filter by status and quality tier
- Sort by name, date, status, or completion percentage
- View PROMPT details with task list and progress bar
- Link to associated PROGRESS files

### Progress Page

- List of active sessions
- Iteration history with expandable details
- Blockers display with resolution status
- Link back to source PROMPT

### Logs Page

- Chronological list of execution logs
- Date range filter
- Search within log content
- Execution statistics and key decisions

### Create Page

- Form-based PROMPT creation
- Input validation (name, goal, tasks, exit criteria)
- Dynamic task input with priority selection
- Live preview of generated markdown
- Duplicate detection

### Theme Toggle

- Light/dark mode switch in sidebar
- Preference persisted in session state

## File Structure

```
ui/
  __init__.py           # Package initialization
  app.py                # Main application entry point
  config.py             # Configuration and paths
  models.py             # Pydantic data models
  parser.py             # Markdown file parsers
  state.py              # Session state management
  requirements.txt      # Python dependencies
  pyproject.toml        # Package metadata

  components/           # Reusable UI components
    file_browser.py     # File listing and selection
    markdown_viewer.py  # Content rendering
    status_badges.py    # Status indicators
    theme.py            # Theme toggle

  pages/                # Streamlit multi-page navigation
    1_Tasks.py          # PROMPT browser
    2_Progress.py       # Session tracking
    3_Logs.py           # Execution history
    4_Create.py         # New PROMPT creation

  tests/                # Unit tests
    test_parser.py      # Parser tests
    test_progress_parser.py
    fixtures/           # Test data files

  logs/                 # Application logs
```

## Development

### Running Tests

```bash
# Run all tests
pytest ui/tests/ -v

# Run with coverage
pytest ui/tests/ -v --cov=ui --cov-report=term-missing
```

### Code Quality

```bash
# Linting
ruff check ui/

# Type checking
mypy ui/ --ignore-missing-imports
```

### Adding New Components

1. Create a new file in `ui/components/`
2. Add the component to `components/__init__.py`
3. Import and use in pages as needed

### Adding New Pages

1. Create a new file in `ui/pages/` with naming convention `N_Name.py`
2. The number prefix controls sidebar order
3. Import shared components and state utilities

## Troubleshooting

### Common Issues

#### "No PROMPT files found"

- Check that `DEVLOOP_PATH` points to a valid directory
- Ensure PROMPT files follow the naming convention: `PROMPT_*.md`
- Verify file permissions

#### "Failed to parse PROMPT"

- Check the file for valid markdown structure
- Ensure required sections exist (Goal, Tasks)
- Look for malformed YAML frontmatter

#### "Module not found" errors

- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (requires 3.11+)

#### Theme not applying

- Streamlit themes are partially controlled by `.streamlit/config.toml`
- The built-in toggle provides CSS adjustments
- For full theme control, create a config file

### Debug Mode

Enable debug logging:

```bash
export DEVLOOP_LOG_LEVEL=DEBUG
streamlit run ui/app.py
```

Check logs at: `ui/logs/devloop_ui.log`

## Architecture

### Data Flow

```
Markdown Files (.claude/dev/)
        |
        v
    Parser (parser.py)
        |
        v
    Pydantic Models (models.py)
        |
        v
    Components (components/)
        |
        v
    Streamlit Pages (pages/)
```

### Key Design Decisions

1. **ParseResult[T] Pattern** - All parsing returns success/failure instead of raising exceptions
2. **Session State** - Centralized in `state.py` for persistence across reruns
3. **Caching** - `@st.cache_data` with TTL for file operations
4. **Cross-Platform** - `pathlib.Path` for all file operations

## API Reference

### Models

- `PromptFile` - Parsed PROMPT_*.md file
- `ProgressFile` - Parsed PROGRESS_*.md file
- `LogFile` - Parsed LOG_*.md file
- `Task` - Individual task with priority and status
- `ParseResult[T]` - Generic result wrapper

### Parser Functions

- `parse_prompt_file(path) -> ParseResult[PromptFile]`
- `parse_progress_file(path) -> ParseResult[ProgressFile]`
- `parse_log_file(path) -> ParseResult[LogFile]`

### State Functions

- `init_session_state()` - Initialize all state values
- `get_state(key, default)` - Get state value
- `set_state(key, value)` - Set state value
- `get_selected_file()` - Get currently selected file

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

---

*Dev Loop UI v0.1.0*
