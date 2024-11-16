from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer
from chore_planner_api.permissions import IsTaskGiverOrReadOnly

class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    
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
    def get_queryset(self):
        user = self.request.user
        households = user.profile.household.all()
        return Task.objects.filter(assigned_to__household__in=households)

    def perform_create(self, serializer):
        serializer.save(task_giver=self.request.user.profile)

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsTaskGiverOrReadOnly]
    queryset = Task.objects.all()
    def get_queryset(self):
        user = self.request.user
        households = user.profile.household.all()
        return Task.objects.filter(assigned_to__household__in=households)