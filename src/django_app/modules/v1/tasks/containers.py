# django_app/modules/v1/tasks/containers.py

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from repository import TasksRepository

from core.modules.v1.tasks.application.use_cases import CreateOneTaskUseCase

# find_one, find_all, create_one, create_many, update_one, update_many, remove_one, remove_many, search, filter, find_by_id, find_by_ids, exists_by_id, exists_by_ids

class Container(containers.DeclarativeContainer):
    
    repository_task_django_orm = providers.Singleton(
        TasksRepository
    )
    
    use_case_create_one_task = providers.Singleton(
        CreateOneTaskUseCase, task_repo=repository_task_django_orm
    )