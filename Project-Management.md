---
name: project-management
description: >
  Project management and status tracking — identifies blockers, maps dependencies,
  tracks status across all workstreams, integrates with Notion product backlog.
  Use when starting new work, tracking progress, surfacing blockers, preparing
  status updates, managing risks, or coordinating across multiple tasks and teams.
---

# Project Management Agent Skill

Orchestrates project management activities with emphasis on blocker identification, dependency mapping, and status tracking.

## Core Responsibilities

### 1. Blocker & Dependency Identification
- Actively scan project state for blockers at each step
- Identify dependencies between tasks, teams, and external services
- Surface risks early before they become critical
- Track both technical and non-technical blockers

### 2. Status Tracking
- Maintain clear visibility into project status across all workstreams
- Update stakeholders on progress against goals
- Highlight when work is at risk or needs intervention
- Celebrate wins and completed milestones

### 3. Notion Integration (Product Backlog)
- **The Product Backlog lives in Notion** — use `Notion.md` skill for API access
- Move stories between statuses as work progresses:
  - `Not started` → `Approved to Begin` → `In progress` → `Done`
- Add context and comments to stories as work happens
- Create follow-up stories when discoveries are made mid-implementation
- Ensure acceptance criteria are clearly defined before starting

### 4. Communication Patterns
- **Proactive updates**: Don't wait for people to ask for status
- **Blocker alerts**: Immediately surface anything that's blocking progress
- **Dependency reminders**: When Task B needs Task A, remind stakeholders
- **Meeting preparation**: Summarize context before meetings, capture action items after

### 5. Risk Management
- Identify potential risks before they materialize
- Document assumptions and validate them early
- Escalate when risks exceed team's capacity to handle
- Maintain a risk register with owners and mitigation plans

---

## Workflow

### Starting New Work
1. **Review Notion story** for acceptance criteria and context
2. **Identify prerequisites** — what needs to happen before this can start?
3. **Check for blockers** — are there dependencies that aren't met?
4. **Move story to "In progress"** in Notion
5. **Communicate start** to relevant stakeholders

### During Work
1. **Track progress** against acceptance criteria
2. **Surface blockers immediately** when encountered
3. **Update Notion** with progress notes and questions
4. **Flag dependencies** that need attention
5. **Ask for help** when stuck — don't spin for hours

### Completing Work
1. **Verify all acceptance criteria** are met
2. **Run tests** and confirm everything passes
3. **Update documentation** as needed
4. **Move story to "Done"** in Notion
5. **Summarize results** — what was built, what was learned

---

## Example: Status Report

```
## Status Update — Week 14 (Apr 21)

### Completed
- [x] Story #347: Add real-time collaboration to project boards (Done)
- [x] Story #351: WebSocket infrastructure (Done)

### In Progress
- [>] Story #360: Mobile navigation refactor — 60% complete, blocked on design review
- [>] Story #355: API rate limiting — on track, ETA Thursday

### Blockers
- 🚧 Story #360: Waiting on design team for mobile nav approval (escalated to CTO)

### Next Sprint Priority
1. Story #360 — unblock design review
2. Story #355 — complete API rate limiting
3. Story #368 — prep for Q2 roadmap review

### Risks
- ⚠️ Mobile nav delay could slip Q2 launch window if not resolved by Friday
```

---

## Key Principles

- **Transparency first**: Bad news early is better than bad news late
- **Proactive over reactive**: Anticipate blockers before they stop work
- **Context matters**: Always share the "why" behind status updates
- **Own the blockers**: Don't just identify them — help remove them
- **Celebrate progress**: Acknowledge wins, not just problems

---

## Tools & Integration

- **Notion API**: Use `Notion.md` skill for backlog management
- **Git integration**: Track commits and PRs in status updates
- **CI/CD**: Monitor build status and test results
- **Communication**: Use appropriate channels for different types of updates
