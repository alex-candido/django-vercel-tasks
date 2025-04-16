# core/modules/v1/tasks/application/use_cases.py

from dataclasses import dataclass, asdict
from typing import Optional

from core.modules.v1.tasks.domain.entities import Task
from core.modules.v1.tasks.application.output import TaskOutputMapper, TaskOutput 
from core.__seedwork.application.use_cases import UseCase
from core.modules.v1.tasks.domain.repositories import TaskRepository

@dataclass(slots=True, frozen=True)
class CreateOneTaskInput:
    title: str
    description: Optional[str]
    status: Optional[str]
    completed: Optional[bool]
    position: Optional[int]

@dataclass(slots=True, frozen=True)
class CreateOneTaskUseCase(UseCase):
    
    task_repo: TaskRepository

    def execute(self, input_param: CreateOneTaskInput) -> 'Output':
        task = Task(**asdict(input_param))
        self.task_repo.create_one(task)
        return self.__to_output(task)

    def __to_output(self, task: Task):
        return TaskOutputMapper\
            .from_child(CreateOneTaskUseCase.Output)\
            .to_output(task)

    @dataclass(slots=True, frozen=True)
    class Output(TaskOutput):
        pass
    
    