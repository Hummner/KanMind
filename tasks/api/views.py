from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from tasks.models import Tasks, Comment
from rest_framework.authentication import TokenAuthentication
from .serializers import TasksSerializer, AddCommentSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from boards.models import Boards
from .permissions import IsMember, IsTaskOrBoardOwner, IsCommentAuthor
from django.shortcuts import get_object_or_404


class TasksViewSet(ModelViewSet):
    """
     ViewSet for managing tasks.
     Only board members can access it.
     Delete requests are restricted to task or board owners.
     """
    queryset = Tasks.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsMember]
    serializer_class = TasksSerializer


    def get_permissions(self):
         if self.request.method == "DELETE":
              return [IsTaskOrBoardOwner()]

         return super().get_permissions()


  

class TaskAssignedToUserView(ListCreateAPIView):
        """
        API view that lists tasks assigned to the current user or allows creating new ones.
        Access is limited to board members.
        """
        serializer_class = TasksSerializer
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated, IsMember]

        def get_queryset(self):
          user = self.request.user
          tasks = user.task_assignee.select_related("assignee", "reviewer")
          return tasks
        
class TaskReviewerView(ListCreateAPIView):
        """
        API view that lists tasks where the current user is the reviewer.
        Access is limited to board members.
        """
        serializer_class = TasksSerializer
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated, IsMember]

        def get_queryset(self):
            user= self.request.user
            tasks = user.task_reviewer.select_related("assignee", "reviewer")
            return tasks
        

class CommentsView(ModelViewSet):
     """
     ViewSet for managing comments on tasks.
     Only board members can access it.
     Delete requests are restricted to the comment author.
     """
     queryset = Comment.objects.all()
     serializer_class = CommentSerializer
     authentication_classes = [TokenAuthentication]
     permission_classes = [IsAuthenticated, IsMember]


     def get_task(self):
        """
        Retrieves the task object based on the task_pk from the URL.
        """
        task_pk = int(self.kwargs.get('task_pk'))
        task = get_object_or_404(Tasks, pk=task_pk)
        return task


     def get_permissions(self):
          """
          Applies custom permission for DELETE requests (only comment authors can delete).
          """
          if self.request.method == 'DELETE':
               return [IsCommentAuthor()]

          return super().get_permissions()
     
     def get_queryset(self):
          """
          Returns all comments for the given task, ordered by creation date (newest first).
          """
          task = self.get_task()
          return Comment.objects.filter(task = task).order_by('-created_at')

     def create(self, request, *args, **kwargs):
        """
        Creates a new comment for the given task with the current user as the author.
        """
        user = self.request.user
        task = self.get_task()
        serializer = AddCommentSerializer(data=request.data, context={'request': request, 'user':user, 'task':task})

        if serializer.is_valid():
                serializer.save()
        else:
            raise serializers.ValidationError(serializer.errors)

        return Response(serializer.data)


