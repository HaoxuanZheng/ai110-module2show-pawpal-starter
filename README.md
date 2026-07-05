# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

- Sorts tasks chronologically with `Scheduler.sort_by_time()`.
- Filters tasks by pet, completion state, frequency, and date with `Scheduler.filter_tasks()`.
- Flags exact-time collisions with `Scheduler.detect_conflicts()`.
- Creates the next daily or weekly occurrence when a recurring task is completed with `Task.mark_complete()`.
- Shows a readable CLI demo and a Streamlit schedule table for quick verification.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule for Jordan
- 2026-07-05 07:30 - Morning walk (Luna, 25 min, priority high, pending)
- 2026-07-05 08:30 - Breakfast feeding (Mochi, 10 min, priority high, pending)
- 2026-07-05 08:30 - Medication (Luna, 5 min, priority high, pending)
- 2026-07-05 18:00 - Evening play (Mochi, 20 min, priority medium, pending)

Conflict Check
- Conflict at 2026-07-05 08:30: Luna: Medication; Mochi: Breakfast feeding

Recurring Task Demo
- Created next occurrence: 2026-07-06 08:30 - Medication (Luna, 5 min, priority high, pending)
- Tomorrow's schedule
- 2026-07-06 08:30 - Medication (Luna, 5 min, priority high, pending)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
python -m pytest --cov
```

The test suite covers sorting correctness, recurrence logic, task addition, and conflict detection.

Sample test output:

```
4 passed in 0.01s
```

Confidence level: ★★★★☆

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts by date, time, and priority. |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet, completion status, frequency, or date. |
| Conflict handling | `Scheduler.detect_conflicts()` | Warns when tasks share the same date and time. |
| Recurring tasks | `Task.mark_complete()`, `Pet.complete_task()` | Daily and weekly tasks create the next occurrence automatically. |

## Demo Walkthrough

1. Open the Streamlit app and enter the owner name.
2. Add one or more pets with the pet form.
3. Add tasks with a time, date, recurrence, duration, and priority.
4. Use the schedule filters to narrow the table by pet or status.
5. Review the sorted schedule table and any conflict warning banner.
6. Run `python main.py` to see the same scheduling logic in the terminal.

Sample CLI output:

```text
Today's Schedule for Jordan
- 2026-07-05 07:30 - Morning walk (Luna, 25 min, priority high, pending)
- 2026-07-05 08:30 - Breakfast feeding (Mochi, 10 min, priority high, pending)
- 2026-07-05 08:30 - Medication (Luna, 5 min, priority high, pending)
- 2026-07-05 18:00 - Evening play (Mochi, 20 min, priority medium, pending)

Conflict Check
- Conflict at 2026-07-05 08:30: Luna: Medication; Mochi: Breakfast feeding

Recurring Task Demo
- Created next occurrence: 2026-07-06 08:30 - Medication (Luna, 5 min, priority high, pending)
- Tomorrow's schedule
- 2026-07-06 08:30 - Medication (Luna, 5 min, priority high, pending)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
