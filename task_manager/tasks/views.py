from django.shortcuts import render
from rest_framework import generics
from .models import SubTask
from .serializers import SubTaskSerializer, SubTaskCreateSerializer


class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer


class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
