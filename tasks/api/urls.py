from django.urls import path, include
from rest_framework import routers
from .views import TasksViewSet

router = routers.SimpleRouter()
router.register(r'', TasksViewSet)



urlpatterns = [
    path('', include(router.urls))
]