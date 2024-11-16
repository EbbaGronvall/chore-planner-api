from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profile
from .serializers import ProfileSerializer
from chore_planner_api.permissions import IsMemberOrReadOnly

class ProfileList(generics.ListAPIView):
    serializer_class = ProfileSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    filterset_fields = ['role', 'household']
    search_fields = ['member__username']
    queryset = Profile.objects.all()


class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsMemberOrReadOnly]
    queryset = Profile.objects.all()