from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from tasks.models import Tasks, Comment
from rest_framework.authentication import TokenAuthentication
from .serializers import TasksSerializer, TasksAssignedUserSerializer, AddCommentSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from boards.models import Boards
from .permissions import IsMember, IsTaskOrBoardOwner, IsCommentAuthor
from django.shortcuts import get_object_or_404


class TasksViewSet(ModelViewSet):
    queryset = Tasks.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsMember]
    serializer_class = TasksSerializer


    def get_permissions(self):
         if self.request.method == "DELETE":
              return [IsTaskOrBoardOwner()]

         return super().get_permissions()

  

class TaskAssignedToUserView(ListCreateAPIView):
        queryset = Tasks.objects.all()
        serializer_class = TasksSerializer
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated, IsMember]

        def get_queryset(self):
          user = self.request.user
          print(user.task_assignee.all())
          tasks = user.task_assignee.select_related("assignee")
          print(tasks)
          return tasks


        def list(self, request):
            queryset = self.get_queryset()
            serializer = TasksSerializer(queryset, many=True)
            return Response(serializer.data)
        
class TaskReviewerView(ListCreateAPIView):
        queryset = Tasks.objects.all()
        serializer_class = TasksSerializer
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated, IsMember]

        def get_queryset(self):
            user_pk = self.request.user.id
            
            user = User.objects.get(pk=user_pk)
            tasks = user.task_reviewer.all()
            return tasks


        def list(self, request):
            queryset = self.get_queryset()
            serializer = TasksSerializer(queryset, many=True)
            return Response(serializer.data)
        

class CommentsView(ModelViewSet):
     queryset = Comment.objects.all()
     serializer_class = CommentSerializer
     authentication_classes = [TokenAuthentication]
     permission_classes = [IsAuthenticated, IsMember]


     def get_task(self):
        task_pk = int(self.kwargs.get('task_pk'))
        task = get_object_or_404(Tasks, pk=task_pk)
        return task


     def get_permissions(self):
          if self.request.method == 'DELETE':
               return [IsCommentAuthor()]

          return super().get_permissions()
     
     def get_queryset(self):
          task = self.get_task()
          return Comment.objects.filter(task = task)

     def create(self, request, *args, **kwargs):
        user_pk = self.request.user.id
        user = User.objects.get(pk=user_pk)
        task = self.get_task()
        serializer = AddCommentSerializer(data=request.data, context={'request': request, 'user':user, 'task':task})

        if serializer.is_valid():
                serializer.save()
        else:
            raise serializers.ValidationError(serializer.errors)

        return Response(serializer.data)


