# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The initial UML design consisted of four classes: Owner, Pet, Task, and Scheduler. The Owner class was responsible for storing contact information and holding a list of pets. The Pet class tracked species, breed, age, and medical history, and maintained its own list of associated tasks. The Task class represented a single care action with a title, category, and completion status. The Scheduler class acted as the central coordinator, holding a reference to the owner and a queue of all tasks to be managed.

**b. Design changes**

Yes, the design changed during implementation. The first draft of the Scheduler did not account for constraints. It simply held a list of tasks with no logic for time availability, priority, or owner preferences. After revisiting the design, `priority`, `estimated_duration`, and `deadline` were added to `Task`, and `start_time`, `end_time`, and `preferences` were added to `Owner`. The `Scheduler` gained `apply_constraints()`, `prioritize_tasks()`, and `explain_plan()` methods so the daily plan could be built around what the owner actually has time for, rather than just listing all pending tasks.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
