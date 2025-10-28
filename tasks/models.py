from django.db import models
from django.contrib.auth.models import User
from boards.models import Boards

class Tasks(models.Model):
    class Priority(models.TextChoices):
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
    
    class Status(models.TextChoices):
        TODO = "to-do"
        INPROGRESS = "in-progress"
        REVIEW = "review"
        DONE = "done"

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(choices=Status.choices)
    priority = models.CharField(choices=Priority.choices)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_assignee', null=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_reviewer', null=True)
    due_date = models.DateField()
    board = models.ForeignKey(Boards, on_delete=models.CASCADE, related_name='tasks')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taks_owner')

    class Meta:
        verbose_name = 'Task'


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    content = models.CharField(max_length=1000)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name='comments')


    def __str__(self):
        return self.author.username
    
    class Meta:
        verbose_name = 'Comment'
