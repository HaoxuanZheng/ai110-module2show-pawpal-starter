"""Tests for PawPal+."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_creates_next_daily_task() -> None:
    """Daily tasks should spawn the next occurrence when completed."""
    task = Task("Medication", "08:00", due_date=date(2026, 7, 5), frequency="daily")

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == date(2026, 7, 6)
    assert next_task.completed is False
    assert next_task.frequency == "daily"


def test_add_task_increases_pet_task_count() -> None:
    """Adding a task should increase the pet's task count."""
    pet = Pet("Mochi", "cat")

    pet.add_task(Task("Breakfast", "08:30", due_date=date(2026, 7, 5)))

    assert len(pet.tasks) == 1


def test_sort_by_time_orders_tasks_chronologically() -> None:
    """The scheduler should sort tasks by date and time."""
    owner = Owner("Jordan")
    pet = owner.add_pet(Pet("Mochi", "cat"))
    pet.add_task(Task("Later", "09:00", due_date=date(2026, 7, 5)))
    pet.add_task(Task("Earlier", "07:30", due_date=date(2026, 7, 5)))
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_time()

    assert [task.description for task in sorted_tasks] == ["Earlier", "Later"]


def test_detect_conflicts_flags_duplicate_times() -> None:
    """The scheduler should warn about exact time collisions."""
    owner = Owner("Jordan")
    mochi = owner.add_pet(Pet("Mochi", "cat"))
    luna = owner.add_pet(Pet("Luna", "dog"))
    mochi.add_task(Task("Breakfast", "08:00", due_date=date(2026, 7, 5)))
    luna.add_task(Task("Medication", "08:00", due_date=date(2026, 7, 5)))
    scheduler = Scheduler(owner)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "Conflict at 2026-07-05 08:00" in warnings[0]
