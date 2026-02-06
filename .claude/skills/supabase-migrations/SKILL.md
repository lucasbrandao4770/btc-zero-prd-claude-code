---
name: supabase-migrations
description: Database migration management for Supabase/PostgreSQL projects. Activates when creating/modifying database schemas, working with migrations folder, or when user mentions migrations, schema changes, or database alterations.
---

# Supabase Migrations Skill

Manages database migrations for Supabase/PostgreSQL projects following data engineering best practices.

## When This Skill Activates

- User mentions "migration", "database change", "schema change", "alter table"
- Working in a `supabase/migrations/` directory
- Creating new database tables, columns, indexes, or constraints
- Modifying existing database schema
- User asks to "add a column", "create a table", "add an index"

## CRITICAL: Check Repository Guidelines First (MANDATORY)

**Before creating any migration, ALWAYS check for repository-specific templates and guidelines.**

### Step 1: Search for Local Guidelines

Search the repository root and supabase directory for:

```bash
# Check for guidelines document
ls -la {repo_root}/MIGRATIONS.md
ls -la {repo_root}/docs/MIGRATIONS.md
ls -la {repo_root}/supabase/MIGRATIONS.md

# Check for template files (NEVER in migrations/ - would interfere with Supabase CLI)
ls -la {repo_root}/supabase/templates/migration-template.sql
ls -la {repo_root}/templates/migration-template.sql
ls -la {repo_root}/docs/templates/migration-template.sql
```

**Common file patterns to search:**
- `MIGRATIONS.md` - Guidelines document
- `_template.sql` or `template.sql` - SQL template
- `CONTRIBUTING.md` - May contain database guidelines
- `docs/database/` - Database documentation folder

### Step 2: If Local Guidelines Found

1. **Read the guidelines document** - Follow project-specific conventions
2. **Use the template file** - Copy and modify for new migrations
3. **Follow project patterns** - Match existing migration style in the repo
4. **Update project CHANGELOG.md** - Using project's format

### Step 3: If NO Local Guidelines Found

Fall back to this skill's generic templates AND:

1. **Consult data engineering KB** at `kb/python/` or via ai-data-engineer agent
2. **Read 2-3 existing migrations** in the repo to understand patterns
3. **Offer to create guidelines** - Suggest creating MIGRATIONS.md and template for the project

### Why This Matters

- **Consistency**: Each project may have unique patterns (multi-tenancy, RLS, vectors)
- **Team standards**: Existing guidelines represent team decisions
- **Avoid conflicts**: Generic templates may not match project conventions

## Migration Naming Convention

All migrations follow the Supabase CLI format:

```
YYYYMMDDHHMMSS_descriptive_name.sql
```

**Examples:**
- `20250127143022_add_status_column_to_orders.sql`
- `20250127150000_create_audit_log_table.sql`
- `20250127160000_add_index_on_customer_id.sql`

**Naming Rules:**
- Use lowercase with underscores
- Be descriptive but concise
- Start with action verb: `add_`, `create_`, `remove_`, `alter_`, `drop_`
- Include affected table name

## Quick Commands

| Action | Command |
|--------|---------|
| Create migration | `supabase migration new <name>` |
| List migrations | `supabase migration list` |
| Apply locally | `supabase db reset` |
| Push to remote | `supabase db push` |
| Pull remote schema | `supabase db pull` |
| Check diff | `supabase db diff` |

## Migration Templates

### Simple ALTER TABLE

```sql
-- Add column(s) to existing table
ALTER TABLE public.table_name
ADD COLUMN IF NOT EXISTS column_name data_type;
```

### Transactional Migration (Recommended)

```sql
-- =================================================================
-- MIGRATION: Brief description of what this migration does
-- =================================================================

BEGIN;

-- -----------------------------------------------------------------
-- SECTION 1: Description of changes
-- -----------------------------------------------------------------

ALTER TABLE public.table_name
ADD COLUMN IF NOT EXISTS new_column VARCHAR(100),
ADD COLUMN IF NOT EXISTS another_column JSONB;

-- -----------------------------------------------------------------
-- SECTION 2: Indexes (if needed)
-- -----------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_table_column
ON public.table_name(new_column);

COMMIT;
```

### Create Table with Constraints

```sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.new_table (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Business columns
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    metadata JSONB,

    -- Foreign keys
    parent_id UUID REFERENCES public.parent_table(id) ON DELETE CASCADE
);

-- Index for common queries
CREATE INDEX IF NOT EXISTS idx_new_table_status
ON public.new_table(status);

-- RLS Policy (if needed)
ALTER TABLE public.new_table ENABLE ROW LEVEL SECURITY;

COMMIT;
```

### Trigger and Function

```sql
BEGIN;

-- Create or replace the function
CREATE OR REPLACE FUNCTION public.function_name()
RETURNS TRIGGER AS $$
BEGIN
    -- Trigger logic here
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Drop existing trigger if present
DROP TRIGGER IF EXISTS trg_name ON public.table_name;

-- Create the trigger
CREATE TRIGGER trg_name
BEFORE UPDATE ON public.table_name
FOR EACH ROW
EXECUTE FUNCTION public.function_name();

COMMIT;
```

## CHANGELOG Management

Every migration MUST update the CHANGELOG.md in the repository root.

### CHANGELOG Format

```markdown
# Database Migrations Changelog

All notable database schema changes.

## [Unreleased]

## [YYYY-MM-DD] - Migration Name
### Added
- New tables, columns, indexes

### Changed
- Modified columns, constraints, defaults

### Removed
- Dropped tables, columns, indexes

### Fixed
- Data corrections, constraint fixes
```

### Changelog Update Process

1. After creating a migration file, immediately update CHANGELOG.md
2. Add entry under `[Unreleased]` section
3. Use the same date as the migration timestamp
4. Be specific about what changed

## Pre-Migration Checklist

Before creating a migration:

- [ ] Verify the change is necessary (not already in schema)
- [ ] Check for dependent objects (foreign keys, views, functions)
- [ ] Consider data migration if modifying existing columns
- [ ] Plan rollback strategy
- [ ] Use `IF NOT EXISTS` / `IF EXISTS` for idempotency

## Post-Migration Checklist

After creating a migration:

- [ ] Migration file follows naming convention
- [ ] SQL is wrapped in BEGIN/COMMIT for safety
- [ ] CHANGELOG.md is updated
- [ ] Test locally with `supabase db reset`
- [ ] Verify no data loss occurs

## Best Practices

### DO

- Use transactions (BEGIN/COMMIT) for multi-statement migrations
- Use `IF NOT EXISTS` and `IF EXISTS` clauses
- Add comments explaining the purpose
- Create indexes for frequently queried columns
- Use appropriate data types (UUID for IDs, TIMESTAMPTZ for dates)
- Consider RLS policies for security

### DON'T

- Drop columns/tables without backup plan
- Use production-specific values in migrations
- Create migrations that depend on application code
- Skip the CHANGELOG update
- Use `CASCADE` without understanding implications

## Rollback Patterns

### For Column Additions

Keep rollback SQL as a comment:

```sql
-- ROLLBACK: ALTER TABLE public.table_name DROP COLUMN IF EXISTS column_name;
```

### For Table Creations

```sql
-- ROLLBACK: DROP TABLE IF EXISTS public.table_name CASCADE;
```

### For Index Creations

```sql
-- ROLLBACK: DROP INDEX IF EXISTS idx_name;
```

## Integration with Agents

This skill works with:

- **faturamento-data-layer**: For Faturamento-specific database patterns
- **ai-data-engineer**: For general data engineering best practices
- **ai-data-engineer-gcp**: When integrating with GCP services

## Error Handling

If a migration fails:

1. Check the error message in Supabase logs
2. Fix the migration file (don't create a new one for typos)
3. Reset local database: `supabase db reset`
4. If already pushed to remote, create a corrective migration
