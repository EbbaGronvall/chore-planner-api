from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer
from chore_planner_api.permissions import IsTaskGiverOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class TaskList(generics.ListCreateAPIView):
    """
    API view for listing and creating tasks.
    """
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = [
        'title', 'status'
    ]
    search_fields = [
            'assigned_to__member__username', 'title',
            'task_giver__member__username'
            ]
    ordering_fields = [
        'title', 'due_date', 'status', 'assigned_to__member__username'
    ]

    def get_queryset(self):
        """
        Retrieves the queryset of tasks for the current user's household.
        """
        user = self.request.user
        households = user.profile.household
        return Task.objects.filter(assigned_to__household=households)

    def perform_create(self, serializer):
        """
        Saves a new task with the task_giver set to the request user.
        """
        serializer.save(task_giver=self.request.user.profile)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a specific task.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsTaskGiverOrReadOnly]
    queryset = Task.objects.all()

    def get_queryset(self):
        """
        Retrieves the queryset of tasks for the current user's household.
        """
        user = self.request.user
        households = user.profile.household
        return Task.objects.filter(assigned_to__household=households)
