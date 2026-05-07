from dataclasses import dataclass, field
from typing import List
from datetime import datetime

@dataclass
class Task:
    task_id: str
    priority: int
    status: str
    dependencies: List[str] | None = None
    submitted_at: int | None = None
    payload: dict[str, str] | None = None


@dataclass
class DependencyAwareTaskQueue:
    tasks: List[Task] = field(default_factory=list)

    def get_task(self, task_id: str) -> Task:
        if self.tasks:
            for task in self.tasks:
                if task.task_id == task_id:
                    return task
            raise ValueError(f'No task have the ID {task_id}')
        raise ValueError(f'The queue is empty')
    
    def add_task(
        self,
        task_id: str,
        priority: int,
        dependencies: List[str] | None = None,
        payload: dict[str, str] | None = None,
        submitted_at: int | None = None,
    ) -> None:
        for task in self.tasks:
            if task.task_id == task_id:
                raise ValueError(f"{task_id} Task already exists")
        task = Task(task_id, priority, "pending", dependencies, submitted_at, payload)
        self.tasks.append(task)

    def get_next_task(self) -> str | None:
        if not self.tasks:
            return None
        nextTask = None
        for task in self.tasks:
            blocked = False
            if task.dependencies != None:
                for dep in task.dependencies:
                    dependency = self.get_task(dep)
                    if dependency.status != "completed":
                        blocked = True
                        task.status = "blocked"
                        break
            if blocked == False and task.status == "blocked":
                task.status = "pending"
            if task.status != "pending":
                continue
            if blocked != True:
                if not nextTask or task.priority > nextTask.priority:
                    nextTask = task
                elif task.priority == nextTask.priority:
                    if task.submitted_at < nextTask.submitted_at:
                        nextTask = task
                    elif task.submitted_at == nextTask.submitted_at:
                        if task.task_id < nextTask.task_id:
                            nextTask = task
        if nextTask is None:
            return None
        nextTask.status = "in_progress"
        return nextTask.task_id


    def complete_task(self, task_id: str) -> None:
        if self.tasks is None:
            raise ValueError(f'The queue is empty')
        for task in self.tasks:
            if task.task_id == task_id:
                if task.status == "blocked":
                    raise ValueError(f'The task with ID: {task_id} is blocked')
                task.status = "completed"
                return None
        raise ValueError(f'The task with ID: {task_id} doesn\'t exist') 

    def get_status(self, task_id: str) -> str | None:
        if self.tasks is None:
            raise ValueError(f'The queue is empty')
        for task in self.tasks:
            if task.task_id == task_id:
                return task.status
        return None

    def get_blocked_tasks(self) -> list[str]:
        blocked_tasks: list[str] = []
        if self.tasks is None:
            raise ValueError(f'The queue is empty')
        for task in self.tasks:
            if task.status == "blocked":
                blocked_tasks.append(task.task_id)
        return blocked_tasks


    def pending_count(self) -> int:
        count = 0
        if self.tasks is None:
            raise ValueError(f'The queue is empty')
        for task in self.tasks:
            if task.status == "pending":
                count += 1
        return count

    def completed_count(self) -> int:
        count = 0
        if self.tasks is None:
            raise ValueError(f'The queue is empty')
        for task in self.tasks:
            if task.status == "completed":
                count += 1
        return count





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

    # Test get_task()
    assert queue.get_task("label-image-1").task_id == "label-image-1"

    # Test initial counts
    assert queue.pending_count() == 5
    assert queue.completed_count() == 0

    # First scheduled task should be quick-independent.
    # audit-image-1 has higher priority, but it is blocked.
    first_task = queue.get_next_task()
    print("First task:", first_task)
    assert first_task == "quick-independent"
    assert queue.get_status("quick-independent") == "in_progress"

    # get_next_task() should have discovered that audit-image-1 is blocked.
    assert queue.get_status("audit-image-1") == "blocked"
    assert queue.get_blocked_tasks() == ["audit-image-1"]

    # Test completing a blocked task should fail.
    try:
        queue.complete_task("audit-image-1")
        assert False, "Expected ValueError when completing blocked task"
    except ValueError:
        pass

    # Complete first task
    queue.complete_task("quick-independent")
    assert queue.get_status("quick-independent") == "completed"
    assert queue.completed_count() == 1

    # Next task should be label-image-1.
    # audit-image-1 is still blocked because its dependencies are incomplete.
    second_task = queue.get_next_task()
    print("Second task:", second_task)
    assert second_task == "label-image-1"
    assert queue.get_status("label-image-1") == "in_progress"

    queue.complete_task("label-image-1")
    assert queue.get_status("label-image-1") == "completed"
    assert queue.completed_count() == 2

    # audit-image-1 should still be blocked because validate-image-1 is not completed yet.
    assert queue.get_status("audit-image-1") == "blocked"
    assert queue.get_blocked_tasks() == ["audit-image-1"]

    # Next task should be validate-image-1.
    third_task = queue.get_next_task()
    print("Third task:", third_task)
    assert third_task == "validate-image-1"
    assert queue.get_status("validate-image-1") == "in_progress"

    queue.complete_task("validate-image-1")
    assert queue.get_status("validate-image-1") == "completed"
    assert queue.completed_count() == 3

    # Now audit-image-1 should become unblocked and be selected next.
    fourth_task = queue.get_next_task()
    print("Fourth task:", fourth_task)
    assert fourth_task == "audit-image-1"
    assert queue.get_status("audit-image-1") == "in_progress"

    queue.complete_task("audit-image-1")
    assert queue.get_status("audit-image-1") == "completed"
    assert queue.completed_count() == 4

    # Last remaining task should be low-independent.
    fifth_task = queue.get_next_task()
    print("Fifth task:", fifth_task)
    assert fifth_task == "low-independent"
    assert queue.get_status("low-independent") == "in_progress"

    queue.complete_task("low-independent")
    assert queue.get_status("low-independent") == "completed"
    assert queue.completed_count() == 5

    # No task should remain schedulable.
    assert queue.get_next_task() is None

    # Test get_status() for unknown task
    assert queue.get_status("unknown-task") is None

    # Test duplicate task rejection
    try:
        queue.add_task("label-image-1", priority=99, submitted_at=99)
        assert False, "Expected ValueError for duplicate task"
    except ValueError:
        pass

    # Test completing unknown task
    try:
        queue.complete_task("unknown-task")
        assert False, "Expected ValueError for unknown task"
    except ValueError:
        pass

    print("All tests passed")