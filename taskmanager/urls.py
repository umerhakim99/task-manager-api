from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = router.urls