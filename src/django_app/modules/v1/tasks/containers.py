from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from repository import TasksRepository


class Container(containers.DeclarativeContainer):
    
    repository_task_django_orm = providers.Singleton(
        TasksRepository
    )