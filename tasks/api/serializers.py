from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from tasks.models import Tasks
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




    class Meta:
        model = Tasks
        fields = '__all__'
        read_only_fields = ['id']

        

 