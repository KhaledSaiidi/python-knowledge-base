from dataclasses import dataclass, field
from enum import Enum
import heapq
from datetime import datetime

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"

@dataclass
class Task:
    task_id: str 
    title: str
    priority: int
    dependencies: set = field(default_factory=set)
    created_at: datetime = field(default_factory=datetime.now)
    status: TaskStatus = field(default=TaskStatus.PENDING)


@dataclass
class TaskQueue:
    tasks_by_id: dict = field(default_factory=dict)
    pending_queue: list = field(default_factory=list)
    completed_tasks: set = field(default_factory=set)

    def add_task(self, task: Task) -> bool:
        if task.task_id in self.tasks_by_id:
            return False
        
        for dependency_id in task.dependencies:
            if dependency_id not in self.tasks_by_id:
                return False
            
        self.tasks_by_id[task.task_id] = task
        heapq.heappush(self.pending_queue, (-task.priority, task.created_at, task.task_id))
        return True

    def is_ready(self, task: Task) -> bool:
        if not task.dependencies:
            return True
        for task_id in task.dependencies:
            task_deps = self.tasks_by_id[task_id]
            if task_deps.status != TaskStatus.COMPLETED:
                return False
        return True

    def get_next_task(self) -> Task | None:
        blocked_tasks = []
        while self.pending_queue:
            _, _, task_id = heapq.heappop(self.pending_queue)
            if not task_id:
                return None
            task = self.tasks_by_id[task_id]
            if task.status == TaskStatus.PENDING and self.is_ready(task):
                task.status = TaskStatus.IN_PROGRESS
                for blocked_task in blocked_tasks:
                    heapq.heappush(self.pending_queue, blocked_task)
                return task
            elif task.status == TaskStatus.PENDING:
                blocked_tasks.append((-task.priority, task.created_at, task.task_id))
        for blocked_task in blocked_tasks:
            heapq.heappush(self.pending_queue, blocked_task)
        return None
        
    def complete_task(self, task_id: str) -> bool:
        if task_id not in self.tasks_by_id:
            return False
        task = self.tasks_by_id[task_id]
        if task.status != TaskStatus.IN_PROGRESS:
            return False
        
        task.status = TaskStatus.COMPLETED
        self.completed_tasks.add(task_id)
        return True

 
if __name__ == "__main__":
    queue = TaskQueue()

    # 1. Add independent tasks
    queue.add_task(Task(task_id="task-1", title="Annotate image 1", priority=2))
    queue.add_task(Task(task_id="task-2", title="Annotate image 2", priority=5))

    # 2. Add task with dependency on task-1
    queue.add_task(Task(
        task_id="task-3",
        title="Review annotation",
        priority=10,
        dependencies={"task-1"}
    ))

    # 3. Should return task-2 first
    # task-3 has higher priority, but it is blocked by task-1
    task = queue.get_next_task()
    print("Next task:", task.task_id)
    print("Expected: task-2")

    queue.complete_task(task.task_id)

    # 4. Should return task-1 next
    # task-3 is still blocked because task-1 is not completed yet
    task = queue.get_next_task()
    print("Next task:", task.task_id)
    print("Expected: task-1")

    queue.complete_task(task.task_id)

    # 5. Now task-3 dependency is completed, so it should be returned
    task = queue.get_next_task()
    print("Next task:", task.task_id)
    print("Expected: task-3")

    queue.complete_task(task.task_id)

    # 6. No more tasks
    task = queue.get_next_task()
    print("Next task:", task)
    print("Expected: None")

    # 7. Invalid dependency should not be added
    result = queue.add_task(Task(
        task_id="task-4",
        title="Invalid dependency task",
        priority=20,
        dependencies={"missing-task"}
    ))

    print("Invalid dependency add result:", result)
    print("Expected: None")