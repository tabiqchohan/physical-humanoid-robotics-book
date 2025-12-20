---
id: 0001
title: Book Chapter Task Breakdown Template Generation
stage: tasks
date: 2025-12-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: book-chapter-template
branch: 1-physical-ai-robotics-book
user: user
command: /sp.tasks
labels: ["book-writing","task-template","robotics"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/book-chapter-template/tasks.md
tests:
null
---

## Prompt

```text
     You are a senior editor and robotics engineer.
Generate a **Task Breakdown** for writing every chapter of the book
**Physical AI & Humanoid Robotics**.

For each chapter provide:
- Writing tasks (detailed)
- Research tasks (include categories of sources)
- Code example tasks (Python or C++)
- Simulation tasks (e.g., Isaac Gym, MuJoCo, PyBullet)
- Diagram tasks (what visual must be created)
- Testing/validation tasks
- Review checklist

Output in a structured, repeatable template that can be applied to all chapters.
Use bullet lists for clarity.
```

## Response snapshot

Generated a detailed task breakdown template for a book chapter, covering writing, research, code examples, simulation, diagrams, testing, and review. The template is structured to be repeatable for each chapter of 'Physical AI & Humanoid Robotics'.

## Outcome

- ✅ Impact: Task breakdown template successfully generated.
- 🧪 Tests: No direct tests generated; template includes testing/validation tasks.
- 📁 Files: Created specs/book-chapter-template/tasks.md.
- 🔁 Next prompts: User can now apply the template or request generation for a specific chapter.
- 🧠 Reflection: The template adheres to the specified format and covers all requested categories for book chapter development.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
