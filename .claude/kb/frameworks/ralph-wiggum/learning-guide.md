# Ralph Wiggum - Learning Guide

> Educational resource for mastering Ralph Wiggum concepts and applications

---

## Learning Objectives

By studying this framework, you will:

- [x] Understand iterative AI development loops and self-referential feedback patterns
- [x] Learn how to write effective prompts with clear completion criteria
- [x] Be able to implement autonomous overnight development workflows
- [x] Apply the "deterministically bad" philosophy to improve prompt engineering
- [x] Understand when to use raw iteration vs. structured development phases

---

## Prerequisites

| Prerequisite | Why Needed | Resource |
|--------------|------------|----------|
| Claude Code basics | Ralph is a Claude Code plugin | https://code.claude.com/docs/en/overview |
| Bash scripting fundamentals | Stop hook is bash-based | Any bash tutorial |
| Git workflow | Ralph tracks progress via git history | `git log`, `git diff` |
| Prompt engineering basics | Success depends on prompt quality | .claude/kb/agentic-ai (if available) |

---

## Difficulty Level

| Aspect | Level | Notes |
|--------|-------|-------|
| Conceptual | Beginner | Core idea is simple: repeat until done |
| Implementation | Intermediate | Requires understanding hooks, state files, bash |
| Time Investment | 2-4 hours | To fully understand and customize |

---

## Learning Path

### Level 1: Foundations (Beginner)

**Goal:** Understand what Ralph Wiggum is and why it matters

1. **Read the README**
   - Location: `plugins/ralph-wiggum/README.md`
   - Time: 15 min
   - Key concepts to note: Stop hook, completion promise, self-reference through files

2. **Explore the Architecture**
   - Read: `analysis.md` in this folder
   - Time: 30 min
   - Focus on: Component diagram, workflow section

3. **Try the Quick Start**
   - Instructions:
     1. Install the Ralph Wiggum plugin in Claude Code
     2. Run: `/ralph-loop "Create a file called hello.txt with 'Hello World'" --max-iterations 5 --completion-promise "FILE CREATED"`
     3. Observe Claude create the file and output the promise
   - Expected outcome: Loop terminates after Claude creates the file and outputs `<promise>FILE CREATED</promise>`

**Checkpoint:** Can you explain what Ralph Wiggum does in one sentence?
> "Ralph Wiggum is a Claude Code plugin that runs Claude in a continuous loop, re-feeding the same prompt until a completion promise is detected or max iterations reached."

---

### Level 2: Core Concepts (Intermediate)

**Goal:** Understand the key mechanisms and patterns

1. **Deep Dive: Stop Hook Mechanism**
   - What it is: A shell script that intercepts Claude's exit attempts
   - Why it matters: Creates the loop without external bash scripts
   - Code example:
   ```bash
   # From stop-hook.sh - the decision to continue or exit
   if [[ -n "$PROMISE_TEXT" ]] && [[ "$PROMISE_TEXT" = "$COMPLETION_PROMISE" ]]; then
     echo "Ralph loop: Detected <promise>$COMPLETION_PROMISE</promise>"
     rm "$RALPH_STATE_FILE"
     exit 0  # Allow exit
   fi

   # Not complete - block exit and re-prompt
   jq -n --arg prompt "$PROMPT_TEXT" '{
     "decision": "block",
     "reason": $prompt
   }'
   ```

2. **Deep Dive: State File Format**
   - What it is: Markdown with YAML frontmatter storing loop state
   - Why it matters: Enables iteration tracking and prompt persistence
   - Example:
   ```markdown
   ---
   active: true
   iteration: 3
   max_iterations: 20
   completion_promise: "ALL TESTS PASSING"
   started_at: "2026-02-03T10:00:00Z"
   ---

   Build a REST API with:
   1. GET /todos - list all
   2. POST /todos - create new
   3. Tests for each endpoint

   When all tests pass, output <promise>ALL TESTS PASSING</promise>
   ```

3. **Deep Dive: Self-Reference Pattern**
   - What it is: Claude seeing its own previous file modifications
   - Why it matters: Enables learning and self-correction without explicit memory
   - Key insight: The loop doesn't feed output as input; instead:
     - Iteration 1: Claude writes code with bugs
     - Iteration 2: Claude reads the buggy code from files, sees test failures, fixes them
     - Iteration 3: Claude reads fixed code, verifies tests pass, outputs promise

4. **Hands-on Exercise**
   - Task: Create a Ralph loop that writes a Python function with tests
   - Steps:
     1. Write a prompt that asks for a function + pytest tests
     2. Include completion criteria: "All pytest tests passing"
     3. Start the loop with `--max-iterations 10`
     4. Observe Claude iterate until tests pass
   - Success criteria: Tests pass and loop exits cleanly

**Checkpoint:** Can you implement a basic TDD workflow using Ralph Wiggum?

---

### Level 3: Advanced Patterns (Advanced)

**Goal:** Master advanced usage and edge cases

1. **Pattern: Phased Development**
   - When to use: Complex projects requiring multiple stages
   - Implementation:
   ```markdown
   Build an e-commerce API in phases:

   PHASE 1: User authentication
   - JWT tokens
   - Login/logout endpoints
   - Tests for auth
   Checkpoint: Output "PHASE 1 COMPLETE" when auth tests pass.

   PHASE 2: Product catalog
   - CRUD for products
   - Search endpoint
   - Tests for products
   Checkpoint: Output "PHASE 2 COMPLETE" when product tests pass.

   PHASE 3: Integration
   - Protected product routes
   - Full integration tests

   When all phases complete, output <promise>E-COMMERCE API COMPLETE</promise>
   ```
   - Pitfalls: Don't make phases too large; Claude may lose track

2. **Pattern: Self-Correction with Test Output**
   - When to use: Test-driven development
   - Implementation:
   ```markdown
   Implement the DateParser class following TDD:

   1. Read existing tests in tests/test_date_parser.py
   2. Run: pytest tests/test_date_parser.py -v
   3. If any tests fail:
      - Read the error messages carefully
      - Fix the implementation in src/date_parser.py
      - Run tests again
   4. Repeat until all tests pass
   5. Output <promise>ALL TESTS GREEN</promise>

   IMPORTANT: Do not modify the tests. Only fix the implementation.
   ```
   - Pitfalls: Ensure tests are correct before starting; Claude cannot fix bad tests

3. **Pattern: Escape Hatch for Stuck Loops**
   - When to use: Tasks that might be impossible
   - Implementation:
   ```markdown
   Try to implement feature X.

   After 15 iterations, if not complete:
   - Document what's blocking progress in BLOCKED.md
   - List all approaches attempted
   - Suggest alternative solutions
   - Output <promise>BLOCKED - SEE BLOCKED.md</promise>

   If successful before iteration 15:
   - Output <promise>FEATURE X COMPLETE</promise>
   ```
   - Pitfalls: Completion promise is exact match; need two separate loops or use max-iterations

4. **Real-World Exercise**
   - Scenario: You need to refactor a legacy module with poor test coverage
   - Challenge: Create a Ralph loop that:
     1. Adds tests for existing functionality
     2. Refactors the code
     3. Ensures tests still pass after refactoring
     4. Documents the changes
   - Hints: Use git commits as checkpoints; run tests after each significant change

**Checkpoint:** Can you solve a complex refactoring task using Ralph Wiggum?

---

## Key Concepts Glossary

| Term | Definition | Example |
|------|------------|---------|
| **Stop Hook** | Shell script that intercepts Claude's exit and decides whether to allow it | `hooks/stop-hook.sh` |
| **Completion Promise** | Exact phrase in `<promise>` tags that signals task completion | `<promise>DONE</promise>` |
| **State File** | Markdown file storing loop configuration and iteration count | `.claude/ralph-loop.local.md` |
| **Self-Reference** | Claude seeing its own previous work in files, not through output-input | Reading modified source files |
| **Iteration** | One complete cycle of: prompt -> work -> exit attempt -> hook check | Iteration 1, 2, 3... |
| **Deterministically Bad** | Philosophy that predictable failures enable systematic improvement | Failed test = clear next step |

---

## Common Mistakes & How to Avoid Them

### Mistake 1: Vague Completion Criteria

**What happens:** Loop runs forever because Claude doesn't know when to stop

**Why it happens:** Prompt says "make it good" without defining "good"

**How to avoid:** Always include:
- Specific success metrics (tests passing, lint clean, etc.)
- Explicit completion phrase to output
- Example of what "done" looks like

**How to fix:** Rewrite prompt with concrete criteria:
```markdown
# Bad
Build a todo API and make it good.

# Good
Build a todo API with:
- GET /todos (returns JSON array)
- POST /todos (creates item, returns 201)
- All endpoints have pytest tests
- All tests pass

When complete: <promise>TODO API COMPLETE</promise>
```

---

### Mistake 2: No Max Iterations Safety

**What happens:** Impossible tasks run forever, wasting API credits

**Why it happens:** Overconfidence that the task will complete

**How to avoid:** Always use `--max-iterations` as a safety bound

**How to fix:** Add escape hatch:
```bash
/ralph-loop "Complex task here" --max-iterations 25 --completion-promise "DONE"
```

---

### Mistake 3: Lying About Completion

**What happens:** Claude outputs the promise phrase when task is not actually complete

**Why it happens:** Claude tries to exit the loop by any means

**How to avoid:** Include explicit instruction in prompt:
```markdown
CRITICAL: Only output <promise>DONE</promise> when the statement is TRUE.
Do NOT output false statements to exit the loop.
```

---

### Mistake 4: Overly Complex Single Prompt

**What happens:** Claude loses track of requirements; inconsistent progress

**Why it happens:** Too much in one prompt

**How to avoid:** Break into phases or use multiple smaller loops

---

## Practice Exercises

### Exercise 1: Hello World Loop (Beginner)

**Objective:** Understand the basic loop mechanics

**Instructions:**
1. Create a simple prompt: "Create a file called greeting.py that prints 'Hello, Ralph!'"
2. Start the loop: `/ralph-loop "..." --completion-promise "FILE CREATED" --max-iterations 5`
3. Observe the loop behavior

**Solution:** Claude should create the file and output `<promise>FILE CREATED</promise>` on first or second iteration.

---

### Exercise 2: TDD Loop (Intermediate)

**Objective:** Practice test-driven development with Ralph

**Instructions:**
1. Create a test file first (manually): `tests/test_calculator.py`
   ```python
   def test_add():
       from calculator import add
       assert add(2, 3) == 5

   def test_subtract():
       from calculator import subtract
       assert subtract(5, 3) == 2
   ```
2. Start Ralph: `/ralph-loop "Implement calculator.py to make all tests pass. Run pytest -v. Output <promise>TESTS PASS</promise> when all green." --max-iterations 10`
3. Watch Claude iterate until tests pass

---

### Exercise 3: Overnight Refactor (Advanced)

**Objective:** Run an extended autonomous task

**Challenge:** Refactor a module to use type hints throughout

**Instructions:**
1. Identify a module without type hints
2. Create prompt:
   ```markdown
   Add type hints to all functions in src/my_module.py

   Requirements:
   - Every function parameter typed
   - Every return type annotated
   - Run mypy src/my_module.py --strict
   - Fix any mypy errors

   Output <promise>MYPY CLEAN</promise> when mypy reports no errors.
   ```
3. Start with generous iterations: `--max-iterations 50`
4. Let it run overnight if needed

---

## Transferable Skills

What you learn here applies to:

| Skill | Where Else It Applies |
|-------|----------------------|
| Writing prompts with clear completion criteria | Any LLM workflow, Jarvis Dev Loop |
| Designing self-correcting loops | CI/CD pipelines, test automation |
| State management via files | GitOps, configuration management |
| Hook-based interception | Pre-commit hooks, git workflows |
| Iteration tracking | Project management, sprint tracking |
| Truthfulness constraints in prompts | Any AI system requiring reliability |

---

## Study Resources

### Essential Reading

1. **Geoffrey Huntley's Original Post** (https://ghuntley.com/ralph/) - Philosophy and origin story
2. **Ralph Wiggum Plugin README** - Official documentation and examples

### Supplementary Materials

- The Register article on Ralph Wiggum: https://www.theregister.com/2026/01/27/ralph_wiggum_claude_loops/
- Sivaramp blog post on running AI agents for hours: https://blog.sivaramp.com/blog/claude-code-the-ralph-wiggum-approach/
- HumanLayer blog: Brief history of Ralph: https://www.humanlayer.dev/blog/brief-history-of-ralph

### Community Resources

- Claude Developers Discord: https://anthropic.com/discord
- Ralph Orchestrator (external tool): https://github.com/mikeyobrien/ralph-orchestrator

---

## Self-Assessment

### Quiz Yourself

1. What problem does Ralph Wiggum solve?
   > Single-shot AI limitations; enables continuous self-correcting iteration

2. How does the self-reference mechanism work?
   > Claude reads its own previous file modifications; not output-to-input feedback

3. When would you use Ralph Wiggum vs. Jarvis Dev Loop?
   > Ralph: simple, well-defined tasks; unattended overnight execution
   > Jarvis: complex tasks requiring multiple specialists; interactive development

4. What are the main trade-offs of Ralph Wiggum?
   > Pro: Simplicity, overnight execution, cost efficiency
   > Con: No semantic completion detection, exact string matching only, requires good prompts

### Practical Assessment

Build: A Ralph loop that creates a complete CLI tool with tests

Success criteria:
- [x] Tool has at least 3 subcommands
- [x] Each subcommand has pytest tests
- [x] All tests pass
- [x] Help text is generated
- [x] Loop exits via completion promise, not max iterations

---

## What's Next?

After mastering Ralph Wiggum, consider:

1. **Apply to Jarvis:** See `jarvis-integration.md` for integration ideas
   - Add completion promises to Dev Loop
   - Implement iteration counters
   - Enhance verify-before-completion with truthfulness

2. **Related Frameworks:** Study these for comparison:
   - **Jarvis Dev Loop** - Structured iteration with phases
   - **SWARM/Sandbox mode** - Multi-agent orchestration
   - **feature-dev plugin** - 7-phase development workflow

3. **Advanced Topics:**
   - Parallel loops with git worktrees
   - Chaining multiple Ralph loops
   - Custom stop hooks for specialized workflows
   - Integrating with CI/CD for nightly runs

---

*Learning guide created: 2026-02-03 | For: Ralph Wiggum*
