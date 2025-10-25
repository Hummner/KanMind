from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest_framework import serializers
from boards.models import Boards
from tasks.api.serializers import TasksSerializer
from auth_app.api.serializers import UserSerializer
from django.contrib.auth.models import User
from tasks.models import Tasks


class BoardsSeralizer(ModelSerializer):

    members = PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        many=True,
        write_only = True
        )
    
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()
    
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)

    class Meta:
        model = Boards
        fields = ['id', 'title', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id', 'members', 'owner']
        read_only_fields = ['id', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']
        extra_kwargs = {
            'owner': {'write_only': True}
        }

    def get_ticket_count(self, obj):
        return obj.tasks.count()
    
    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to-do').count()
    
    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()
    
    def get_member_count(self, obj):
        return obj.members.count()



class BoardDetailSerializer(ModelSerializer):

    tasks = TasksSerializer(many=True, read_only = True)

    members = UserSerializer(many=True, read_only = True)

    class Meta:
         model = Boards
         fields = ['id', 'title', 'owner_id', 'members', 'tasks']


class BoardUpdateSerializer(ModelSerializer):

    members = PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        many=True,
        write_only = True,
        source="members_data"
    )


    owner_data = UserSerializer(read_only = True)
    members_data = UserSerializer(many = True, read_only = True)

    def update(self, instance, validated_data):
        pk = instance.pk
        board = Boards.objects.get(pk=pk)
        owner_pk = board.owner.id
        owner = User.objects.get(pk=owner_pk)
        instance.owner_data = owner

        return super().update(instance, validated_data)

    class Meta:
        model = Boards
        fields = ['id', 'title', 'owner_data', 'members_data', 'members']