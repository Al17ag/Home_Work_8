from django.urls import path
from .views import SubTaskListCreateView, SubTaskDetailUpdateDeleteView, TaskListCreateView, TaskDetailUpdateDeleteView
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailUpdateDeleteView.as_view(), name='task-detail-update-delete'),
]