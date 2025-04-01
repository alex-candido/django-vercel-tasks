# django_app/modules/tasks/urls.py
from rest_framework.routers import DefaultRouter
from .api import TaskViewSet

router = DefaultRouter()
router.register(r'', TaskViewSet, basename='task')

urlpatterns = router.urls
