# 30-Minute Python Coding Interview Task — Annotation Task Queue

## Goal

Build an in-memory service that manages annotation tasks.

The service should:

1. Accept new tasks.
2. Return the next best task.
3. Track task state.
4. Prevent already-claimed or completed tasks from being returned again.

> [!IMPORTANT]
> Do not use a database, web server, or external libraries.
>
> Use plain Python.

---

## Iteration 1 — Pick the Best Task

### Time target

5 to 7 minutes.

### What to build first

Create a `Task` dataclass and a helper function that can select the best task from a list.

A task has:

- `task_id`
- `priority`
- `payload`
- `submitted_at`
- `status`

The best task is selected by:

1. Highest priority first.
2. If same priority, oldest `submitted_at` first.
3. If still tied, smallest `task_id` alphabetically.

### Expected shape

```python
@dataclass
class Task:
    task_id: str
    priority: int
    payload: dict[str, str] | None = None
    submitted_at: int | None = None
    status: str = "pending"


def get_best_task(tasks: list[Task]) -> Task | None:
    ...
```

### Important rule

Only tasks with status `"pending"` can be selected.

### Example

```python
tasks = [
    Task("task-1", priority=5, submitted_at=10),
    Task("task-2", priority=10, submitted_at=20),
    Task("task-3", priority=10, submitted_at=15),
]

best = get_best_task(tasks)

# expected: task-3
```

### Why?

- task-2 and task-3 both have priority 10.
- task-3 was submitted earlier.
- So task-3 wins.

---

## Iteration 2 — Wrap It in a Queue Class

### Time target

8 to 10 minutes.

Now move the logic into a service class.

### Expected class

```python
class AnnotationTaskQueue:
    def __init__(self):
        ...

    def add_task(
        self,
        task_id: str,
        priority: int,
        payload: dict[str, str] | None = None,
        submitted_at: int | None = None,
    ) -> None:
        ...

    def get_next_task(self) -> str | None:
        ...
```

### Requirements

#### add_task

Adds a task to memory.

New tasks start with status `"pending"`.

Duplicate `task_id` should raise `ValueError`.

#### get_next_task

Finds the best pending task.

Marks it as `"in_progress"`.

Returns only the `task_id`.

Returns `None` if no pending task exists.

### Example

```python
queue = AnnotationTaskQueue()

queue.add_task("task-1", priority=5, submitted_at=10)
queue.add_task("task-2", priority=10, submitted_at=20)
queue.add_task("task-3", priority=10, submitted_at=15)

print(queue.get_next_task())
# expected: task-3

print(queue.get_next_task())
# expected: task-2
```

### Important

After `task-3` is returned once, it becomes `"in_progress"` and should not be returned again.

---

## Iteration 3 — Add Task State Management

### Time target

8 to 10 minutes.

Add these methods:

```python
def complete_task(self, task_id: str) -> None:
    ...

def get_status(self, task_id: str) -> str | None:
    ...

def pending_count(self) -> int:
    ...
```

### Requirements

#### complete_task

Only an `"in_progress"` task can be completed.

If the task does not exist, raise `ValueError`.

If the task is still `"pending"`, raise `ValueError`.

If the task is already `"completed"`, raise `ValueError`.

When completed, status becomes `"completed"`.

#### get_status

Returns the task status.

Returns `None` if task does not exist.

#### pending_count

Returns the number of tasks with status `"pending"`.

---

## Iteration 4 — Manual Test Scenario

### Time target

5 minutes.

Use this to validate your solution manually.

```python
if __name__ == "__main__":
    queue = AnnotationTaskQueue()

    queue.add_task("task-1", priority=5, submitted_at=10)
    queue.add_task("task-2", priority=10, submitted_at=20)
    queue.add_task("task-3", priority=10, submitted_at=15)

    print(queue.get_next_task())
    # expected: task-3

    print(queue.get_status("task-3"))
    # expected: in_progress

    print(queue.get_next_task())
    # expected: task-2

    queue.complete_task("task-3")

    print(queue.get_status("task-3"))
    # expected: completed

    print(queue.pending_count())
    # expected: 1
```

---

## What You Should NOT Do Yet

Do not implement these unless the interviewer asks:

- dependencies
- heap optimization
- cancellation
- priority update
- concurrency
- database
- web API
- workers
- retries

Those are follow-ups, not the first 30-minute target.

---

## If the Interviewer Adds a Follow-Up

Only after the main queue works, they may ask one of these.

### Follow-up A — Update priority

Add:

```python
def update_priority(self, task_id: str, new_priority: int) -> None:
    ...
```

Rules:

- Only pending tasks can be updated.
- Unknown task raises `ValueError`.
- In-progress task raises `ValueError`.
- Completed task raises `ValueError`.

### Follow-up B — Cancel pending task

Add:

```python
def cancel_task(self, task_id: str) -> None:
    ...
```

Rules:

- Only pending tasks can be cancelled.
- Cancelled tasks should never be returned.
- Add `"cancelled"` as a new status.

### Follow-up C — Discuss optimization

Do not code this unless asked.

Explain:

- current `get_next_task()` scans all tasks: `O(n)`
- optimized version could use `heapq`
- heap key would be:

```python
(-priority, submitted_at, task_id)
```
