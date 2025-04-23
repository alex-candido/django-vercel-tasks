# core/modules/v1/tasks/infra/mappers.py

from core.modules.v1.tasks.domain.entities import Task

if TYPE_CHECKING:
    from django_app.modules.v1.tasks.models import TasksModel

class TaskModelMapper:
  
    @staticmethod  
    def to_entity(model: 'TasksModel') -> Task:
      return Task()
    
    @staticmethod
    def to_model(entity: Task) -> 'TasksModel':
      return TasksModel(**entity.to_dict())
  