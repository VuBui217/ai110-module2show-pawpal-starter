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
        pass

    def remove_pet(self, pet: "Pet") -> None:
        pass

    def update_availability(self, start_time: time, end_time: time) -> None:
        pass

    def update_preferences(self, preferences: List[str]) -> None:
        pass


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
        pass

    def remove_task(self, task: "Task") -> None:
        pass

    def get_tasks_by_category(self, category: str) -> List["Task"]:
        pass


class Task:
    def __init__(self, title: str, description: str, category: str, priority: int,
                 estimated_duration: float, deadline: datetime):
        self.title: str = title
        self.description: str = description
        self.category: str = category
        self.priority: int = priority
        self.estimated_duration: float = estimated_duration
        self.deadline: datetime = deadline
        self.is_completed: bool = False
        self.recurrence_pattern: Optional[str] = None

    def mark_complete(self) -> None:
        pass

    def is_overdue(self) -> bool:
        pass

    def compare_priority(self, other: "Task") -> int:
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner: Owner = owner
        self.scheduled_tasks: List[Task] = []
        self.daily_plan: Dict[str, List[Task]] = {}
        self.plan_rationale: List[str] = []

    def generate_daily_plan(self) -> Dict[str, List[Task]]:
        pass

    def apply_constraints(self) -> None:
        pass

    def prioritize_tasks(self) -> List[Task]:
        pass

    def explain_plan(self) -> str:
        pass

    def reschedule_task(self, task: Task, new_time: datetime) -> None:
        pass

    def get_tasks_due_today(self) -> List[Task]:
        pass
