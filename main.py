from datetime import datetime, time
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup Owner ---
owner = Owner(
    name="Alex Rivera",
    contact_info="alex@email.com",
    start_time=time(8, 0),   # available 8:00 AM
    end_time=time(11, 0),    # until 11:00 AM (180 minutes)
)
owner.update_preferences(["no_grooming"])  # block grooming tasks today

# --- Setup Pets ---
buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3, owner=owner)
luna  = Pet(name="Luna",  species="Cat", breed="Siamese",  age=5, owner=owner)

owner.add_pet(buddy)
owner.add_pet(luna)

# --- Add Tasks to Buddy ---
buddy.add_task(Task(
    title="Morning Walk",
    description="30-minute walk around the block",
    category="exercise",
    priority=1,
    estimated_duration=30,
    deadline=datetime.today().replace(hour=9, minute=0),
))
buddy.add_task(Task(
    title="Flea Medicine",
    description="Apply monthly flea treatment",
    category="medication",
    priority=2,
    estimated_duration=10,
    deadline=datetime.today().replace(hour=10, minute=0),
))
buddy.add_task(Task(
    title="Bath & Brush",
    description="Full grooming session",
    category="grooming",
    priority=3,
    estimated_duration=60,
    deadline=datetime.today().replace(hour=11, minute=0),
))

# --- Add Tasks to Luna ---
luna.add_task(Task(
    title="Breakfast Feeding",
    description="Half cup of dry food",
    category="feeding",
    priority=1,
    estimated_duration=5,
    deadline=datetime.today().replace(hour=8, minute=30),
))
luna.add_task(Task(
    title="Playtime",
    description="Interactive toy session",
    category="enrichment",
    priority=3,
    estimated_duration=20,
    deadline=datetime.today().replace(hour=10, minute=30),
))

# --- Generate Plan ---
scheduler = Scheduler(owner=owner)
plan = scheduler.generate_daily_plan()
today = datetime.today().strftime("%Y-%m-%d")

# --- Print Today's Schedule ---
print("=" * 45)
print(f"  PawPal+ — Today's Schedule ({today})")
print("=" * 45)

scheduled = plan.get(today, [])
if not scheduled:
    print("No tasks scheduled for today.")
else:
    for i, task in enumerate(scheduled, start=1):
        status = "✓" if task.is_completed else "○"
        print(f"{i}. [{status}] {task.title} ({task.category})")
        print(f"     Duration : {task.estimated_duration} min")
        print(f"     Priority : {task.priority}")
        print(f"     Deadline : {task.deadline.strftime('%I:%M %p')}")

total = sum(t.estimated_duration for t in scheduled)
print("-" * 45)
print(f"  Total scheduled time : {total} min")
print(f"  Available time       : {owner.available_minutes()} min")
print("=" * 45)

print("\n--- Plan Explanation ---")
print(scheduler.explain_plan())
