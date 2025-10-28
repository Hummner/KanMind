from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Boards(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_boards')
    members = models.ManyToManyField(User, related_name='members_board')

    class Meta:
        verbose_name = 'Board'