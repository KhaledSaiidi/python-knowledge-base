# Task 2 — Dependency-Aware Annotation Workflow Queue

## 1. Problem statement

You are now building a more realistic work queue for a data annotation platform.

Some tasks cannot be worked on until other tasks are completed.

Example:

- A raw image must be labeled first.
- Then a reviewer can review the annotation.
- Then a senior reviewer can audit the result.

So a task may depend on one or more prerequisite tasks.

A task is eligible to be returned by the scheduler only when:

1. It is pending.
2. All of its dependencies are completed.

Among eligible tasks, return the next best task using the same priority logic:

1. Higher priority first.
2. Older submitted task first.
3. Deterministic tie-break by `task_id`.

---

## 2. Expected Python class/API design

Implement a class similar to this:

    class DependencyAwareTaskQueue:
        def add_task(
            self,
            task_id: str,
            priority: int,
            dependencies: list[str] | None = None,
            payload: dict | None = None,
            submitted_at: int | None = None,
        ) -> None:
            ...

        def get_next_task(self) -> str | None:
            ...

        def complete_task(self, task_id: str) -> None:
            ...

        def get_status(self, task_id: str) -> str | None:
            ...

        def get_blocked_tasks(self) -> list[str]:
            ...

        def pending_count(self) -> int:
            ...

        def completed_count(self) -> int:
            ...

Statuses:

- `"pending"`
- `"in_progress"`
- `"completed"`
- `"blocked"`

Important design choice:

You may either store `"blocked"` as a real status, or compute blocked dynamically as:

- task is not completed
- task is not in progress
- at least one dependency is incomplete

Be ready to explain your choice.

---

## 3. Functional requirements

### Required

- Add tasks with zero or more dependencies.
- A task with no dependencies is immediately eligible.
- A task with completed dependencies is eligible.
- A task with incomplete dependencies must not be returned.
- Completing a task may unblock dependent tasks.
- `get_next_task()` returns only eligible pending tasks.
- Duplicate task IDs are rejected.
- Unknown dependencies should be handled intentionally.

You must choose one behavior for unknown dependencies:

Option A:

- Reject a task if any dependency is unknown.

Option B:

- Allow dependencies that will be added later.

Pick one and document it in your code comments.

For an interview, Option A is simpler and usually better for a first implementation.

---

## 4. Example input/output behavior

Example:

    queue = DependencyAwareTaskQueue()

    queue.add_task("label-image-1", priority=5, submitted_at=1)
    queue.add_task(
        "review-image-1",
        priority=10,
        dependencies=["label-image-1"],
        submitted_at=2,
    )

    queue.get_next_task()
    # returns "label-image-1"
    # even though review-image-1 has higher priority,
    # because review-image-1 is blocked

    queue.complete_task("label-image-1")

    queue.get_next_task()
    # returns "review-image-1"

Another example:

    queue = DependencyAwareTaskQueue()

    queue.add_task("A", priority=1, submitted_at=1)
    queue.add_task("B", priority=100, dependencies=["A"], submitted_at=2)
    queue.add_task("C", priority=50, submitted_at=3)

    queue.get_next_task()
    # returns "C"
    # B has higher priority but is blocked by A

---

## 5. Incremental follow-up requirements

An interviewer may add these after your basic version works.

### Follow-up A — Support adding tasks before dependencies exist

Allow this:

    queue.add_task("review-1", priority=10, dependencies=["label-1"])
    queue.add_task("label-1", priority=5)

Requirements:

- `review-1` remains blocked until `label-1` is completed.
- If a dependency is never added, the task remains blocked.
- You should be able to list missing dependencies.

Add:

    def get_missing_dependencies(self, task_id: str) -> list[str]:
        ...

### Follow-up B — Detect cycles

Example cycle:

    A depends on B
    B depends on C
    C depends on A

Requirements:

- Detect cycles when adding tasks, or before scheduling.
- Raise `ValueError` if a cycle exists.
- Explain the algorithm you used.

Possible algorithms:

- DFS with visiting states
- topological sort

### Follow-up C — Return why a task is blocked

Add:

    def explain_blocked(self, task_id: str) -> list[str]:
        ...

Example:

    queue.explain_blocked("review-image-1")
    # returns ["label-image-1"]

Meaning:

- `review-image-1` cannot run because `label-image-1` is not completed.

---

## 6. Data structures to consider

Core structures:

- `dict[str, Task]`
  - task ID to task object
- `dict[str, set[str]]`
  - task ID to dependency IDs
- `dict[str, set[str]]`
  - task ID to dependents/reverse dependencies
- `set[str]`
  - completed task IDs
- `set[str]`
  - in-progress task IDs
- optional `set[str]`
  - pending task IDs

For optimization:

- maintain a ready queue of eligible tasks
- use `heapq` for ready tasks
- when a task completes, inspect only its dependents
- track remaining dependency count per task:
  - `remaining_dependencies_count[task_id]`

This is similar to topological scheduling.

---

## 7. Edge cases you must handle

- Empty queue.
- Task with no dependencies.
- Task with one dependency.
- Task with many dependencies.
- Multiple tasks depending on the same prerequisite.
- Dependency task completed before dependent is scheduled.
- Duplicate task ID.
- Unknown dependency.
- Self-dependency:
  - task A depends on A
- Dependency cycle:
  - A depends on B, B depends on A
- Completing unknown task.
- Completing blocked task.
- Completing pending task that has not been claimed.
- Calling `get_next_task()` when all remaining tasks are blocked.
- Higher-priority task blocked while lower-priority task is available.

---

## 8. Expected time complexity

Simple scan implementation:

- `add_task`: O(d), where d is number of dependencies
- `get_next_task`: O(n * d) if checking dependencies by scanning
- `complete_task`: O(1) basic, or O(k) if updating dependents
- `get_blocked_tasks`: O(n * d)

Optimized ready-queue implementation:

- `add_task`: O(d + log n) if immediately eligible
- `get_next_task`: O(log n)
- `complete_task`: O(k log n)
  - k = number of tasks depending on the completed task
- dependency check using remaining count: O(1)
- cycle detection with DFS/topological sort: O(V + E)

Where:

- V = number of tasks
- E = number of dependency edges

---

## 9. Small test suite

Use this after implementing your class.

    import unittest

    class TestDependencyAwareTaskQueue(unittest.TestCase):

        def test_task_without_dependencies_is_schedulable(self):
            queue = DependencyAwareTaskQueue()
            queue.add_task("task-1", priority=5, submitted_at=1)

            self.assertEqual(queue.get_next_task(), "task-1")

        def test_blocked_task_not_returned(self):
            queue = DependencyAwareTaskQueue()
            queue.add_task("label-1", priority=1, submitted_at=1)
            queue.add_task(
                "review-1",
                priority=100,
                dependencies=["label-1"],
                submitted_at=2,
            )

            self.assertEqual(queue.get_next_task(), "label-1")

        def test_dependent_task_unblocked_after_completion(self):
            queue = DependencyAwareTaskQueue()
            queue.add_task("label-1", priority=1, submitted_at=1)
            queue.add_task(
                "review-1",
                priority=100,
                dependencies=["label-1"],
                submitted_at=2,
            )

            self.assertEqual(queue.get_next_task(), "label-1")
            queue.complete_task("label-1")

            self.assertEqual(queue.get_next_task(), "review-1")

        def test_lower_priority_available_beats_higher_priority_blocked(self):
            queue = DependencyAwareTaskQueue()
            queue.add_task("A", priority=1, submitted_at=1)
            queue.add_task("B", priority=100, dependencies=["A"], submitted_at=2)
            queue.add_task("C", priority=50, submitted_at=3)

            self.assertEqual(queue.get_next_task(), "C")

        def test_multiple_dependencies(self):
            queue = DependencyAwareTaskQueue()
            queue.add_task("label", priority=5, submitted_at=1)
            queue.add_task("validate", priority=5, submitted_at=2)
            queue.add_task(
                "audit",
                priority=100,
                dependencies=["label", "validate"],
                submitted_at=3,
            )

            self.assertEqual(queue.get_next_task(), "label")
            queue.complete_task("label")

            self.assertEqual(queue.get_next_task(), "validate")
            queue.complete_task("validate")

            self.assertEqual(queue.get_next_task(), "audit")

        def test_get_next_returns_none_when_all_tasks_blocked(self):
            queue = DependencyAwareTaskQueue()

            # This test assumes you allow missing dependencies.
            # If you choose to reject unknown dependencies, adjust this test.
            queue.add_task("review-1", priority=10, dependencies=["missing-label"], submitted_at=1)

            self.assertIsNone(queue.get_next_task())

        def test_self_dependency_rejected(self):
            queue = DependencyAwareTaskQueue()

            with self.assertRaises(ValueError):
                queue.add_task("A", priority=1, dependencies=["A"], submitted_at=1)

        def test_duplicate_task_rejected(self):
            queue = DependencyAwareTaskQueue()
            queue.add_task("A", priority=1, submitted_at=1)

            with self.assertRaises(ValueError):
                queue.add_task("A", priority=2, submitted_at=2)

    if __name__ == "__main__":
        unittest.main()

---

## 10. Rubric for a strong solution

A strong solution should include:

- Clear representation of task state.
- Correct distinction between:
  - pending
  - blocked
  - in_progress
  - completed
- Correct scheduling of only eligible tasks.
- Higher-priority blocked tasks should not prevent lower-priority eligible tasks from being returned.
- Good handling of dependencies.
- Good error handling for invalid state transitions.
- Clean internal data structures:
  - tasks by ID
  - dependencies
  - reverse dependencies
  - completed set
- Ability to explain simple scan vs optimized ready-queue design.
- Good tests for:
  - blocked tasks
  - unblocking
  - multiple dependencies
  - duplicate IDs
  - invalid completion
- Clear explanation of complexity.

Interviewer focus:

- Can you model relationships between tasks?
- Can you track completed work separately from pending work?
- Can you evolve your design from scan-based scheduling to graph-aware scheduling?