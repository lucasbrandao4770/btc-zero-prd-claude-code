# Supermemory - Jarvis Integration Analysis

> Evaluating Supermemory for integration with or inspiration for Jarvis system

---

## Integration Summary

| Aspect | Assessment |
|--------|------------|
| **Integration Difficulty** | Medium |
| **Value to Jarvis** | High |
| **Conflict Level** | Minor |
| **Recommendation** | **Learn From** |

---

## Comparison Matrix

### Feature-by-Feature

| Feature | Supermemory | Jarvis Current | Winner | Notes |
|---------|-------------|----------------|--------|-------|
| **Memory Storage** | Cloud API (Supermemory.ai) | Local SQLite via jarvis-crud | Jarvis | Local storage is faster, no API costs, works offline |
| **Semantic Search** | Hybrid (vectors + profile + keyword) | None (exact match only) | Supermemory | Jarvis lacks semantic retrieval |
| **Session Capture** | Hook-based (Stop event) | Manual via `/memory` command | Supermemory | Automatic is less friction |
| **Context Injection** | SessionStart hook | PreCompact/UserPromptSubmit hooks | Tie | Both use hooks effectively |
| **Profile Extraction** | Automatic (static + dynamic facts) | Manual (user-defined goals, config) | Supermemory | Auto-extraction reduces burden |
| **Project Isolation** | Container tags (SHA256 of git root) | None (global database) | Supermemory | Jarvis memories are global |
| **Cost** | $9+/month (Pro required) | Free (local) | Jarvis | No recurring costs |
| **Offline Support** | No | Yes | Jarvis | Critical for air-gapped environments |
| **Multi-modal** | Text only | Text only | Tie | Neither handles images/files |
| **Data Ownership** | Cloud (Supermemory owns) | Local (user owns) | Jarvis | Privacy and compliance |

### Architectural Comparison

| Aspect | Supermemory | Jarvis |
|--------|-------------|--------|
| **Core Philosophy** | "Continuity over memory" - context should flow across sessions | "Persistence via explicit capture" - user controls what's saved |
| **State Management** | Cloud-first with local cache | Local-first with optional export |
| **Agent Model** | Single plugin, no agents | Multi-agent with 43 specialized agents |
| **Memory System** | Semantic vector store + profile extraction | Key-value SQLite with jarvis-crud CLI |
| **Planning Approach** | None (pure memory) | R&D Framework (Reduce + Delegate) for context optimization |

---

## What Jarvis Can Learn

### Ideas to Adopt

1. **Hook-based Automatic Capture**
   - What: Use `Stop` hook to auto-capture session summaries
   - Why: Reduces friction - users don't need to remember `/memory`
   - How: Add `summary-hook.js` equivalent to Jarvis hooks
   - Effort: Low (hooks infrastructure exists)

2. **Container Tags for Project Isolation**
   - What: Scope memories by git repository using SHA256 hash
   - Why: Prevents cross-project memory pollution
   - How: Add `project_id` column to jarvis-crud database, generate from git root
   - Effort: Medium (schema change + migration)

3. **Hybrid Memory Retrieval**
   - What: Combine profile facts + recent context + semantic search
   - Why: More effective than pure RAG (81.6% vs 40-60% benchmark)
   - How: Add vector embeddings via local model (e.g., ollama/nomic-embed)
   - Effort: High (requires embedding pipeline)

4. **Transcript Compression**
   - What: Compress tool observations to summaries before storage
   - Why: Reduces token bloat in stored memories
   - How: Port `compress.js` patterns to Python for Jarvis
   - Effort: Low (pure function)

5. **Configurable Tool Filtering**
   - What: `skipTools` / `captureTools` settings
   - Why: Avoids capturing noise (Read, Glob, Grep)
   - How: Add to Jarvis settings file
   - Effort: Low

### Patterns to Study

| Pattern | Framework Implementation | Jarvis Adaptation |
|---------|-------------------------|-------------------|
| **Profile Extraction** | Supermemory cloud extracts static/dynamic facts automatically | Could use local LLM to extract facts from session summaries |
| **UUID Tracking** | Tracks last captured transcript entry by UUID | Could track last auto-compact timestamp to avoid re-processing |
| **Context Formatting** | `<supermemory-context>` tags with sections | Already use similar patterns in PreCompact hooks |
| **Deduplication** | Removes duplicate memories before injection | Could add to jarvis-crud before session restore |
| **Relative Time** | Shows "2d ago", "just now" | Could enhance jarvis-crud list output |

---

## Conflicts & Incompatibilities

### Philosophical Conflicts

| Jarvis Principle | Framework Approach | Resolution |
|------------------|-------------------|------------|
| **Local-first** | Cloud-required | Keep Jarvis local; add optional cloud sync later |
| **Explicit capture** | Automatic capture | Add auto-capture as opt-in, keep `/memory` for explicit |
| **Manual control** | Opaque cloud storage | Maintain jarvis-crud transparency; auto-capture should be viewable |
| **Multi-agent** | Single-purpose plugin | Supermemory is additive, not replacement |

### Technical Conflicts

| Jarvis Component | Framework Conflict | Impact |
|------------------|-------------------|--------|
| **jarvis-crud CLI** | Supermemory client JS | Low - different languages, can coexist |
| **SQLite database** | Cloud vector store | Low - complementary, not overlapping |
| **R&D Framework** | None (no context optimization) | None - orthogonal concerns |
| **PreCompact hooks** | SessionStart hook | Minor - both inject context, need to coordinate |

---

## Integration Options

### Option A: Full Integration

**Description:** Replace jarvis-crud with Supermemory client, migrate all data to cloud

| Pros | Cons |
|------|------|
| Semantic search out of box | Monthly cost ($9+) |
| Auto profile extraction | Cloud dependency |
| Less code to maintain | Data ownership concerns |

**Effort:** 4-6 weeks
**Risk:** High (breaking change, vendor lock-in)

### Option B: Partial Adoption

**Description:** Keep jarvis-crud for goals/sprints/config, add Supermemory for semantic memory

| Components to Adopt | Components to Skip |
|--------------------|-------------------|
| Session capture hook | Cloud storage |
| Transcript compression | Profile extraction |
| Context formatting patterns | Semantic search (for now) |

**Effort:** 1-2 weeks
**Risk:** Medium (two memory systems to maintain)

### Option C: Learn & Adapt (Recommended)

**Description:** Extract patterns from Supermemory, implement locally in Jarvis

**Key Learnings to Apply:**
1. Add `Stop` hook for automatic session summaries (save to jarvis-crud)
2. Add `project_id` to jarvis-crud for project isolation
3. Port compression logic (`compress.js`) to Python
4. Enhance context formatting with relative timestamps
5. Add `skipTools` setting to reduce noise in captures

---

## Cost-Benefit Analysis

### Benefits

| Benefit | Impact | Confidence |
|---------|--------|------------|
| Reduced context setup time | High | High |
| Better memory retrieval | Medium | Medium (depends on local implementation) |
| Project isolation | High | High |
| Automatic capture | Medium | High |

### Costs

| Cost | Type | Estimate |
|------|------|----------|
| Implementation time | Time | 2-3 weeks for Option C |
| Testing & validation | Time | 1 week |
| Potential semantic search addition | Complexity | High (future work) |
| Schema migration | Risk | Low (additive changes) |

### ROI Assessment

**Option C (Learn & Adapt) provides best ROI:**

- No monthly costs (vs $108+/year for Supermemory)
- No vendor lock-in
- Maintains local-first, data-ownership principles
- Gets 80% of benefit with 20% of effort
- Foundation for future semantic search addition

---

## Implementation Roadmap

If proceeding with **Option C: Learn & Adapt**:

### Phase 1: Auto-Capture Foundation (Week 1)

- [ ] Add `Stop` hook to Jarvis plugin
- [ ] Port transcript parsing logic from `transcript-formatter.js`
- [ ] Add `jarvis-crud memory auto-add` command for hook to call
- [ ] Add `skipTools` setting to Jarvis config

### Phase 2: Project Isolation (Week 2)

- [ ] Add `project_id` column to jarvis-crud schema
- [ ] Implement `getContainerTag()` equivalent in Python
- [ ] Modify `session get/set` to scope by project
- [ ] Migration script for existing data

### Phase 3: Enhanced Context (Week 3)

- [ ] Port compression logic to Python
- [ ] Add relative timestamps to context formatting
- [ ] Implement deduplication before context injection
- [ ] Update PreCompact hook to use new format

### Phase 4: Future - Semantic Search (Backlog)

- [ ] Evaluate local embedding models (nomic-embed, e5-small)
- [ ] Add vector column to jarvis-crud or separate index
- [ ] Implement hybrid retrieval (keyword + semantic)
- [ ] Profile extraction via local LLM

---

## Decision

### Recommendation

**Learn From**

### Rationale

Supermemory demonstrates valuable patterns for persistent memory, but direct integration conflicts with Jarvis principles:

1. **Cloud dependency** - Jarvis is local-first
2. **Cost** - Monthly subscription vs free
3. **Data ownership** - Jarvis keeps data on user's machine
4. **Existing infrastructure** - jarvis-crud already works well

The patterns to learn are:
- Hook-based auto-capture
- Project isolation via container tags
- Transcript compression
- Hybrid memory retrieval (future)

### Next Steps

1. **Immediate**: Implement Phase 1 (auto-capture hook) in Jarvis
2. **Short-term**: Add project isolation to jarvis-crud
3. **Medium-term**: Evaluate local semantic search options
4. **Long-term**: Consider optional cloud sync for users who want it

---

## Code Patterns to Port

### Compression Logic (Python equivalent)

```python
# jarvis/lib/compress.py - Port of Supermemory's compress.js

def compress_observation(tool_name: str, tool_input: dict, tool_response: dict | None = None) -> str:
    """Compress tool observations to concise summaries."""

    def get_relative_path(file_path: str) -> str:
        if not file_path:
            return "unknown"
        parts = file_path.replace("\\", "/").split("/")
        return "/".join(parts[-2:])

    def truncate(s: str, max_len: int = 50) -> str:
        if not s or len(s) <= max_len:
            return s or ""
        return s[:max_len] + "..."

    match tool_name:
        case "Edit":
            file = get_relative_path(tool_input.get("file_path", ""))
            old_snippet = truncate(tool_input.get("old_string", ""), 30)
            new_snippet = truncate(tool_input.get("new_string", ""), 30)
            if tool_input.get("replace_all"):
                return f'Replaced all "{old_snippet}" with "{new_snippet}" in {file}'
            return f'Edited {file}: "{old_snippet}" -> "{new_snippet}"'

        case "Write":
            file = get_relative_path(tool_input.get("file_path", ""))
            content_len = len(tool_input.get("content", ""))
            return f"Created {file} ({content_len} chars)"

        case "Bash":
            cmd = truncate(tool_input.get("command", ""), 80)
            success = not (tool_response and tool_response.get("error"))
            desc = f' - {truncate(tool_input.get("description", ""), 40)}' if tool_input.get("description") else ""
            return f"Ran: {cmd}{desc}{'' if success else ' [FAILED]'}"

        case "Task":
            desc = tool_input.get("description") or truncate(tool_input.get("prompt", ""), 60) or "subtask"
            agent = tool_input.get("subagent_type", "agent")
            return f"Spawned {agent}: {desc}"

        case _:
            return f"Used {tool_name}"
```

### Container Tag Generation (Python equivalent)

```python
# jarvis/lib/container_tag.py - Port of Supermemory's container-tag.js

import hashlib
import subprocess
from pathlib import Path

def sha256_short(s: str) -> str:
    """Generate truncated SHA256 hash."""
    return hashlib.sha256(s.encode()).hexdigest()[:16]

def get_git_root(cwd: str | Path) -> str | None:
    """Get the git repository root directory."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def get_container_tag(cwd: str | Path) -> str:
    """Generate project-scoped container tag."""
    git_root = get_git_root(cwd)
    base_path = git_root or str(cwd)
    return f"jarvis_project_{sha256_short(base_path)}"

def get_project_name(cwd: str | Path) -> str:
    """Get human-readable project name."""
    git_root = get_git_root(cwd)
    base_path = git_root or str(cwd)
    return Path(base_path).name or "unknown"
```

---

*Integration analysis completed: 2026-02-03 | Analyst: kb-architect*
