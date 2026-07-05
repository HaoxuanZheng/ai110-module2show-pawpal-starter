# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

I designed four core classes: `Task` for individual care items, `Pet` for grouping a pet's tasks, `Owner` for managing multiple pets, and `Scheduler` for sorting, filtering, and conflict checks. The UML keeps behavior focused in the scheduler while `Pet` and `Owner` mainly act as containers and lookup helpers.

**b. Design changes**

Yes. I added `due_date`, `priority`, and recurrence handling to `Task` so the scheduler could support daily planning and recurring items without extra helper objects. I also gave `Task.mark_complete()` the ability to create the next occurrence, which kept recurrence logic close to the task itself.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers due date, task time, priority, completion state, recurrence, and pet ownership. I treated date and time as the primary constraints because they drive the daily schedule, then used priority as a tie-breaker so urgent care tasks rise to the top when times collide.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
The scheduler only detects exact time matches, not overlapping durations. That is reasonable for a first version because the assignment focuses on simple daily routines, and exact collisions are easy to explain and verify in tests.
---

## 3. AI Collaboration

**a. How you used AI**

I used AI for UML brainstorming, class-skeleton generation, test drafting, and UI wiring ideas. The most useful prompts were specific ones that named the file and asked for one behavior at a time, such as sorting by time, recurring-task creation, or conflict detection.

**b. Judgment and verification**

I did not accept a more elaborate scheduling strategy that tried to reason about overlapping durations and task lengths. I kept the simpler exact-time conflict check because it matched the project scope, was easier to explain in reflection, and was directly covered by tests and the CLI demo.

Using separate chat sessions kept the phases from blending together. One session stayed focused on design and skeletons, another on core logic, another on testing, and that made it easier to compare suggestions without dragging earlier assumptions into later phases.

Being the lead architect meant treating AI output as a draft, not a decision. I had to decide which features belonged in the model, keep the design simple enough to test, and verify every important behavior with the CLI and pytest instead of trusting the first suggestion blindly.

---

## 4. Testing and Verification

**a. What you tested**

I tested task completion, task addition, chronological sorting, and conflict detection. Those cases matter because they verify the core state changes and the main scheduler rules that the rest of the app depends on.

**b. Confidence**

I am moderately confident because the main behaviors are covered by focused tests and the CLI demo prints a readable schedule. Next I would test invalid time strings, duplicate pet names, and multiple recurring completions across several days.

---

## 5. Reflection

**a. What went well**

I am most satisfied that the scheduler is now genuinely reusable: the same logic supports the CLI demo and the Streamlit UI, and the recurrence and conflict behaviors are visible in both places.

**b. What you would improve**

If I had another iteration, I would add persistence so pets and tasks survive refreshes, and I would improve conflict detection to reason about duration overlap instead of exact timestamp collisions.

**c. Key takeaway**

I learned that AI is most useful when it helps generate options quickly, but the human designer still has to keep the data model coherent, the scope realistic, and the verification tight.
