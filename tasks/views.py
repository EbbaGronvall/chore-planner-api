from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer


class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Task.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = [
        'title', 'due_date', 'status', 'assigned_to'
    ]
    search_fields = ['assigned_to__username']
    ordering_fields = [
        'title', 'due_date', 'status', 'assigned_to__username'
    ]

    def perform_create(self, serializer):
        serializer.save(task_giver=self.request.user.profile)

