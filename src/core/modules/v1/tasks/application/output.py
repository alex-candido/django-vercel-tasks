from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Type, TypeVar

from core.modules.v1.tasks.domain.entities import Task

@dataclass(slots=True, frozen=True)
class TaskOutput:
    id: str
    title: str
    description: Optional[str]
    status: str
    completed: bool
    position: int
    created_at: str
    updated_at: str

Output = TypeVar('Output', bound=TaskOutput)

@dataclass(frozen=True, slots=True)
class TaskOutputMapper:
    output_class: Type[Output] = TaskOutput 
    
    @staticmethod
    def from_child(output_class: Type[Output]) -> 'TaskOutputMapper':
        return TaskOutputMapper(output_class)

    @staticmethod
    def without_child() -> 'TaskOutputMapper':
        return TaskOutputMapper()

    def to_output(self, task: Task) -> Output:
        return self.output_class(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            completed=task.completed,
            position=task.position,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat(),
        )
