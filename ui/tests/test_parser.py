"""Tests for PROMPT file parsing.

This module tests the parse_prompt_file function and related utilities.
All tests use fixtures from ui/tests/fixtures/.
"""

from __future__ import annotations

# Add ui to path for imports
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ui.models import ParseResult, QualityTier, TaskPriority, TaskStatus
from ui.parser import parse_prompt_file, read_file

# =============================================================================
# Fixtures
# =============================================================================

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def valid_prompt_path() -> Path:
    """Path to a complete valid PROMPT file."""
    return FIXTURES_DIR / "valid_prompt.md"


@pytest.fixture
def minimal_prompt_path() -> Path:
    """Path to a minimal PROMPT file."""
    return FIXTURES_DIR / "minimal_prompt.md"


@pytest.fixture
def malformed_frontmatter_path() -> Path:
    """Path to a PROMPT with invalid YAML frontmatter."""
    return FIXTURES_DIR / "malformed_frontmatter.md"


@pytest.fixture
def empty_tasks_path() -> Path:
    """Path to a PROMPT with no tasks."""
    return FIXTURES_DIR / "empty_tasks_prompt.md"


@pytest.fixture
def unicode_prompt_path() -> Path:
    """Path to a PROMPT with unicode content."""
    return FIXTURES_DIR / "unicode_prompt.md"


@pytest.fixture
def missing_sections_path() -> Path:
    """Path to a PROMPT with missing optional sections."""
    return FIXTURES_DIR / "missing_sections_prompt.md"


# =============================================================================
# Test read_file
# =============================================================================


class TestReadFile:
    """Tests for the read_file function."""

    def test_read_existing_file(self, valid_prompt_path: Path) -> None:
        """Should successfully read an existing file."""
        result = read_file(valid_prompt_path)
        assert result.is_success
        assert "PROMPT: VALID_TEST" in result.value

    def test_read_nonexistent_file(self) -> None:
        """Should return failure for non-existent file."""
        result = read_file(Path("/nonexistent/file.md"))
        assert result.is_failure
        assert "not found" in result.error.lower()

    def test_read_directory_fails(self, tmp_path: Path) -> None:
        """Should return failure when path is a directory."""
        result = read_file(tmp_path)
        assert result.is_failure
        assert "not a file" in result.error.lower()


# =============================================================================
# Test parse_prompt_file - Basic Functionality
# =============================================================================


class TestParsePromptFileBasic:
    """Basic tests for parse_prompt_file function."""

    def test_parse_valid_prompt(self, valid_prompt_path: Path) -> None:
        """Should successfully parse a valid PROMPT file."""
        result = parse_prompt_file(valid_prompt_path)
        assert result.is_success
        prompt = result.value
        assert prompt.name == "VALID_TEST"

    def test_parse_returns_parse_result(self, valid_prompt_path: Path) -> None:
        """Should return a ParseResult object."""
        result = parse_prompt_file(valid_prompt_path)
        assert isinstance(result, ParseResult)

    def test_parse_nonexistent_file(self) -> None:
        """Should return failure for non-existent file."""
        result = parse_prompt_file(Path("/nonexistent/prompt.md"))
        assert result.is_failure
        assert "not found" in result.error.lower()

    def test_parse_minimal_prompt(self, minimal_prompt_path: Path) -> None:
        """Should parse a minimal PROMPT with only required sections."""
        result = parse_prompt_file(minimal_prompt_path)
        assert result.is_success
        prompt = result.value
        assert prompt.name == "MINIMAL_TEST"
        assert len(prompt.tasks) == 1


# =============================================================================
# Test parse_prompt_file - Goal Extraction
# =============================================================================


class TestParsePromptGoal:
    """Tests for goal extraction from PROMPT files."""

    def test_extracts_goal(self, valid_prompt_path: Path) -> None:
        """Should extract the goal statement."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        assert "test feature" in prompt.goal.lower()

    def test_minimal_prompt_goal(self, minimal_prompt_path: Path) -> None:
        """Should extract goal from minimal prompt."""
        result = parse_prompt_file(minimal_prompt_path)
        prompt = result.value
        assert "minimal" in prompt.goal.lower()

    def test_empty_goal_handled(self, missing_sections_path: Path) -> None:
        """Should handle PROMPT with goal present."""
        result = parse_prompt_file(missing_sections_path)
        prompt = result.value
        assert prompt.goal  # Goal exists


# =============================================================================
# Test parse_prompt_file - Quality Tier
# =============================================================================


class TestParsePromptQualityTier:
    """Tests for quality tier extraction."""

    def test_extracts_production_tier(self, valid_prompt_path: Path) -> None:
        """Should extract production quality tier."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        assert prompt.quality_tier == QualityTier.PRODUCTION

    def test_extracts_prototype_tier(self, empty_tasks_path: Path) -> None:
        """Should extract prototype quality tier."""
        result = parse_prompt_file(empty_tasks_path)
        prompt = result.value
        assert prompt.quality_tier == QualityTier.PROTOTYPE

    def test_defaults_to_production(self, minimal_prompt_path: Path) -> None:
        """Should default to production tier when not specified."""
        result = parse_prompt_file(minimal_prompt_path)
        prompt = result.value
        assert prompt.quality_tier == QualityTier.PRODUCTION


# =============================================================================
# Test parse_prompt_file - Task Parsing
# =============================================================================


class TestParsePromptTasks:
    """Tests for task parsing from PROMPT files."""

    def test_parses_all_tasks(self, valid_prompt_path: Path) -> None:
        """Should parse all tasks from all priority sections."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        assert len(prompt.tasks) == 7

    def test_parses_risky_tasks(self, valid_prompt_path: Path) -> None:
        """Should correctly identify RISKY priority tasks."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        risky_tasks = prompt.risky_tasks
        assert len(risky_tasks) == 2
        assert all(t.priority == TaskPriority.RISKY for t in risky_tasks)

    def test_parses_core_tasks(self, valid_prompt_path: Path) -> None:
        """Should correctly identify CORE priority tasks."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        core_tasks = prompt.core_tasks
        assert len(core_tasks) == 3
        assert all(t.priority == TaskPriority.CORE for t in core_tasks)

    def test_parses_polish_tasks(self, valid_prompt_path: Path) -> None:
        """Should correctly identify POLISH priority tasks."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        polish_tasks = prompt.polish_tasks
        assert len(polish_tasks) == 2
        assert all(t.priority == TaskPriority.POLISH for t in polish_tasks)

    def test_parses_completed_tasks(self, valid_prompt_path: Path) -> None:
        """Should correctly identify completed tasks."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        completed = [t for t in prompt.tasks if t.completed]
        assert len(completed) == 2

    def test_parses_incomplete_tasks(self, valid_prompt_path: Path) -> None:
        """Should correctly identify incomplete tasks."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        incomplete = [t for t in prompt.tasks if not t.completed]
        assert len(incomplete) == 5

    def test_empty_tasks_handled(self, empty_tasks_path: Path) -> None:
        """Should handle PROMPT with no tasks."""
        result = parse_prompt_file(empty_tasks_path)
        prompt = result.value
        assert len(prompt.tasks) == 0

    def test_parses_plain_text_headers(self, minimal_prompt_path: Path) -> None:
        """Should parse tasks with plain text priority headers."""
        result = parse_prompt_file(minimal_prompt_path)
        prompt = result.value
        assert len(prompt.tasks) == 1
        assert prompt.tasks[0].priority == TaskPriority.RISKY


# =============================================================================
# Test parse_prompt_file - Agent References
# =============================================================================


class TestParsePromptAgentRefs:
    """Tests for agent reference extraction."""

    def test_extracts_agent_reference(self, valid_prompt_path: Path) -> None:
        """Should extract @agent references from tasks."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        tasks_with_agents = [t for t in prompt.tasks if t.agent_ref]
        assert len(tasks_with_agents) >= 2

    def test_agent_reference_value(self, valid_prompt_path: Path) -> None:
        """Should correctly parse agent reference name."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        tasks_with_agents = [t for t in prompt.tasks if t.agent_ref]
        agent_refs = [t.agent_ref for t in tasks_with_agents]
        assert "python-developer" in agent_refs
        assert "test-generator" in agent_refs

    def test_task_without_agent(self, valid_prompt_path: Path) -> None:
        """Should handle tasks without agent references."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        tasks_without_agents = [t for t in prompt.tasks if not t.agent_ref]
        assert len(tasks_without_agents) >= 1


# =============================================================================
# Test parse_prompt_file - Status
# =============================================================================


class TestParsePromptStatus:
    """Tests for status extraction."""

    def test_extracts_in_progress_status(self, valid_prompt_path: Path) -> None:
        """Should extract IN_PROGRESS status."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        assert prompt.status == TaskStatus.IN_PROGRESS

    def test_extracts_not_started_status(self, empty_tasks_path: Path) -> None:
        """Should extract NOT_STARTED status."""
        result = parse_prompt_file(empty_tasks_path)
        prompt = result.value
        assert prompt.status == TaskStatus.NOT_STARTED

    def test_defaults_to_not_started(self, minimal_prompt_path: Path) -> None:
        """Should default to NOT_STARTED when status not specified."""
        result = parse_prompt_file(minimal_prompt_path)
        prompt = result.value
        assert prompt.status == TaskStatus.NOT_STARTED


# =============================================================================
# Test parse_prompt_file - Computed Fields
# =============================================================================


class TestParsePromptComputedFields:
    """Tests for computed fields on PromptFile."""

    def test_task_count(self, valid_prompt_path: Path) -> None:
        """Should compute total task count."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        assert prompt.task_count == 7

    def test_completed_count(self, valid_prompt_path: Path) -> None:
        """Should compute completed task count."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        assert prompt.completed_count == 2

    def test_completion_percentage(self, valid_prompt_path: Path) -> None:
        """Should compute completion percentage."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        # 2 completed out of 7 = ~28.6%
        assert 28 <= prompt.completion_percentage <= 29

    def test_completion_percentage_empty(self, empty_tasks_path: Path) -> None:
        """Should handle zero tasks for completion percentage."""
        result = parse_prompt_file(empty_tasks_path)
        prompt = result.value
        assert prompt.completion_percentage == 0.0


# =============================================================================
# Test parse_prompt_file - Exit Criteria
# =============================================================================


class TestParsePromptExitCriteria:
    """Tests for exit criteria extraction."""

    def test_extracts_exit_criteria(self, valid_prompt_path: Path) -> None:
        """Should extract exit criteria."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        assert len(prompt.exit_criteria) == 3

    def test_exit_criteria_status(self, valid_prompt_path: Path) -> None:
        """Should correctly parse exit criteria completion status."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        met_criteria = [c for c in prompt.exit_criteria if c.met]
        assert len(met_criteria) == 1  # Only "All tests pass" is checked


# =============================================================================
# Test parse_prompt_file - Error Handling
# =============================================================================


class TestParsePromptErrorHandling:
    """Tests for error handling in parse_prompt_file."""

    def test_malformed_frontmatter_graceful(self, malformed_frontmatter_path: Path) -> None:
        """Should handle malformed YAML frontmatter gracefully."""
        result = parse_prompt_file(malformed_frontmatter_path)
        # Should still succeed - malformed frontmatter is ignored
        assert result.is_success
        prompt = result.value
        assert prompt.name == "MALFORMED_FRONTMATTER"

    def test_returns_failure_not_raises(self) -> None:
        """Should return ParseResult.failure instead of raising exceptions."""
        result = parse_prompt_file(Path("/nonexistent/file.md"))
        assert result.is_failure
        assert isinstance(result.error, str)

    def test_file_path_stored(self, valid_prompt_path: Path) -> None:
        """Should store the file path in the result."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        assert prompt.file_path == valid_prompt_path


# =============================================================================
# Test parse_prompt_file - Unicode
# =============================================================================


class TestParsePromptUnicode:
    """Tests for unicode handling in PROMPT files."""

    def test_unicode_goal(self, unicode_prompt_path: Path) -> None:
        """Should handle unicode in goal."""
        result = parse_prompt_file(unicode_prompt_path)
        assert result.is_success
        prompt = result.value
        assert "日本語" in prompt.goal or "中文" in prompt.goal

    def test_unicode_tasks(self, unicode_prompt_path: Path) -> None:
        """Should handle unicode in tasks."""
        result = parse_prompt_file(unicode_prompt_path)
        prompt = result.value
        assert len(prompt.tasks) >= 1

    def test_emoji_in_content(self, unicode_prompt_path: Path) -> None:
        """Should handle emojis in content."""
        result = parse_prompt_file(unicode_prompt_path)
        assert result.is_success


# =============================================================================
# Test parse_prompt_file - Raw Content
# =============================================================================


class TestParsePromptRawContent:
    """Tests for raw content preservation."""

    def test_stores_raw_content(self, valid_prompt_path: Path) -> None:
        """Should store the raw markdown content."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        assert prompt.raw_content
        assert "# PROMPT: VALID_TEST" in prompt.raw_content

    def test_raw_content_complete(self, valid_prompt_path: Path) -> None:
        """Should store complete raw content."""
        result = parse_prompt_file(valid_prompt_path)
        prompt = result.value
        # Check that various sections are in raw content
        assert "## Goal" in prompt.raw_content
        assert "## Tasks" in prompt.raw_content
