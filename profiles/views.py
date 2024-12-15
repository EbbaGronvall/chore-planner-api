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
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Profile.objects.none()
        return Profile.objects.filter(household=user.profile.household)


class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsMemberOrReadOnly]
    queryset = Profile.objects.all()
