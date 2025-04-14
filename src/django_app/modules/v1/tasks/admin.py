# django_app/modules/v1/tasks/admin.py

from django.contrib import admin
from .models import TasksModel

# Register your models here.
admin.site.register(TasksModel)