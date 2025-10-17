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

        
class TaskAssignedToUserView(APIView):
    authentication_classes = [TokenAuthentication]


    def get(self, request, *args, **kwargs):
        user_pk = request.user.id
        user = User.objects.get(pk=user_pk)
        tasks = user.task_assignee.all().values('id')
        sertialiezer = TasksAssignedUserSerializer(data={'tasks':tasks})
        print(list(sertialiezer.data))
        

        return Response({"tasks": tasks})

class UserList(ListCreateAPIView):
        queryset = Tasks.objects.all()
        serializer_class = TasksSerializer
        authentication_classes = [TokenAuthentication]

        def get_queryset(self):
            user_pk = self.request.user.id
            user = User.objects.get(pk=user_pk)
            tasks = user.task_assignee.all()
             

            return tasks



        def list(self, request):
            # Note the use of `get_queryset()` instead of `self.queryset`
            queryset = self.get_queryset()
            serializer = TasksAssignedUserSerializer(queryset, many=True)
            return Response(serializer.data)

