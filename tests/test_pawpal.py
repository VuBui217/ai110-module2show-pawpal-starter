import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime, time
from pawpal_system import Owner, Pet, Task


def make_task(title="Test Task"):
    return Task(
        title=title,
        description="A test task",
        category="exercise",
        priority=1,
        estimated_duration=30,
        deadline=datetime.today().replace(hour=10, minute=0),
    )


def make_pet():
    owner = Owner("Test Owner", "test@test.com", time(8, 0), time(12, 0))
    return Pet(name="Buddy", species="Dog", breed="Lab", age=2, owner=owner)


def test_mark_complete_changes_status():
    task = make_task()
    assert task.is_completed == False
    task.mark_complete()
    assert task.is_completed == True


def test_add_task_increases_pet_task_count():
    pet = make_pet()
    assert len(pet.tasks) == 0
    pet.add_task(make_task("Walk"))
    pet.add_task(make_task("Feed"))
    assert len(pet.tasks) == 2
