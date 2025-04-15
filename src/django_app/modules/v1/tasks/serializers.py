# django_app/modules/v1/tasks/serializers.py

from rest_framework import serializers
from .models import TasksModel

class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = TasksModel
        fields = ['id', 'title', 'description', 'status', 'completed', 'position', 'created_at', 'updated_at']  # Campos específicos
        
    def create(self, validated_data):
        # Garantir que a posição seja definida no momento da criação
        position = validated_data.get('position', 0)
        return TasksModel.objects.create(position=position, **validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.position = validated_data.get('position', instance.position) 
        instance.save()
        return instance
