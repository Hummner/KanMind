from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Boards(models.Model):
    title = models.CharField(max_length=255)
    member_count = models.IntegerField()
    ticket_count = models.IntegerField(default=0)
    tasks_to_do_count = models.IntegerField(default=0)
    tasks_high_prio_count = models.IntegerField(default=0)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards_owner')
    members = models.ManyToManyField(User, related_name='boards_members')

class Tasks(models.Model):
    class Priority(models.TextChoices):
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
    
    class Status(models.TextChoices):
        TODO = "to-do"
        REVIEW = "review"
        DONE = "done"

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(choices=Status.choices)
    priority = models.CharField(choices=Priority.choices)
    assignee = models.ManyToManyField(User, related_name='task_assignee')
    reviewer = models.ManyToManyField(User, related_name='task_reviewer')
    due_date = models.DateField()
    comments_count = models.IntegerField(default=0)


 