from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Boards(models.Model):
    title = models.CharField(max_length=255)
    member_count = models.IntegerField()
    ticket_count = models.IntegerField(default=0)
    tasks_to_do_count = models.IntegerField(default=0)
    tasks_high_prio_count = models.IntegerField(default=0)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_boards')
    members = models.ManyToManyField(User, related_name='members_board')




 