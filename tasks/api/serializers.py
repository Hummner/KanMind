from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from tasks.models import Tasks, Comment
from django.contrib.auth.models import User
from auth_app.api.serializers import UserSerializer
from boards.models import Boards




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

    # owner = serializers.HiddenField()

    class Meta:
        model = Tasks
        fields = ['id', 'board', 'title', 'description', 'status', 'priority', 'assignee', 'reviewer', 'due_date', 'comments_count', 'assignee_id', 'reviewer_id']
        read_only_fields = ['id', 'comments_count']

    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user

        return super().create(validated_data)
    
    def to_representation(self, instance):
         rep = super().to_representation(instance)
         request = self.context.get('request')
         
         if request.method == "PATCH":
              rep.pop('comments_count')

         return rep
    
    def get_board_from_request(self):
        request = self.context.get("request")
        board_id = None

        if request:
            board_id = request.data.get("board")  # POST/PATCH ha küldve van

        if not board_id and self.instance:
            return getattr(self.instance, "board", None)

        if board_id:
            return Boards.objects.filter(pk=board_id).first()

        return None

    def validate_reviewer_id(self, value):
        board = self.get_board_from_request()
        user = value
        is_member = user.members_board.get(board=board.id)

        if not board.members.filter(pk=value.pk).exists():
            raise serializers.ValidationError("Reviewer must be members in Board")
        
        return value

              


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
    

        

 