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

    # owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Tasks
        fields = '__all__'
        read_only_fields = ['id', 'comments_count, owner']

    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data.pop('comments_count')
        return super().update(instance, validated_data)


class AddCommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    author = serializers.StringRelatedField()
 

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
    

        

 