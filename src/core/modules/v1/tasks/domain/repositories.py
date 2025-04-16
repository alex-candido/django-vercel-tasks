# core/modules/v1/tasks/domain/repositories.py

from abc import ABC
from core.__seedwork.domain.repositories import RepositoryInterface
from core.modules.v1.tasks.domain.entities import Task

class TaskRepository(RepositoryInterface[Task], ABC):
    pass