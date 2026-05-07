from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    task_id: str
    priority: int
    status: str
    payload: dict[str, str] | None = None
    submitted_at: datetime | None = None
    def get_task_payload(self):
        s = ""
        if not self.payload:
            s = "With No payload"
        else:
            for key, value in  self.payload.items():
                s += "key is: " + key + " value is: " + value + ", "
        return s
    

def getBestTask(tasks: list[Task]) -> Task | None:
    if not tasks:
        print("The list of Tasks is empty")
        return None
    bestTask = None
    for task in tasks:
        if task.status != "pending":
            continue
        if bestTask is None:
            bestTask = task
        elif task.priority > bestTask.priority:
            bestTask = task
        elif task.priority == bestTask.priority:
            if task.submitted_at > bestTask.submitted_at:
                bestTask = task
            elif task.task_id >= bestTask.task_id:
                bestTask = task
    return bestTask


class AnnotationTaskQueue:
    def __init__(self,):
        self.tasks: list[Task] = []    

    def add_task(
        self,
        task_id: str,
        priority: int,
        status: str,
        payload: dict[str, str] | None,
        submitted_at: datetime | None,
    ) -> None:
        for task in self.tasks:
            if task.task_id == task_id:
                raise ValueError(f"Task with id {task_id} already exists")
            
        task = Task(task_id, priority, status, payload, submitted_at)
        self.tasks.append(task)
    def get_next_task(self) -> str | None:
        bestTask = getBestTask(self.tasks)
        if bestTask:
            bestTask.status = "in_progress"
            return bestTask.task_id
        return None
    def complete_task(self, task_id: str) -> None:
        for task in self.tasks:
            if task.task_id == task_id:
                if task.status != "in_progress":
                    raise ValueError(f"Task {task_id} is not in progress")
                task.status = "completed"
                return
        raise ValueError(f'Task with id {task_id} does not exist')
        

    def get_status(self, task_id: str) -> str | None:
        for task in self.tasks:
            if task.task_id == task_id:
                return task.status


    def pending_count(self) -> int:
        count = 0
        for task in self.tasks:
            if task.status == "pending":
                count += 1
        return count


if __name__ == "__main__":
    queue = AnnotationTaskQueue()

    tasks = [
        Task(
            task_id="task-0",
            priority=20,
            status="progressing",
            payload={"type": "image", "label": "cat"},
            submitted_at=datetime(2026, 5, 6, 10, 0, 0),
        ),
        Task(
            task_id="task-1",
            priority=10,
            status="pending",
            payload={"type": "image", "label": "cat"},
            submitted_at=datetime(2026, 5, 6, 10, 0, 0),
        ),
        Task(
            task_id="task-2",
            priority=10,
            status="pending",
            payload={"type": "text", "label": "invoice"},
            submitted_at=datetime(2026, 5, 6, 10, 5, 0),
        ),
        Task(
            task_id="task-3",
            priority=3,
            status="pending",
            payload={"type": "audio", "label": "speech"},
            submitted_at=datetime(2026, 5, 6, 10, 10, 0),
        ),
    ]

    for task in tasks:
        queue.add_task(
            task_id=task.task_id,
            priority=task.priority,
            payload=task.payload,
            status=task.status,
            submitted_at=task.submitted_at,
        )
        
    task = getBestTask(queue.tasks)
    print(queue.tasks)
    print("------------------")
    print("best Task:--------")
    print(f'''The Best Task is the one with id {task.task_id} 
as it have a priority of {task.priority}, 
Status is {task.status}
payload of {task.get_task_payload()} 
submitted at {task.submitted_at}''')
    print("------------------")
    print("Start Task:-------")
    task_id = queue.get_next_task()
    print(f"The Best Task is processd id {task_id}, {task.status}")
    next_task = queue.get_next_task()
    print("Get Next Task: " + next_task)

    print(f"Get Staus of {next_task}: " + queue.get_status(next_task))

    queue.complete_task(next_task)

    print(f"Get Next Task {next_task} Staus After processed: " + queue.get_status("task-1"))

    print("Get Pending Tasks: " + str(queue.pending_count()))

## Iteration 3 — Add Task State Management
