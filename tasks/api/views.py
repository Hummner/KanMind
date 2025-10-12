from rest_framework.viewsets import ModelViewSet
from tasks.models import Tasks
from rest_framework.authentication import TokenAuthentication
from .serializers import TasksSerializer

class TasksViewSet(ModelViewSet):
    queryset = Tasks.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = TasksSerializer

        
