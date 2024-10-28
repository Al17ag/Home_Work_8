from rest_framework import serializers   # pip install djangorestframework
from .models import SubTask
from .models import Category, Task, SubTask
from django.utils import timezone

class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'deadline', 'task', 'created_at', 'owner']
        read_only_fields = ['created_at']

class CategoryCreateSerialalizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def create(self, validated_data):
# Проверка уникальности названия категории
        if Category.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError('Category with this name already exists.')
        return super().create(validated_data)

    def update(self, instance, validated_data):
# Проверка уникальности названия категории при обновлении
        if 'name' in validated_data and Category.objects.filter(name=validated_data['name']).exclude(id=instance.id).exists():
            raise serializers.ValidationError("Category with this name already exists.")
        return super().update(instance, validated_data)

class SubTaskSerializer(serializers.ModelSerializer): # сериализатор определяет, какие поля подзадачи будут отображаться
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'owner']


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True) # many=True указывает, что это поле может содержать несколько
    # подзадач, а read_only=True делает его доступным только для чтения.

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'subtasks', 'owner']


# Задание 4: Валидация данных в сериализаторах

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'categories', 'owner']

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("The deadline cannot be in the past. Крайний срок не может быть в прошлом")
        return value



