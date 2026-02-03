# Brainstorm Pattern

> Effective idea exploration before capturing requirements

---

## Purpose

The Brainstorm phase transforms vague ideas into clear, actionable requirements through **structured dialogue**. It prevents premature commitment to solutions and ensures YAGNI (You Aren't Gonna Need It) is applied early.

---

## When to Use

| Use Brainstorm | Skip Brainstorm |
|----------------|-----------------|
| Vague idea needs exploration | Clear requirements already exist |
| Multiple valid approaches | Simple, well-defined request |
| Uncertain about scope/users | Meeting notes with explicit asks |
| Need to apply YAGNI | Time pressure requires direct Define |

---

## The Pattern

### Step 1: Present the Initial Idea

Start with a raw description—it can be incomplete or vague:

```text
"I want to build a notification system for our users"
```

### Step 2: One Question at a Time

The AI asks **one clarifying question at a time** (never dumps multiple questions):

```text
AI: "What types of events should trigger notifications?"

User: "New messages, task assignments, and deadline reminders"

AI: "Should notifications be real-time, or is periodic delivery acceptable?"

User: "Real-time for messages, periodic for everything else"
```

**Why one question?**
- Reduces cognitive load
- Prevents information overload
- Enables deeper exploration per topic
- Maintains conversational flow

### Step 3: Explore Multiple Approaches

Present 2-3 approaches with trade-offs:

```markdown
## Approach 1: Event-Driven with WebSockets

**How it works**: Real-time push for all notification types

**Pros**:
- Immediate delivery
- Consistent user experience
- Lower server polling load

**Cons**:
- Higher complexity
- Connection management overhead
- Not all users need real-time

## Approach 2: Hybrid (WebSocket + Polling)

**How it works**: WebSocket for real-time, polling for batch

**Pros**:
- Optimized for actual needs
- Simpler where real-time isn't critical
- Easier to scale

**Cons**:
- Two systems to maintain
- Potential inconsistency

## Recommendation: Approach 2 (Hybrid)

Rationale: Matches stated requirements (real-time for messages,
periodic for others) without over-engineering.
```

### Step 4: Apply YAGNI Ruthlessly

Explicitly identify and remove speculative features:

```markdown
## Features Removed (YAGNI Applied)

| Proposed Feature | Reason Removed |
|-----------------|----------------|
| Email notifications | Not in initial requirements |
| Notification grouping | Optimization before problem exists |
| Read receipts | "Might be nice" - not explicitly needed |
| Scheduled notifications | Future feature, not MVP |

**Remaining Scope**:
- In-app notifications for messages (real-time)
- In-app notifications for tasks/deadlines (periodic)
```

### Step 5: Validate Understanding

Confirm with the user before proceeding:

```markdown
## Validation Checkpoint

Based on our discussion, here's my understanding:

**Building**: In-app notification system
**Users**: All app users
**Triggers**: Messages (real-time), Tasks/Deadlines (periodic)
**Approach**: Hybrid WebSocket + Polling

**Not Building** (deferred):
- Email notifications
- Mobile push
- Notification preferences UI

Is this correct? Ready for Define?
```

---

## Quality Gate

Before exiting Brainstorm, verify:

| Criteria | Check |
|----------|-------|
| Minimum 3 clarifying questions asked | ☐ |
| 2+ approaches explored with pros/cons | ☐ |
| 2+ validation checkpoints passed | ☐ |
| User confirmed selected approach | ☐ |
| YAGNI applied (features explicitly removed) | ☐ |

---

## Output Template

```markdown
# BRAINSTORM: {Feature Name}

## Metadata
| Attribute | Value |
|-----------|-------|
| **Date** | {date} |
| **Status** | Ready for Define |

---

## Discovery

### Initial Idea
{Raw description from user}

### Questions & Answers

**Q1**: {Question}
**A1**: {Answer}

**Q2**: {Question}
**A2**: {Answer}

**Q3**: {Question}
**A3**: {Answer}

---

## Approaches Explored

### Approach 1: {Name}
{Description, pros, cons}

### Approach 2: {Name}
{Description, pros, cons}

### Selected: {Approach Name}
**Rationale**: {Why this approach}

---

## YAGNI Applied

| Removed Feature | Reason |
|-----------------|--------|
| {Feature 1} | {Reason} |
| {Feature 2} | {Reason} |

---

## Draft Requirements

### Core Requirements
- {Requirement 1}
- {Requirement 2}

### Out of Scope
- {Out of scope 1}
- {Out of scope 2}

---

## Validation

User confirmed: [x] Approach / [x] Scope / [x] Ready for Define

---

## Next Step
`/define .claude/sdd/features/BRAINSTORM_{FEATURE}.md`
```

---

## Common Pitfalls

### 1. Dumping All Questions at Once

❌ **Wrong**:
```text
"Let me ask about: notification types, delivery channels,
frequency, user preferences, error handling, and retry logic."
```

✅ **Right**:
```text
"What types of events should trigger notifications?"
[Wait for answer]
"How should these be delivered to users?"
[Wait for answer]
```

### 2. Skipping Trade-off Analysis

❌ **Wrong**:
```text
"We'll use WebSockets for real-time notifications."
```

✅ **Right**:
```text
"Here are three approaches: WebSockets, SSE, and Polling.
Let me explain the trade-offs for your use case..."
```

### 3. Accepting Scope Creep

❌ **Wrong**:
```text
User: "We might also want email notifications..."
AI: "Great, I'll add email notifications to the scope."
```

✅ **Right**:
```text
User: "We might also want email notifications..."
AI: "Is email required for MVP, or can we add it later?
     Applying YAGNI, I'd suggest starting with in-app only."
```

### 4. Insufficient Validation

❌ **Wrong**:
```text
"Based on what you said, I'll proceed to Define."
```

✅ **Right**:
```text
"Here's my understanding: [summary].
Is this correct? Anything missing or wrong?"
```

---

## Example: Real Brainstorm Session

```text
USER: "I want to add caching to our API"

AI: "What specific performance problem are you trying to solve
     with caching?"

USER: "The product catalog API is slow - about 2 seconds
       for listing products"

AI: "Is this slowness during initial load, or does it stay
     slow on repeated requests?"

USER: "It's slow every time, even for the same query"

AI: "What's the data change frequency for product catalog?
     How often do products/prices update?"

USER: "Maybe once a day, during overnight batch imports"

AI: "Given low change frequency, here are three approaches:

     1. **Application-level cache (Redis)**
        - Store results in Redis with TTL
        - Fast reads, easy invalidation
        - Adds infrastructure dependency

     2. **HTTP caching (CDN)**
        - Cache responses at CDN level
        - No code changes, scalable
        - Less control over invalidation

     3. **Query optimization**
        - Optimize database queries instead
        - No new infrastructure
        - May not achieve 2s → <100ms

     Recommendation: Application cache (Redis) because
     you need predictable sub-100ms responses with
     daily invalidation on import.

     Should we proceed with this approach?"

USER: "Yes, Redis sounds right. But keep it simple."

AI: "For YAGNI, I'm removing:
     - Cache warming (optimize later if needed)
     - Distributed cache (single Redis is fine for now)
     - Complex invalidation patterns (daily clear is sufficient)

     Draft scope:
     - Redis cache for product catalog GET endpoints
     - 24-hour TTL with manual clear on import
     - Simple key-value storage (no complex patterns)

     Is this the right scope for MVP?"

USER: "Perfect, let's move to Define."
```

---

## Integration with Jarvis Planner Mode

Brainstorm aligns with **pre-Strategic phase** in Jarvis Planner Mode:

| Jarvis Phase | SDD Phase |
|--------------|-----------|
| Pre-planning (informal) | **Brainstorm** |
| Strategic | Define |
| Tactical | Design |
| Operational | Build |

When using Jarvis Planner Mode, you can skip formal Brainstorm if requirements are clear and proceed directly to Strategic Requirements.

---

## Next Steps

- **After Brainstorm**: [define-pattern.md](define-pattern.md)
- **Full lifecycle**: [../concepts/sdd-lifecycle.md](../concepts/sdd-lifecycle.md)

---

*References: AgentSpec 4.2 Phase 0, Spec-Kit /speckit.clarify*
