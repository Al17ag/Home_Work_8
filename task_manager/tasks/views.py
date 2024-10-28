from django.shortcuts import render
from rest_framework import generics, pagination
from rest_framework.response import Response

from .models import Task
from .models import SubTask
from .permissions import IsOwner
from .serializers import SubTaskSerializer, SubTaskCreateSerializer, TaskCreateSerializer, TaskDetailSerializer
from django_filters import rest_framework as filters  # pip install django-filter
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Пагинация
class TaskPagination(pagination.PageNumberPagination):
    page_size = 10   # Количество задач на странице
    page_size_query_param = 'page_size'
    max_page_size = 100

class SubTaskPagination(pagination.PageNumberPagination):
    page_size = 10  # Количество подзадач на странице
    page_size_query_param = 'page_size'
    max_page_size = 10

class TaskFilter(filters.FilterSet):    # Фильтры для задач
    status = filters.CharFilter(field_name='status', lookup_expr='exact')
    deadline = filters.DateTimeFilter(field_name='deadline', lookup_expr='exact')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Task
        fields = ['status', 'deadline', 'title', 'description']

# Фильтры для подзадач
class SubTaskFilter(filters.FilterSet):
    status = filters.CharFilter(field_name='status', lookup_expr='exact')
    deadline = filters.DateTimeFilter(field_name='deadline', lookup_expr='exact')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = SubTask
        fields = ['status', 'deadline', 'title', 'description']


class TaskListCreateView(generics.ListCreateAPIView): # Представление для списка и создания задач
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    pagination_class = TaskPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TaskFilter
    permission_classes = [IsAuthenticated] # Только авторизованные пользователи могут создавать задачи

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) # Устанавливаем текущего пользователя как владельца

# Представление для получения, обновления и удаления задач
class TaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticated, IsOwner]


# Представление для списка и создания подзадач
class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    pagination_class = SubTaskPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SubTaskFilter
    permission_classes = [IsAuthenticated] # Только авторизованные пользователи могут создавать подзадачи

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Устанавливаем текущего пользователя как владельца

class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    pagination_class = SubTaskPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SubTaskFilter
    ordering_fields = ['created_at']  # Добавлено для сортировки
    ordering = ['-created_at']  # По умолчанию сортировка по убыванию

class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class UserTasksView(APIView):  # {{ edit_1 }}
    permission_classes = [IsAuthenticated]  # {{ edit_2 }}

    def get(self, request):  # {{ edit_3 }}
        tasks = Task.objects.filter(owner=request.user)  # {{ edit_4 }}
        serializer = TaskDetailSerializer(tasks, many=True)  # {{ edit_5 }}
        return Response(serializer.data)  # {{ edit_6 }}

