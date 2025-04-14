# django_app/modules/v1/tasks/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _

class TasksModel(models.Model):
    class TaskStatus(models.TextChoices):
        ACTIVE = 'active', _('Active')
        INACTIVE = 'inactive', _('Inactive')

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=8,
        choices=TaskStatus.choices,
        default=TaskStatus.ACTIVE
    )
    completed = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tasks'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['completed']),
            models.Index(fields=['position']),  # Índice para o campo position
        ]