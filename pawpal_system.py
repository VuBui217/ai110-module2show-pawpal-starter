from datetime import datetime, time
from typing import List, Dict, Optional


class Owner:
    def __init__(self, name: str, contact_info: str, start_time: time, end_time: time):
        self.name: str = name
        self.contact_info: str = contact_info
        self.start_time: time = start_time
        self.end_time: time = end_time
        self.preferences: List[str] = []
        self.pets: List["Pet"] = []

    def add_pet(self, pet: "Pet") -> None:
        """Add a pet to the owner's list and set the back-reference."""
        if pet not in self.pets:
            self.pets.append(pet)
            pet.owner = self

    def remove_pet(self, pet: "Pet") -> None:
        """Remove a pet from the owner's list if present."""
        if pet in self.pets:
            self.pets.remove(pet)

    def update_availability(self, start_time: time, end_time: time) -> None:
        """Update the owner's daily availability window."""
        self.start_time = start_time
        self.end_time = end_time

    def update_preferences(self, preferences: List[str]) -> None:
        """Replace the owner's preference list (e.g. ['no_grooming'])."""
        self.preferences = preferences

    def available_minutes(self) -> int:
        """Total minutes the owner is available in a day."""
        start = datetime.combine(datetime.today(), self.start_time)
        end = datetime.combine(datetime.today(), self.end_time)
        return max(0, int((end - start).total_seconds() / 60))


class Pet:
    def __init__(self, name: str, species: str, breed: str, age: int, owner: "Owner"):
        self.name: str = name
        self.species: str = species
        self.breed: str = breed
        self.age: int = age
        self.medical_history: List[str] = []
        self.tasks: List["Task"] = []
        self.owner: Owner = owner

    def add_task(self, task: "Task") -> None:
        """Add a task to the pet's list, ignoring duplicates."""
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: "Task") -> None:
        """Remove a task from the pet's list if present."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks_by_category(self, category: str) -> List["Task"]:
        """Return all tasks matching the given category (case-insensitive)."""
        return [t for t in self.tasks if t.category.lower() == category.lower()]


class Task:
    def __init__(self, title: str, description: str, category: str, priority: int,
                 estimated_duration: float, deadline: datetime):
        self.title: str = title
        self.description: str = description
        self.category: str = category
        self.priority: int = priority          # 1 = highest, higher number = lower priority
        self.estimated_duration: float = estimated_duration  # in minutes
        self.deadline: datetime = deadline
        self.is_completed: bool = False
        self.recurrence_pattern: Optional[str] = None
        self.scheduled_time: Optional[datetime] = None

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def is_overdue(self) -> bool:
        """Return True if the task is incomplete and past its deadline."""
        return not self.is_completed and datetime.now() > self.deadline

    def compare_priority(self, other: "Task") -> int:
        """Returns -1 if self is higher priority, 1 if lower, 0 if equal."""
        if self.priority < other.priority:
            return -1
        elif self.priority > other.priority:
            return 1
        return 0


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner: Owner = owner
        self.scheduled_tasks: List[Task] = []
        self.daily_plan: Dict[str, List[Task]] = {}
        self.plan_rationale: List[str] = []

    def generate_daily_plan(self) -> Dict[str, List[Task]]:
        """Build today's plan by applying constraints and prioritizing tasks."""
        today = datetime.today().strftime("%Y-%m-%d")
        self.plan_rationale = []

        self.apply_constraints()

        self.daily_plan[today] = self.scheduled_tasks
        return self.daily_plan

    def apply_constraints(self) -> None:
        """Filter and fit tasks within the owner's available time and preferences."""
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend([t for t in pet.tasks if not t.is_completed])

        prioritized = sorted(all_tasks, key=lambda t: (t.priority, t.deadline))

        available = self.owner.available_minutes()
        scheduled = []
        time_used = 0

        for task in prioritized:
            # Skip categories the owner has blocked via preferences
            blocked = [p for p in self.owner.preferences if p.startswith("no_")]
            blocked_categories = [b.replace("no_", "") for b in blocked]
            if task.category.lower() in blocked_categories:
                self.plan_rationale.append(
                    f"EXCLUDED '{task.title}': category '{task.category}' blocked by owner preferences."
                )
                continue

            if time_used + task.estimated_duration <= available:
                scheduled.append(task)
                time_used += task.estimated_duration
                self.plan_rationale.append(
                    f"INCLUDED '{task.title}' (priority={task.priority}, "
                    f"duration={task.estimated_duration}min): fits within available time."
                )
            else:
                self.plan_rationale.append(
                    f"EXCLUDED '{task.title}': adding {task.estimated_duration}min would exceed "
                    f"available {available}min (used={time_used}min)."
                )

        self.scheduled_tasks = scheduled

    def prioritize_tasks(self) -> List[Task]:
        """Return all incomplete tasks sorted by priority then deadline."""
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend([t for t in pet.tasks if not t.is_completed])
        return sorted(all_tasks, key=lambda t: (t.priority, t.deadline))

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why the plan was built this way."""
        if not self.plan_rationale:
            return "No plan has been generated yet. Call generate_daily_plan() first."

        available = self.owner.available_minutes()
        total_scheduled = sum(t.estimated_duration for t in self.scheduled_tasks)
        lines = [
            f"Daily plan for {self.owner.name}",
            f"Available time: {available} minutes | Scheduled: {total_scheduled} minutes",
            "",
            "Task decisions:",
        ]
        for reason in self.plan_rationale:
            lines.append(f"  - {reason}")

        if self.owner.preferences:
            lines.append(f"\nOwner preferences applied: {', '.join(self.owner.preferences)}")

        return "\n".join(lines)

    def reschedule_task(self, task: Task, new_time: datetime) -> None:
        """Update a task's scheduled time."""
        task.scheduled_time = new_time

    def get_tasks_due_today(self) -> List[Task]:
        """Return all incomplete tasks whose deadline falls on today."""
        today = datetime.today().date()
        due = []
        for pet in self.owner.pets:
            for task in pet.tasks:
                if not task.is_completed and task.deadline.date() == today:
                    due.append(task)
        return due
