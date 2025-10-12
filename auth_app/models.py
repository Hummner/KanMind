from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.username

class UserSerializer(ModelSerializer):
    fullname = serializers.CharField(source='username')

    class Meta:
        model = User
        fields= ['id', 'fullname', 'email']
