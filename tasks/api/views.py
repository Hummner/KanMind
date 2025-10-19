from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from tasks.models import Tasks
from rest_framework.authentication import TokenAuthentication
from .serializers import TasksSerializer, TasksAssignedUserSerializer, AddCommentSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers

class TasksViewSet(ModelViewSet):
    queryset = Tasks.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = TasksSerializer

    @action(detail=True, methods=['POST', 'GET'])
    def comments(self, request, pk):
        if request.method == 'POST':
            user_pk = self.request.user.id
            user = User.objects.get(pk=user_pk)
            task = self.get_object()
            serializer = AddCommentSerializer(data=request.data, context={'request': request, 'user':user, 'task':task})
            

            if serializer.is_valid():
                serializer.save()
            else:
                raise serializers.ValidationError(serializer.errors)

            return Response(serializer.data)
        else: 
            task = self.get_object()
            comments = task.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
    

       

        


        


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
        

class CommentsView(ModelViewSet):

    def get_queryset(self):
         user_pk = self.request.user.id
         user = User.objects.get(pk=user_pk)

         return super().get_queryset()
         

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
