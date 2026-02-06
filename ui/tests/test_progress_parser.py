"""Tests for PROGRESS file parsing.

This module tests the parse_progress_file function.
All tests use fixtures from ui/tests/fixtures/.
"""

from __future__ import annotations

# Add ui to path for imports
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ui.models import ParseResult, TaskStatus
from ui.parser import parse_progress_file

# =============================================================================
# Fixtures
# =============================================================================

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def valid_progress_path() -> Path:
    """Path to a complete valid PROGRESS file."""
    return FIXTURES_DIR / "valid_progress.md"


# =============================================================================
# Test parse_progress_file - Basic Functionality
# =============================================================================


class TestParseProgressFileBasic:
    """Basic tests for parse_progress_file function."""

    def test_parse_valid_progress(self, valid_progress_path: Path) -> None:
        """Should successfully parse a valid PROGRESS file."""
        result = parse_progress_file(valid_progress_path)
        assert result.is_success
        progress = result.value
        assert progress.name == "VALID_TEST"

    def test_parse_returns_parse_result(self, valid_progress_path: Path) -> None:
        """Should return a ParseResult object."""
        result = parse_progress_file(valid_progress_path)
        assert isinstance(result, ParseResult)

    def test_parse_nonexistent_file(self) -> None:
        """Should return failure for non-existent file."""
        result = parse_progress_file(Path("/nonexistent/progress.md"))
        assert result.is_failure
        assert "not found" in result.error.lower()

    def test_file_path_stored(self, valid_progress_path: Path) -> None:
        """Should store the file path in the result."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        assert progress.file_path == valid_progress_path


# =============================================================================
# Test parse_progress_file - Summary Metrics
# =============================================================================


class TestParseProgressSummary:
    """Tests for summary metrics extraction."""

    def test_extracts_status(self, valid_progress_path: Path) -> None:
        """Should extract the status from summary."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        assert progress.status == TaskStatus.IN_PROGRESS

    def test_extracts_tasks_completed(self, valid_progress_path: Path) -> None:
        """Should extract tasks completed count."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        assert progress.tasks_completed == 3

    def test_extracts_total_tasks(self, valid_progress_path: Path) -> None:
        """Should extract total tasks count."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        assert progress.total_tasks == 7

    def test_extracts_current_iteration(self, valid_progress_path: Path) -> None:
        """Should extract current iteration number."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        assert progress.current_iteration == 4

    def test_extracts_started_timestamp(self, valid_progress_path: Path) -> None:
        """Should extract started timestamp."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        assert progress.started is not None
        assert progress.started.year == 2026

    def test_extracts_last_updated_timestamp(self, valid_progress_path: Path) -> None:
        """Should extract last updated timestamp."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        assert progress.last_updated is not None


# =============================================================================
# Test parse_progress_file - Iteration Log
# =============================================================================


class TestParseProgressIterationLog:
    """Tests for iteration log extraction."""

    def test_extracts_iteration_log(self, valid_progress_path: Path) -> None:
        """Should extract iteration log entries."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        assert len(progress.iteration_log) >= 1

    def test_iteration_has_number(self, valid_progress_path: Path) -> None:
        """Should extract iteration number."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        if progress.iteration_log:
            assert progress.iteration_log[0].iteration == 1

    def test_iteration_has_task(self, valid_progress_path: Path) -> None:
        """Should extract task description from iteration."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        if progress.iteration_log:
            assert progress.iteration_log[0].task

    def test_iteration_has_status(self, valid_progress_path: Path) -> None:
        """Should extract status from iteration."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        if progress.iteration_log:
            assert progress.iteration_log[0].status in ["COMPLETE", "IN_PROGRESS", "FAIL"]


# =============================================================================
# Test parse_progress_file - Blockers
# =============================================================================


class TestParseProgressBlockers:
    """Tests for blocker extraction."""

    def test_extracts_blockers(self, valid_progress_path: Path) -> None:
        """Should extract blockers from table."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        assert len(progress.blockers) >= 1

    def test_blocker_has_description(self, valid_progress_path: Path) -> None:
        """Should extract blocker description."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        if progress.blockers:
            assert progress.blockers[0].description

    def test_resolved_blocker(self, valid_progress_path: Path) -> None:
        """Should identify resolved blockers."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        resolved = [b for b in progress.blockers if b.is_resolved]
        assert len(resolved) >= 1

    def test_unresolved_blocker(self, valid_progress_path: Path) -> None:
        """Should identify unresolved blockers."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        unresolved = [b for b in progress.blockers if not b.is_resolved]
        # Check active_blockers computed field
        assert len(progress.active_blockers) == len(unresolved)


# =============================================================================
# Test parse_progress_file - Computed Fields
# =============================================================================


class TestParseProgressComputedFields:
    """Tests for computed fields on ProgressFile."""

    def test_completion_percentage(self, valid_progress_path: Path) -> None:
        """Should compute completion percentage."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        # 3 out of 7 = ~42.9%
        assert 42 <= progress.completion_percentage <= 43

    def test_has_blockers(self, valid_progress_path: Path) -> None:
        """Should compute has_blockers flag."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        # The fixture has one unresolved blocker
        assert progress.has_blockers is True


# =============================================================================
# Test parse_progress_file - Raw Content
# =============================================================================


class TestParseProgressRawContent:
    """Tests for raw content preservation."""

    def test_stores_raw_content(self, valid_progress_path: Path) -> None:
        """Should store the raw markdown content."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        assert progress.raw_content
        assert "# PROGRESS:" in progress.raw_content

    def test_raw_content_complete(self, valid_progress_path: Path) -> None:
        """Should store complete raw content."""
        result = parse_progress_file(valid_progress_path)
        progress = result.value
        assert "## Summary" in progress.raw_content
        assert "## Iteration Log" in progress.raw_content


# =============================================================================
# Test parse_progress_file - Error Handling
# =============================================================================


class TestParseProgressErrorHandling:
    """Tests for error handling in parse_progress_file."""

    def test_returns_failure_not_raises(self) -> None:
        """Should return ParseResult.failure instead of raising exceptions."""
        result = parse_progress_file(Path("/nonexistent/file.md"))
        assert result.is_failure
        assert isinstance(result.error, str)

    def test_handles_empty_sections(self, tmp_path: Path) -> None:
        """Should handle PROGRESS with empty sections."""
        test_file = tmp_path / "PROGRESS_EMPTY.md"
        test_file.write_text("""# PROGRESS: EMPTY

## Summary

| Metric | Value |
|--------|-------|
| **Status** | NOT_STARTED |

## Iteration Log

## Blockers

| Blocker | Iteration | Resolution |
|---------|-----------|------------|
| - | - | - |
""")
        result = parse_progress_file(test_file)
        assert result.is_success
        progress = result.value
        assert progress.status == TaskStatus.NOT_STARTED
