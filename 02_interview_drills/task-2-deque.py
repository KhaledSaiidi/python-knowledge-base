from collections import deque
from dataclasses import dataclass, field


@dataclass
class Task:
    task_id: str
    priority: int
    status: str
    dependencies: list[str] | None = None
    submitted_at: int | None = None
    payload: dict[str, str] | None = None


@dataclass
class DependencyAwareTaskQueue:
    tasks: deque[Task] = field(default_factory=deque)
    _tasks_by_id: dict[str, Task] = field(default_factory=dict, init=False, repr=False)

    def get_task(self, task_id: str) -> Task:
        task = self._tasks_by_id.get(task_id)
        if task is None:
            raise ValueError(f"No task has the ID {task_id}")
        return task

    def add_task(
        self,
        task_id: str,
        priority: int,
        dependencies: list[str] | None = None,
        payload: dict[str, str] | None = None,
        submitted_at: int | None = None,
    ) -> None:
        if task_id in self._tasks_by_id:
            raise ValueError(f"{task_id} task already exists")

        dependency_ids = list(dependencies) if dependencies else []

        # Option A from the prompt: reject tasks that depend on unknown task IDs.
        for dependency_id in dependency_ids:
            if dependency_id not in self._tasks_by_id:
                raise ValueError(f"Unknown dependency: {dependency_id}")
            if dependency_id == task_id:
                raise ValueError("A task cannot depend on itself")

        status = "blocked" if self._has_incomplete_dependencies(dependency_ids) else "pending"
        task = Task(
            task_id=task_id,
            priority=priority,
            status=status,
            dependencies=dependency_ids or None,
            submitted_at=submitted_at,
            payload=payload,
        )
        self.tasks.append(task)
        self._tasks_by_id[task_id] = task

    def get_next_task(self) -> str | None:
        self._refresh_task_statuses()

        next_task: Task | None = None
        for task in self.tasks:
            if task.status != "pending":
                continue
            if next_task is None or self._is_better_candidate(task, next_task):
                next_task = task

        if next_task is None:
            return None

        next_task.status = "in_progress"
        return next_task.task_id

    def complete_task(self, task_id: str) -> None:
        task = self.get_task(task_id)
        if task.status == "blocked":
            raise ValueError(f"The task with ID {task_id} is blocked")
        if task.status != "in_progress":
            raise ValueError(f"The task with ID {task_id} is not in progress")
        task.status = "completed"

    def get_status(self, task_id: str) -> str | None:
        self._refresh_task_statuses()
        task = self._tasks_by_id.get(task_id)
        if task is None:
            return None
        return task.status

    def get_blocked_tasks(self) -> list[str]:
        self._refresh_task_statuses()
        return [task.task_id for task in self.tasks if task.status == "blocked"]

    def pending_count(self) -> int:
        self._refresh_task_statuses()
        return sum(1 for task in self.tasks if task.status == "pending")

    def completed_count(self) -> int:
        return sum(1 for task in self.tasks if task.status == "completed")

    def _refresh_task_statuses(self) -> None:
        for task in self.tasks:
            if task.status in {"completed", "in_progress"}:
                continue
            if self._has_incomplete_dependencies(task.dependencies or []):
                task.status = "blocked"
            else:
                task.status = "pending"

    def _has_incomplete_dependencies(self, dependency_ids: list[str]) -> bool:
        for dependency_id in dependency_ids:
            dependency = self._tasks_by_id[dependency_id]
            if dependency.status != "completed":
                return True
        return False

    def _is_better_candidate(self, candidate: Task, current_best: Task) -> bool:
        if candidate.priority != current_best.priority:
            return candidate.priority > current_best.priority

        candidate_submitted_at = (
            candidate.submitted_at if candidate.submitted_at is not None else float("inf")
        )
        current_best_submitted_at = (
            current_best.submitted_at if current_best.submitted_at is not None else float("inf")
        )
        if candidate_submitted_at != current_best_submitted_at:
            return candidate_submitted_at < current_best_submitted_at

        return candidate.task_id < current_best.task_id


if __name__ == "__main__":
    queue = DependencyAwareTaskQueue()
    queue.add_task("label-image-1", priority=5, submitted_at=1)
    queue.add_task("validate-image-1", priority=4, submitted_at=2)

    queue.add_task(
        "audit-image-1",
        priority=100,
        dependencies=["label-image-1", "validate-image-1"],
        submitted_at=3,
    )

    queue.add_task("quick-independent", priority=20, submitted_at=4)
    queue.add_task("low-independent", priority=1, submitted_at=5)

    assert queue.get_task("label-image-1").task_id == "label-image-1"
    assert queue.pending_count() == 4
    assert queue.completed_count() == 0

    first_task = queue.get_next_task()
    print("First task:", first_task)
    assert first_task == "quick-independent"
    assert queue.get_status("quick-independent") == "in_progress"

    assert queue.get_status("audit-image-1") == "blocked"
    assert queue.get_blocked_tasks() == ["audit-image-1"]

    try:
        queue.complete_task("audit-image-1")
        assert False, "Expected ValueError when completing blocked task"
    except ValueError:
        pass

    queue.complete_task("quick-independent")
    assert queue.get_status("quick-independent") == "completed"
    assert queue.completed_count() == 1

    second_task = queue.get_next_task()
    print("Second task:", second_task)
    assert second_task == "label-image-1"
    assert queue.get_status("label-image-1") == "in_progress"

    queue.complete_task("label-image-1")
    assert queue.get_status("label-image-1") == "completed"
    assert queue.completed_count() == 2

    assert queue.get_status("audit-image-1") == "blocked"
    assert queue.get_blocked_tasks() == ["audit-image-1"]

    third_task = queue.get_next_task()
    print("Third task:", third_task)
    assert third_task == "validate-image-1"
    assert queue.get_status("validate-image-1") == "in_progress"

    queue.complete_task("validate-image-1")
    assert queue.get_status("validate-image-1") == "completed"
    assert queue.completed_count() == 3

    fourth_task = queue.get_next_task()
    print("Fourth task:", fourth_task)
    assert fourth_task == "audit-image-1"
    assert queue.get_status("audit-image-1") == "in_progress"

    queue.complete_task("audit-image-1")
    assert queue.get_status("audit-image-1") == "completed"
    assert queue.completed_count() == 4

    fifth_task = queue.get_next_task()
    print("Fifth task:", fifth_task)
    assert fifth_task == "low-independent"
    assert queue.get_status("low-independent") == "in_progress"

    queue.complete_task("low-independent")
    assert queue.get_status("low-independent") == "completed"
    assert queue.completed_count() == 5

    assert queue.get_next_task() is None
    assert queue.get_status("unknown-task") is None

    try:
        queue.add_task("label-image-1", priority=1, submitted_at=10)
        assert False, "Expected ValueError when adding duplicate task"
    except ValueError:
        pass
