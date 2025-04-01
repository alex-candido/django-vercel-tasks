from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_app.modules.v1.tasks'
    label = 'tasks'
    verbose_name = 'Tasks'
