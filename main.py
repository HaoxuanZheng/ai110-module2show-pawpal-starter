"""CLI demo for PawPal+."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_owner() -> Owner:
    """Create a demo owner with pets and tasks."""
    owner = Owner("Jordan")

    mochi = owner.add_pet(Pet("Mochi", "cat"))
    luna = owner.add_pet(Pet("Luna", "dog"))

    mochi.add_task(
        Task(
            "Breakfast feeding",
            "08:30",
            due_date=date(2026, 7, 5),
            duration_minutes=10,
            priority="high",
        )
    )
    mochi.add_task(
        Task(
            "Evening play",
            "18:00",
            due_date=date(2026, 7, 5),
            duration_minutes=20,
            priority="medium",
        )
    )
    luna.add_task(
        Task(
            "Morning walk",
            "07:30",
            due_date=date(2026, 7, 5),
            duration_minutes=25,
            priority="high",
            frequency="daily",
        )
    )
    luna.add_task(
        Task(
            "Medication",
            "08:30",
            due_date=date(2026, 7, 5),
            duration_minutes=5,
            priority="high",
            frequency="daily",
        )
    )

    return owner


def main() -> None:
    """Print the demo schedule and a few scheduler behaviors."""
    owner = build_demo_owner()
    scheduler = Scheduler(owner)
    today = date(2026, 7, 5)

    print(f"Today's Schedule for {owner.name}")
    print(scheduler.format_schedule(scheduler.tasks_for_day(today)))
    print()

    warnings = scheduler.detect_conflicts(scheduler.tasks_for_day(today))
    print("Conflict Check")
    if warnings:
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("- No conflicts found")
    print()

    print("Recurring Task Demo")
    next_task = scheduler.mark_task_complete("Luna", 1)
    if next_task is not None:
        print(f"- Created next occurrence: {next_task.summary()}")
    print("- Tomorrow's schedule")
    print(scheduler.format_schedule(scheduler.tasks_for_day(date(2026, 7, 6))))


if __name__ == "__main__":
    main()
