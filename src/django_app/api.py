# django_app/api.py

from django.urls import path, include

urlpatterns = [
    path('tasks/', include('django_app.modules.v1.tasks.urls'))
]