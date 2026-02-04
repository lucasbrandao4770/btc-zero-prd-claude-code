---
title: "Lovable Prompting Guide"
description: "Best practices for writing effective prompts in Lovable AI"
layer: "lovable"
source_refs: ["LOV001"]
source_urls:
  - "https://lovable.dev/docs"
  - "https://lovable.dev/tips"
created: "2026-01-30"
updated: "2026-01-30"
keywords: [lovable, prompting, ai, ui-development, best-practices]
related:
  - "./02-github-workflow.md"
  - "./03-tool-division.md"
  - "../agentic-ai/03-prompt-engineering/core-principles.md"
complexity: "beginner"
---

# Lovable Prompting Guide

## Overview

Lovable is an AI-powered web application builder that transforms natural language descriptions into functional React applications. This guide covers prompting best practices to maximize output quality and minimize iteration cycles.

Effective prompting in Lovable differs from traditional code assistants. Lovable excels at understanding visual descriptions and user intent, making natural language the primary interface for creating sophisticated UIs.

---

## Core Principles

### 1. Be Specific, Not Vague

| Avoid | Prefer |
|-------|--------|
| "Make it look nice" | "Use a clean design with 16px padding, rounded corners (8px), and subtle shadows" |
| "Add a form" | "Add a contact form with name, email, and message fields, each with validation" |
| "Make it modern" | "Use a minimalist design with plenty of whitespace and a blue (#3B82F6) accent color" |

### 2. Use Natural Language

Lovable understands context and intent. Write as if explaining to a designer:

```
Create a dashboard for tracking daily habits. The user should see:
- A list of their habits on the left side
- A calendar view on the right showing completion status
- Each habit should be clickable to mark as complete
- Use green checkmarks for completed items
```

### 3. Provide Visual Context

Reference familiar patterns when possible:

```
Build a settings page similar to iOS Settings app:
- Grouped sections with gray backgrounds
- White card-style rows with icons on the left
- Chevron indicators for navigation items
- Toggle switches for boolean settings
```

### 4. One Task at a Time

Break complex requests into sequential prompts:

**Instead of:**
```
Build a complete e-commerce site with products, cart, checkout, user auth, and admin panel
```

**Do:**
```
Prompt 1: Create a product listing page with a grid of product cards
Prompt 2: Add a product detail page with image gallery and add-to-cart button
Prompt 3: Create a shopping cart sidebar that shows selected items
Prompt 4: Add a checkout flow with shipping and payment forms
```

---

## CTGC Prompt Structure

For complex requests, use the CTGC framework:

### Context (C)
Background information about the project or component:
```
I'm building a healthcare patient portal. Users are medical professionals
who need to quickly access patient information.
```

### Task (T)
The specific action you want Lovable to perform:
```
Create a patient search interface that allows filtering by name,
date of birth, or medical record number.
```

### Guidelines (G)
Style preferences and design direction:
```
Use a clean, professional design. Prioritize readability and quick scanning.
Include loading states and empty states.
```

### Constraints (C)
Technical requirements and limitations:
```
Must work on mobile devices. Search should be debounced (300ms).
Display maximum 20 results per page with pagination.
```

### Complete CTGC Example

```
CONTEXT:
I'm building an internal tool for a logistics company. Users are
warehouse managers who track shipments throughout the day.

TASK:
Create a shipment tracking dashboard that shows:
- Active shipments in a sortable table
- Quick filters for status (pending, in-transit, delivered)
- A map view toggle showing shipment locations

GUIDELINES:
- Use a data-dense design (managers handle 100+ shipments daily)
- Include keyboard shortcuts for common actions
- Dark mode support for overnight shifts

CONSTRAINTS:
- Table must handle 500+ rows without performance issues
- Map should use placeholder markers (will integrate real API later)
- Mobile responsive for tablet use in warehouse
```

---

## Advanced Techniques

### Meta Prompting

Ask Lovable to help you write better prompts:

```
I want to build a task management app. Can you suggest the key features
and screens I should include? Help me break this down into a series of
prompts I can use to build it step by step.
```

### Reverse Meta Prompting

After Lovable creates something, ask it to explain:

```
What prompts would recreate the design you just built? I want to
understand the key decisions so I can refine them.
```

### Iterative Refinement

Build on previous context:

```
Prompt 1: Create a data table component for displaying user records
Prompt 2: Add sorting functionality to each column
Prompt 3: Add a search bar that filters across all columns
Prompt 4: Add row selection with a bulk actions dropdown
```

### Reference Images (When Supported)

If Lovable supports image input:
```
Here's a screenshot of the design we want to implement [attach image].
Recreate this layout using React components. Pay attention to:
- The card spacing and shadows
- The header navigation style
- The color scheme (extract colors from the image)
```

---

## Prompt Templates

### Landing Page
```
Create a landing page for [PRODUCT_NAME], a [BRIEF_DESCRIPTION].

Hero section:
- Headline: "[MAIN_VALUE_PROPOSITION]"
- Subheadline explaining the key benefit
- Primary CTA button: "[CTA_TEXT]"
- Hero image placeholder on the right

Features section:
- 3 feature cards with icons
- Feature 1: [FEATURE]
- Feature 2: [FEATURE]
- Feature 3: [FEATURE]

Use [COLOR_SCHEME] colors and modern, clean typography.
```

### Dashboard
```
Create a dashboard for [USE_CASE].

Layout:
- Sidebar navigation with [NAV_ITEMS]
- Top header with search and user menu
- Main content area with [WIDGET_DESCRIPTION]

Key metrics to display:
- [METRIC_1]
- [METRIC_2]
- [METRIC_3]

Design style: [STYLE_DESCRIPTION]
```

### Form
```
Create a [FORM_PURPOSE] form with the following fields:

Required fields:
- [FIELD_1]: [TYPE] with [VALIDATION]
- [FIELD_2]: [TYPE] with [VALIDATION]

Optional fields:
- [FIELD_3]: [TYPE]

Include:
- Inline validation with error messages
- Loading state on submit
- Success/error toast notifications
```

---

## Common Mistakes to Avoid

### 1. Overloading Single Prompts

**Wrong:**
```
Build a complete CRM with contacts, deals, tasks, email integration,
reporting, team management, and API webhooks
```

**Right:** Break into 8+ separate prompts, each building on the previous.

### 2. Vague Visual Descriptions

**Wrong:**
```
Make the buttons look better
```

**Right:**
```
Update buttons to use:
- Primary: solid blue (#3B82F6) with white text
- Secondary: white with blue border
- All buttons: 8px border radius, medium font weight
- Hover: darken by 10%
```

### 3. Assuming Technical Context

**Wrong:**
```
Use zustand for state management and implement optimistic updates
```

**Right:**
```
When a user marks a task complete:
1. Immediately show it as complete (optimistic)
2. Send the update to the backend
3. If it fails, revert and show an error message
```

### 4. Mixing UI and Backend Logic

**Wrong:**
```
Create a user registration form that validates emails against
the database and sends verification emails via SendGrid
```

**Right:**
```
Create a user registration form with:
- Email field with format validation
- Password field with strength indicator
- Confirm password field with match validation
- Submit button with loading state
- Success message placeholder for post-submission

[Backend integration will be handled separately in Claude Code]
```

### 5. Ignoring Mobile

**Wrong:**
```
Create a three-column dashboard layout
```

**Right:**
```
Create a dashboard layout:
- Desktop (1024px+): three columns
- Tablet (768px-1023px): two columns, stack third below
- Mobile (<768px): single column, collapsible sections
```

---

## Prompting for Specific Scenarios

### Prototyping New Features
```
I want to explore a new feature for [CONTEXT]. Create a prototype that:
- Shows the main user flow
- Uses placeholder data
- Includes interactive elements (buttons work, forms show validation)
- Skip backend integration for now

Focus on: [SPECIFIC_ASPECTS_TO_TEST]
```

### Fixing UI Issues
```
The current [COMPONENT] has these issues:
1. [ISSUE_1]
2. [ISSUE_2]

Update it to:
- [FIX_1]
- [FIX_2]

Keep the existing [ELEMENTS_TO_PRESERVE] unchanged.
```

### Implementing Design System
```
Create a component library following this design system:

Colors:
- Primary: [HEX]
- Secondary: [HEX]
- Background: [HEX]
- Text: [HEX]

Typography:
- Headings: [FONT], [SIZES]
- Body: [FONT], [SIZE]

Spacing: [SCALE]

Create these components: [LIST]
```

---

## Measuring Prompt Effectiveness

### Signs of Good Prompts
- First iteration is 80%+ correct
- Minimal back-and-forth refinements needed
- Output matches mental model
- Code is clean and maintainable

### Signs of Weak Prompts
- Multiple iterations to get basic structure right
- Lovable asks clarifying questions
- Output looks nothing like expected
- Need to rewrite significant portions

### Improvement Loop
1. Write initial prompt
2. Evaluate output against expectations
3. Identify gaps in prompt specificity
4. Refine prompt for next iteration
5. Document effective patterns for reuse

---

## Related Resources

- [GitHub Workflow](./02-github-workflow.md) - Syncing Lovable projects
- [Tool Division](./03-tool-division.md) - When to use Lovable vs Claude Code
- [Limitations](./04-limitations.md) - Understanding Lovable constraints
- [Prompt Engineering Principles](../agentic-ai/03-prompt-engineering/core-principles.md) - General prompting guidance

---

*Effective prompting is iterative. Start simple, evaluate results, and refine.*
