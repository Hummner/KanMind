from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from tasks.models import Tasks, Comment
from django.contrib.auth.models import User
from auth_app.api.serializers import UserSerializer





class TasksSerializer(ModelSerializer):

    reviewer = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset= User.objects.all(),
        write_only = True,
        source="reviewer"
    )

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset= User.objects.all(),
        write_only = True,
        source="assignee"
    )

    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Tasks
        fields = '__all__'
        read_only_fields = ['id', 'comments_count']

    def get_comments_count(self, obj):
        return obj.comments.count()




class TasksAssignedUserSerializer(serializers.Serializer):

    tasks = TasksSerializer(many=True, read_only =' True')

    task_ids = serializers.PrimaryKeyRelatedField(
        queryset= Tasks.objects.all(),
        write_only = True,
        source='tasks'
    )
class AddCommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
 

    class Meta:
        model = Comment
        fields= ['id', 'author', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

    
    def create(self, validated_data):
        author = self.context['user']
        task = self.context['task']
        

        return Comment.objects.create(author=author, task=task, **validated_data)
    
class CommentSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Comment
        fields= ['id', 'author', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'created_at', 'content']
    

        

 