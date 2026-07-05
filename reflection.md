# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

I designed four core classes: `Task` for individual care items, `Pet` for grouping a pet's tasks, `Owner` for managing multiple pets, and `Scheduler` for sorting, filtering, and conflict checks. The UML keeps behavior focused in the scheduler while `Pet` and `Owner` mainly act as containers and lookup helpers.

**b. Design changes**

Yes. I added `due_date`, `priority`, and recurrence handling to `Task` so the scheduler could support daily planning and recurring items without extra helper objects. I also gave `Task.mark_complete()` the ability to create the next occurrence, which kept recurrence logic close to the task itself.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

The scheduler only detects exact time matches, not overlapping durations. That is reasonable for a first version because the assignment focuses on simple daily routines, and exact collisions are easy to explain and verify in tests.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

I tested task completion, task addition, chronological sorting, and conflict detection. Those cases matter because they verify the core state changes and the main scheduler rules that the rest of the app depends on.

**b. Confidence**

I am moderately confident because the main behaviors are covered by focused tests and the CLI demo prints a readable schedule. Next I would test invalid time strings, duplicate pet names, and multiple recurring completions across several days.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
