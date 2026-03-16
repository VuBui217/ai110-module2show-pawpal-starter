# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app that helps a pet owner plan daily care tasks for their pets based on time availability, priority, and owner preferences.

---

## Features

### Owner Management
- Enter owner name, contact info, and daily availability window (start time → end time)
- Set blocked task categories via preferences (e.g. `no_grooming` skips all grooming tasks)

### Pet Management
- Register multiple pets with name, species, breed, and age
- All pets are linked to the owner and persist for the session

### Task Management
- Add tasks to any registered pet
- Each task includes: title, description, category, priority (1 = highest), duration (minutes), and deadline
- Supported categories: `exercise`, `feeding`, `medication`, `grooming`, `enrichment`, `other`

### Smart Scheduling
- Generates a daily plan that fits within the owner's available time
- Tasks are sorted by priority then deadline before scheduling
- Tasks that exceed remaining time or match a blocked category are automatically excluded
- Displays total scheduled time vs. available time

### Plan Explanation
- Every include/exclude decision is logged with a plain-English reason
- Full rationale is shown in an expandable "Plan Explanation" section in the UI

---

## Project Structure

```
pawpal_system.py   # Backend: Owner, Pet, Task, Scheduler classes
app.py             # Frontend: Streamlit UI connected to backend
main.py            # Demo script — runs a sample schedule in the terminal
tests/
  test_pawpal.py   # Pytest unit tests
reflection.md      # Project reflection and design notes
requirements.txt   # Dependencies
```

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Running the App

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`. Use the UI to:
1. Save an owner with availability and preferences
2. Add one or more pets
3. Add tasks to each pet
4. Click **Generate Schedule** to build and explain today's plan

---

## Running the Terminal Demo

```bash
python main.py
```

Runs a hardcoded demo with two pets (Buddy + Luna) and five tasks, printing today's schedule and plan explanation to the terminal.

---

## Running Tests

```bash
python -m pytest tests/ -v
```

Current tests in `tests/test_pawpal.py`:

| Test | What it checks |
|---|---|
| `test_mark_complete_changes_status` | `Task.mark_complete()` sets `is_completed` to `True` |
| `test_add_task_increases_pet_task_count` | `Pet.add_task()` correctly grows the task list |

---

## Class Overview

| Class | Responsibility |
|---|---|
| `Owner` | Stores contact info, availability window, preferences, and list of pets |
| `Pet` | Tracks species, breed, medical history, and a list of tasks |
| `Task` | Represents one care action with priority, duration, deadline, and completion status |
| `Scheduler` | Generates a daily plan by applying constraints and explaining every decision |

---

## Preferences Format

Owner preferences use a `no_<category>` convention to block task categories:

```
no_grooming     → skips all grooming tasks
no_exercise     → skips all exercise tasks
```

Multiple preferences can be entered comma-separated in the UI.
