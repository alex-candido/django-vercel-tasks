# core/modules/v1/tasks/infra/repositories.py

from typing import List, Type, TYPE_CHECKING
from django.shortcuts import get_object_or_404

from core.modules.v1.tasks.domain.repositories import TaskRepository

if TYPE_CHECKING:
    from django_app.modules.v1.tasks.models import TasksModel
    
# find_one, find_all, create_one, create_many, update_one, update_many, remove_one, remove_many, search, filter, find_by_id, find_by_ids, exists_by_id, exists_by_ids

class TaskDjangoRepository(TaskRepository):
    sortable_fields: List[str] = ['title', 'created_at']
    model: Type['TasksModel']
    
    def __init__(self) -> None:
      self.model = TasksModel
  
    def find_one(self, key, value):
        return self.model.objects.filter(**{key: value}).first()

    def find_all(self):
        return self.model.objects.all()

    def create_one(self, data):
        return self.model.objects.create(**data)

    def create_many(self, data_list):
        tasks = [self.model(**data) for data in data_list]
        return self.model.objects.bulk_create(tasks)

    def update_one(self, task_id, data):
        task = get_object_or_404(self.model, id=task_id)
        for key, value in data.items():
            setattr(task, key, value)
        task.save()
        return task

    def update_many(self, tasks_data):
        updated_tasks = []
        for task_data in tasks_data:
            task_id = task_data.get('id')
            task = self.model.objects.filter(id=task_id).first()
            if task:
                for key, value in task_data.items():
                    setattr(task, key, value)
                task.save()
                updated_tasks.append(task)
        return updated_tasks

    def remove_one(self, task_id):
        task = get_object_or_404(self.model, id=task_id)
        task.delete()

    def remove_many(self, tasks_ids):
        for task_id in tasks_ids:
            get_object_or_404(self.model, id=task_id).delete()

    def search(self, key, value):
        return self.model.objects.filter(**{key: value})

    def filter(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def find_by_id(self, task_id):
        return get_object_or_404(self.model, id=task_id)

    def find_by_ids(self, tasks_ids):
        return self.model.objects.filter(id__in=tasks_ids)

    def exists_by_id(self, task_id):
        return self.model.objects.filter(id=task_id).exists()

    def exists_by_ids(self, tasks_ids):
        return self.model.objects.filter(id__in=tasks_ids).exists()
