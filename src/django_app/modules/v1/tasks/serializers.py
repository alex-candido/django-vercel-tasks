from rest_framework import serializers
from .models import TasksModel

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasksModel
        fields = '__all__'
        
    def create(self, validated_data):
        return TasksModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.save()
        return instance