from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from .serializers import TaskSerializer
from .repository import TasksRepository
from .models import TasksModel

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    @action(detail=False, methods=['get'])
    def find_one(self, request):
        key = request.query_params.get('key')
        value = request.query_params.get('value')
        if key and value:
            task = TasksRepository.find_one(key, value)
            if task:
                serializer = TaskSerializer(task)
                return Response(serializer.data)
            else:
                return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "Invalid parameters"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], renderer_classes=[JSONRenderer])
    def find_all(self, request):
        tasks = TasksRepository.find_all()  
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'])
    def update_one(self, request):
        task_id = request.data.get('id')
        task = get_object_or_404(TasksModel, id=task_id)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        task_id = request.data.get('id')
        task = get_object_or_404(TasksModel, id=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['delete'])
    def remove_many(self, request):
        ids = request.data.get('ids')
        tasks = TasksModel.objects.filter(id__in=ids)
        tasks.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def search(self, request):
        search_query = request.query_params.get('search')
        tasks = TasksModel.objects.filter(title__icontains=search_query)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def filter(self, request):
        status = request.query_params.get('status')
        if not status:
            return Response({'error': 'Status parameter is required'}, status=400)
        tasks = self.queryset.filter(status=status)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def find_by_id(self, request):
        task_id = request.query_params.get('id')
        if not task_id:
            return Response({'error': 'ID parameter is required'}, status=400)
        try:
            task = TasksModel.objects.get(id=task_id)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except TasksModel.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def find_by_ids(self, request):
        ids = request.query_params.get('ids').split(',')
        tasks = TasksModel.objects.filter(id__in=ids)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def exists_by_id(self, request):
        task_id = request.query_params.get('id')
        exists = TasksModel.objects.filter(id=task_id).exists()
        return Response({"exists": exists})