from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import sqlite3

from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
# -----------------------------------------------------------------------
class Task(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In progress'),
        ('PENDING', 'Pending'),
        ('BLOCKED', 'Blocked'),
        ('DONE', 'Done'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        unique_together = ['title', 'deadline']

    def save(self, *args, **kwargs):
        if not self.pk:  # Только для новых объектов
            # Проверяем, существует ли задача с таким же названием и датой дедлайна
            same_day_tasks = Task.objects.filter(
                title=self.title,
                deadline__date=self.deadline.date()
            )
            if same_day_tasks.exists():
                raise ValidationError('A task with this title already exists for the given deadline date.')
        super().save(*args, **kwargs)

# -----------------------------------------------------------------------
class SubTask(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In progress'),
        ('PENDING', 'Pending'),
        ('BLOCKED', 'Blocked'),
        ('DONE', 'Done'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subtasks')
    def __str__(self):
        return f"{self.task.title} - {self.title}"

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'
        unique_together = ['title', 'task']

