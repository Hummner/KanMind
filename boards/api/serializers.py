from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from boards.models import Boards
from tasks.api.serializers import TasksSerializer
from auth_app.api.serializers import UserSerializer
from django.contrib.auth.models import User


class BoardsSeralizer(ModelSerializer):
   

    members = PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        many=True,
        write_only = True
        )
    class Meta:
        model = Boards
        fields = ['id', 'title', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id', 'members']
        read_only_fields = ('id', 'member_count','ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id')

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
        owner_pk = board.owner_id_id
        owner = User.objects.get(pk=owner_pk)
        instance.owner_data = owner

        return super().update(instance, validated_data)


    class Meta:
        model = Boards
        fields = ['id', 'title', 'owner_data', 'members_data', 'members']