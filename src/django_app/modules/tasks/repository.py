from django.shortcuts import get_object_or_404

from .models import TasksModel

class TasksRepository:
    @staticmethod
    def find_one(key, value):
        return TasksModel.objects.filter(**{key: value}).first()
    
    @staticmethod
    def find_all():
        return TasksModel.objects.all()
    
    @staticmethod
    def create_one(data):
        return TasksModel.objects.create(**data)
    
    @staticmethod
    def create_many(self, data_list):
        tasks = [TasksModel(**data) for data in data_list]
        return TasksModel.objects.bulk_create(tasks)
    
    @staticmethod
    def update_one(self, task_id, data):
        task = get_object_or_404(TasksModel, id=task_id)
        for key, value in data.items():
            setattr(task, key, value)
        task.save()
        return task
    
    @staticmethod
    def update_many(self, tasks_data):
        updated_tasks = []
        for task_data in tasks_data:
            task_id = task_data.get('id')
            task = TasksModel.objects.filter(id=task_id).first()
            if task:
                for key, value in task_data.items():
                    setattr(task, key, value)
                task.save()
                updated_tasks.append(task)
        return updated_tasks
    
    @staticmethod
    def remove_one(self, task_id):
        task = get_object_or_404(TasksModel, id=task_id)
        task.delete()
        
    @staticmethod
    def remove_many(self, tasks_ids):
        tasks = TasksModel.objects.filter(id__in=tasks_ids)
        tasks.delete()
        
    @staticmethod
    def search(self, key, value):
        return TasksModel.objects.filter(**{key: value})
    
    @staticmethod
    def filter(self, **kwargs):
        return TasksModel.objects.filter(**kwargs)
    
    @staticmethod
    def exclude(self, **kwargs):
        return TasksModel.objects.exclude(**kwargs)
    
    @staticmethod
    def find_by_id(self, task_id):
        return get_object_or_404(TasksModel, id=task_id).first()
    
    @staticmethod
    def find_by_ids(self, tasks_ids):
        return TasksModel.objects.filter(id__in=tasks_ids)
    
    @staticmethod
    def exists_by_id(self, task_id):
        return TasksModel.objects.filter(id=task_id).exists()