"""Core PawPal+ scheduling logic."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Iterable, Optional


def _parse_time_value(time_value: str) -> datetime.time:
    """Parse an HH:MM time string."""
    return datetime.strptime(time_value, "%H:%M").time()


def _priority_rank(priority: str) -> int:
    """Return a sorting rank for task priority."""
    order = {"high": 0, "medium": 1, "low": 2}
    return order.get(priority.lower(), 1)


@dataclass
class Task:
    """Represent a single pet care task."""

    description: str
    time: str
    due_date: date = field(default_factory=date.today)
    frequency: str = "once"
    completed: bool = False
    duration_minutes: int = 15
    priority: str = "medium"
    pet_name: str = ""

    def __post_init__(self) -> None:
        """Normalize and validate task data."""
        _parse_time_value(self.time)
        self.frequency = self.frequency.lower()
        self.priority = self.priority.lower()

    def scheduled_datetime(self) -> datetime:
        """Build the task's scheduled datetime."""
        return datetime.combine(self.due_date, _parse_time_value(self.time))

    def mark_complete(self) -> Optional[Task]:
        """Mark the task complete and return the next recurring task if needed."""
        self.completed = True
        if self.frequency not in {"daily", "weekly"}:
            return None
        offset_days = 1 if self.frequency == "daily" else 7
        return Task(
            description=self.description,
            time=self.time,
            due_date=self.due_date + timedelta(days=offset_days),
            frequency=self.frequency,
            completed=False,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            pet_name=self.pet_name,
        )

    def summary(self) -> str:
        """Format the task for terminal output."""
        status = "done" if self.completed else "pending"
        return (
            f"{self.due_date.isoformat()} {self.time} - {self.description} "
            f"({self.pet_name or 'unassigned'}, {self.duration_minutes} min, "
            f"priority {self.priority}, {status})"
        )

    def __str__(self) -> str:
        """Return a readable task string."""
        return self.summary()


@dataclass
class Pet:
    """Represent a pet and the tasks attached to it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> Task:
        """Add a task to the pet and attach the pet name."""
        task.pet_name = self.name
        self.tasks.append(task)
        return task

    def complete_task(self, task_index: int) -> Optional[Task]:
        """Complete a task by index and append the next recurring task if needed."""
        task = self.tasks[task_index]
        next_task = task.mark_complete()
        if next_task is not None:
            self.add_task(next_task)
        return next_task

    def incomplete_tasks(self) -> list[Task]:
        """Return the pet's pending tasks."""
        return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
    """Represent the owner of one or more pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> Pet:
        """Add a pet, or update an existing one with the same name."""
        existing = self.find_pet(pet.name)
        if existing is not None:
            existing.species = pet.species
            return existing
        self.pets.append(pet)
        return pet

    def find_pet(self, pet_name: str) -> Optional[Pet]:
        """Find a pet by name."""
        return next((pet for pet in self.pets if pet.name == pet_name), None)

    def get_all_tasks(self) -> list[Task]:
        """Collect every task from every pet."""
        tasks: list[Task] = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


@dataclass
class Scheduler:
    """Organize, filter, and inspect owner tasks."""

    owner: Owner

    def all_tasks(self) -> list[Task]:
        """Return all tasks for the owner."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: Optional[Iterable[Task]] = None) -> list[Task]:
        """Sort tasks by due date, time, and priority."""
        task_list = list(tasks) if tasks is not None else self.all_tasks()
        return sorted(
            task_list,
            key=lambda task: (
                task.due_date,
                _parse_time_value(task.time),
                _priority_rank(task.priority),
                task.pet_name,
                task.description,
            ),
        )

    def filter_tasks(
        self,
        tasks: Optional[Iterable[Task]] = None,
        *,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
        frequency: Optional[str] = None,
        due_date: Optional[date] = None,
    ) -> list[Task]:
        """Filter tasks by pet, completion state, frequency, or date."""
        filtered = list(tasks) if tasks is not None else self.all_tasks()
        if pet_name is not None:
            filtered = [task for task in filtered if task.pet_name == pet_name]
        if completed is not None:
            filtered = [task for task in filtered if task.completed == completed]
        if frequency is not None:
            filtered = [task for task in filtered if task.frequency == frequency.lower()]
        if due_date is not None:
            filtered = [task for task in filtered if task.due_date == due_date]
        return filtered

    def tasks_for_day(self, day: Optional[date] = None, *, include_completed: bool = False) -> list[Task]:
        """Return the tasks scheduled for a specific day."""
        target_day = day or date.today()
        day_tasks = self.filter_tasks(due_date=target_day)
        if not include_completed:
            day_tasks = [task for task in day_tasks if not task.completed]
        return self.sort_by_time(day_tasks)

    def detect_conflicts(self, tasks: Optional[Iterable[Task]] = None) -> list[str]:
        """Report tasks that share the same date and time."""
        task_list = list(tasks) if tasks is not None else self.all_tasks()
        grouped: dict[datetime, list[Task]] = {}
        for task in task_list:
            grouped.setdefault(task.scheduled_datetime(), []).append(task)

        warnings: list[str] = []
        for scheduled_time, grouped_tasks in grouped.items():
            if len(grouped_tasks) > 1:
                task_descriptions = "; ".join(
                    f"{task.pet_name or 'unassigned'}: {task.description}"
                    for task in self.sort_by_time(grouped_tasks)
                )
                warnings.append(
                    f"Conflict at {scheduled_time.strftime('%Y-%m-%d %H:%M')}: {task_descriptions}"
                )
        return warnings

    def mark_task_complete(self, pet_name: str, task_index: int) -> Optional[Task]:
        """Mark a pet task complete by pet name and index."""
        pet = self.owner.find_pet(pet_name)
        if pet is None:
            raise ValueError(f"Unknown pet: {pet_name}")
        return pet.complete_task(task_index)

    def format_schedule(self, tasks: Optional[Iterable[Task]] = None) -> str:
        """Format a schedule as readable terminal text."""
        task_list = self.sort_by_time(tasks)
        if not task_list:
            return "No tasks scheduled."
        return "\n".join(f"- {task.summary()}" for task in task_list)
