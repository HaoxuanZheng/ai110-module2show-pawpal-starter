from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("CLI-first logic, Streamlit-friendly controls.")


def get_owner(owner_name: str) -> Owner:
    """Return the session owner and keep the name in sync."""
    if "owner" not in st.session_state:
        st.session_state.owner = Owner(owner_name)
    elif st.session_state.owner.name != owner_name:
        st.session_state.owner.name = owner_name
    return st.session_state.owner


owner_name = st.text_input("Owner name", value=st.session_state.get("owner_name", "Jordan"))
st.session_state.owner_name = owner_name
owner = get_owner(owner_name)
scheduler = Scheduler(owner)

st.markdown(
    """
PawPal+ keeps track of pets and their care tasks, then builds a readable daily schedule.
Use the forms below to add pets and tasks, and the planner will sort the result for you.
"""
)

with st.form("add_pet_form"):
    st.subheader("Add a Pet")
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet = st.form_submit_button("Add pet")
    if add_pet and pet_name.strip():
        owner.add_pet(Pet(pet_name.strip(), species))
        st.success(f"Added {pet_name.strip()}.")

if owner.pets:
    pet_options = [pet.name for pet in owner.pets]
    with st.form("add_task_form"):
        st.subheader("Add a Task")
        selected_pet_name = st.selectbox("Pet", pet_options)
        description = st.text_input("Task description", value="Morning walk")
        time_value = st.text_input("Time (HH:MM)", value="08:00")
        due_date = st.date_input("Date", value=date.today())
        duration_minutes = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        add_task = st.form_submit_button("Add task")
        if add_task and description.strip():
            pet = owner.find_pet(selected_pet_name)
            if pet is not None:
                pet.add_task(
                    Task(
                        description.strip(),
                        time_value,
                        due_date=due_date,
                        frequency=frequency,
                        duration_minutes=int(duration_minutes),
                        priority=priority,
                    )
                )
                st.success(f"Added task for {selected_pet_name}.")
else:
    st.info("Add at least one pet before creating tasks.")

st.divider()

st.subheader("Today's Schedule")
today = st.date_input("Schedule date", value=date.today(), key="schedule_date")
todays_tasks = scheduler.tasks_for_day(today, include_completed=True)

view_columns = st.columns(2)
with view_columns[0]:
    pet_filter_options = ["All pets"] + [pet.name for pet in owner.pets]
    selected_pet_filter = st.selectbox("Filter by pet", pet_filter_options)
with view_columns[1]:
    status_filter = st.selectbox("Filter by status", ["All statuses", "pending", "done"])

filtered_tasks = todays_tasks
if selected_pet_filter != "All pets":
    filtered_tasks = scheduler.filter_tasks(filtered_tasks, pet_name=selected_pet_filter)
if status_filter != "All statuses":
    filtered_tasks = scheduler.filter_tasks(filtered_tasks, completed=(status_filter == "done"))

if filtered_tasks:
    schedule_rows = [
        {
            "Time": task.time,
            "Pet": task.pet_name or "Unassigned",
            "Task": task.description,
            "Priority": task.priority,
            "Frequency": task.frequency,
            "Status": "done" if task.completed else "pending",
        }
        for task in scheduler.sort_by_time(filtered_tasks)
    ]
    st.table(schedule_rows)
else:
    st.info("No tasks match the current filters for this date.")

conflicts = scheduler.detect_conflicts(todays_tasks)
if conflicts:
    st.warning("Potential scheduling conflict detected:\n" + "\n".join(conflicts))
else:
    st.success("No exact-time conflicts found for this date.")
