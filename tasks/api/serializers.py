from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from tasks.models import Tasks, Comment
from django.contrib.auth.models import User
from auth_app.api.serializers import UserSerializer
from boards.models import Boards
from rest_framework.exceptions import NotFound


class BoardFKSerializer(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        return Boards.objects.all()


    def to_internal_value(self, data):
        try:
            
            self.get_queryset().get(pk=data)
        except Boards.DoesNotExist:
            raise NotFound(f"Board with id '{data}' not found.")

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
    board = BoardFKSerializer()

    class Meta:
        model = Tasks
        fields = ['id', 'board', 'title', 'description', 'status', 'priority', 'assignee', 'reviewer', 'due_date', 'comments_count', 'assignee_id', 'reviewer_id']
        read_only_fields = ['id', 'comments_count']
        write_only_fields = ['board']

    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def create(self, validated_data):
        """
        Sets the task owner to the current user before creating the task.
        """
        validated_data['owner'] = self.context['request'].user

        return super().create(validated_data)
    
    def to_representation(self, instance):
         """
         Customizes the serialized output by removing 'comments_count' during PATCH requests.
         """
         rep = super().to_representation(instance)
         request = self.context.get('request')
         
         if request.method == "PATCH":
              rep.pop('comments_count')

         return rep
    
    def get_board_from_request(self):
        """
        Returns the Board object based on the request method.

        POST: gets board from request data.
        PATCH: uses the instance's board.
        """

        request = self.context.get('request')
        board = None

        if request.method == 'POST':
            board_id = request.data['board']
            board = Boards.objects.get(pk=board_id)

        if request.method == 'PATCH':
            board = self.instance.board

        return board
     
    
    def validate(self, attrs):
        """
        Validates that reviewer and assignee are members of the board.
        """
        board = self.get_board_from_request()
        reviewer = attrs.get('reviewer')
        assignee = attrs.get('assignee')

        if not board.members.filter(pk=reviewer.id).exists():
            raise serializers.ValidationError('The reviewer must be a board member.')
        
        if not board.members.filter(pk=assignee.id).exists():
            raise serializers.ValidationError('The assignee must be a board member.')

        return attrs
    
    def update(self, instance, validated_data):
        """
        Prevents changing the board during update and delegates the rest to the parent update method.
        """

        board = validated_data.get('board', None)

        if board:
            raise serializers.ValidationError('Board can not change')
        return super().update(instance, validated_data)

              


class AddCommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    author = serializers.StringRelatedField()
 

    class Meta:
        model = Comment
        fields= ['id', 'author', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

    
    def create(self, validated_data):
        """
        Creates a new comment and assigns the author and task from the serializer context.
        """
        author = self.context['user']
        task = self.context['task']
        
        return Comment.objects.create(author=author, task=task, **validated_data)
    
class CommentSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField()
        
    class Meta:
        model = Comment
        fields= ['id', 'author', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'created_at', 'content']
    

        

 