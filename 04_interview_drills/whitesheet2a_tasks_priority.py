from dataclasses import dataclass, field
from enum import Enum
import heapq
from datetime import datetime

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"

@dataclass(order=True)
class Task:
    task_id: str = field(compare=False)
    title: str = field(compare=False)
    priority: int = field(compare=False)
    created_at: datetime = field(default_factory=datetime.now)
    status: TaskStatus = field(default=TaskStatus.PENDING, compare=False)
    def __post_init__(self):
        self.sort_priority = -self.priority
@dataclass
class TaskQueue:
    tasks_by_id: dict = field(default_factory=dict)
    pending_queue: list[Task] = field(default_factory=list)
    completed_tasks: set = field(default_factory=set)

    def add_task(self, task: Task) -> None:
        self.tasks_by_id[task.task_id] = task
        heapq.heappush(self.pending_queue,task)
    def get_next_task(self) -> Task | None:
        while self.pending_queue:
            task = heapq.heappop(self.pending_queue)
            if not task:
                return None
            if task.status == TaskStatus.PENDING:
                task.status = TaskStatus.IN_PROGRESS
                return task
        return None
        
    def complete_Task(self, task_id: str) -> bool:
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

    queue.add_task(Task(task_id="task-1", title="Annotate image 1", priority=2))
    queue.add_task(Task(task_id="task-2", title="Annotate image 2", priority=1))

    task = queue.get_next_task()
    print("Next task:", task.task_id)
    print("Status after get:", task.status)

    result = queue.complete_Task(task.task_id)
    print("Completed successfully:", result)
    print("Status after complete:", queue.tasks_by_id[task.task_id].status)

    task = queue.get_next_task()
    print("Next task:", task.task_id)
    print("Status after get:", task.status)

    result = queue.complete_Task("task-999")
    print("Complete invalid task:", result)