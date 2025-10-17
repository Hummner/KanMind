from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from tasks.models import Tasks
from rest_framework.authentication import TokenAuthentication
from .serializers import TasksSerializer, TasksAssignedUserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response

class TasksViewSet(ModelViewSet):
    queryset = Tasks.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = TasksSerializer

        


class TaskAssignedToUserView(ListCreateAPIView):
        queryset = Tasks.objects.all()
        serializer_class = TasksSerializer
        authentication_classes = [TokenAuthentication]

        def get_queryset(self):
            user_pk = self.request.user.id
            user = User.objects.get(pk=user_pk)
            tasks = user.task_assignee.all()
            return tasks


        def list(self, request):
            queryset = self.get_queryset()
            serializer = TasksSerializer(queryset, many=True)
            return Response(serializer.data)
        
class TaskReviewerView(ListCreateAPIView):
        queryset = Tasks.objects.all()
        serializer_class = TasksSerializer
        authentication_classes = [TokenAuthentication]

        def get_queryset(self):
            user_pk = self.request.user.id
            print(self.request.get_full_path)
            
            user = User.objects.get(pk=user_pk)
            tasks = user.task_reviewer.all()
            return tasks


        def list(self, request):
            queryset = self.get_queryset()
            serializer = TasksSerializer(queryset, many=True)
            return Response(serializer.data)

