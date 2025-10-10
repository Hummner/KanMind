from rest_framework.serializers import ModelSerializer
from boards.models import Boards


class BoardsSeralizer(ModelSerializer):
    class Meta:
        model = Boards
        fields = ['id', 'title', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id', 'members']
        read_only_fields = ('id', 'member_count','ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id')



