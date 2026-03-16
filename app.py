import streamlit as st
from datetime import datetime, time

# Step 1: Import classes from backend
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# -------------------------------------------------------
# Step 2: Initialize session_state — only runs once per session
# -------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

# -------------------------------------------------------
# Section 1: Owner Setup
# -------------------------------------------------------
st.subheader("Owner Info")

with st.form("owner_form"):
    owner_name    = st.text_input("Owner name", value="Jordan")
    contact_info  = st.text_input("Contact info", value="jordan@email.com")
    start_time    = st.time_input("Available from", value=time(8, 0))
    end_time      = st.time_input("Available until", value=time(11, 0))
    raw_prefs     = st.text_input("Blocked categories (comma-separated, e.g. no_grooming)", value="")
    owner_submit  = st.form_submit_button("Save Owner")

if owner_submit:
    # Step 3: Wire form submission → Owner constructor
    owner = Owner(owner_name, contact_info, start_time, end_time)
    prefs = [p.strip() for p in raw_prefs.split(",") if p.strip()]
    owner.update_preferences(prefs)
    st.session_state.owner = owner
    st.session_state.scheduler = Scheduler(owner)
    st.success(f"Owner '{owner_name}' saved. Available: {start_time.strftime('%I:%M %p')} – {end_time.strftime('%I:%M %p')}")

st.divider()

# -------------------------------------------------------
# Section 2: Add a Pet
# -------------------------------------------------------
st.subheader("Add a Pet")

if st.session_state.owner is None:
    st.info("Save an owner first before adding pets.")
else:
    with st.form("pet_form"):
        pet_name    = st.text_input("Pet name", value="Buddy")
        species     = st.selectbox("Species", ["dog", "cat", "bird", "other"])
        breed       = st.text_input("Breed", value="Labrador")
        age         = st.number_input("Age (years)", min_value=0, max_value=30, value=3)
        pet_submit  = st.form_submit_button("Add Pet")

    if pet_submit:
        # Step 3: Wire form submission → Owner.add_pet()
        new_pet = Pet(pet_name, species, breed, int(age), st.session_state.owner)
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Added pet '{pet_name}' ({species}).")

    # Display current pets
    pets = st.session_state.owner.pets
    if pets:
        st.write("**Registered pets:**")
        for p in pets:
            st.write(f"- {p.name} ({p.species}, {p.breed}, age {p.age})")

st.divider()

# -------------------------------------------------------
# Section 3: Add a Task
# -------------------------------------------------------
st.subheader("Add a Task")

if st.session_state.owner is None or not st.session_state.owner.pets:
    st.info("Add at least one pet before adding tasks.")
else:
    pets = st.session_state.owner.pets
    pet_names = [p.name for p in pets]

    with st.form("task_form"):
        selected_pet  = st.selectbox("Assign to pet", pet_names)
        task_title    = st.text_input("Task title", value="Morning walk")
        description   = st.text_input("Description", value="")
        category      = st.selectbox("Category", ["exercise", "feeding", "medication", "grooming", "enrichment", "other"])
        priority      = st.number_input("Priority (1 = highest)", min_value=1, max_value=10, value=1)
        duration      = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30)
        deadline_date = st.date_input("Deadline date", value=datetime.today().date())
        deadline_time = st.time_input("Deadline time", value=time(10, 0))
        task_submit   = st.form_submit_button("Add Task")

    if task_submit:
        # Step 3: Wire form submission → Pet.add_task()
        pet = next(p for p in pets if p.name == selected_pet)
        deadline = datetime.combine(deadline_date, deadline_time)
        new_task = Task(task_title, description, category, int(priority), float(duration), deadline)
        pet.add_task(new_task)
        st.success(f"Task '{task_title}' added to {pet.name}.")

    # Display tasks per pet
    for pet in pets:
        if pet.tasks:
            st.write(f"**{pet.name}'s tasks:**")
            for t in pet.tasks:
                status = "✓" if t.is_completed else "○"
                st.write(f"  [{status}] {t.title} — {t.category}, {t.estimated_duration} min, priority {t.priority}")

st.divider()

# -------------------------------------------------------
# Section 4: Generate Schedule
# -------------------------------------------------------
st.subheader("Build Schedule")

if st.session_state.scheduler is None:
    st.info("Save an owner to enable scheduling.")
else:
    if st.button("Generate Schedule"):
        scheduler = st.session_state.scheduler
        plan = scheduler.generate_daily_plan()
        today = datetime.today().strftime("%Y-%m-%d")
        scheduled = plan.get(today, [])

        st.markdown(f"### Today's Schedule ({today})")

        if not scheduled:
            st.warning("No tasks fit today's constraints.")
        else:
            for i, task in enumerate(scheduled, start=1):
                st.markdown(
                    f"**{i}. {task.title}** ({task.category})  \n"
                    f"Duration: {task.estimated_duration} min &nbsp;|&nbsp; "
                    f"Priority: {task.priority} &nbsp;|&nbsp; "
                    f"Deadline: {task.deadline.strftime('%I:%M %p')}"
                )

            total = sum(t.estimated_duration for t in scheduled)
            available = st.session_state.owner.available_minutes()
            st.info(f"Total scheduled: **{total} min** of {available} min available.")

        with st.expander("Plan Explanation"):
            st.text(scheduler.explain_plan())
