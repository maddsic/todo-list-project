from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# creating our database models


class Todo(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# returning the string representation of title
    def __str__(self):
        return self.title

# This class is responsible for quering the database based on completed task!
    class meta:
        ordering = ['complete']
