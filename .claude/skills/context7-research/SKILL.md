---
name: context7-research
description: Deep research using Context7 MCP for up-to-date library documentation. Activates when installing/upgrading packages, encountering library errors or deprecations, asking "how to use X library", or when documentation/docs are mentioned. Always query Context7 BEFORE implementing library features.
---

# Context7 Research

## When This Skill Activates

- Installing or upgrading packages
- Using a library feature for the first time
- Encountering deprecation warnings
- Debugging library-specific errors
- User asks "how do I use [library]?"
- Documentation or docs mentioned

## Research Workflow

### Step 1: Identify the Need
Recognize when library documentation is needed:
- New library installation
- Unfamiliar API usage
- Error messages mentioning library internals
- Version compatibility questions

### Step 2: Resolve Library ID
```
mcp__upstash-context-7-mcp__resolve-library-id({
  libraryName: "pandas"
})
```

### Step 3: Query Documentation
```
mcp__upstash-context-7-mcp__get-library-docs({
  context7CompatibleLibraryID: "/pypi/pandas",
  topic: "merge dataframes with different join types",
  tokens: 8000
})
```

### Step 4: Validate and Implement
- Cross-reference critical features with official docs
- Note version-specific behavior
- Implement following the documented patterns

## Query Patterns

### Feature Discovery
```
topic: "all available parameters for pandas DataFrame.merge"
topic: "fastapi dependency injection patterns"
topic: "pydantic v2 model validators"
```

### Troubleshooting
```
topic: "pandas SettingWithCopyWarning causes and solutions"
topic: "fastapi BackgroundTasks not executing after response"
topic: "sqlalchemy session lifecycle and connection pooling"
```

### Migration Guidance
```
topic: "pydantic v1 to v2 migration breaking changes"
topic: "sqlalchemy 1.4 to 2.0 migration guide"
topic: "pandas deprecation warnings and replacements"
```

### Best Practices
```
topic: "pytest fixtures best practices database testing"
topic: "fastapi async vs sync endpoints performance"
topic: "pandas memory optimization large datasets"
```

## Supported Libraries

### Python Core
| Library | ID Pattern | Common Topics |
|---------|------------|---------------|
| pandas | `/pypi/pandas` | DataFrames, merge, groupby, IO |
| numpy | `/pypi/numpy` | Arrays, broadcasting, ufuncs |
| fastapi | `/pypi/fastapi` | Routes, deps, middleware |
| pydantic | `/pypi/pydantic` | Models, validators, settings |
| sqlalchemy | `/pypi/sqlalchemy` | ORM, sessions, queries |
| pytest | `/pypi/pytest` | Fixtures, marks, plugins |
| httpx | `/pypi/httpx` | HTTP client, async |

### Data Engineering
| Library | ID Pattern | Common Topics |
|---------|------------|---------------|
| apache-spark | Check Context7 | RDDs, DataFrames, SQL |
| delta-lake | Check Context7 | Tables, time travel |
| polars | `/pypi/polars` | Fast DataFrames |

### Web/API
| Library | ID Pattern | Common Topics |
|---------|------------|---------------|
| requests | `/pypi/requests` | HTTP, sessions |
| aiohttp | `/pypi/aiohttp` | Async HTTP |
| flask | `/pypi/flask` | Routes, blueprints |

## Integration with Code

After Context7 research, always:

1. **Implement following official patterns**
   ```python
   # Based on Context7 research for pandas 2.x
   result = df.merge(other, on="key", how="left")
   ```

2. **Add type hints from library signatures**
   ```python
   def process(df: pd.DataFrame) -> pd.DataFrame:
   ```

3. **Include version note if relevant**
   ```python
   # Note: Requires pandas >= 2.0 (API changed from 1.x)
   ```

4. **Handle library-specific exceptions**
   ```python
   from pandas.errors import MergeError

   try:
       result = df.merge(other, on="key")
   except MergeError as e:
       logger.error(f"Merge failed: {e}")
   ```

## Fallback Chain

If Context7 doesn't have the library:

1. **Exa Code Search** - Community examples
   ```
   mcp__exa__get_code_context_exa({
     query: "pandas merge example python"
   })
   ```

2. **WebSearch** - Recent updates, blog posts

3. **Ref Tools** - Deep documentation reading
   ```
   mcp__ref-tools__ref_read_url({
     url: "https://docs.library.com/guide"
   })
   ```

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| Outdated examples | Always specify version in query |
| Missing library | Use fallback chain |
| Too much context | Be specific in topic |
| Conflicting info | Cross-reference official docs |

## Quick Reference

```python
# Template for library research
# 1. Identify need
library = "pandas"
topic = "merge with multiple keys"

# 2. Query Context7
# mcp__upstash-context-7-mcp__get-library-docs(...)

# 3. Implement with type hints
def merge_data(
    left: pd.DataFrame,
    right: pd.DataFrame,
    keys: list[str],
) -> pd.DataFrame:
    """Merge dataframes on multiple keys.

    Based on pandas 2.x documentation (Context7).
    """
    return left.merge(right, on=keys, how="left")
```
