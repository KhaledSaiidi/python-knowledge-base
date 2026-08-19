# Task Scheduler Interview

## Part 1 — Basic Queue

Question:  
Design an in-memory task queue.

Expected:
- Add task
- Get next pending task
- Mark task completed by `task_id`
- Track statuses: `PENDING`, `IN_PROGRESS`, `COMPLETED`
- Use a queue for order and a dict for lookup


## Part 2 — Priority Scheduling

Question:  
Update the scheduler to return tasks by priority.

Expected:
- Highest priority first
- Same priority: oldest task first
- Completed tasks are not returned
- Use a heap for scheduling
- Keep a dict as source of truth


## Part 3 — Dependencies

Question:  
Update the scheduler so tasks can depend on other tasks.

Expected:
- A task may have dependency task IDs
- Return a task only if all dependencies are completed
- Skip blocked tasks without losing them
- Reject invalid dependency IDs
- Keep priority order among eligible tasks

## Part 4 — Optimization and Edge Cases

Question:  
Now analyze your scheduler design and discuss edge cases.

Expected:
- Explain `add_task()` time complexity
- Explain `get_next_task()` time complexity
- Explain what happens when many high-priority tasks are blocked
- Explain how priority updates would work
- Explain what happens if two workers call `get_next_task()` at the same time
- Explain how you would test the scheduler
- Compare trade-offs between list, deque, heap, and dict