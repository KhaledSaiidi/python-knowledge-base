# Task 3 — Fair Multi-Project Scheduling with Leases and Retries

## 1. Problem statement

You are building a harder version of the in-memory task queue for a data annotation platform.

The platform has many annotation projects.

Example projects:

- medical-image-labeling
- receipt-transcription
- street-scene-review
- document-QA-validation

Each task belongs to one project.

The scheduler must return the next best task, but it must avoid starving smaller or lower-priority projects.

The service should support:

- priority scheduling
- project-level fairness
- task claiming
- task completion
- task failure/retry
- lease timeout for workers that crash or disappear

There is still no database and no web server.

Everything should be implemented in memory using Python classes.

---

## 2. Expected Python class/API design

Implement a class similar to this:

    class FairAnnotationScheduler:
        def add_task(
            self,
            task_id: str,
            project_id: str,
            priority: int,
            payload: dict | None = None,
            submitted_at: int | None = None,
            max_retries: int = 3,
        ) -> None:
            ...

        def claim_next_task(
            self,
            worker_id: str,
            now: int,
            lease_seconds: int = 60,
        ) -> str | None:
            ...

        def complete_task(
            self,
            task_id: str,
            worker_id: str,
        ) -> None:
            ...

        def fail_task(
            self,
            task_id: str,
            worker_id: str,
            reason: str | None = None,
        ) -> None:
            ...

        def expire_leases(self, now: int) -> list[str]:
            ...

        def get_status(self, task_id: str) -> str | None:
            ...

        def project_pending_count(self, project_id: str) -> int:
            ...

Statuses:

- `"pending"`
- `"leased"`
- `"completed"`
- `"failed"`
- `"dead"`

Meaning:

- `"pending"`: task can be scheduled.
- `"leased"`: task was claimed by a worker and should not be given to another worker.
- `"completed"`: task is finished.
- `"failed"`: task failed but may be retried.
- `"dead"`: task exceeded retry limit and should not be scheduled again.

---

## 3. Functional requirements

### Basic scheduling

- Add tasks to different projects.
- Claim the next task for a worker.
- Claimed tasks become leased.
- Leased tasks should not be returned to another worker.
- Completed tasks should not be returned again.

### Priority behavior

Within the same project:

1. Higher priority first.
2. Older submitted task first.
3. Deterministic tie-break by `task_id`.

### Fairness behavior

Across projects, avoid always draining one project while ignoring others.

You may choose one fairness policy.

Recommended first policy:

Round-robin across projects that currently have pending tasks.

Example:

- Project A has 100 tasks.
- Project B has 2 tasks.
- Project C has 1 task.

The scheduler should not return all A tasks before B and C get work.

Expected behavior:

    A, B, C, A, B, A, A, A ...

Within each selected project, return that project's best task.

### Lease behavior

When a worker claims a task:

- Store the `worker_id`.
- Store `lease_expires_at = now + lease_seconds`.
- The task status becomes `"leased"`.

Only the worker that owns the lease can complete or fail the task.

### Retry behavior

When a task fails:

- Increment its attempt count.
- If attempts <= max_retries, put it back to `"pending"`.
- If attempts > max_retries, mark it `"dead"`.

### Lease expiration behavior

If a worker claims a task but does not complete it before the lease expires:

- `expire_leases(now)` should move expired leased tasks back to `"pending"`.
- It should return the list of expired task IDs.
- Expired tasks may be claimed again.

---

## 4. Example input/output behavior

Example 1 — Fair scheduling:

    scheduler = FairAnnotationScheduler()

    scheduler.add_task("A1", project_id="A", priority=10, submitted_at=1)
    scheduler.add_task("A2", project_id="A", priority=9, submitted_at=2)
    scheduler.add_task("B1", project_id="B", priority=1, submitted_at=3)

    scheduler.claim_next_task(worker_id="worker-1", now=100)
    # returns "A1"

    scheduler.claim_next_task(worker_id="worker-2", now=100)
    # returns "B1"
    # even though A2 has higher priority than B1,
    # because project-level fairness gives B a turn

    scheduler.claim_next_task(worker_id="worker-3", now=100)
    # returns "A2"

Example 2 — Lease expiration:

    scheduler = FairAnnotationScheduler()

    scheduler.add_task("task-1", project_id="A", priority=5, submitted_at=1)

    scheduler.claim_next_task(worker_id="worker-1", now=100, lease_seconds=30)
    # returns "task-1"

    scheduler.claim_next_task(worker_id="worker-2", now=110)
    # returns None
    # task-1 is leased

    scheduler.expire_leases(now=131)
    # returns ["task-1"]

    scheduler.claim_next_task(worker_id="worker-2", now=132)
    # returns "task-1"

Example 3 — Retry limit:

    scheduler = FairAnnotationScheduler()

    scheduler.add_task("task-1", project_id="A", priority=5, submitted_at=1, max_retries=1)

    scheduler.claim_next_task("worker-1", now=100)
    # returns "task-1"

    scheduler.fail_task("task-1", "worker-1")
    # task-1 becomes pending again

    scheduler.claim_next_task("worker-2", now=110)
    # returns "task-1"

    scheduler.fail_task("task-1", "worker-2")
    # task-1 becomes dead because retry limit was exceeded

    scheduler.get_status("task-1")
    # returns "dead"

---

## 5. Incremental follow-up requirements

An interviewer may add these after your first version works.

### Follow-up A — Add thread safety

Multiple workers may call `claim_next_task()` at the same time.

Requirements:

- Prevent two workers from claiming the same task.
- Use only Python standard library tools.

Consider:

    import threading

    self._lock = threading.Lock()

Then protect state mutations:

- add task
- claim task
- complete task
- fail task
- expire leases

Be ready to explain what operations must be atomic.

### Follow-up B — Weighted project fairness

Some projects are more important than others.

Example:

- Project A weight = 3
- Project B weight = 1

Expected rough scheduling pattern:

    A, A, A, B, A, A, A, B ...

Add:

    def set_project_weight(self, project_id: str, weight: int) -> None:
        ...

Requirements:

- Weight must be positive.
- A project with no pending tasks should be skipped.
- When it gets new tasks again, it should re-enter scheduling.

### Follow-up C — Add task dependencies

Combine Task 2 with Task 3.

A task should be claimable only if:

- it is pending
- its dependencies are completed
- its project is selected fairly

This follow-up tests whether your internal design can evolve without rewriting everything.

---

## 6. Data structures to consider

Core structures:

- `dict[str, Task]`
  - task ID to task object
- `dict[str, list | heap]`
  - project ID to that project's pending tasks
- `collections.deque`
  - project round-robin order
- `set[str]`
  - active projects with pending tasks
- `dict[str, str]`
  - leased task ID to worker ID
- `dict[str, int]`
  - leased task ID to lease expiration time

For per-project priority scheduling:

- `heapq`
- key:
  - `(-priority, submitted_at, task_id)`

For fairness:

- `collections.deque`
- rotate projects after each successful claim
- skip projects with no pending tasks

For concurrency:

- `threading.Lock`
- keep critical sections small but correct

For retries:

- attempt count field in task object
- max retry field in task object

Recommended Python tools:

- `dataclasses.dataclass`
- `heapq`
- `collections.deque`
- `threading.Lock`
- `unittest`

---

## 7. Edge cases you must handle

- Empty scheduler.
- Project has no pending tasks.
- All tasks are leased.
- All tasks are completed.
- All tasks are dead.
- Duplicate task ID.
- Unknown task completion.
- Wrong worker tries to complete a leased task.
- Wrong worker tries to fail a leased task.
- Lease expires exactly at `now`.
- Task fails and is retried.
- Task exceeds retry limit.
- Project with many high-priority tasks should not starve smaller projects.
- New project added after scheduling already started.
- New task added to a project that was previously empty.
- Multiple tasks in same project with same priority and timestamp.
- Concurrent calls to `claim_next_task()`.

---

## 8. Expected time complexity

Assuming per-project heaps and round-robin project queue:

- `add_task`: O(log p)
  - p = number of pending tasks in that project
- `claim_next_task`: O(k + log p)
  - k = number of projects skipped because they have no pending tasks
  - p = number of pending tasks in selected project
- `complete_task`: O(1)
- `fail_task`: O(log p) if task is retried
- `expire_leases`: O(l)
  - l = number of currently leased tasks
- `get_status`: O(1)
- `project_pending_count`: O(1) if tracked

For a simpler implementation using scans:

- `claim_next_task`: O(n)
- `expire_leases`: O(n)

The simple version is acceptable first if it is correct and readable, but you should be able to explain the optimized design.

---

## 9. Small test suite

Use this after implementing your class.

    import unittest

    class TestFairAnnotationScheduler(unittest.TestCase):

        def test_claim_single_task(self):
            scheduler = FairAnnotationScheduler()
            scheduler.add_task("task-1", project_id="A", priority=5, submitted_at=1)

            self.assertEqual(
                scheduler.claim_next_task(worker_id="worker-1", now=100),
                "task-1",
            )

            self.assertEqual(scheduler.get_status("task-1"), "leased")

        def test_leased_task_not_returned_twice(self):
            scheduler = FairAnnotationScheduler()
            scheduler.add_task("task-1", project_id="A", priority=5, submitted_at=1)

            self.assertEqual(scheduler.claim_next_task("worker-1", now=100), "task-1")
            self.assertIsNone(scheduler.claim_next_task("worker-2", now=100))

        def test_complete_task(self):
            scheduler = FairAnnotationScheduler()
            scheduler.add_task("task-1", project_id="A", priority=5, submitted_at=1)

            scheduler.claim_next_task("worker-1", now=100)
            scheduler.complete_task("task-1", "worker-1")

            self.assertEqual(scheduler.get_status("task-1"), "completed")

        def test_wrong_worker_cannot_complete_task(self):
            scheduler = FairAnnotationScheduler()
            scheduler.add_task("task-1", project_id="A", priority=5, submitted_at=1)

            scheduler.claim_next_task("worker-1", now=100)

            with self.assertRaises(ValueError):
                scheduler.complete_task("task-1", "worker-2")

        def test_round_robin_fairness_between_projects(self):
            scheduler = FairAnnotationScheduler()

            scheduler.add_task("A1", project_id="A", priority=100, submitted_at=1)
            scheduler.add_task("A2", project_id="A", priority=90, submitted_at=2)
            scheduler.add_task("B1", project_id="B", priority=1, submitted_at=3)

            self.assertEqual(scheduler.claim_next_task("worker-1", now=100), "A1")
            self.assertEqual(scheduler.claim_next_task("worker-2", now=100), "B1")
            self.assertEqual(scheduler.claim_next_task("worker-3", now=100), "A2")

        def test_priority_within_same_project(self):
            scheduler = FairAnnotationScheduler()

            scheduler.add_task("A-low", project_id="A", priority=1, submitted_at=1)
            scheduler.add_task("A-high", project_id="A", priority=10, submitted_at=2)

            self.assertEqual(scheduler.claim_next_task("worker-1", now=100), "A-high")

        def test_expired_lease_returns_to_pending(self):
            scheduler = FairAnnotationScheduler()
            scheduler.add_task("task-1", project_id="A", priority=5, submitted_at=1)

            scheduler.claim_next_task("worker-1", now=100, lease_seconds=30)

            self.assertEqual(scheduler.expire_leases(now=131), ["task-1"])
            self.assertEqual(scheduler.get_status("task-1"), "pending")

            self.assertEqual(scheduler.claim_next_task("worker-2", now=132), "task-1")

        def test_non_expired_lease_does_not_expire(self):
            scheduler = FairAnnotationScheduler()
            scheduler.add_task("task-1", project_id="A", priority=5, submitted_at=1)

            scheduler.claim_next_task("worker-1", now=100, lease_seconds=30)

            self.assertEqual(scheduler.expire_leases(now=120), [])
            self.assertEqual(scheduler.get_status("task-1"), "leased")

        def test_fail_task_retries_until_dead(self):
            scheduler = FairAnnotationScheduler()
            scheduler.add_task("task-1", project_id="A", priority=5, submitted_at=1, max_retries=1)

            self.assertEqual(scheduler.claim_next_task("worker-1", now=100), "task-1")
            scheduler.fail_task("task-1", "worker-1")

            self.assertEqual(scheduler.get_status("task-1"), "pending")

            self.assertEqual(scheduler.claim_next_task("worker-2", now=110), "task-1")
            scheduler.fail_task("task-1", "worker-2")

            self.assertEqual(scheduler.get_status("task-1"), "dead")

        def test_duplicate_task_rejected(self):
            scheduler = FairAnnotationScheduler()
            scheduler.add_task("task-1", project_id="A", priority=5, submitted_at=1)

            with self.assertRaises(ValueError):
                scheduler.add_task("task-1", project_id="A", priority=10, submitted_at=2)

    if __name__ == "__main__":
        unittest.main()

---

## 10. Rubric for a strong solution

A strong solution should include:

- Clean task model with fields such as:
  - task_id
  - project_id
  - priority
  - submitted_at
  - status
  - worker_id
  - lease_expires_at
  - attempts
  - max_retries
- Correct state transitions:
  - pending → leased → completed
  - pending → leased → pending after failure
  - pending → leased → dead after too many failures
  - leased → pending after lease expiration
- No double-claiming of leased tasks.
- Correct worker ownership checks.
- Fair scheduling across projects.
- Priority scheduling within each project.
- Good error handling.
- Clear explanation of fairness policy.
- Ability to discuss tradeoffs:
  - simple scan vs heap
  - global priority vs project fairness
  - round-robin vs weighted fair scheduling
  - lock granularity for concurrency
- Tests for:
  - priority
  - fairness
  - lease expiration
  - retries
  - invalid worker actions
  - duplicate IDs
- Optional but strong:
  - use `threading.Lock` around mutations
  - use per-project heaps
  - use `deque` for project rotation

Interviewer focus:

- Can you build a realistic in-memory service?
- Can you preserve correctness while adding constraints?
- Can you discuss concurrency and atomicity clearly?
- Can your design evolve without becoming messy?