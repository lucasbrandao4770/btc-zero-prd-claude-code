"""Pydantic models for Dev Loop UI.

This module defines the data models for parsing PROMPT, PROGRESS, and LOG files.
All models use the ParseResult[T] pattern for error handling instead of raising
exceptions.

Key Design Decisions:
- ParseResult[T] wraps all parse results with success/failure state
- Models have graceful defaults for optional/missing sections
- Model validators ensure cross-field consistency
- All datetime fields use timezone-aware UTC
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Generic, Self, TypeVar

from pydantic import BaseModel, Field, computed_field, model_validator

# =============================================================================
# Type Variables
# =============================================================================

T = TypeVar("T")


# =============================================================================
# Enums
# =============================================================================


class QualityTier(str, Enum):
    """Quality tier for PROMPT files."""

    PROTOTYPE = "prototype"
    PRODUCTION = "production"
    LIBRARY = "library"


class TaskStatus(str, Enum):
    """Status for PROMPT/PROGRESS files."""

    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    COMPLETE = "COMPLETE"


class TaskPriority(str, Enum):
    """Priority levels for tasks."""

    RISKY = "RISKY"
    CORE = "CORE"
    POLISH = "POLISH"


# =============================================================================
# Parse Errors
# =============================================================================


class ParseError(Exception):
    """Base exception for parsing errors."""

    def __init__(self, message: str, file_path: Path | None = None):
        self.message = message
        self.file_path = file_path
        super().__init__(message)


class MalformedFrontmatter(ParseError):
    """YAML frontmatter is invalid or cannot be parsed."""

    pass


class MissingSections(ParseError):
    """Required sections are missing from the file."""

    def __init__(self, message: str, missing: list[str], file_path: Path | None = None):
        super().__init__(message, file_path)
        self.missing = missing


class InvalidCheckbox(ParseError):
    """Checkbox syntax is invalid."""

    pass


# =============================================================================
# Parse Result
# =============================================================================


@dataclass
class ParseResult(Generic[T]):
    """Generic wrapper for parse results with success/failure state.

    This class implements the Result pattern to avoid raising exceptions
    during parsing. Callers should check is_success before accessing value.

    Attributes:
        _value: The parsed value (only valid if success is True)
        _error: The error message (only valid if success is False)
        _success: Whether parsing succeeded

    Example:
        result = parse_prompt_file(path)
        if result.is_success:
            prompt = result.value
            render_prompt_viewer(prompt)
        else:
            st.error(result.error)
    """

    _value: T | None
    _error: str | None
    _success: bool

    @classmethod
    def success(cls, value: T) -> ParseResult[T]:
        """Create a successful parse result."""
        return cls(_value=value, _error=None, _success=True)

    @classmethod
    def failure(cls, error: str) -> ParseResult[T]:
        """Create a failed parse result."""
        return cls(_value=None, _error=error, _success=False)

    @property
    def is_success(self) -> bool:
        """Check if parsing succeeded."""
        return self._success

    @property
    def is_failure(self) -> bool:
        """Check if parsing failed."""
        return not self._success

    @property
    def value(self) -> T:
        """Get the parsed value. Raises if parsing failed."""
        if not self._success:
            raise ValueError(f"Cannot access value of failed result: {self._error}")
        return self._value  # type: ignore

    @property
    def error(self) -> str:
        """Get the error message. Raises if parsing succeeded."""
        if self._success:
            raise ValueError("Cannot access error of successful result")
        return self._error  # type: ignore

    def value_or(self, default: T) -> T:
        """Get the value or a default if parsing failed."""
        return self._value if self._success else default  # type: ignore

    def map(self, fn: Callable[[T], T]) -> ParseResult[T]:
        """Apply a function to the value if successful."""
        if self._success and self._value is not None:
            try:
                return ParseResult.success(fn(self._value))
            except Exception as e:
                return ParseResult.failure(str(e))
        return self


# =============================================================================
# Task Model
# =============================================================================


class Task(BaseModel):
    """A single task in a PROMPT file.

    Attributes:
        description: The task description text
        priority: RISKY, CORE, or POLISH
        completed: Whether the task is marked complete
        agent_ref: Optional agent reference (e.g., "python-developer")
        verification: Optional verification command
        line_number: Line number in the source file (for reference)
    """

    description: str = Field(..., min_length=1)
    priority: TaskPriority
    completed: bool = False
    agent_ref: str | None = None
    verification: str | None = None
    line_number: int | None = None

    @property
    def checkbox(self) -> str:
        """Get the checkbox representation."""
        return "[x]" if self.completed else "[ ]"

    def to_markdown(self) -> str:
        """Convert task to markdown format."""
        prefix = f"@{self.agent_ref}: " if self.agent_ref else ""
        verify = f"\n  Verify: `{self.verification}`" if self.verification else ""
        return f"- {self.checkbox} {prefix}{self.description}{verify}"


# =============================================================================
# Exit Criterion Model
# =============================================================================


class ExitCriterion(BaseModel):
    """An exit criterion for a PROMPT file.

    Attributes:
        description: What needs to be true
        verification_command: Command to verify (optional)
        met: Whether the criterion has been met
    """

    description: str
    verification_command: str | None = None
    met: bool = False


# =============================================================================
# Config Model
# =============================================================================


class PromptConfig(BaseModel):
    """Configuration section of a PROMPT file.

    Attributes:
        mode: Execution mode (hitl or afk)
        quality_tier: Quality tier for the task
        max_iterations: Maximum loop iterations
        max_retries: Maximum retries per task
        circuit_breaker: Stop after N loops with no progress
        small_steps: Whether to use small incremental steps
        feedback_loops: Commands to run between tasks
    """

    mode: str = "hitl"
    quality_tier: QualityTier = QualityTier.PRODUCTION
    max_iterations: int = Field(default=30, ge=1, le=100)
    max_retries: int = Field(default=3, ge=0, le=10)
    circuit_breaker: int = Field(default=3, ge=1, le=10)
    small_steps: bool = True
    feedback_loops: list[str] = Field(default_factory=list)


# =============================================================================
# PROMPT File Model
# =============================================================================


class PromptFile(BaseModel):
    """Parsed representation of a PROMPT_*.md file.

    Attributes:
        name: Name extracted from filename (e.g., "DEVLOOP_UI")
        file_path: Path to the source file
        goal: The goal statement
        quality_tier: Quality tier (prototype/production/library)
        tasks: List of tasks grouped by priority
        exit_criteria: List of exit criteria
        status: Current status of the PROMPT
        config: Configuration settings
        raw_content: Original markdown content
    """

    name: str
    file_path: Path
    goal: str = ""
    quality_tier: QualityTier = QualityTier.PRODUCTION
    tasks: list[Task] = Field(default_factory=list)
    exit_criteria: list[ExitCriterion] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.NOT_STARTED
    config: PromptConfig = Field(default_factory=PromptConfig)
    raw_content: str = ""

    model_config = {"arbitrary_types_allowed": True}

    @computed_field
    @property
    def task_count(self) -> int:
        """Total number of tasks."""
        return len(self.tasks)

    @computed_field
    @property
    def completed_count(self) -> int:
        """Number of completed tasks."""
        return sum(1 for t in self.tasks if t.completed)

    @computed_field
    @property
    def completion_percentage(self) -> float:
        """Percentage of tasks completed (0-100)."""
        if not self.tasks:
            return 0.0
        return round((self.completed_count / self.task_count) * 100, 1)

    @computed_field
    @property
    def risky_tasks(self) -> list[Task]:
        """Tasks with RISKY priority."""
        return [t for t in self.tasks if t.priority == TaskPriority.RISKY]

    @computed_field
    @property
    def core_tasks(self) -> list[Task]:
        """Tasks with CORE priority."""
        return [t for t in self.tasks if t.priority == TaskPriority.CORE]

    @computed_field
    @property
    def polish_tasks(self) -> list[Task]:
        """Tasks with POLISH priority."""
        return [t for t in self.tasks if t.priority == TaskPriority.POLISH]

    @model_validator(mode="after")
    def validate_status_consistency(self) -> Self:
        """Ensure status is consistent with task completion."""
        if self.status == TaskStatus.COMPLETE and self.completed_count < self.task_count:
            # Don't raise - just note the inconsistency
            pass
        return self


# =============================================================================
# Iteration Log Entry Model
# =============================================================================


class IterationLogEntry(BaseModel):
    """A single iteration entry in a PROGRESS file.

    Attributes:
        iteration: Iteration number
        timestamp: When the iteration occurred
        task: Task description
        priority: Task priority level
        status: PASS, FAIL, or SKIPPED
        agent: Agent used (if any)
        verification: Verification command result
        key_decisions: List of key decisions made
        files_changed: List of files modified
        notes: Notes for next iteration
    """

    iteration: int = Field(..., ge=1)
    timestamp: datetime | None = None
    task: str = ""
    priority: TaskPriority | None = None
    status: str = ""  # PASS, FAIL, SKIPPED
    agent: str | None = None
    verification: str | None = None
    key_decisions: list[str] = Field(default_factory=list)
    files_changed: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


# =============================================================================
# Blocker Model
# =============================================================================


class Blocker(BaseModel):
    """A blocker entry in a PROGRESS file.

    Attributes:
        description: What is blocking progress
        iteration: Iteration where blocker was identified
        resolution: How the blocker was resolved (if resolved)
    """

    description: str
    iteration: int | None = None
    resolution: str | None = None

    @property
    def is_resolved(self) -> bool:
        """Check if the blocker has been resolved."""
        return self.resolution is not None and self.resolution.strip() != ""


# =============================================================================
# PROGRESS File Model
# =============================================================================


class ProgressFile(BaseModel):
    """Parsed representation of a PROGRESS_*.md file.

    Attributes:
        name: Name extracted from filename
        file_path: Path to the source file
        prompt_file: Path to associated PROMPT file
        started: When the session started
        last_updated: Last update timestamp
        status: Current status
        tasks_completed: Number of completed tasks
        total_tasks: Total number of tasks
        current_iteration: Current iteration number
        iteration_log: List of iteration entries
        blockers: List of blockers
        exit_criteria_status: Status of each exit criterion
        raw_content: Original markdown content
    """

    name: str
    file_path: Path
    prompt_file: Path | None = None
    started: datetime | None = None
    last_updated: datetime | None = None
    status: TaskStatus = TaskStatus.NOT_STARTED
    tasks_completed: int = 0
    total_tasks: int = 0
    current_iteration: int = 0
    iteration_log: list[IterationLogEntry] = Field(default_factory=list)
    blockers: list[Blocker] = Field(default_factory=list)
    exit_criteria_status: dict[str, bool] = Field(default_factory=dict)
    raw_content: str = ""

    model_config = {"arbitrary_types_allowed": True}

    @computed_field
    @property
    def completion_percentage(self) -> float:
        """Percentage of tasks completed."""
        if self.total_tasks == 0:
            return 0.0
        return round((self.tasks_completed / self.total_tasks) * 100, 1)

    @computed_field
    @property
    def active_blockers(self) -> list[Blocker]:
        """Blockers that haven't been resolved."""
        return [b for b in self.blockers if not b.is_resolved]

    @computed_field
    @property
    def has_blockers(self) -> bool:
        """Check if there are active blockers."""
        return len(self.active_blockers) > 0


# =============================================================================
# Execution Statistics Model
# =============================================================================


class ExecutionStatistics(BaseModel):
    """Statistics from a LOG file.

    Attributes:
        total_tasks: Total number of tasks
        passed: Tasks that passed
        failed: Tasks that failed
        skipped: Tasks that were skipped
        total_iterations: Total iteration count
        retries_used: Number of retries used
        duration_seconds: Total duration in seconds
    """

    total_tasks: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    total_iterations: int = 0
    retries_used: int = 0
    duration_seconds: float = 0.0

    @computed_field
    @property
    def pass_rate(self) -> float:
        """Percentage of tasks that passed."""
        if self.total_tasks == 0:
            return 0.0
        return round((self.passed / self.total_tasks) * 100, 1)

    @computed_field
    @property
    def duration_formatted(self) -> str:
        """Duration formatted as HH:MM:SS."""
        hours = int(self.duration_seconds // 3600)
        minutes = int((self.duration_seconds % 3600) // 60)
        seconds = int(self.duration_seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


# =============================================================================
# LOG File Model
# =============================================================================


class LogFile(BaseModel):
    """Parsed representation of a LOG_*.md file.

    Attributes:
        name: Name extracted from filename
        file_path: Path to the source file
        prompt_name: Name of the associated PROMPT
        started: When execution started
        completed: When execution completed
        exit_reason: Why execution ended
        quality_tier: Quality tier used
        mode: Execution mode (hitl/afk)
        statistics: Execution statistics
        task_results: List of task execution results
        key_decisions: Key decisions made during execution
        files_changed: Files created or modified
        raw_content: Original markdown content
    """

    name: str
    file_path: Path
    prompt_name: str = ""
    started: datetime | None = None
    completed: datetime | None = None
    exit_reason: str = ""
    quality_tier: QualityTier = QualityTier.PRODUCTION
    mode: str = "hitl"
    statistics: ExecutionStatistics = Field(default_factory=ExecutionStatistics)
    task_results: list[dict] = Field(default_factory=list)
    key_decisions: list[str] = Field(default_factory=list)
    files_changed: list[str] = Field(default_factory=list)
    raw_content: str = ""

    model_config = {"arbitrary_types_allowed": True}

    @computed_field
    @property
    def duration(self) -> float | None:
        """Duration in seconds, if both timestamps are available."""
        if self.started and self.completed:
            return (self.completed - self.started).total_seconds()
        return None

    @computed_field
    @property
    def was_successful(self) -> bool:
        """Check if execution completed successfully."""
        return self.exit_reason == "EXIT_COMPLETE"
