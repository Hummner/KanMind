from django.urls import path, include
from rest_framework import routers
from .views import TasksViewSet, TaskAssignedToUserView

router = routers.SimpleRouter()
router.register(r'', TasksViewSet)



urlpatterns = [
    path('assigned-to-me/', TaskAssignedToUserView.as_view()),
    path('', include(router.urls)),
    
]