# django_app/modules/v1/tasks/api.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from .serializers import TaskSerializer
from .repository import TasksRepository
from .models import TasksModel

# find_one, find_all, create_one, create_many, update_one, update_many, remove_one, remove_many, search, filter,  find_by_id, find_by_ids, exists_by_id, exists_by_ids

class TaskViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['get'])
    def find_one(self, request):
        key = request.query_params.get('key')
        value = request.query_params.get('value')
        if key and value:
            task = TasksRepository.find_one(key, value)
            if task:
                return Response(TaskSerializer(task).data)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def find_all(self, request):
        tasks = TasksRepository.find_all()
        return Response(TaskSerializer(tasks, many=True).data)

    @action(detail=False, methods=['post'])
    def create_one(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = TasksRepository.create_one(serializer.validated_data)
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def create_many(self, request):
        serializer = TaskSerializer(data=request.data, many=True)
        if serializer.is_valid():
            tasks = TasksRepository.create_many(serializer.validated_data)
            return Response(TaskSerializer(tasks, many=True).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'])
    def update_one(self, request):
        task_id = request.data.get('id')
        task = TasksRepository.find_by_id(task_id)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            updated_task = TasksRepository.update_one(task_id, serializer.validated_data)
            return Response(TaskSerializer(updated_task).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False, methods=['put'])
    # def update_many(self, request):
    #     serializer = TaskSerializer(data=request.data, many=True)
    #     if serializer.is_valid():
    #         updated_tasks = TasksRepository.update_many(serializer.validated_data)
    #         return Response(TaskSerializer(updated_tasks, many=True).data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['put'])
    def update_many(self, request):
        tasks_data = request.data
        updated_tasks = []
        for task_data in tasks_data:
            task_id = task_data.get('id')
            task = TasksModel.objects.filter(id=task_id).first()
            if task:
                serializer = TaskSerializer(task, data=task_data)
                if serializer.is_valid():
                    serializer.save()
                    updated_tasks.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': f'Task with id {task_id} not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(updated_tasks)

    @action(detail=False, methods=['delete'])
    def remove_one(self, request):
        task_id = request.query_params.get('id')
        TasksRepository.remove_one(task_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['delete'])
    def remove_many(self, request):
        ids = request.data.get('ids')
        TasksRepository.remove_many(ids)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def search(self, request):
        search_query = request.query_params.get('search')
        tasks = TasksRepository.search('title__icontains', search_query)
        return Response(TaskSerializer(tasks, many=True).data)

    @action(detail=False, methods=['get'])
    def filter(self, request):
        status_param = request.query_params.get('status')
        tasks = TasksRepository.filter(status=status_param)
        return Response(TaskSerializer(tasks, many=True).data)

    @action(detail=False, methods=['get'])
    def find_by_id(self, request):
        task_id = request.query_params.get('id')
        task = TasksRepository.find_by_id(task_id)
        return Response(TaskSerializer(task).data)

    @action(detail=False, methods=['post'])
    def find_by_ids(self, request):
        ids = request.data.get('ids')
        tasks = TasksRepository.find_by_ids(ids)
        return Response(TaskSerializer(tasks, many=True).data)

    @action(detail=False, methods=['get'])
    def exists_by_id(self, request):
        task_id = request.query_params.get('id')
        exists = TasksRepository.exists_by_id(task_id)
        return Response({"exists": exists})

    @action(detail=False, methods=['post'])
    def exists_by_ids(self, request):
        ids = request.data.get('ids')
        result = {str(task_id): TasksRepository.exists_by_id(task_id) for task_id in ids}
        return Response({"exists": result})